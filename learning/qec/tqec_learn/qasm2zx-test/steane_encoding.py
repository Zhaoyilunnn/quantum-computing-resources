"""
pyzx==0.9.0
qiskit==2.1.1
"""

from qiskit import QuantumCircuit
import qiskit.qasm2 as qasm2
from pyzx.circuit import Circuit as ZxCircuit


def steane_encoding() -> QuantumCircuit:
    qc = QuantumCircuit(8, 1, name="Steane Encoding")

    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.h(0)
    qc.measure(0, 0)

    qc.reset(0)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 5)
    qc.cx(0, 6)
    qc.h(0)
    qc.measure(0, 0)

    qc.reset(0)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 3)
    qc.cx(0, 5)
    qc.cx(0, 7)
    qc.h(0)
    qc.measure(0, 0)

    return qc


def qiskit2zx(circuit: QuantumCircuit) -> ZxCircuit:
    qasm_str = qasm2.dumps(circuit)
    zx_circuit = ZxCircuit.from_qasm(qasm_str)
    return zx_circuit


if __name__ == "__main__":
    circuit = steane_encoding()
    print(circuit)
    zx_circuit = qiskit2zx(circuit)
    print(zx_circuit)
    zx_graph = zx_circuit.to_graph()
    print(zx_graph)
