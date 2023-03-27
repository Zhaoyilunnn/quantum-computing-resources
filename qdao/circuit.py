"""
This module provides methods to partition original circuit
into sub-circuits.
"""
import logging

from typing import List
from qiskit.circuit import QuantumCircuit, CircuitInstruction


class VirtualCircuit:

    def __init__(
            self,
            circ: QuantumCircuit,
            real_qubits: List[int]
        ) -> None:
        self._circ = circ
        self._real_qubits = real_qubits

    @property
    def circ(self) -> QuantumCircuit:
        return self._circ

    @circ.setter
    def circ(self, circ: QuantumCircuit):
        self._circ = circ

    @property
    def real_qubits(self) -> List[int]:
        return self._real_qubits


class BasePartitioner:
    """ Base class of circuit partition """

    def __init__(
            self,
            np=4,
            nl=2
        ) -> None:
        self._np = np
        self._nl = nl

    @property
    def np(self):
        return self._np

    @np.setter
    def np(self, n):
        self._np = n

    @property
    def nl(self):
        return self._nl

    @nl.setter
    def nl(self, n):
        self._nl = n

    def _gen_sub_circ(
            self,
            circ: QuantumCircuit,
            instrs: List[CircuitInstruction]
        ) -> VirtualCircuit:
        """Generate a sub circuit based on a list of circuit instructions
        We assume there's no conditional instructions and no measurement
        instructions

        Args:
            circ (QuantumCircuit): The circuit that originally contains
                instrs. Used to extract qubit object.
            instrs (List[CircuitInstruction]): A list of instructions
        Return:
            VirtualCircuit
        """

        # 1. Get the set of qubits
        qset = set(range(self._nl))
        for instr in instrs:
            for q in instr.qubits:
                qset.add(q._index)

        #num_qubits = len(qset)
        sub_circ = QuantumCircuit(self._np)

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
        return VirtualCircuit(sub_circ, real_qubits)

    def run(self, circuit: QuantumCircuit) -> List[VirtualCircuit]:

        sub_circs = []

        return sub_circs

class StaticPartitioner(BasePartitioner):
    """ Static partitioner which traverse the operations in original order """


    def run(self, circuit: QuantumCircuit) -> List[VirtualCircuit]:

        sub_circs = []

        instrs = []
        qset = set()
        for instr in circuit.data:
            qs = set()
            for q in instr.qubits:
                if q._index >= self._nl:
                    qs.add(q._index)
            if len(qset | qs) <= (self._np - self._nl):
                qset = qset | qs
                instrs.append(instr)
            else:
                sub_circ = self._gen_sub_circ(circuit, instrs)
                sub_circs.append(sub_circ)
                logging.info("Find sub-circuit: {}, qubits: {}".format(sub_circ.circ, qset))
                instrs = [instr]
                qset = qs
        if instrs:
            sub_circ = self._gen_sub_circ(circuit, instrs)
            sub_circs.append(sub_circ)

        return sub_circs


PARTITIONERS = {
    "static": StaticPartitioner
}


class PartitionerProvider:

    @classmethod
    def get_partitioner(
            cls,
            part_name: str,
            **configs,
        ):
        return PARTITIONERS[part_name](**configs)
