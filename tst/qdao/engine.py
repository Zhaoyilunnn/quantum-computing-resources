import copy
import numpy as np

from qiskit.compiler import transpile

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

        sv_load = engine._preprocess(sub_circs[0], 1, 0)
        print(sub_circs[0].circ)

        assert sv == sv_load

    def test_run(self):
        circ = self.get_small_bench_circ("random", num_qubits=6, depth=20, measure=False)
        circ = transpile(circ, self._sv_sim)
        org_circ = copy.deepcopy(circ)

        engine = Engine(circuit=circ, num_primary=6, num_local=2)
        engine.run()

        sv = retrieve_sv(6, num_local=2)
        print(sv)
        assert circ == org_circ
        circ.save_state()
        sv_org = self._sv_sim.run(circ).result().get_statevector().data
        print(sv_org)
        assert np.array_equal(sv, sv_org) or np.array_equal(sv, -sv_org)
