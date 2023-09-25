from qiskit import QuantumCircuit
from qiskit.primitives import Estimator
from qiskit.opflow import Z, I

circ = QuantumCircuit(5)

for i in range(5):
    if i % 2 == 0:
        circ.h(i)

circ.cnot(0, 1)

# circ.measure_all()

print(circ)

hamiltonian = (1 * I^I^I^Z^Z) + (1 * Z^Z^I^I^I) + (1 * I^Z^Z^I^I) + (1 * Z^I^I^I^Z)

est = Estimator()
res = est.run(circ, hamiltonian).result()
print(res)
