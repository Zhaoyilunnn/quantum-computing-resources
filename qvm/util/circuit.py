import copy

from typing import List
from qiskit.circuit import \
        QuantumCircuit, \
        QuantumRegister, \
        ClassicalRegister, \
        Qubit, \
        Clbit

def relocate_circuit(circuit: QuantumCircuit,
                     locations: List[int],
                     num_qubits: int) -> QuantumCircuit:
    """ Relocate circuit's qubit locations 
    
    Args:
        circuit: the original circuit;
        qubits: the new locations, q_i in original circuit will be
                relocated to q_qubits[i]
        num_qubits: the number of qubits in new circuit
    
    Return:
        A QuantumCircuit with relocated qubits 
    
    """

    # Create relocated circuits and registers
    r_circ = copy.deepcopy(circuit)
    r_qregister = QuantumRegister(num_qubits, 'q')
    r_cregister = ClassicalRegister(num_qubits, 'c')

    # Reset qregs and cregs
    r_circ.qregs = [r_qregister]
    r_circ.cregs = [r_cregister]

    # Reset qubits and clbits
    r_circ._qubits = [Qubit(r_qregister, iq) for iq in range(num_qubits)]
    r_circ._clbits = [Clbit(r_cregister, ic) for ic in range(num_qubits)]

    for ii, inst in enumerate(r_circ._data):
        r_qubits = [] # Create new real qubits and then transform to tuple
        for iq, q in enumerate(inst.qubits):
            r_qubits.append(r_circ.qubits[locations[q.index]])
        r_circ._data[ii].qubits = tuple(r_qubits)

        r_clbits = [] # Create new real clbits and then transform to tuple
        for ic, c in enumerate(inst.clbits):
            r_clbits.append(r_circ.clbits[locations[c.index]])
        r_circ._data[ii].clbits = tuple(r_clbits)

    return r_circ
