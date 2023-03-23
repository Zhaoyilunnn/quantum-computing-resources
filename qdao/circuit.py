"""
This module provides methods to partition original circuit 
into sub-circuits. 
"""

from re import sub
from typing import List
from qiskit.circuit import QuantumCircuit, CircuitInstruction


class BasePartitioner:
    """ Base class of circuit partition """

    def __init__(self) -> None:
        pass

    def _gen_sub_circ(self, 
                      circ: QuantumCircuit,
                      instrs: List[CircuitInstruction]) -> QuantumCircuit:
        """Generate a sub circuit based on a list of circuit instructions
        We assume there's no conditional instructions and no measurement 
        instructions
        
        Args:
            circ (QuantumCircuit): The circuit that originally contains
                instrs. Used to extract qubit object.
            instrs (List[CircuitInstruction]): A list of instructions
        Return:
            QuantumCircuit
        """
        
        # 1. Get the set of qubits
        qset = set()
        for instr in instrs:
            for q in instr.qubits:
                qset.add(q._index)

        num_qubits = len(qset)
        sub_circ = QuantumCircuit(num_qubits)
        
        real_qubits = sorted(list(qset))
        qubit_map = {
            circ.qubits[q]: sub_circ.qubits[i] 
            for i, q in enumerate(real_qubits)
        }

        for instr in instrs:
            op = instr.operation.copy()
            if len(instr.clbits) > 0:
                raise NotImplementedError("Currently not support measure/control operations")
            qubits = [qubit_map[q] for q in instr.qubits]
            sub_instr = CircuitInstruction(op, qubits=qubits)
            sub_circ.append(sub_instr)

        sub_circ.save_state()
        #print(sub_circ)
        return sub_circ

    def run(self, circuit: QuantumCircuit) -> List[QuantumCircuit]:

        sub_circs = []

        return sub_circs

class StaticPartitioner(BasePartitioner):
    """ Static partitioner which traverse the operations in original order """

    def __init__(self) -> None:
        super().__init__()

    def run(self, circuit: QuantumCircuit) -> List[QuantumCircuit]:

        sub_circs = []

        return sub_circs
