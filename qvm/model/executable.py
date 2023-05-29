from collections.abc import MutableSequence
from typing import Iterable, List, Set

from qiskit.circuit import QuantumCircuit

from qvm.model.compute_unit import ComputeUnit


class BaseExecutable:
    """An Executable is a compiled circuit on some comp units"""

    def __init__(self,
            circ: QuantumCircuit,
            comp_unit: ComputeUnit) -> None:
        self._circ = circ
        self._comp_unit = comp_unit

    @property
    def circ(self):
        """Compiled quantum circuit"""
        return self._circ

    @property
    def comp_unit(self):
        """Compute unit"""
        return self._comp_unit

    @property
    def comp_unit_ids(self):
        """Indices of original compute units

        An executable may be compiled on multiple connected
        compute units, which are then merged to one comp unit"""
        return self._comp_unit_ids

    @comp_unit_ids.setter
    def comp_unit_ids(self, idxes: int | Set[int]):
        if isinstance(idxes, int):
            self.comp_unit_ids = {idxes}
            return
        self._comp_unit_ids = idxes

    @property
    def num_total_cus(self):
        """Total number of comp units within the backend"""
        return self._num_total_cus

    @num_total_cus.setter
    def num_total_cus(self, num_total_cus):
        self._num_total_cus = num_total_cus


class Process:
    """Quantum Process

    Contains a list of executables compiled on different compute units,
    also serves as a executable queue, sorted by priority

    TODO: implement priority based `append`"""

    def __init__(self, num_qubits=None) -> None:
        self._comp_unit_ids = set()
        self._data = []
        self._num_qubits = 0
        if num_qubits:
            self._num_qubits = num_qubits

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, idx):
        """Get executable that is compile on resource[rid]"""
        return self._data[idx]

    @property
    def data(self):
        """List of executables"""
        return self._data

    @property
    def num_qubits(self):
        """Number of qubits"""
        return self._num_qubits

    @property
    def comp_unit_ids(self):
        """Indices of compute units from all executables"""
        return self._comp_unit_ids

    @data.setter
    def data(self, data_input: Iterable):
        """Sets the process data from a list of executables

        Args:
            data_input (Iterable): A sequence of executables
        """
        data_input = list(data_input)
        self._data = []
        if not data_input:
            return
        if isinstance(data_input[0], BaseExecutable):
            for exe in data_input:
                self.append(exe)

    def append(self, exe: BaseExecutable):
        """Append executable to the end of the process"""
        self._data.append(exe)
        for idx in exe.comp_unit_ids:
            self._comp_unit_ids.add(idx)
