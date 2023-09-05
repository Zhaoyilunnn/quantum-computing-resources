import sys
import time
from qiskit.circuit import QuantumCircuit

from qiskit.compiler import transpile
from qiskit_aer import Aer

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"python {sys.argv[0]} <num-qubits> <depth>")
        sys.exit(1)

    from qiskit.circuit.random.utils import random_circuit

    # Number of qubits
    n = int(sys.argv[1])

    # Depth
    d = int(sys.argv[2])

    sim = Aer.get_backend("aer_simulator")
    circ = random_circuit(n, d, max_operands=2, measure=False)
    circ.draw(output="mpl", filename="temp.svg")

    circ = transpile(circ, sim)
    file_name = "qasm/rqc_n{}_d{}.qasm".format(n, d)
    with open(file_name, 'w') as f:
        f.write(circ.qasm())
