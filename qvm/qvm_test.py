from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile, schedule
from qiskit.providers import backend

from qiskit.providers.fake_provider import *
from qiskit.providers.fake_provider.fake_backend import decode_pulse_defaults
from qvm.backend_manager import * 
from qvm.process_manager import *

from util import *


class BaseTest:

    _backend = FakeLagos()
        
    def show_scheduled_debug_info(self, scheduled: Schedule) -> None:
        for inst in scheduled.instructions:
            print(inst)
    
    def run_experiments(self, transpiled, scheduled, verify):
        counts = {}
        if verify == 'pulse':
            counts = self._backend.run(scheduled).result().get_counts()
        elif verify == 'qasm':
            counts = self._backend.run(transpiled).result().get_counts()
        else:
            raise NotImplementedError("Unsupported verfication level, please choose either `pulse` or `qasm`")
        print(counts)

    def create_dummy_bell_state(self, q0: int, q1: int) -> QuantumCircuit:
        """
        Create a bell state circuit for test
        q0: the first qubit id to operate on
        q1: the second qubit id to operate on

        The circuit size will be q1+1, which is 
        useful to emulate virtualization
        """
        if q0 >= q1:
            raise ValueError("q0 should be smaller than q1")

        dummy_circ = QuantumCircuit(q1+1, q1+1)
        dummy_circ.h(q0)
        dummy_circ.cx(q0, q1)
        dummy_circ.measure([q0, q1], [q0, q1])
        return dummy_circ



class TestBackendManager(BaseTest):
    
    def setup_class(self):
        self._manager = BackendManager(self._backend)
        self._conf = self._backend.configuration()
        self._props = self._backend.properties() 

    def test_extract_compute_unit(self):

        sub_graph = [1, 2]

        compute_unit = self._manager.extract_single_compute_unit(sub_graph) 
        
        cu_conf = compute_unit.backend.configuration()
        cu_props = compute_unit.backend.properties()
        
        assert cu_conf.coupling_map == [[0, 1], [1, 0]]
        assert len(cu_props.qubits) == 2
        assert compute_unit.real_qubits == [1, 2]
        assert compute_unit.real_to_virtual == {1:0, 2:1}

        for gate in cu_props.gates:

            # Create a test gate coping from 
            # gate in compute unit, the only
            # difference should be qubits
            test_gate = copy.deepcopy(gate)
            real_q = compute_unit.real_qubits
            
            for i, q in enumerate(gate.qubits):
                vq = gate.qubits[i] # Virtual qubit id in compute unit gate
                test_gate.qubits[i] = real_q[vq] # Remap to real qubit id

            # Then the test gate should be the same as the original one
            assert test_gate in self._props.gates

    
    def test_compilation_on_compute_unit(self, verify):


        # Defined the qubits in compute unit
        sub_graph = [1,2,3]
        
        # Extract a compute unit from backend
        compute_unit = self._manager.extract_single_compute_unit(sub_graph) 

        plot_error(self._backend, figname="backend.png")
        plot_error(compute_unit.backend, figname="compute_unit.png")

        dummy_circ = self.create_dummy_bell_state(0, 1)

        fig = dummy_circ.draw(output='mpl')
        fig.savefig("bell_state.png")

        transpiled = transpile(dummy_circ, compute_unit.backend)
        print(transpiled._data) 
        real_transpiled = self._manager.circuit_virtual_to_real(transpiled, compute_unit)
        print(real_transpiled._data)
        scheduled = schedule(real_transpiled, self._backend)
        self.show_scheduled_debug_info(scheduled)

        #FIXME: uncomment this if you want to verify the execution results
        self.run_experiments(transpiled, scheduled, verify)

        print("================== Original ========================")
        dummy_circ = self.create_dummy_bell_state(1, 2)
        transpiled = transpile(dummy_circ, self._backend)
        scheduled = schedule(transpiled, self._backend)
        
        self.run_experiments(transpiled, scheduled, verify)


class TestProcessManager(BaseTest):

    def setup_class(self):
        self._manager = SimpleProcessManager(FakeLagos())

    def test_merge_schedules(self):
        dummy_circ = self.create_dummy_bell_state(0, 1)
        transpiled = transpile(dummy_circ, self._manager._backend)
        scheduled_0 = schedule(transpiled, self._manager._backend)
        print("===================== Schedule 0 ===========================")
        self.show_scheduled_debug_info(scheduled_0)

        dummy_circ = self.create_dummy_bell_state(3, 5)
        transpiled = transpile(dummy_circ, self._manager._backend)
        scheduled_1 = schedule(transpiled, self._manager._backend)
        print("===================== Schedule 1 ===========================")
        self.show_scheduled_debug_info(scheduled_1) 

        merged_sch = self._manager._merge_schedules([scheduled_0, scheduled_1])
        print("===================== Schedule ===========================")
        self.show_scheduled_debug_info(merged_sch)


class TestQvm:
    """
    Integration of backend manager and process manager
    """
    pass
