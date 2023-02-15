from typing import List
from qiskit.providers.backend import BackendV2
from qiskit.circuit import QuantumCircuit
from qiskit.pulse import Schedule
from util import *

class BackendManager:
    """ A simple qubit device manager
    """

    _compute_units = []

    def __init__(self, backend: BackendV2) -> None:
        _compute_units = self.init_compute_units(backend)

    def init_compute_units(self, backend: BackendV2) -> List[BackendV2]:
        """ Transform backend into a list of compute units based on some strategy """
        compute_units = []
        # TODO(zhaoyilun): compute unit extraction method
        return compute_units
         
    def allocate(self, circuit: QuantumCircuit):
        """ Allocate compute units for a quantum circuit """
        # TODO(zhaoyilun):
        # 1. Get #qubits
        # 2. Get List[BackendV2]
        # 3. Merge 2 into a single backend
        pass

    def batch_execute(self, executables: List[Schedule]) -> None:
        """ Merge multiple quantum executables into a large quantum executable and execute on the backend """
        # 1. merge_executables(executables)
        # 2. backend.execute(executables)
        # 3. ..
        pass

    def merge_executables(self, circuits: List[Schedule]) -> Schedule:
        exe = Schedule()

        return exe
