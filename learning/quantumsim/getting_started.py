import numpy as np
from quantumsim.circuit import Circuit

t1, t2 = 3000, 1500

c = Circuit(title="CNOT gate")
c.add_qubit("A", t1, t2)
c.add_qubit("B", t1, t2)

c.add_hadamard("B", time=0)
c.add_hadamard("B", time=40)
c.add_cphase("A", "B", time=20)
# c.plot()


from quantumsim.circuit import uniform_noisy_sampler

c.add_qubit("M")

sampler = uniform_noisy_sampler(readout_error=0.03, seed=42)

c.add_measurement("B", time=80, output_bit="M", sampler=sampler)
c.plot()


c.add_waiting_gates()
c.plot()


from quantumsim.sparsedm import SparseDM

sdm = SparseDM(c.get_qubit_names())

import quantumsim.sparsedm

print("GPU is used: ", quantumsim.sparsedm.using_gpu)

sdm.classical["A"] = 1
print("initial state:", sdm.classical)
