"""
Reference:
    https://www.nature.com/articles/s41586-023-06846-3
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(7, 3)
qc.initialize("+0+0+0+")

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

print("M\tProb\t\t\tMeasurement\tData")
sv = Statevector(qc)
prob_dict = sv.probabilities_dict()
for k, v in prob_dict.items():
    if v > 1e-6:
        k = str(k)
        print(f"{k}\t{v}\t{k[1]+k[3]+k[5]}\t\t{k[0]+k[2]+k[4]+k[6]}")

# for i, a in enumerate(sv):
#     if a > 1e-6:
#         print(f"{i}\t{a}")

# sv.draw("paulivec")
# import matplotlib.pyplot as plt
# plt.savefig("test.pdf")

qc.measure(1, 0)
qc.measure(3, 1)
qc.measure(5, 2)
