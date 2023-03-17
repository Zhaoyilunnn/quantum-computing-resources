import copy
import logging
import numpy as np

from collections import OrderedDict
from logging import warning 
from warnings import warn
from networkx.algorithms.community import kernighan_lin_bisection
from qvm.exceptions import *
from qvm.util.misc import split_list

from typing import Any, Dict, List, Optional

# Logging configuration
#logging.basicConfig(filename='qvm_util_graph.log', encoding='utf-8', level=logging.DEBUG,
#                format='%(asctime)s %(message)s')
#logger = logging.getLogger("qvm_util_graph_logger")


def coupling_map_to_nodes(coupling_map: List[List[int]]) -> List[int]:
    """
    Transform coupling map to graph node set
    """

    nodes = set()

    for edge in coupling_map:
        for node in edge:
            nodes.add(node)

    return list(nodes)

def virtualize_coupling_map(
        coupling_map: List[List[int]],
        real_to_virtual: Dict[int, int]
    ):
    """ Virtualize the coupling map based on real to virtual mapping 
    It simply replace the qubit id to virtualized qubit id
    """
    virt_coupling_map = []
    for edge in coupling_map:
        virt_coupling_map.append([real_to_virtual[real] for real in edge])
    return virt_coupling_map

def merge_sub_graphs_nodes(sub_graph_nodes: List[List[int]]) -> List[int]:
    """
    Merge multiple subgraphs' nodes to a single node list
    """

    merged_graph_nodes = []

    # TODO(zhaoyilun): check there's no overlap between different subgraph
    for subgraph in sub_graph_nodes:
        merged_graph_nodes += subgraph

    return merged_graph_nodes


def extract_coupling_map(
        coupling_map: List[List[int]],
        subgraph_nodes: List[int]):
    """
    Extract new coupling_map from subgraph_nodes.
    For each edge in coupling_map, if any node not in subgraph_nodes we simply eliminate it
    """
    new_coupling_map = []

    for edge in coupling_map:
        if set(edge).issubset(subgraph_nodes): # Original edge should have both ends in subgrap
            new_coupling_map.append(edge)

    return new_coupling_map


class BasePartitioner:

    def __init__(self) -> None:
        pass

    def partition(self, 
            graph: Dict[int, List[int]], 
            k=4) -> List[List[int]]:
        return [] 


class NaivePartitioner(BasePartitioner):

    def __init__(self) -> None:
        super().__init__()

    def _dfs(self, 
            node: int,
            graph: Dict[int, List[int]], 
            visited: set, 
            cur_part: List[int], 
            partitions: List[List[int]],
            k: int) -> None:
    
        if len(cur_part) == k:
            partitions.append(copy.deepcopy(cur_part))
            cur_part.clear()
    
        cur_part.append(node)
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                self._dfs(neighbor, graph, visited, cur_part, partitions, k)
    
        return
    
    
    def partition(self, 
            graph: Dict[int, List[int]], 
            k=4) -> List[List[int]]:
        """
        Simple graph partition: 
        DFS the graph, when visited k nodes, put these nodes to a sub graph 
        """
        partitions = []
        visited = set()
        cur_part = []
        
        self._dfs(0, graph, visited, cur_part, partitions, k) 
        if cur_part:
            partitions.append(copy.deepcopy(cur_part))
    
        return partitions


class KlPartitioner(BasePartitioner):

    def __init__(self) -> None:
        super().__init__()

    def partition(self, graph) -> List[List[int]]:

        return list(kernighan_lin_bisection(graph)) 

class BfsPartitioner(BasePartitioner):

    def __init__(self) -> None:
        super().__init__()

    def _bfs_part(self,
            node: int,
            graph: Dict[int, List[int]],
            visited: set,
            partitions: List[List[int]],
            k: int):
        que = [] 
        que.append(node)
        count = 0
        part = []
        
        while len(que) > 0:
            layer_size = len(que) 
            for _ in range(layer_size):
                front = que[0]
                part.append(front)
                visited.add(front)
                count += 1
                if count == k:
                    break
                for neighbor in graph[front]:
                    if neighbor not in visited:
                        que.append(neighbor)
                que.pop(0)
            if count == k:
                break

        partitions.append(part)

    def partition(self, graph: Dict[int, List[int]], k=4) -> List[List[int]]:
        partitions = []
        visited = set()
        has_unvisited = True

        while has_unvisited:
            has_unvisited = False
            for node in graph:
                if node not in visited:
                    self._bfs_part(node, graph, visited, partitions, k)
                    has_unvisited = True

        return partitions 


class FrpPartitioner(BasePartitioner):

    """Implementation of MICRO-2019: A Case for Multi-Programming Quantum Computers

    Algorithm 1: Fair and Reliable Partitioning (FRP)
    
    Reference: https://dl.acm.org/doi/10.1145/3352460.3358287
    """

    def __init__(self,
                 graph: Optional[np.ndarray]=None,
                 errs: Optional[List[float]]=None) -> None:
        super().__init__()

        # Initialize some parameters for partitioning
        self._NUM_LEVELS = 3
        #alpha (float): alpha percent of root's neighbors
        #    should have `high` utility
        #beta (float): beta percent of nodes including root
        #    should have measurement errors lower than avg 
        #    measurement error
        self._alpha, self._beta = 0, 0
        self._is_low_cmr = False

        self._visited = set()
        self._utilities = []
        self._ranks = OrderedDict() 
        self._levels = []

        self._graph = None
        self._readout_errs = []
        self._mean_rd_errs = 0  # Average readout errors
        if errs:
            self._readout_errs = errs
        if graph:
            self._graph = graph
        
        # When called initialize() explicitly, this flag will be set to True
        self._init = False

    @property
    def is_low_cmr(self):
        return self._is_low_cmr

    @is_low_cmr.setter
    def is_low_cmr(self, is_low_cmr: bool):
        self._is_low_cmr = is_low_cmr

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph: np.ndarray):
        self._graph = graph

    @property
    def readout_errs(self):
        return self._readout_errs

    @readout_errs.setter
    def readout_errs(self, errs: List[float]):
        self._readout_errs = errs
        self._mean_rd_errs = np.average(errs)

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        self._alpha = val

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, val):
        self._beta = val

    def _get_utilities(self):
        """Compute utility for each vertex
        utility = (number of links)/(sum of link errors)
        """
        if self._graph is None:
            raise ValueError("Please first set the graph of FrpPartitioner")

        self._utilities = []
        for v in self._graph:
            n_links = sum(1 for l in v if l > 0)
            sum_err = sum(v)
            self._utilities.append(n_links / sum_err)
        return self._utilities

    def _bfs_single_part(self,
                         root: int,
                         sub_size: int):
        """Start from root node and grow a graph satisfying sub_size
        Args:
            root (int): Root node id
            sub_size (int): Subgraph size, i.e., the program size
        """
        if self._graph is None:
            raise ValueError("Please first set the graph of FrpPartitioner")

        que = []
        que.append(root)
        count = 0
        part = []

        while len(que) > 0:
            layer_size = len(que)
            for _ in range(layer_size):
                front = que[0]
                part.append(front)
                self._visited.add(front)
                count += 1
                if count == sub_size:
                    break
                neighbors = [i for i, e in enumerate(self._graph[front]) if e > 0 ]
                for n in neighbors:
                    # Here we also need to filter high measurement error nodes
                    # if current program is low CMR (Alg. 1 >> line 14-15)
                    need_filter_high_mer, _ = self._filter_high_mer(n)
                    if need_filter_high_mer:
                        warn("Find high measurement error node:{} "\
                                "when growing from root:{}".format(n, root))
                        continue

                    if n not in self._visited:
                        que.append(n)
                que.pop(0)
            if count == sub_size:
                break
        if count < sub_size:
            raise QvmError("Cannot grow a graph "\
                    "that satisfy the subgraph size from current root: {}".format(root))
        return part
    
    def _get_ranks(self):
        """Rank the vertexes in order of utility"""
        indexed_list = [(i,v) for i, v in enumerate(self._utilities)]
        sorted_list = sorted(indexed_list, key=lambda x: x[1], reverse=True)
        self._ranks = OrderedDict([(i[0], i[1]) for i in sorted_list])
        return self._ranks

    def _get_levels(self):
        """Partition the vertexes (physical qubits) into high, medium, low,
        3 levels based on utilities. 
        Here we assume it is a simple splict
        """
        if len(self._ranks) == 0:
            raise ValueError("Please calculate ranks first!")

        vertexes = list(self._ranks.keys())
        self._levels = [set(l) for l in split_list(vertexes, self._NUM_LEVELS)]
        return self._levels

    def _filter_high_mer(self, v: int):
        """Check if we need to filter a node with high measurement error"""
        is_cur_high_rd = 1 if self._readout_errs[v] >= self._mean_rd_errs else 0
        return is_cur_high_rd and self._is_low_cmr, is_cur_high_rd

    def _get_root(self):
        """Find root node to generate a subgraph
        A root with good quality should satisfy:
        1. alpha percent of root’s neighbors have high utility
        2. beta percent of nodes including root have measurement
           errors lower than avg measurement error
        Return:
            int: Id of root
        """
        if len(self._ranks) == 0:
            raise ValueError("Please first calculate ranks!")

        if len(self._levels) == 0:
            raise ValueError("Please first calculate levels")
        
        if not isinstance(self._graph, np.ndarray):
            raise ValueError("Please first set graph!")
        
        root = -1
        for v, _ in self._ranks.items():
            if v not in self._visited:
                # See Alg. 1 >> line 14-15: If CMR is low, exclude nodes with large measurement
                # errors. Here if CMR is low, we will not consider vertex with measurement error
                # larger than average measurement error
                need_filter_high_mer, is_cur_high_rd = self._filter_high_mer(v)
                if need_filter_high_mer:
                    continue
                
                # See Alg. 1 >> line 5-6: A valid root should have alpha percent of neighbors
                # with high utility, and beta percent of nodes have measurement errors lower 
                # than average measurement errors
                num_neighbors = sum([1 for n in self._graph[v] if n > 0])
                num_valid_nbs = sum([1 for n in self._graph[v] if n in self._levels[0]])
                if num_valid_nbs/num_neighbors < self._alpha:
                    continue
                num_valid_rds = (1 - is_cur_high_rd) +\
                                sum([1 for i,_ in enumerate(self._graph[v]) \
                                        if self._readout_errs[i] < self._mean_rd_errs])
                if num_valid_rds/(num_neighbors+1) < self._beta:
                    continue

                # Root is found
                root = v
                break
        if root < 0:
            raise QvmError("FRP Partition: No root available!")
        return root

    def initialize(self):
        """Initialize some intermediate reusable properties of the graph
        1. Initialize utilities
        2. Initialize ranks
        3. Initialize levels
        """
        if not isinstance(self._graph, np.ndarray):
            raise ValueError("Please first set the backend graph")

        self._get_utilities()
        self._get_ranks()
        self._get_levels()
        self._init = True

    def partition(self, 
                  sub_size: int) -> List[Any]:
        """Implementation of Fair and Reliable Partitioning
        See reference Algorithm. 1
        Ref: https://dl.acm.org/doi/10.1145/3352460.3358287
        Args:
            sub_size: Size of subgraph
        """ 
        if not self._init:
            self.initialize()

        part = []
        while len(self._visited) < self._graph.shape[0]:
            root = self._get_root()
            # Keep current status of visited
            cur_visited = copy.deepcopy(self._visited)
            try:
                part = self._bfs_single_part(root, sub_size)
                break
            except QvmError:
                warn("Failed to grow a subgraph from root: {}, "\
                        "current visited status: {}".format(root, self._visited)) 
                self._visited = cur_visited # Reset visited status
                self._visited.add(root) # But root should be visited
                #logger.warning("Failed to grow a subgraph from root: {}".format(root)) 
        return part


PARTITIONERS = {
    "naive": NaivePartitioner,
    "kl": KlPartitioner,
    "bfs": BfsPartitioner,
    "frp": FrpPartitioner
}


class ParitionProvider:

    _partitions = PARTITIONERS
    
    @classmethod
    def get_partioner(cls, name: str):
        return cls._partitions[name]()


