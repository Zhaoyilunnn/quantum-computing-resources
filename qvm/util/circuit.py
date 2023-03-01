import copy

from typing import List
from qiskit.circuit import \
        QuantumCircuit, \
        QuantumRegister, \
        ClassicalRegister, \
        Qubit, \
        Clbit

from qiskit.quantum_info import state_fidelity
from qiskit.result import Counts

from qiskit_aer import Aer 

def relocate_circuit(circuit: QuantumCircuit,
                     locations: List[int],
                     num_qubits: int) -> QuantumCircuit:
    """ Relocate qubits in a circuit 
    
    Args:
        circuit: the original circuit;
        qubits: the new locations, qubit `i` in original circuit will be
                relocated to locations[i] 
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
        r_qubits = [] # Create new qubits and then transform to tuple
        for q in inst.qubits:
            r_qubits.append(r_circ._qubits[locations[q._index]])
        r_circ._data[ii].qubits = tuple(r_qubits)

        r_clbits = [] # Create new clbits and then transform to tuple
        for c in inst.clbits:
            r_clbits.append(r_circ._clbits[locations[c._index]])
        r_circ._data[ii].clbits = tuple(r_clbits)

    return r_circ


class BaseFidelityCalculator:
    """
    A simple fidelity calulation, use counts as estimated SV
    """

    _sv_sim = Aer.get_backend("statevector_simulator")

    def __init__(self) -> None:
        pass

    def _counts_to_sv(self, counts: Counts):
        """ Trans form counts to state vector """
        pass

    def calc_fidelity(self, circ: QuantumCircuit, counts: Counts):
        """ Galculate fidelity based on counts
        1. Execute on ideal simulator
        2. Transform ideal counts and noise counts to Statevector 
        3. Calculate fidelity using state_fidelity

        Args:
            circ: Quanutm circuit to execute
            counts: Execution counts result from noise backend (simulator or real device) 
        Return:
            fidelity
        """
        pass

