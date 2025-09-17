"""
pyzx==0.9.0
qiskit==2.1.1
"""

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
import qiskit.qasm2 as qasm2
from pyzx.circuit import Circuit as ZxCircuit


def steane_encoding() -> QuantumCircuit:
    ancilla = QuantumRegister(3, "ancilla")
    data = QuantumRegister(7, "data")
    bits = ClassicalRegister(3, "bits")
    qc = QuantumCircuit(ancilla, data, bits)

    qc.h(ancilla[0])
    qc.cx(ancilla[0], data[0])
    qc.cx(ancilla[0], data[1])
    qc.cx(ancilla[0], data[2])
    qc.cx(ancilla[0], data[3])
    qc.h(ancilla[0])
    qc.measure(ancilla[0], bits[0])

    qc.h(ancilla[1])
    qc.cx(ancilla[1], data[0])
    qc.cx(ancilla[1], data[1])
    qc.cx(ancilla[1], data[4])
    qc.cx(ancilla[1], data[5])
    qc.h(ancilla[1])
    qc.measure(ancilla[1], bits[1])

    qc.h(ancilla[2])
    qc.cx(ancilla[2], data[0])
    qc.cx(ancilla[2], data[2])
    qc.cx(ancilla[2], data[4])
    qc.cx(ancilla[2], data[6])
    qc.h(ancilla[2])
    qc.measure(ancilla[2], bits[2])

    return qc


def qiskit2zx(circuit: QuantumCircuit) -> ZxCircuit:
    qasm_str = qasm2.dumps(circuit)
    print(qasm_str)
    zx_circuit = ZxCircuit.from_qasm(qasm_str)
    return zx_circuit


if __name__ == "__main__":
    circuit = steane_encoding()
    print(circuit)
    zx_circuit = qiskit2zx(circuit)
    print(zx_circuit)
