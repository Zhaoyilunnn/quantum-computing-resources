import copy

from typing import Dict, List

def coupling_map_to_graph(coupling_map: List[List]):
    """
    Transform coupling map to dictionary for convenience
    """
    graph = {}
    
    for edge in coupling_map:
        if len(edge) != 2:
            raise ValueError("Each edge should be a List with length 2!")
        node = edge[0]
        neighbor = edge[1]
        graph.setdefault(node, [])
        graph[node].append(neighbor)

    return graph

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


PARTITIONERS = {
    "naive": NaivePartitioner
}


class ParitionProvider:

    _partitions = PARTITIONERS
    
    @classmethod
    def get_partioner(cls, name: str):
        return cls._partitions[name]()



# ChatGPT generated solution
def partition_graph(graph, subgraph_size):
    visited = [False] * len(graph)
    subgraphs = []
    num_nodes = len(graph)
    subgraph_count = num_nodes // subgraph_size

    # Create subgraphs
    for i in range(subgraph_count):
        start_node = i * subgraph_size
        subgraph = []
        while start_node < num_nodes and visited[start_node]:
            start_node += 1
        if start_node == num_nodes:
            break
        dfs(start_node, graph, visited, subgraph, subgraph_size)
        subgraphs.append(subgraph)

    # Handle any remaining nodes that were not partitioned
    remaining_nodes = [i for i in range(num_nodes) if not visited[i]]
    remaining_index = 0
    for i in range(len(subgraphs)):
        while len(subgraphs[i]) < subgraph_size and remaining_index < len(remaining_nodes):
            node = remaining_nodes[remaining_index]
            if all(n in subgraphs[i] for n in graph[node]):
                subgraphs[i].append(node)
                visited[node] = True
                remaining_index += 1
            else:
                remaining_index += 1

    return subgraphs

def dfs(node, graph, visited, subgraph, subgraph_size):
    visited[node] = True
    subgraph.append(node)
    if len(subgraph) == subgraph_size:
        return
    for neighbor in graph[node]:
        if not visited[neighbor] and len(subgraph) < subgraph_size and all(n in subgraph for n in graph[neighbor]):
            dfs(neighbor, graph, visited, subgraph, subgraph_size)

