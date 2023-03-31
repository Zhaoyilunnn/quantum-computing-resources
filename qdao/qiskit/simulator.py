import numpy as np

from qiskit_aer import Aer


class QiskitSimulator:

    def __init__(self) -> None:
        self._sim = Aer.get_backend("aer_simulator")

    def run(self, simobj) -> np.ndarray:

        res = self._sim.run(simobj.circ).result()
        return res.get_statevector().data

