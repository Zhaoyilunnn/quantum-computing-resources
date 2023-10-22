from quafu import QuantumCircuit, Task

q = QuantumCircuit(5)

for i in range(5):
    if i % 2 == 0:
        q.h(i)

q.draw_circuit()
measures = list(range(5))
q.measure(measures)

task = Task()
task.config(backend="ScQ-P136")

test_Ising = [["X", [i]] for i in range(5)]
test_Ising.extend([["ZZ", [i, i + 1]] for i in range(4)])
res, obsexp = task.submit(q, test_Ising)
