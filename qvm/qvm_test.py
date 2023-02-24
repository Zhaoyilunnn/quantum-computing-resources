from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile, schedule

from qiskit.providers.fake_provider import *
from qvm.backend_manager import * 
from qvm.process_manager import *

from util import *


class BaseTest:

    #_backend = FakeLagos()
    _backend = FakeManila()
        
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

    def create_dummy_bell_state(self, 
            qubits: Union[List[Tuple[int, int]], Tuple[int, int]],
            num_qubits=None) -> QuantumCircuit:
        """
        Create a bell state circuit for test
        q0: the first qubit id to operate on
        q1: the second qubit id to operate on

        The circuit size will be q1+1, which is 
        useful to emulate virtualization
        """
        def do_bell_state(dummy_circ, q0, q1):
            dummy_circ.h(q0)
            dummy_circ.cx(q0, q1)
            dummy_circ.measure([q0, q1], [q0, q1])


        dummy_circ = None
        if isinstance(qubits, tuple):
            q0, q1 = qubits
            if q0 >= q1:
                raise ValueError("q0 should be smaller than q1")

            dummy_circ = QuantumCircuit(q1+1, q1+1)
            do_bell_state(dummy_circ, q0, q1)
        else:
            if not num_qubits:
                raise ValueError("Please specify the number of qubits if input is a set of qubit pairs")

            dummy_circ = QuantumCircuit(num_qubits, num_qubits)
            for (q0, q1) in qubits:
                if q0 >= num_qubits or q1 >= num_qubits:
                    raise ValueError("num_qubits must be larger than all involved qubits")
                do_bell_state(dummy_circ, q0, q1)

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

        dummy_circ = self.create_dummy_bell_state((0, 1))

        fig = dummy_circ.draw(output='mpl')
        fig.savefig("bell_state.png")

        transpiled = transpile(dummy_circ, compute_unit.backend)
        print(transpiled._data) 
        real_transpiled = self._manager.circuit_virtual_to_real(transpiled, compute_unit)
        print(real_transpiled._data)
        sch_cu = schedule(real_transpiled, self._backend)
        self.show_scheduled_debug_info(sch_cu)
        self.run_experiments(transpiled, sch_cu, verify)

        print("================== Original ========================")
        dummy_circ = self.create_dummy_bell_state((1, 2))
        transpiled = transpile(dummy_circ, self._backend)
        sch_original = schedule(transpiled, self._backend)
        self.show_scheduled_debug_info(sch_original)
        self.run_experiments(transpiled, sch_original, verify)

        assert sch_cu.instructions == sch_original.instructions 


class TestProcessManager(BaseTest):

    def test_qvm_manager(self):

        manager = ProcessManagerFactory.get_manager("qvm", FakeManila()) 
        
        test_eprs = [(0,1), (2,3)]

        dummy_circ = self.create_dummy_bell_state(test_eprs[0])
        transpiled = transpile(dummy_circ, manager._backend)
        sch_first = schedule(transpiled, manager._backend)
        print("===================== Schedule 0 ===========================")
        self.show_scheduled_debug_info(sch_first)
        #self.run_experiments(transpiled, sch_first, 'pulse')

        dummy_circ = self.create_dummy_bell_state(test_eprs[1])
        transpiled = transpile(dummy_circ, manager._backend)
        sch_second = schedule(transpiled, manager._backend)
        print("===================== Schedule 1 ===========================")
        self.show_scheduled_debug_info(sch_second) 
        #self.run_experiments(transpiled, sch_second, 'pulse')

        sch_merged = manager._merge_schedules([sch_first, sch_second])
        print("===================== Merged Schedule ===========================")
        self.show_scheduled_debug_info(sch_merged)
        #self.run_experiments(transpiled, sch_merged, 'pulse')

        dummy_circ = self.create_dummy_bell_state(test_eprs, num_qubits=4)
        print("===================== Original Schedule ===========================")
        transpiled = transpile(dummy_circ, manager._backend)
        sch_original = schedule(transpiled, manager._backend)
        self.show_scheduled_debug_info(sch_original)
        #self.run_experiments(transpiled, sch_original, 'qasm')

        #assert sch_merged.instructions == sch_original.instructions

    def test_baseline_manager(self):
        
        manager = ProcessManagerFactory.get_manager("baseline", FakeManila())

        test_eprs = [(0,1), (2,3)]
        dummy_circ_first = self.create_dummy_bell_state(test_eprs[0])
        dummy_circ_second = self.create_dummy_bell_state(test_eprs[1])
        
        dummy_circ_original = self.create_dummy_bell_state(test_eprs, num_qubits=4)
        transpiled = transpile(dummy_circ_original, manager._backend)
        sch_original = schedule(transpiled, manager._backend)

        dummy_circ_merged = manager.merge_circuits([dummy_circ_first, dummy_circ_second])
        transpiled = transpile(dummy_circ_original, manager._backend)
        sch_merged = schedule(transpiled, manager._backend)

        assert sch_original.instructions == sch_merged.instructions



class TestQvm:
    """
    Integration of backend manager and process manager
    """
    pass
