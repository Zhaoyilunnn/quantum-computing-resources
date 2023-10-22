from qiskit.circuit import QuantumCircuit, Parameter

circuit = QuantumCircuit(2)
params = [Parameter("A"), Parameter("B"), Parameter("C")]
circuit.ry(params[0], 0)
circuit.crx(params[1], 0, 1)

print("Original circuit:")
print(circuit.draw())

circuit.assign_parameters({params[0]: params[2]}, inplace=True)

print("Assigned in-place:")
print(circuit.draw())
