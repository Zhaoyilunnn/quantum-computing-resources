import copy

from typing import Final, List
from qiskit.providers.backend import * 
from qiskit.providers.models import *
from qiskit.circuit import QuantumCircuit
from qiskit.pulse import Schedule
from qvm.util import coupling_map_to_nodes, extract_coupling_map, merge_sub_graphs_nodes, virtualize_coupling_map
from util import *

class ComputeUnit:
    """ The minimum resource unit for compilation """
    
    def __init__(self, 
            backend: BackendV1, 
            sub_coupling_graph: List[int],
            real_to_virtual=None) -> None:
        """
        `backend`: The real hardware model under the compute unit
        `sub_coupling_graph`: The real qubit list of this compute unit
        `real_to_virtual`: Each real qubit binds to a virtual qubit id
        """
        self._backend = copy.deepcopy(backend) 
        self._real_qubits = sub_coupling_graph

        if real_to_virtual:
            self._real_to_virtual = real_to_virtual
        else:
            self._real_to_virtual = {real: virtual for virtual, real in enumerate(self._real_qubits)}

    @property
    def backend(self):
        return self._backend

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

    
class BackendManager:
    """ Backend manager implementation
    Functions
    1. Partition a real backend into virtualized compute units
    2. Allocate compute units for quantum circuits
    """

    _compute_units = []
    _backend = None

    def __init__(self, backend: BackendV1) -> None:
        self._backend = copy.deepcopy(backend) 
        self._compute_units = self.init_compute_units()

    def init_compute_units(self) -> List[ComputeUnit]:
        """ Transform backend into a list of compute units based on some strategy """
        compute_units = [] 
        return compute_units

    def extract_compute_unit_props(self, 
            sub_coupling_graph: List[int],
            real_to_virtual: Dict[int, int]):
        """
        Extract new properties for compute unit given a subgraph of original coupling graph
        """
        sub_props = copy.deepcopy(self._backend.properties())
        
        # Extract qubits
        sub_props.qubits = []
        for i, qubit in enumerate(self._backend.properties().qubits):
            if i in sub_coupling_graph:
                sub_props.qubits.append(qubit)

        # Extract gates
        sub_props.gates = []
        for gate in self._backend.properties().gates:
            if set(gate.qubits).issubset(sub_coupling_graph):
                virt_qubits = [real_to_virtual[real] for real in gate.qubits]
                # TODO(zhaoyilun): Ugly!!
                virt_gate = copy.deepcopy(gate)
                virt_gate.qubits = virt_qubits
                sub_props.gates.append(virt_gate) 

        return BackendProperties.from_dict(sub_props.to_dict())

    def extract_compute_unit_conf(self, 
            sub_coupling_graph: List[int],
            real_to_virtual: Dict[int, int]):
        """
        Extract a new configuration for compute unit given a subgraph of original coupling graph
        """
        sub_conf = copy.deepcopy(self._backend.configuration())
        sub_conf.n_qubits = len(sub_coupling_graph)
        
        coupling_map = self._backend.configuration().coupling_map
        real_coupling_map = extract_coupling_map(coupling_map, sub_coupling_graph)
        sub_conf.coupling_map = virtualize_coupling_map(real_coupling_map, real_to_virtual)
        
        # Extract gate configurations from sub_coupling_graph
        compute_unit_gates = [] 

        for gate in self._backend.configuration().gates:
            gate_dict = gate.to_dict() 
            if 'coupling_map' in gate_dict:
                real_coupling_map = extract_coupling_map(gate_dict['coupling_map'], sub_coupling_graph)
                gate_dict['coupling_map'] = virtualize_coupling_map(real_coupling_map, real_to_virtual) 
            compute_unit_gates.append(GateConfig.from_dict(gate_dict))

        sub_conf.gates = compute_unit_gates
        
        return sub_conf

    def extract_single_compute_unit(self, sub_coupling_graph: List[int]):
        """
        Extract a new backend from original backend given a subgraph of original coupling graph
        """

        if not isinstance(self._backend, BackendV1):
            raise ValueError("backend is not set!")
        
        # The real to virtual mapping
        real_to_virtual = {real: virtual for virtual, real in enumerate(sub_coupling_graph)}     

        compute_unit_conf = self.extract_compute_unit_conf(sub_coupling_graph, real_to_virtual)
        compute_unit_props = self.extract_compute_unit_props(sub_coupling_graph, real_to_virtual)

        compute_unit = copy.deepcopy(self._backend)
        compute_unit._configuration = compute_unit_conf

        # TODO(zhaoyilun): some _backends may not support properties
        compute_unit._properties = compute_unit_props
        return ComputeUnit(compute_unit, sub_coupling_graph) 
        
    def merge_compute_units(self, compute_units: List[ComputeUnit]) -> ComputeUnit:
        """ Merge allocated compute units to a single backend for compilation """

        # First get merged list of qubits
        merged_qubits = self.get_graph_nodes_from_cus(compute_units)

        return self.extract_single_compute_unit(merged_qubits)

    def get_graph_nodes_from_cus(self, compute_units: List[ComputeUnit]) -> List[int]:
        """
        Get coupling maps from each compute unit and merge them into a single list of 
        coupling map nodes, i.e., the merged backend's qubit list
        """
        list_subgraph_nodes = []
        for cu in compute_units:
            list_subgraph_nodes.append(cu.real_qubits)

        return merge_sub_graphs_nodes(list_subgraph_nodes)
         
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
