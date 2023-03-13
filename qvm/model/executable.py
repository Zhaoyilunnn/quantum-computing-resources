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
    def resource_id(self):
        return self._resource_id

    @resource_id.setter
    def resource_id(self, rid: int):
        self._resource_id = rid
