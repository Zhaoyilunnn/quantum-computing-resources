"""
Name: qiskit
Version: 2.1.1
Name: qiskit-qasm3-import
Version: 0.6.0
"""

from qiskit import QuantumCircuit, transpile, qasm3

import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "qasm_file", type=str, help="File path of OpenQASM3 benchmark file"
    )

    return parser.parse_args()


def num_condition_ops(circ: QuantumCircuit):
    """Get the number of operations that is conditioned on classical bits"""
    num_cond_ops = 0
    for i in range(len(circ.data)):
        op = circ.data[i].operation
        if op.condition:
            num_cond_ops += 1
    return num_cond_ops


def main():
    args = parse_args()
    # For OpenQASM2

    try:
        circ = qasm3.load(args.qasm_file)
        print(f"Successfully loaded QASM file: {args.qasm_file}")
    except Exception as e:
        print(f"Failed to load QASM file: {args.qasm_file}. Error: {e}")
    # circ = qasm3.load(args.qasm_file)

    # backend = Fake127QPulseV1()


if __name__ == "__main__":
    main()
