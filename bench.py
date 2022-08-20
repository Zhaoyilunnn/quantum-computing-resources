import sys
import numpy as np
from qiskit import *

def main():
    qasm_file = sys.argv[1]
    circ = QuantumCircuit().from_qasm_file(qasm_file)
    backend = Aer.get_backend('statevector_simulator')
    job = backend.run(circ)
    result = job.result()

if __name__ == '__main__':
    main()
