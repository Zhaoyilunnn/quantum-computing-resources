"""
This module provides methods to partition original circuit 
into sub-circuits. 
"""

from re import sub
from typing import List
from qiskit import QuantumCircuit


class BasePartitioner:
    """ Base class of circuit partition """

    def __init__(self) -> None:
        pass

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
