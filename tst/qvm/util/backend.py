from test.qvm import *

from qiskit.circuit import QuantumCircuit
from qiskit.compiler import schedule, transpile
from qvm.util.backend import *


class TestNormalBackendGraphExtractor(QvmBaseTest):
    def setup_class(self):
        self._extractor = BackendAdjMatGraphExtractor(self._backend)

    def test_get_readout_errs(self):
        print("================ Test get readout errors =====================")
        rd_errs = self._extractor.get_readout_errs()
        print(rd_errs)

    def test_graph_extraction(self):
        print("================ Test graph extraction =====================")
        graph = self._extractor.extract()
        print(graph)

        assert graph[6, 7] == 0.01431875092381174
