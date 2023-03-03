from qiskit.providers.backend import BackendV1

from typing import List

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

def conf_to_graph():
    """ Transform backend configuration to error map
    Args:
        conf: Backendconfiguration
    Return:
        graph: np.array[num_qubits, num_qubits], where graph[i][j] is the 
        cx error ratio
    """


class BaseBackendGraphExtractor:
    
    def __init__(self, backend: BackendV1) -> None:
        self._backend = backend 

    def extract(self):
        # Get coupling map from backend
        cm = self._backend.configuration().coupling_map 
        return coupling_map_to_graph(cm)


class NormalBackendGraphExtractor(BaseBackendGraphExtractor):

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def extract(self):
        pass  
