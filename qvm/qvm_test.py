from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile, schedule
from qiskit.providers import backend

from qiskit.providers.fake_provider import *
from qiskit.providers.fake_provider.fake_backend import decode_pulse_defaults
from qvm.backend_manager import * 
from qvm.process_manager import *

from util import *


def show_scheduled_debug_info(scheduled: Schedule) -> None:
    for inst in scheduled.instructions:
        print(inst)


class TestBackendManager:
    
    _backend = FakeLagos() 
    _manager = BackendManager(_backend)
    _conf = _backend.configuration()
    _props = _backend.properties() 
    #pretty(_conf.to_dict())

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

        def run_experiments(transpiled, scheduled, verify):
            counts = {}
            if verify == 'pulse':
                counts = self._backend.run(scheduled).result().get_counts()
            elif verify == 'qasm':
                counts = self._backend.run(transpiled).result().get_counts()
            else:
                raise NotImplementedError("Unsupported verfication level, please choose either `pulse` or `qasm`")
            print(counts)
        

        # Defined the qubits in compute unit
        sub_graph = [1,2,3]
        
        # Extract a compute unit from backend
        compute_unit = self._manager.extract_single_compute_unit(sub_graph) 

        plot_error(self._backend, figname="backend.png")
        plot_error(compute_unit.backend, figname="compute_unit.png")

        dummy_circ = QuantumCircuit(2, 2)
        dummy_circ.h(0)
        dummy_circ.cx(0, 1)
        dummy_circ.measure([0, 1], [0, 1])

        fig = dummy_circ.draw(output='mpl')
        fig.savefig("bell_state.png")

        transpiled = transpile(dummy_circ, compute_unit.backend)
        print(transpiled._data) 
        real_transpiled = self._manager.circuit_virtual_to_real(transpiled, compute_unit)
        print(real_transpiled._data)
        scheduled = schedule(real_transpiled, self._backend)
        show_scheduled_debug_info(scheduled)

        #FIXME: uncomment this if you want to verify the execution results
        run_experiments(transpiled, scheduled, verify)

        print("================== Original ========================")
        dummy_circ = QuantumCircuit(3, 3)
        dummy_circ.h(1)
        dummy_circ.cx(1, 2)
        dummy_circ.measure([1, 2], [1, 2])
        transpiled = transpile(dummy_circ, self._backend)
        scheduled = schedule(transpiled, self._backend)
        
        run_experiments(transpiled, scheduled, verify)


class TestProcessManager:

    #_manager = BaseProcessManager(FakeLagos())
    _manager = SimpleProcessManager(FakeLagos())

    def test_merge_schedules(self):
        dummy_circ = QuantumCircuit(2, 2)
        dummy_circ.h(0)
        dummy_circ.cx(0, 1)
        dummy_circ.measure([0, 1], [0, 1])
        transpiled = transpile(dummy_circ, self._manager._backend)
        scheduled_0 = schedule(transpiled, self._manager._backend)
        print("===================== Schedule 0 ===========================")
        show_scheduled_debug_info(scheduled_0)

        dummy_circ = QuantumCircuit(6, 6)
        dummy_circ.h(3)
        dummy_circ.cx(3, 5)
        dummy_circ.measure([3, 5], [3, 5])
        transpiled = transpile(dummy_circ, self._manager._backend)
        scheduled_1 = schedule(transpiled, self._manager._backend)
        print("===================== Schedule 1 ===========================")
        show_scheduled_debug_info(scheduled_1) 

        merged_sch = self._manager._merge_schedules([scheduled_0, scheduled_1])
        print("===================== Schedule ===========================")
        show_scheduled_debug_info(merged_sch)
