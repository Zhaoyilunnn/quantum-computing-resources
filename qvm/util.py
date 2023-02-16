import copy

from typing import Dict, List

def couple_map_to_graph(coupling_map: List[List]):
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

#TODO(zhaoyilun): graph partition
# 1. DFS and Fix sub-graph size

def DFS(node: int,
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
            DFS(neighbor, graph, visited, cur_part, partitions, k)

    return


def naive_graph_partition(graph: Dict[int, List[int]], k=4) -> List[List[int]]:
    """
    Simple graph partition: 
    DFS the graph, when visited k nodes, put these nodes to a sub graph 
    """
    partitions = []
    visited = set()
    cur_part = []
    
    DFS(0, graph, visited, cur_part, partitions, k) 
    if cur_part:
        partitions.append(copy.deepcopy(cur_part))

    return partitions


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

