"""Print fidelity vs. circuit depth"""



import copy
import sys
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import CircuitInstruction
from qiskit_aer import Aer
from qvm.util.circuit import QvmFidCalculator
from qiskit.circuit.random.utils import random_circuit
from qiskit.providers.fake_provider.backends import FakeCairo


def append_noise_circ(org: QuantumCircuit, noise: QuantumCircuit, rep: int):
    new_circ = copy.deepcopy(org)
    assert rep >= 0
    for _ in range(rep):
        new_circ.append(noise.to_instruction(), qargs=list(range(noise.num_qubits)))
    return new_circ


def append_swap(org: QuantumCircuit, rep: int):
    new_circ = copy.deepcopy(org)
    for _ in range(rep):
        new_circ.swap(0, 1)
        new_circ.swap(0, 1)
    return new_circ

def bell_state():
    bell = QuantumCircuit(2)
    bell.x(0)
    # bell.cnot(0, 1)
    return bell

def main():

    nums = int(sys.argv[1])
    assert nums >= 2

    # benchmark_circ = QuantumCircuit.from_qasm_file("QASMBench/small/qaoa_n3/qaoa_n3.qasm")
    benchmark_circ = bell_state()
    ideal_circ = copy.deepcopy(benchmark_circ)
    ideal_circ.measure_all()
    # noise = random_circuit(2, 30, measure=False)
    device = FakeCairo()
    simulator = Aer.get_backend("aer_simulator")
    counts_ideal = simulator.run(ideal_circ, shots=2**20).result().get_counts()

    print(f"depth\tfidelity")
    for r in range(1, nums):
        # deep_circ = append_noise_circ(noise, noise, r-1)
        deep_circ = append_swap(benchmark_circ, r-1)

        deep_circ.measure_all()
        print(deep_circ)

        pst_calculator = QvmFidCalculator()

        counts_noisy = device.run(deep_circ, shots=2**20).result().get_counts()
        print(counts_ideal)

        pst = pst_calculator.calc_pst(counts_ideal, counts_noisy)
        print(f"{r}\t{pst}")


if __name__ == '__main__':
    main()
