from quafu import QuantumCircuit

circ = QuantumCircuit(5)
circ.cnot(1, 0)
circ.x(2)
circ.h(3)
circ.rz(0, 2.5)
circ.cnot(4, 2)
circ.x(2)
circ.cnot(4, 1)
circ.cnot(2, 0)
circ.h(0)
circ.cnot(2, 0)

circ.plot_circuit(save_path="temp.pdf")
