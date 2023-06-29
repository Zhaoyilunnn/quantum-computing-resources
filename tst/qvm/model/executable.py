from test.qvm import *

from qvm.manager.backend_manager import FrpBackendManagerV2
from qvm.model.executable import *


class TestCostExecutable(QvmBaseTest):
    def test_get_cost(self, nq):
        nq = int(nq)  # Number of qubits
        circ = self.get_qiskit_circ("random", num_qubits=nq, depth=nq)

        # Create backend manager
        bm = FrpBackendManagerV2(self._backend)
        bm.init_helpers()
        bm.init_cus()

        proc = bm.compile(circ)
        for i, exe in enumerate(proc):
            print(f"\ncost-res\t{nq}\t{i}\t{exe.cost[0]}\t{exe.cost[1]}")
