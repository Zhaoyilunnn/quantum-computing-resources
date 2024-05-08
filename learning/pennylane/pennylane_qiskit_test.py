import pennylane as qml

import qiskit
from qiskit_aer import noise

# Error probabilities
prob_1 = 0.001  # 1-qubit gate
prob_2 = 0.01   # 2-qubit gate

# Depolarizing quantum errors
error_1 = noise.depolarizing_error(prob_1, 1)
error_2 = noise.depolarizing_error(prob_2, 2)

# Add errors to noise model
noise_model = noise.NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1, ['u1', 'u2', 'u3'])
noise_model.add_all_qubit_quantum_error(error_2, ['cx'])
# noise_model = None

# Create a PennyLane device
# dev = qml.device('qiskit.aer', wires=2, noise_model=noise_model, shots=None)
# dev = qml.device('qiskit.aer', wires=2, shots=None, backend='statevector_simulator')
# dev = qml.device('qiskit.aer', wires=2, shots=None, backend='aer_simulator_density_matrix')
dev = qml.device('default.mixed', wires=2)

# Create a PennyLane quantum node run on the device
#### @qml.qnode(dev)
#### def circuit(x, y, z):
####     qml.RZ(z, wires=[0])
####     qml.RY(y, wires=[0])
####     qml.RX(x, wires=[0])
####     qml.CNOT(wires=[0, 1])
####     # return qml.expval(qml.PauliZ(wires=1))
####     return qml.state()

@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=[0])
    qml.CNOT(wires=[0, 1])
    qml.BitFlip(0.1, wires=0)
    qml.DepolarizingChannel(0.1, wires=1)
    # return qml.expval(qml.PauliZ(wires=1))
    return qml.state()

# Result of noisy simulator
### print(circuit(0.2, 0.1, 0.3))
print(circuit())
