import copy
import os
import sys
from time import time, sleep
import numpy as np
from qiskit import qiskit

from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector
from qdao.simulator import QdaoSimObj

from qdao.test import QdaoBaseTest
from qdao.engine import Engine
from qdao.util import retrieve_sv

from constants import *

class TestEngine(QdaoBaseTest):


    def test_pre_postprocessing(self):
        circ = self.get_qiskit_circ("random", num_qubits=8, depth=20, measure=False)
        circ = transpile(circ, self._sv_sim)

        engine = Engine(circuit = circ, num_primary=6, num_local=2)

        sub_circs = engine._part.run(engine._circ)

        sv = engine._sim.run(QdaoSimObj(sub_circs[0].circ))
        engine._postprocess(sub_circs[0], 0, sv)

        obj = engine._preprocess(sub_circs[0], 0)
        print(sub_circs[0].circ)

        assert np.array_equal(sv, obj.objs[0])

    def test_run_step(self, nq):
        NQ = int(nq)
        NP = NQ
        NL = NQ - 10

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        circ_sv = copy.deepcopy(circ)
        circ_sv.save_state()
        st = time()
        job = self._sv_sim.run(circ_sv)
        sv0 = job.result().get_statevector()
        print("Qiskit runs: {}".format(time() - st))

        engine = Engine(circuit=circ, num_primary=NP, num_local=NL, is_parallel=True)
        sub_circs = engine._part.run(circ)
        engine._initialize()
        simobj = engine._preprocess(sub_circs[0], 0)
        st = time()
        print("Start running simulation")
        sv1 = engine._sim.run(simobj)
        print("Qiskit runs: {}".format(time() - st))
        print("sub-circs num: {}".format(len(sub_circs)))

        assert sv0.equiv(sv1)

    def test_run_qiskit_random(self, nq):
        NQ = int(nq)
        NP = NQ - 2
        NL = NQ - 10

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)

        engine = Engine(circuit=circ, num_primary=NP, num_local=NL, is_parallel=True)
        st = time()
        engine.run()
        print("Qdao runs: {}".format(time() - st))
        sv = retrieve_sv(NQ, num_local=NL)
        engine.print_statistics()
        engine._manager.print_statistics()

        circ.save_state()
        st = time()
        sv_org = self._sv_sim.run(circ).result().get_statevector().data
        print("Qiskit runs: {}".format(time() - st))
        assert Statevector(sv).equiv(Statevector(sv_org))

    def test_run_quafu_single_random_no_init(self, nq):
        NQ = int(nq)

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())

        from quafu.simulators.simulator import simulate
        st = time()
        sv_wo_init = simulate(quafu_circ, output="state_vector").get_statevector()
        print("Quafu runs: {}".format(time() - st))

        init_sv = np.zeros(1<<NQ, dtype=np.complex128)
        init_sv[0] = 1
        sv_with_init = simulate(quafu_circ, psi=init_sv, output="state_vector").get_statevector()

        assert Statevector(sv_wo_init).equiv(Statevector(sv_with_init))

    def test_run_quafu_single_random(self, nq):
        NQ = int(nq)

        circ = self.get_qiskit_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        from quafu.circuits.quantum_circuit import QuantumCircuit

        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())

        from quafu.simulators.simulator import simulate
        st = time()
        init_sv = np.zeros(1<<NQ, dtype=np.complex128)
        init_sv[0] = 1
        sv_org = simulate(quafu_circ, psi=init_sv, output="state_vector").get_statevector()
        print("Quafu runs: {}".format(time() - st))

    def test_run_quafu_step_by_step_random(self, nq):
        NQ = int(nq)
        NP = NQ - 2
        NL = NQ - 4
        D = NQ-3 # depth

        from qdao.qiskit.utils import random_circuit
        circ = random_circuit(NQ, D, max_operands=2, measure=False)
        circ = transpile(circ, self._sv_sim)

        from quafu.circuits.quantum_circuit import QuantumCircuit
        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())
        print("\nOriginal Circ")
        quafu_circ.draw_circuit()

        engine = Engine(circuit=quafu_circ, num_primary=NP, num_local=NL, backend="quafu", is_parallel=False)

        sub_circs = engine._part.run(engine._circ)
        engine._initialize()

        num_acc_ops = 0
        input_sv = np.zeros(1<<NQ, dtype=np.complex128)
        input_sv[0] = 1
        for sub_circ in sub_circs:
            for ichunk in range(engine._num_chunks):
                simobj = engine._preprocess(sub_circ, ichunk)
                sv = engine._sim.run(simobj)
                engine._postprocess(sub_circ, ichunk, sv)

            sv_expected = retrieve_sv(NQ, num_local=NL)
            print("\n:::::debugging sub-circ::::\n")
            sub_circ.circ.draw_circuit()
            self.debug_run_quafu_circ(
                    quafu_circ,
                    input_sv,
                    sv_expected,
                    (num_acc_ops, num_acc_ops+len(sub_circ.circ.gates))
                )
            num_acc_ops += len(sub_circ.circ.gates)
            input_sv = sv_expected


    def test_run_quafu_random(self, nq):
        NQ = int(nq)
        NP = NQ - 2
        NL = NQ - 4
        D = NQ-3 # depth

        from qdao.qiskit.utils import random_circuit
        circ = random_circuit(NQ, D, max_operands=2, measure=False)
        circ = transpile(circ, self._sv_sim)

        from quafu.circuits.quantum_circuit import QuantumCircuit
        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())
        print("\nOriginal Circ")
        quafu_circ.draw_circuit()

        engine = Engine(circuit=quafu_circ, num_primary=NP, num_local=NL, backend="quafu", is_parallel=False)
        st = time()
        engine.run()
        print("Qdao runs: {}".format(time() - st))
        sv = retrieve_sv(NQ, num_local=NL)
        print(sv)
        engine.print_statistics()
        engine._manager.print_statistics()

        from quafu.simulators.simulator import simulate
        st = time()
        init_sv = np.zeros(1<<NQ, dtype=np.complex128)
        init_sv[0] = 1
        sv_org = simulate(quafu_circ, psi=init_sv, output="state_vector").get_statevector()
        print("Quafu runs: {}".format(time() - st))
        print(sv_org)

        assert Statevector(sv).equiv(Statevector(sv_org))

    def test_run_quafu_vs_qiskit_single_random_with_init(self, nq):
        NQ = int(nq)

        from qdao.qiskit.utils import random_circuit
        circ = random_circuit(NQ, NQ, measure=False)
        circ = transpile(circ, self._sv_sim)

        from quafu.circuits.quantum_circuit import QuantumCircuit
        quafu_circ = QuantumCircuit(1)
        quafu_circ.from_openqasm(circ.qasm())

        from quafu.simulators.simulator import simulate
        st = time()
        init_sv = np.zeros(1<<NQ, dtype=np.complex128)
        init_sv[0] = 1
        sv_quafu = simulate(quafu_circ, psi=init_sv, output="state_vector").get_statevector()
        print("Quafu runs: {}".format(time() - st))

        st = time()
        init_sv = np.zeros(1<<NQ, dtype=np.complex128)
        init_sv[0] = 1

        init_circ = qiskit.circuit.QuantumCircuit(NQ)
        init_circ.initialize(init_sv, range(NQ))
        init_circ.compose(circ, inplace=True)
        init_circ.save_state()
        self._sv_sim.set_options(fusion_enable=False)
        sv_qiskit = self._sv_sim.run(init_circ).result().get_statevector()

        # FIXME(zhaoyilun): when testing small circuits, uncomment this
        #assert sv_qiskit.equiv(Statevector(sv_quafu))

        print("Qiskit runs: {}".format(time() - st))

    def test_run_quafu_bench(self, bench):
        qasm_path = LARGE_BENCH_PATH + '/' + bench + '/' + bench + '.qasm'
        quafu_circ = self.get_quafu_circ_from_qasm(qasm_path)
        NQ = quafu_circ.num
        NP = NQ - 2
        NL = NQ - 10

        engine = Engine(circuit=quafu_circ, num_primary=NP, num_local=NL, backend="quafu", is_parallel=True)
        engine.run()
        sv = retrieve_sv(NQ, num_local=NL)

        init_sv = np.zeros(1<<NQ, dtype=np.complex128)
        init_sv[0] = 1
        from quafu.simulators.simulator import simulate
        sv_org = simulate(quafu_circ, psi=init_sv, output="state_vector").get_statevector()

        assert Statevector(sv).equiv(Statevector(sv_org))

        qiskit_circ = self.get_qiskit_circ("qasm", qasm_path=qasm_path)
        qiskit_circ.remove_final_measurements()
        qiskit_circ.save_state()
        sv_qiskit = self._sv_sim.run(qiskit_circ).result().get_statevector().data

        assert Statevector(sv_qiskit).equiv(Statevector(sv_org))
