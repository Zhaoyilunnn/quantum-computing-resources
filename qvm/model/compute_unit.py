import copy
import matplotlib.pyplot as plt

from typing import List
from qiskit.providers.backend import * 
from qiskit.providers.models import *

from qvm.util.graph import * 
from qvm.util.backend import *
from qvm.util.misc import *
from utils.misc import *


class ComputeUnit:
    """ The minimum resource unit for compilation """
    
    def __init__(self, 
            backend: BackendV1,
            real_n_qubits: int,
            sub_coupling_graph: List[int],
            real_to_virtual=None) -> None:
        """
        `backend`: The real hardware model under the compute unit
        `real_n_qubits`: The actual number of qubits in the real backend
        `sub_coupling_graph`: The real qubit list of this compute unit
        `real_to_virtual`: Each real qubit binds to a virtual qubit id
        """
        self._backend = copy.deepcopy(backend) 
        self._real_qubits = sub_coupling_graph
        self._real_n_qubits = real_n_qubits

        if real_to_virtual:
            self._real_to_virtual = real_to_virtual
        else:
            self._real_to_virtual = {real: virtual for virtual, real in enumerate(self._real_qubits)}

    @property
    def backend(self):
        return self._backend

    @property
    def real_n_qubits(self):
        return self._real_n_qubits

    @property
    def real_qubits(self):
        """ The real qubit list, i.e., the node list in real backend
        """
        return self._real_qubits

    @property
    def real_to_virtual(self):
        """ The mapping from real qubit id to vircutal qubit id
        """
        return self._real_to_virtual

    def draw_nx_cmap(self, figname=None):
        """ Plot networkx format coupling map graph 
        """
        cmap = self._backend.configuration().coupling_map
        G = nx.Graph()

        for line in cmap:
            q0, q1 = line
            G.add_edge(q0, q1)

        plt.figure()
        nx.draw(G)

        if figname:
            plt.savefig(figname)

