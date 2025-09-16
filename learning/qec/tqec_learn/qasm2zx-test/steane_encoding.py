"""
pyzx==0.9.0
qiskit==2.1.1
"""

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
import qiskit.qasm2 as qasm2
from pyzx.circuit import Circuit as ZxCircuit


def steane_encoding() -> QuantumCircuit:
    qc = QuantumCircuit(10)

    qc.h(0)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    qc.cx(0, 6)
    qc.h(0)

    qc.h(1)
    qc.cx(1, 3)
    qc.cx(1, 4)
    qc.cx(1, 7)
    qc.cx(1, 8)
    qc.h(1)

    qc.h(2)
    qc.cx(2, 3)
    qc.cx(2, 5)
    qc.cx(2, 7)
    qc.cx(2, 9)
    qc.h(2)

    return qc


def qiskit2zx(circuit: QuantumCircuit) -> ZxCircuit:
    qasm_str = qasm2.dumps(circuit)
    zx_circuit = ZxCircuit.from_qasm(qasm_str)
    return zx_circuit


if __name__ == "__main__":
    circuit = steane_encoding()
    print(circuit)
    print(qasm2.dumps(circuit))
    zx_circuit = qiskit2zx(circuit)
    zx_circuit.to_graph()
    print(zx_circuit)
