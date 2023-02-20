from qiskit.circuit import QuantumCircuit
from qiskit import transpile, schedule
from qiskit.providers import backend

from qiskit.providers.fake_provider import *
from qvm.backend_manager import * 

from util import *


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

    
    def test_compilation_on_compute_unit(self):

        sub_graph = [1, 2, 3]

        compute_unit = self._manager.extract_single_compute_unit(sub_graph) 

        plot_error(self._backend, figname="backend.png")
        plot_error(compute_unit.backend, figname="compute_unit.png")

        dummy_circ = QuantumCircuit(2, 2)
        dummy_circ.h(0)
        dummy_circ.cx(0, 1)
        dummy_circ.measure([0, 1], [0, 1])

        #pretty(self._backend.configuration().channels)
        print(self._backend.configuration().coupling_map)
        #pretty(self._backend.defaults().to_dict())

        print(dummy_circ.qregs)
        print(dummy_circ.qubits)

        transpiled = transpile(dummy_circ, compute_unit.backend)
        print(transpiled.qregs)
        print(transpiled._data) 
        for inst in transpiled._data:
            for q in inst.qubits:
                print(q.index)
        real_transpiled = self._manager.circuit_virtual_to_real(transpiled, compute_unit)
        print(real_transpiled._data)
        scheduled = schedule(real_transpiled, self._backend)
        for inst in scheduled.instructions:
            print(inst)

        print("================== Original ========================")
        transpiled = transpile(dummy_circ, self._backend)
        scheduled = schedule(transpiled, self._backend)
        for inst in scheduled.instructions:
            print(inst)
