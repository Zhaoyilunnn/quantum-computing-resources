from quafu import QuantumCircuit

circ = QuantumCircuit(3)
circ.h(0)
circ.x(2)
circ.cnot(1, 2)
circ.measure()

circ.plot_circuit(save_path="temp.pdf")
