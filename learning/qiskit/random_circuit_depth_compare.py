"""
This script compares the circuit depths of randomly generated quantum circuits and their corresponding synthesized circuits from unitary matrices.

Intent:
- For a number of samples, generate random quantum circuits with varying numbers of qubits and depths.
- Transpile each random circuit to a specified basis gate set and record its depth.
- Compute the unitary matrix of each random circuit, then synthesize a new circuit from this unitary using Qiskit's UnitarySynthesis pass, and record its depth.
- Save the results (number of qubits, original depth, synthesized depth, etc.) to a CSV file.
- Plot a bar chart comparing the depths of the original and synthesized circuits for each sample.

Usage:
- Run the script directly: `python random_circuit_depth_compare.py`
- You can adjust parameters such as the number of samples, qubit range, basis gates, output CSV path, and SVG plot path by modifying the arguments in the `compare_circuit_depths` call in the `__main__` block.
- The script will output a CSV file with depth data and an SVG file with a bar chart visualization.

Dependencies:
- numpy==2.3.2
- matplotlib==3.10.6
- qiskit==2.1.1

Example:
    python random_circuit_depth_compare.py
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator
from qiskit.circuit.random import random_circuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import UnitarySynthesis
from qiskit.circuit.library import UnitaryGate


def generate_random_circuit(num_qubits, depth, seed=None):
    # Generate a random circuit with the given number of qubits and depth
    return random_circuit(num_qubits, depth, max_operands=2, measure=False, seed=seed)


def get_unitary_matrix(circuit):
    # Get the unitary matrix of the circuit
    return Operator(circuit).data


def synthesize_unitary_circuit(unitary, num_qubits, basis_gates):
    # Use Qiskit's UnitarySynthesis pass to decompose the unitary into a circuit
    unitary_gate = UnitaryGate(unitary)
    qc = QuantumCircuit(num_qubits)
    qc.append(unitary_gate, range(num_qubits))
    # Transpile to the given basis gates
    transpiled_qc = transpile(qc, basis_gates=basis_gates, optimization_level=3)
    return transpiled_qc


def compare_circuit_depths(
    num_samples=5,
    min_qubits=3,
    max_qubits=8,
    basis_gates=["cx", "u3"],
    seed_base=42,
    csv_path="depths.csv",
    svg_path="depths.svg",
):
    depths = []
    for i in range(num_samples):
        num_qubits = np.random.randint(min_qubits, max_qubits + 1)
        depth = np.random.randint(3, 10)
        seed = seed_base + i
        print(f"\nSample {i + 1}: {num_qubits} qubits, depth {depth}, seed {seed}")

        # Generate random circuit
        rand_circ = generate_random_circuit(num_qubits, depth, seed=seed)
        rand_circ_t = transpile(
            rand_circ, basis_gates=basis_gates, optimization_level=3
        )
        orig_depth = rand_circ_t.depth()
        print(f"Original random circuit depth: {orig_depth}")

        # Get unitary matrix
        unitary = get_unitary_matrix(rand_circ)

        # Synthesize new circuit from unitary
        synth_circ = synthesize_unitary_circuit(unitary, num_qubits, basis_gates)
        synth_depth = synth_circ.depth()
        print(f"Synthesized circuit from unitary depth: {synth_depth}")

        depths.append(
            {
                "sample": i + 1,
                "num_qubits": num_qubits,
                "depth_param": depth,
                "seed": seed,
                "original_depth": orig_depth,
                "synthesized_depth": synth_depth,
            }
        )

    # Write depths to CSV
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "sample",
            "num_qubits",
            "depth_param",
            "seed",
            "original_depth",
            "synthesized_depth",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in depths:
            writer.writerow(row)

    # Plot bar chart
    samples = [row["sample"] for row in depths]
    orig_depths = [row["original_depth"] for row in depths]
    synth_depths = [row["synthesized_depth"] for row in depths]

    x = np.arange(len(samples))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x - width / 2, orig_depths, width, label="Original", log=True)
    ax.bar(x + width / 2, synth_depths, width, label="Synthesized", log=True)

    ax.set_xlabel("Sample")
    ax.set_ylabel("Circuit Depth (log scale)")
    ax.set_title("Comparison of Circuit Depths")
    ax.set_xticks(x)
    ax.set_xticklabels(samples)
    ax.legend()

    plt.tight_layout()
    plt.savefig(svg_path, format="svg")


if __name__ == "__main__":
    # You can change basis_gates as needed, e.g. ['cx', 'u3'] or ['cx', 'rz', 'sx', 'x']
    compare_circuit_depths(
        num_samples=5,
        min_qubits=3,
        max_qubits=8,
        basis_gates=["cx", "u3"],
        seed_base=42,
        csv_path="depths.csv",
        svg_path="depths.svg",
    )
