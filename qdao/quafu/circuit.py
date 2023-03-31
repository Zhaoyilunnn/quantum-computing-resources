import numpy as np
import copy

from typing import List, Optional
from quafu.circuits.quantum_circuit import QuantumCircuit, QuantumGate, SingleQubitGate


class QuafuCircuitHelper:

    def __init__(
            self,
            circ: Optional[QuantumCircuit]=None
        ) -> None:
        self._circ = circ or None

    @property
    def circ(self):
        return self._circ

    @circ.setter
    def circ(self, circ: QuantumCircuit):
        self._circ = circ

    @property
    def num_qubits(self):
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        return self._circ.num

    @property
    def instructions(self):
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        # FIXME(zhaoyilun): temporarily remove barrier like this
        # Needs better impl
        return self._circ.gates[:-1]

    def get_instr_qubits(self, instruction: QuantumGate):
        if isinstance(instruction, SingleQubitGate):
            return [instruction.pos]
        return instruction.pos

    def init_circ_from_sv(self, sv: np.ndarray):
        from qdao.simulator import QdaoSimObj
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ")
        return QdaoSimObj(sv, self._circ)

    def gen_sub_circ(
            self,
            instrs: List[QuantumGate],
            num_local: int,
            num_primary: int
        ):
        """Generate a sub circuit based on a list of circuit instructions
        We assume there's no conditional instructions and no measurement
        instructions

        Args:
            instrs (List[QuantumGate]): A list of instructions
        Return:
            QdaoCircuit
        """
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set self._circ")

        from qdao.circuit import QdaoCircuit
        # 1. Get the set of qubits
        qset = set(range(num_local))
        for instr in instrs:
            for q in self.get_instr_qubits(instr):
                qset.add(q)

        sub_circ = QuantumCircuit(num_primary)

        real_qubits = sorted(list(qset))

        assert len(real_qubits) <= num_primary

        qubit_map = {
            q: i
            for i, q in enumerate(real_qubits)
        }

        for instr in instrs:
            new_instr = copy.deepcopy(instr)
            if isinstance(instr, SingleQubitGate):
                new_pos = qubit_map[instr.pos]
            else:
                new_pos = [qubit_map[q] for q in instr.pos]
            new_instr.pos = new_pos
            sub_circ.add_gate(new_instr)

        return QdaoCircuit(sub_circ, real_qubits)
