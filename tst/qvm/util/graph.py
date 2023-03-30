import logging

from qvm.util.backend import *
from qvm.test.base import *

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

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

        assert graph[6,7] == 0.01431875092381174


class TestKlPartitioner(QvmBaseTest):

    def setup_class(self):
        self._extractor = NormalBackendNxGraphExtractor(self._backend)
        self._partitioner = GraphPartitionProvider.get_partitioner("kl")

    def test_graph_partition(self):
        graph = self._extractor.extract()
        parts = self._partitioner.partition(graph)
        print(parts)


class TestBfsPartitioner(QvmBaseTest):

    def setup_class(self):
        self._extractor = BaseBackendGraphExtractor(self._backend)
        self._partitioner = GraphPartitionProvider.get_partitioner("bfs")

    def test_graph_partition(self):
        graph = self._extractor.extract()
        parts = self._partitioner.partition(graph)
        print(parts)


class TestFrpPartitioner(QvmBaseTest):

    def setup_class(self):
        self._extractor = BackendAdjMatGraphExtractor(self._backend)
        self._partitioner = GraphPartitionProvider.get_partitioner("frp")
        graph = self._extractor.extract()
        self._partitioner.graph = graph
        readout_errs = self._extractor.get_readout_errs()
        #print(readout_errs)
        self._partitioner.readout_errs = readout_errs

    def test_get_utilities(self):
        utility = self._partitioner._get_utilities()
        print(utility)

    def test_get_levels(self):
        utility = self._partitioner._get_utilities()
        ranks = self._partitioner._get_ranks()
        levels = self._partitioner._get_levels()
        print(ranks)
        print(levels)

    def test_get_root(self):
        self._partitioner.initialize()
        print(self._partitioner.readout_errs)
        print(self._partitioner._mean_rd_errs)
        root0 = self._partitioner._get_root()
        print(root0)

    def test_partition(self, alpha, beta):
        self._partitioner.alpha = alpha
        self._partitioner.beta = beta
        part0 = self._partitioner.partition(4)
        part1 = self._partitioner.partition(4)
        part2 = self._partitioner.partition(4)
        part3 = self._partitioner.partition(4)
        print(part0, part1, part2, part3)

        # Test filter high measurement error
        self._partitioner.is_low_cmr = True
        self._partitioner._visited = set()
        part0 = self._partitioner.partition(4)
        part1 = self._partitioner.partition(4)
        part2 = self._partitioner.partition(4)
        part3 = self._partitioner.partition(4)
        print(part0, part1, part2, part3)


class TestUtilMisc(QvmBaseTest):

    def test_split_list(self):
        lst = [1,2,3,4,5,6,7,8,9,10]
        res = split_list(lst, 3)
        assert res == [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]
