from qualesim.plugin import *
from qualesim.host import *
sim = Simulator(stderr_verbosity=Loglevel.INFO)

sim.with_frontend("./qft.qi", verbosity=Loglevel.INFO)
# sim.with_frontend("<path-to-qi-file>", verbosity=Loglevel.INFO)
# Loglevel is for output information for DEBUG/INFO/OFF
# If you only want the simulation output, please set it OFF

sim.with_backend("quantumsim", verbosity=Loglevel.INFO)
# sim.with_backend("tequila", verbosity=Loglevel.INFO)
# now we have DQCsim-Tequila and DQCsim-QuantumSim backend for Simulator

sim.simulate()
res = sim.run(measure_mod="state_vector", num_shots=10)
# Start the simulation with different exe mod,
# measure_mod="one_shot" and num_shots=int /
#             "state_vector"
# the output should be

sim.stop()
final_state = dict()
final_state = res["res"]
print(final_state)
