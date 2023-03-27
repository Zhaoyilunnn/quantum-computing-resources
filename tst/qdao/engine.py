import copy
import numpy as np

from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector

from qdao.test import QdaoBaseTest
from qdao.engine import Engine
from qdao.util import retrieve_sv


class TestEngine(QdaoBaseTest):


    def test_pre_postprocessing(self):
        circ = self.get_small_bench_circ("random", num_qubits=8, depth=20, measure=False)
        circ = transpile(circ, self._sv_sim)

        engine = Engine(circuit = circ, num_primary=6, num_local=2)

        sub_circs = engine._part.run(engine._circ)

        res = engine._sim.run(sub_circs[0].circ).result()
        sv = res.get_statevector()
        engine._postprocess(sub_circs[0], 0, sv)

        sv_load, _ = engine._preprocess(sub_circs[0], 0)
        print(sub_circs[0].circ)

        assert sv == sv_load

    def test_run(self):
        NQ = 8
        NP = 6
        NL = 2

        circ = self.get_small_bench_circ("random", num_qubits=NQ, depth=9, measure=False)
        circ = transpile(circ, self._sv_sim)
        circ.global_phase = 0
        org_circ = copy.deepcopy(circ)

        engine = Engine(circuit=circ, num_primary=NP, num_local=NL)
        engine.run()
        sv = retrieve_sv(NQ, num_local=NL)

        circ.save_state()
        sv_org = self._sv_sim.run(circ).result().get_statevector().data
        assert Statevector(sv).equiv(Statevector(sv_org))
