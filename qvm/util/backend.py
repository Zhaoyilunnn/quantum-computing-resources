import networkx as nx
import numpy as np

from qiskit.providers.backend import BackendV1
from qiskit.providers.models import BackendConfiguration, BackendProperties

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
        """ Transform backend configuration to error map
        Return:
            graph: np.array[num_qubits, num_qubits], where graph[i][j] is the 
            cx error ratio
        """
        conf = self._backend.configuration()
        props = self._backend.properties()

        cm = conf.coupling_map # couplng map
        props_dict = props.to_dict()

        num_qubits = conf.num_qubits
        graph = np.zeros((num_qubits, num_qubits)) 

        for line in cm:
            for item in props_dict["gates"]:
                if item["qubits"] == line:
                    q0, q1 = line
                    graph[q0, q1] = item["parameters"][0]["value"]
                    break
        
        return graph


class NormalBackendNxGraphExtractor(BaseBackendGraphExtractor):

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def extract(self):
        """ Transform coupling map to networkx graph """
        graph = nx.Graph()

        conf = self._backend.configuration()
        props = self._backend.properties()

        cm = conf.coupling_map # couplng map
        props_dict = props.to_dict()

        for line in cm:
            for item in props_dict["gates"]:
                if item["qubits"] == line:
                    q0, q1 = line
                    err = item["parameters"][0]["value"]
                    graph.add_edge(q0, q1, weight=1-err)
                    break
        
        return graph
