from collections.abc import MutableSequence
from typing import Iterable, List

from qiskit.circuit import QuantumCircuit


class BaseExecutable:

    def __init__(self,
            circ: QuantumCircuit,
            resource) -> None:
        self._circ = circ
        self._resource = resource

    @property
    def circ(self):
        return self._circ

    @property
    def resource(self):
        return self._resource

    @property
    def resource_ids(self):
        return self._resource_ids

    @resource_ids.setter
    def resource_ids(self, rid: int | List[int]):
        self._resource_ids = rid

    @property
    def num_resources(self):
        return self._num_resources

    @num_resources.setter
    def num_resources(self, n):
        self._num_resources = n


class Process:

    def __init__(self) -> None:
        self._resources = set()
        self._data = {}

    @property
    def data(self):
        return self._data

    @property
    def resources(self):
        return self._resources

    @data.setter
    def data(self, data_input: Iterable):
        """Sets the process data from a list of executables

        Args:
            data_input (Iterable): A sequence of executables
        """
        data_input = list(data_input)
        self._data = {}
        if not data_input:
            return
        if isinstance(data_input[0], BaseExecutable):
            for exe in data_input:
                self.append(exe)

    def append(self, exe: BaseExecutable):
        """Append executable to the end of the process"""
        self._data[exe.resource_ids] = exe
        self._resources.add(exe.resource_ids)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, rid):
        """Get executable that is compile on resource[rid]"""
        return self._data[rid]
