from qiskit.providers.fake_provider import *
from qvm.backend_manager import * 


class TestBackendManager:
    
    _backend = FakeLondon()
    _manager = BackendManager(FakeLondon())
    _conf = _backend.configuration()
    _props = _backend.properties() 

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
