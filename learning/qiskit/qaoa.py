"""
Reference: https://github.com/Qiskit/qiskit-ibm-runtime/blob/main/docs/tutorials/qaoa_with_primitives.ipynb

"""


import numpy as np

# Pre-defined ansatz circuit, operator class and visualization tools
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.visualization import plot_distribution
from qiskit.opflow import Z, I, X, Y

from qiskit.primitives import Estimator, Sampler

# SciPy minimizer routine
from scipy.optimize import minimize


# Problem to Hamiltonian operator
# hamiltonian = SparsePauliOp.from_list([("IIIZZ", 1), ("IIZIZ", 1), ("IZIIZ", 1), ("ZIIIZ", 1)])
hamiltonian = (1 * I^I^I^Z^Z) + (1 * I^I^Z^I^Z) + (1 * I^Z^I^I^Z) + (1 * Z^I^I^I^Z)
np.save("test_hamiltonian.npy", hamiltonian.to_matrix())
hamiltonian_2 = (0.3980 * Y^Z) + (-0.3980 * Z^I) + (-0.0113 * Z^Z) + (0.1810 * X^X)
np.save("vqe_hamiltonian.npy", hamiltonian_2.to_matrix())
# hamiltonian = 1 * Z^I^I^I^Z
# QAOA ansatz circuit
ansatz = QAOAAnsatz(hamiltonian, reps=2)
# Draw
# ansatz.decompose(reps=3).draw("mpl")
ansatz = ansatz.decompose(reps=3)
print(ansatz)


def cost_func(params, ansatz, hamiltonian, estimator):
    """Return estimate of energy from estimator

    Parameters:
        params (ndarray): Array of ansatz parameters
        ansatz (QuantumCircuit): Parameterized ansatz circuit
        hamiltonian (SparsePauliOp): Operator representation of Hamiltonian
        estimator (Estimator): Estimator primitive instance

    Returns:
        float: Energy estimate
    """
    cost = estimator.run(ansatz, hamiltonian, parameter_values=params).result().values[0]
    return cost


estimator = Estimator()
sampler = Sampler()
x0 = 2 * np.pi * np.random.rand(ansatz.num_parameters)
res = minimize(cost_func, x0, args=(ansatz, hamiltonian, estimator), method="COBYLA")
print(res)

qc = ansatz.assign_parameters(res.x)
# Add measurements to our circuit
qc.measure_all()
print(qc)

samp_dist = sampler.run(qc, shots=int(1e4)).result().quasi_dists[0]

print(samp_dist.binary_probabilities())
