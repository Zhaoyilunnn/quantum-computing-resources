from qualesim.plugin import *
from qualesim.host import *

sim = Simulator(stderr_verbosity=Loglevel.INFO)

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path-to-qcis-or-quiets-source-file>")
    sys.exit(1)

src_file_path = sys.argv[1]

# sim.with_frontend("/tmp/quingo-isiab0q2/main_bell_bell_state.qcis", verbosity=Loglevel.INFO)
# sim.with_frontend("/tmp/quingo-g1rkvum9/main_ghz_GHZ_state.qi", verbosity=Loglevel.DEBUG)
# sim.with_frontend("/home/zhaoyilun/workspace/github/quantum-computing-resources/learning/quingo/benchmark_tests/GHZ_state.qcis", verbosity=Loglevel.DEBUG)
sim.with_frontend(src_file_path, verbosity=Loglevel.DEBUG)
# sim.with_frontend("<path-to-qi-file>", verbosity=Loglevel.INFO)
# Loglevel is for output information for DEBUG/INFO/OFF
# If you only want the simulation output, please set it OFF

sim.with_backend("quantumsim", verbosity=Loglevel.INFO)
# sim.with_backend("tequila", verbosity=Loglevel.INFO)
# now we have DQCsim-Tequila and DQCsim-QuantumSim backend for Simulator

sim.simulate()
res = sim.run(measure_mod="state_vector", num_shots=10)
print(f"res\n{res}")
# Start the simulation with different exe mod,
# measure_mod="one_shot" and num_shots=int /
#             "state_vector"
# the output should be

sim.stop()
final_state = dict()
final_state = res["res"]
print(final_state)
