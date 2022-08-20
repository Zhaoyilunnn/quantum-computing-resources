import sys
import numpy as np
from qiskit import *
from qiskit.circuit.random import random_circuit
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--num-qubits', type=int, default=10, help='number of qubits')
    parser.add_argument('--backend', type=str, default='statevector_simulator', help='simulation method')
    parser.add_argument('--mode', type=str, default='qasm', help='How to construct a circuit')
    parser.add_argument('--qasm-file', type=str, default='', help='The qasm file path')
    parser.add_argument('--depth', type=int, default=10, help='Depth of a circuit')
    return parser.parse_args()

def main():
    args = parse_args()
    
    circ = None
    if args.mode == 'qasm':
        if not args.qasm_file:
            raise Exception("Should set the qasm file path when using qasm mode")
        circ = QuantumCircuit().from_qasm_file(args.qasm_file)
    elif args.mode == 'random':
        num_qubits = int(args.num_qubits)
        depth = int(args.depth)
        circ = random_circuit(num_qubits, depth, measure=True)
    else:
        raise NotImplementedError("Unsupported circuit constructing mode!")
        
    backend = Aer.get_backend(args.backend)
    test = transpile(circ, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    # result = job.result()

if __name__ == '__main__':
    main()
