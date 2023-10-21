from quafu import QuantumCircuit

circ = QuantumCircuit(2)
circ.h(0)
circ.h(1)
circ.cnot(0, 1)
circ.measure()

circ.plot_circuit(save_path="temp.pdf")
