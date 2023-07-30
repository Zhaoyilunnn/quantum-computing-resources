import logging
from test.qvm import *

from qvm.util.backend import *

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

        assert graph[6, 7] == 0.01431875092381174


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
        # print(readout_errs)
        self._partitioner.readout_errs = readout_errs

    def testget_utilities(self):
        utility = self._partitioner.get_utilities()
        print(utility)

    def test_get_levels(self):
        utility = self._partitioner.get_utilities()
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
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        res = split_list(lst, 3)
        assert res == [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]

    def test_get_subgraph_num_v1(self):
        graph = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]

        # num, _ = get_subgraph_num(np.array(graph), 2)
        # assert num == 4

        # backend = FakeCairo()
        # extractor = BackendAdjMatGraphExtractor(backend)
        # graph = extractor.extract()
        # num, _ = get_subgraph_num(graph, 2)
        # assert num == 28
        # num, _ = get_subgraph_num(graph, 3)
        # assert num == 37
        # num, subgraphs = get_subgraph_num(graph, 4)
        # assert num == 28

        subgraphs = find_all_connected_subgraphs(np.array(graph), 2)
        assert len(subgraphs) == 4

        backend = FakeCairo()
        extractor = BackendAdjMatGraphExtractor(backend)
        graph = extractor.extract()
        subgraphs = find_all_connected_subgraphs(np.array(graph), 2)
        assert len(subgraphs) == 28
        subgraphs = find_all_connected_subgraphs(np.array(graph), 3)
        assert len(subgraphs) == 37
        subgraphs = find_all_connected_subgraphs(np.array(graph), 4)
        assert len(subgraphs) == 48

    def test_get_subgraph_num_v2(self):
        graph = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]

        subgraphs = find_all_connected_subgraphs_v2(np.array(graph), 2)
        assert len(subgraphs) == 4

        backend = FakeCairo()
        extractor = BackendAdjMatGraphExtractor(backend)
        graph = extractor.extract()
        subgraphs = find_all_connected_subgraphs_v2(np.array(graph), 2)
        assert len(subgraphs) == 28
        subgraphs = find_all_connected_subgraphs_v2(np.array(graph), 3)
        assert len(subgraphs) == 37
        subgraphs = find_all_connected_subgraphs_v2(np.array(graph), 4)
        assert len(subgraphs) == 48

    def test_fake_backend_subgraph_num(self):
        # k_lst = [2, 3, 4, 5, 6, 7, 8]
        k_lst = [9, 10]

        # backend = FakeMelbourne()
        # extractor = BackendAdjMatGraphExtractor(backend)
        # graph = extractor.extract()
        # print("\n========= test_fake_backend_subgraph_num ===========\n")
        # for i in k_lst:
        #     subgraphs = find_all_connected_subgraphs_v2(graph, i)
        #     print(f"FakeMelbourne\t{i}\t{len(subgraphs)}")

        # backend = FakeCairo()
        # extractor = BackendAdjMatGraphExtractor(backend)
        # graph = extractor.extract()
        # print("\n========= test_fake_backend_subgraph_num ===========\n")
        # for i in k_lst:
        #     subgraphs = find_all_connected_subgraphs_v2(graph, i)
        #     print(f"FakeCairo\t{i}\t{len(subgraphs)}")

        backend = FakeBrooklyn()
        extractor = BackendAdjMatGraphExtractor(backend)
        graph = extractor.extract()
        print("\n========= test_fake_backend_subgraph_num ===========\n")
        for i in k_lst:
            subgraphs = find_all_connected_subgraphs_v2(graph, i)
            print(f"FakeBrooklyn\t{i}\t{len(subgraphs)}")

        # backend = FakeWashington()
        # extractor = BackendAdjMatGraphExtractor(backend)
        # graph = extractor.extract()
        # print("\n========= test_fake_backend_subgraph_num ===========\n")
        # for i in k_lst:
        #     subgraphs = find_all_connected_subgraphs_v2(graph, i)
        #     print(f"FakeWashington\t{i}\t{len(subgraphs)}")
