from qiskit.quantum_info import Operator

XX = Operator([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
input_dims = XX.input_dims()
