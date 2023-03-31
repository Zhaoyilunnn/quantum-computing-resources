import copy
from time import time
import numpy as np

from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector
from qdao.quafu.simulator import QuafuSimulator
from qdao.simulator import QdaoSimObj

from qdao.test import QdaoBaseTest
from qdao.engine import Engine
from qdao.util import retrieve_sv

from constants import *

class TestEngine(QdaoBaseTest):


    def test_pre_postprocessing(self):
        circ = self.get_small_bench_circ("random", num_qubits=8, depth=20, measure=False)
        circ = transpile(circ, self._sv_sim)

        engine = Engine(circuit = circ, num_primary=6, num_local=2)

        sub_circs = engine._part.run(engine._circ)

        #res = engine._sim.run(sub_circs[0].circ).result()
        #sv = res.get_statevector().data
        sv = engine._sim.run(QdaoSimObj(sub_circs[0].circ))
        engine._postprocess(sub_circs[0], 0, sv)

        obj = engine._preprocess(sub_circs[0], 0)
        print(sub_circs[0].circ)

        assert np.array_equal(sv, obj.objs[0])

    def test_run_step(self, nq):
        NQ = int(nq)
        NP = NQ
        NL = NQ - 10

        circ = self.get_small_bench_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        #circ.global_phase = 0
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
        #engine._sim.run(sub_circs[0].sub_circ)
        st = time()
        print("Start running simulation")
        sv1 = engine._sim.run(simobj)
        print("Qiskit runs: {}".format(time() - st))
        print("sub-circs num: {}".format(len(sub_circs)))

        #st = time()
        #print("Start getting statevector")
        #sv1 = job.result().get_statevector()
        #print("Getting statevector runs: {}".format(time() - st))

        assert sv0.equiv(sv1)

    def test_run_qiskit(self, nq):
        NQ = int(nq)
        NP = NQ - 2
        NL = NQ - 10

        circ = self.get_small_bench_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        #circ.global_phase = 0

        #engine = Engine(circuit=circ, num_primary=NP, num_local=NL, is_parallel=False)
        #st = time()
        #engine.run()
        #print("Qdao runs: {}".format(time() - st))
        #sv = retrieve_sv(NQ, num_local=NL)
        #engine.print_statistics()
        #engine._manager.print_statistics()

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

    #def test_run_qiskit(self, nq):
    #    NQ = int(nq)

    #    circ = self.get_small_bench_circ("random", num_qubits=NQ, depth=9, measure=False)
    #    circ = transpile(circ, self._sv_sim)

    #    circ.save_state()
    #    st = time()
    #    sv_org = self._sv_sim.run(circ).result().get_statevector().data
    #    print("Qiskit runs: {}".format(time() - st))

    def test_run_quafu(self, bench):
        qasm_path = LARGE_BENCH_PATH + '/' + bench + '/' + bench + '.qasm'
        quafu_circ = self.get_quafu_circ_from_qasm(qasm_path)
        NQ = quafu_circ.num
        NP = NQ - 2
        NL = NQ - 10

        engine = Engine(circuit=quafu_circ, num_primary=NP, num_local=NL, backend="quafu", is_parallel=True)
        engine.run()
        sv = retrieve_sv(NQ, num_local=NL)

        from quafu.simulators.simulator import simulate
        sv_org = simulate(quafu_circ, output="state_vector").get_statevector()

        assert np.array_equal(sv, sv_org)
