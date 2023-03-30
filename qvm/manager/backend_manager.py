import copy
from logging import warning

from typing import List
from qiskit import transpile
from qiskit.providers.backend import *
from qiskit.providers.models import *
from qiskit.circuit import QuantumCircuit
from qiskit.pulse import Schedule

from qvm.exceptions import QvmError
from qvm.model.compute_unit import ComputeUnit
from qvm.model.executable import BaseExecutable, Process
from qvm.util.graph import *
from qvm.util.circuit import circuit_virtual_to_real
from qvm.util.backend import *
from qvm.util.misc import *
from utils.misc import *


class BaseBackendManager:
    """ Backend manager implementation
    Functions
    1. Partition a real backend into virtualized compute units
    2. Allocate compute units for quantum circuits
    """


    def __init__(self, backend: BackendV1) -> None:
        self._backend = copy.deepcopy(backend)
        self._cu_size = 4
        self._compute_units = []
        # FIXME(zhaoyilun): is it ok to always explicitly init compute units?
        #self._compute_units = self.init_compute_units()

    @property
    def cu_size(self):
        return self._cu_size

    @cu_size.setter
    def cu_size(self, ncu):
        self._cu_size = ncu

    def init_helpers(self) -> None:
        """ Init helper classes """
        self._partitioner = GraphPartitionProvider.get_partitioner("naive")
        self._graph_extractor = BaseBackendGraphExtractor(self._backend)

    def init_compute_units(self) -> List[ComputeUnit]:
        """ Transform backend into a list of compute units based on some strategy """

        if not self._cu_size:
            raise ValueError("Please set compute unit size before init compute units")

        self._compute_units = []
        #cm_graph = coupling_map_to_graph(self._backend.configuration().coupling_map)
        cm_graph = self._graph_extractor.extract()
        parts = self._partitioner.partition(cm_graph, self._cu_size)
        for part in parts:
            cu = self.extract_single_compute_unit(part)
            self._compute_units.append(cu)
        return self._compute_units

    def extract_compute_unit_props(self,
            sub_coupling_graph: List[int],
            real_to_virtual: Dict[int, int]):
        """
        Extract new properties for compute unit given a subgraph of original coupling graph
        """
        cu_props = copy.deepcopy(self._backend.properties())

        # Extract qubits
        cu_props.qubits = []
        for i, qubit in enumerate(self._backend.properties().qubits):
            if i in sub_coupling_graph:
                cu_props.qubits.append(qubit)

        # Extract gates
        cu_props.gates = []
        for gate in self._backend.properties().gates:
            if set(gate.qubits).issubset(sub_coupling_graph):
                virt_qubits = [real_to_virtual[real] for real in gate.qubits]
                # TODO(zhaoyilun): Ugly!!
                virt_gate = copy.deepcopy(gate)
                virt_gate.qubits = virt_qubits
                cu_props.gates.append(virt_gate)

        return BackendProperties.from_dict(cu_props.to_dict())

    def extract_compute_unit_conf(self,
            sub_coupling_graph: List[int],
            real_to_virtual: Dict[int, int]):
        """
        Extract a new configuration for compute unit given a subgraph of original coupling graph
        """
        cu_conf = copy.deepcopy(self._backend.configuration())
        cu_conf.n_qubits = len(sub_coupling_graph)

        coupling_map = self._backend.configuration().coupling_map
        real_coupling_map = extract_coupling_map(coupling_map, sub_coupling_graph)
        cu_conf.coupling_map = virtualize_coupling_map(real_coupling_map, real_to_virtual)

        # Extract gate configurations from sub_coupling_graph
        conf_gates = []

        for gate in self._backend.configuration().gates:
            gate_dict = gate.to_dict()
            if 'coupling_map' in gate_dict:
                real_coupling_map = extract_coupling_map(
                        gate_dict['coupling_map'], sub_coupling_graph)
                gate_dict['coupling_map'] = virtualize_coupling_map(
                        real_coupling_map, real_to_virtual)
            conf_gates.append(GateConfig.from_dict(gate_dict))

        cu_conf.gates = conf_gates

        return cu_conf

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
        return ComputeUnit(compute_unit,
                self._backend.configuration().n_qubits,
                sub_coupling_graph)

    def select_compute_units(self, circuit: QuantumCircuit):
        """ Select compute units for given quantum circuit """
        #TODO(zhaoyilun): implementation
        pass

    def merge_compute_units(self, compute_units: List[ComputeUnit]) -> ComputeUnit:
        """ Merge allocated compute units to a single backend for compilation """

        # First get merged list of qubits
        merged_qubits = self.merge_graph_nodes_from_cus(compute_units)

        return self.extract_single_compute_unit(merged_qubits)

    def merge_graph_nodes_from_cus(self, compute_units: List[ComputeUnit]) -> List[int]:
        """
        Get coupling maps from each compute unit and merge them into a single list of
        coupling map nodes, i.e., the merged backend's qubit list
        """
        list_subgraph_nodes = [cu.real_qubits for cu in compute_units]
        return merge_sub_graphs_nodes(list_subgraph_nodes)

    def circuit_virtual_to_real(self,
            circuit: QuantumCircuit,
            compute_unit: ComputeUnit) -> QuantumCircuit:
        """
        Transform virtual circuit to real circuit.
        i.e., map the QuantunCircuitInstruction's virtual qubit id to real qubit id

        This method should be called after circuit level compilation and before pulse
        level compilation
        """
        return circuit_virtual_to_real(circuit, compute_unit)


    def allocate(self, circuit: QuantumCircuit):
        """ Allocate compute units for a quantum circuit
        This is the naive impl
        1. Get #qubits and then get #cus
        2. Randomly select #cus cus
        3. Merge these cus and return

        """
        # Number of qubits
        nq = circuit.num_qubits
        # Number of compute units
        ncu = (nq//self._cu_size+1 if nq % self._cu_size > 0 else nq//self._cu_size)

        # Randomly select #ncu compute units
        num_cus = len(self._compute_units)
        cu_ids = select_n_integers(ncu, 0, num_cus)
        cu_list = [self._compute_units[i] for i in cu_ids]

        # Merge allocated cus
        merged_nodes = self.merge_graph_nodes_from_cus(cu_list)
        return self.extract_single_compute_unit(merged_nodes)

    def compile(self, circuit: QuantumCircuit) -> Process:
        """ Implement a simple redundant compilation
        In this version, we assume that compute unit size is the same as
        circuit size
        """
        if not self._compute_units:
            raise QvmError("Compute units should be initialized first")

        proc = Process()
        for cu_id, cu in enumerate(self._compute_units):
            try:
                exe = self._do_compile(circuit, cu)
            except Exception:
                warning("Current circuit: {} cannot compile on compute unit: {}".format(circuit, cu))
                continue
            exe.resource_id = cu_id
            exe.num_resources = len(self._compute_units)
            proc.append(exe)
        return proc

    def _do_compile(self, circuit: QuantumCircuit, cu: ComputeUnit) -> BaseExecutable:
        """ Compilation on compute unit
        For exp on simulator, this just compile to circuit,
        For exp on real-device, this needs to compile to pulse
        """
        # Transpile on virtual backend
        vtrans = transpile(circuit, cu.backend)
        # Transform to real circuit
        #rtrans = circuit_virtual_to_real(vtrans, cu)
        # Construct executable
        #exe = BaseExecutable(rtrans, cu)
        exe = BaseExecutable(vtrans, cu)
        return exe

    def batch_execute(self, executables: List[Schedule]) -> None:
        """ Merge multiple quantum executables into a large quantum executable and execute on the backend """
        # 1. merge_executables(executables)
        # 2. backend.execute(executables)
        # 3. ..
        pass

    def merge_executables(self, circuits: List[Schedule]) -> Schedule:
        exe = Schedule()

        return exe


class KlBackendManager(BaseBackendManager):

    """ Manager using KL algorithm to get compute units """

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def init_helpers(self) -> None:
        self._partitioner = GraphPartitionProvider.get_partitioner("kl")
        self._graph_extractor = NormalBackendNxGraphExtractor(self._backend)

    def init_compute_units(self) -> List[ComputeUnit]:
        self._compute_units = []
        cm_graph = self._graph_extractor.extract()
        parts = self._partitioner.partition(cm_graph)
        for part in parts:
            cu = self.extract_single_compute_unit(part)
            self._compute_units.append(cu)
        return self._compute_units


class BfsBackendManager(BaseBackendManager):
    """Manager using BFS to get connected compute units
    Workflow:
        1. Randomly select a root
        2. Grow a compute unit (with fixed size) from the root
        3. Remove the compute unit from the original graph and
           repeat 1 & 2 until all nodes are assigned to compute
           units
    """

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def init_helpers(self) -> None:
        self._partitioner = GraphPartitionProvider.get_partitioner("bfs")
        self._graph_extractor = BaseBackendGraphExtractor(self._backend)

class FrpBackendManager(BaseBackendManager):
    """Using FRP to extract a compute unit"""

    def init_helpers(self) -> None:
        self._graph_extractor = BackendAdjMatGraphExtractor(self._backend)
        graph = self._graph_extractor.extract()
        rd_errs = self._graph_extractor.get_readout_errs()
        self._partitioner = GraphPartitionProvider.get_partitioner(
                                                "frp",
                                                graph=graph,
                                                errs=rd_errs)

    def init_compute_units(self) -> List[ComputeUnit]:
        if not self._cu_size:
            raise ValueError("Please set compute unit size before init compute units")

        self._compute_units = []
        part = self._partitioner.partition(self._cu_size)
        while part:
            cu = self.extract_single_compute_unit(part)
            self._compute_units.append(cu)
            part = self._partitioner.partition(self._cu_size)
        return self._compute_units
