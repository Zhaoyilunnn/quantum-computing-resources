"""
Reference:
    https://www.nature.com/articles/s41586-023-06846-3
"""

import sys
import argparse
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector


def apply_measure_w_block(qc: QuantumCircuit):
    qc.t(0)
    qc.t(2).inverse()
    qc.h(3)
    qc.t(4).inverse()
    qc.t(6)

    qc.cx(3, 5)
    qc.cx(3, 1)
    qc.cx(1, 2)
    qc.cx(1, 0)
    qc.cx(5, 4)
    qc.cx(5, 6)

    qc.cx(3, 5)
    qc.cx(3, 1)
    qc.h(3)

    qc.t(0).inverse()
    qc.t(2)
    qc.t(4)
    qc.t(6).inverse()



def apply_measure_sz_block(qc: QuantumCircuit):

    qc.h(0)
    qc.h(2)
    qc.h(3)
    qc.h(4)
    qc.h(6)

    qc.cx(3, 5)
    qc.cx(3, 1)
    qc.cx(1, 2)
    qc.cx(1, 0)
    qc.cx(5, 4)
    qc.cx(5, 6)

    qc.cx(3, 5)
    qc.cx(3, 1)
    qc.h(3)

    qc.h(0)
    qc.h(2)
    qc.h(4)
    qc.h(6)


def measure_ancilla(qc: QuantumCircuit):
    qc.barrier()
    qc.measure(1, 0)
    qc.measure(3, 1)
    qc.measure(5, 2)


def get_args():
    parser = argparse.ArgumentParser(description="Implementation of the paper 'Encoding a magic state with beyond break-even fidelity'")
    parser.add_argument("--stage", type=int, default=1, help="How many stages to construct the quantum circuit in Fig. 2(a); 1: Only code preparation; 2: 1 + magic state initialization by measurement; 3: 1 + 2 + Error detection measurement")
    return parser.parse_args()


def breakdown_sv(sv):
    print("M\tProb\t\t\tMeasurement\tData")
    prob_dict = sv.probabilities_dict()
    for k, v in prob_dict.items():
        if v > 1e-6:
            k = str(k)
            print(f"{k}\t{v}\t{k[1]+k[3]+k[5]}\t\t{k[0]+k[2]+k[4]+k[6]}")


def probe_sv(qc):
    sv = Statevector(qc)
    breakdown_sv(sv)


def main():

    args = get_args()
    stage = args.stage

    qc = QuantumCircuit(7, 3)
    qc.initialize("+0+0+0+")
    # qc.initialize("0000000")
    if stage >= 1:
        apply_measure_sz_block(qc)
        # probe_sv(qc)
        measure_ancilla(qc)
        qc.x(6).c_if(1, 1)
        # qc.save_state()
    if stage >= 2:
        qc.reset(3)
        apply_measure_w_block(qc)
        qc.save_state()
        measure_ancilla(qc)

    sim = Aer.get_backend("statevector_simulator")
    res = sim.run(qc).result()
    # print(res.get_counts())
    sv = res.get_statevector()
    breakdown_sv(sv)

    # for i, a in enumerate(sv):
    #     if a > 1e-6:
    #         print(f"{i}\t{a}")

    # sv.draw("paulivec")
    # import matplotlib.pyplot as plt
    # plt.savefig("test.pdf")

    # qc.measure(1, 0)
    # qc.measure(3, 1)
    # qc.measure(5, 2)

if __name__ == "__main__":
    main()
