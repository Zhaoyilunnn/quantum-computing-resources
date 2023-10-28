from quafu import Task
from build_your_first_quantum_circuit import qc
from quafu import simulate
task = Task()

task.config(backend="ScQ-P18", shots=2000, compile=True)

res = task.send(qc, wait=True)

print(res.counts) #counts
print(res.probabilities) #probabilities
res.plot_probabilities()

res.transpiled_circuit.plot_circuit("Compiled Circuit")

simu_res = simulate(qc, output="probabilities")
simu_res.plot_probabilities()
