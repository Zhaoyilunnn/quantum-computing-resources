import copy

from typing import List
from qiskit.providers.backend import * 
from qiskit.providers.models import *
from qiskit.circuit import QuantumCircuit
from qiskit.pulse import Schedule
from qvm.util import extract_coupling_map
from util import *

class BackendManager:
    """ A simple qubit device manager
    """

    _compute_units = []

    def __init__(self, backend: BackendV1) -> None:
        _compute_units = self.init_compute_units(backend)

    def extract_compute_unit_conf(self, configuration: BackendConfiguration, sub_coupling_graph: List[int]):
        """
        Extract a new configuration for compute unit given a subgraph of original coupling graph
        """
        compute_unit_conf = copy.deepcopy(configuration)
        compute_unit_conf.n_qubits = len(sub_coupling_graph)
        compute_unit_conf.coupling_map = extract_coupling_map(configuration.coupling_map, sub_coupling_graph)

        # Extract gate configurations from sub_coupling_graph
        compute_unit_gates = [] 

        for gate in configuration.gates:
            gate_dict = gate.to_dict() 
            if 'coupling_map' in gate_dict:
                gate_dict['coupling_map'] = extract_coupling_map(gate_dict['coupling_map'], sub_coupling_graph)
            compute_unit_gates.append(GateConfig.from_dict(gate_dict))

        compute_unit_conf.gates = compute_unit_gates
        
        return compute_unit_conf


    def extract_single_compute_unit(self, backend: BackendV1, sub_coupling_graph: List[int]):
        """
        Extract a new backend from original backend given a subgraph of original coupling graph
        """

        compute_unit_conf = self.extract_compute_unit_conf(backend.configuration(), sub_coupling_graph)
        print(compute_unit_conf)
        compute_unit = copy.deepcopy(backend)
        compute_unit._configuration = compute_unit_conf
        return compute_unit
        

    def init_compute_units(self, backend: BackendV1) -> List[BackendV1]:
        """ Transform backend into a list of compute units based on some strategy """
        compute_units = []
        # TODO(zhaoyilun): compute unit extraction method
        # Input: backend, output: backend_list
        return compute_units

    def merge_compute_units(self, compute_units: List[BackendV1]) -> BackendV1:
        """ Merge allocated compute units to a single backend for compilation """
        backend = BackendV1()

        return backend
         
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
