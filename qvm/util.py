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
