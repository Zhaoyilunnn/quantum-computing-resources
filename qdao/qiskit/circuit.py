from typing import Optional
import numpy as np
from qiskit.circuit import QuantumCircuit
from .initializer import initialize

QuantumCircuit.initialize = initialize

class QiskitCircuitHelper:

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

    def init_circ_from_sv(self, sv: np.ndarray) -> QuantumCircuit:
        """Initialize qiskit QuantumCircuit from given statevector

        Comments:
            1. Currently qiskit QuantumCircuit.initialize will
               append an initialize instruction at the end of
               the circuit, we need create a new instance and
               init from statevector at the begining
        """
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ before initializing from sv!")

        nq = self._circ.num_qubits
        circ = QuantumCircuit(nq)
        circ.initialize(sv, range(nq))
        circ.compose(self._circ, inplace=True)
        return circ

    def get_num_qubits(self):
        if not isinstance(self._circ, QuantumCircuit):
            raise ValueError("Please set circ before initializing from sv!")
        return self._circ.num_qubits
