"""Simulator provider"""

from qiskit_aer import Aer


SIMS = {
    "qiskit": Aer.get_backend("aer_simulator")
}


class SimulatorProvider:

    @classmethod
    def get_simulator(
            cls,
            backend_name: str
        ):
        return SIMS[backend_name]
