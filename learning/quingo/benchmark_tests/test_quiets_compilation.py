from quingo import *
from quingo.backend.qisa import Qisa
import qututor.global_config as gc
import sys

qu_file = gc.quingo_dir / sys.argv[1]

circ_name = sys.argv[2]

task = Quingo_task(qu_file, circ_name, qisa=Qisa.QUIET)
cfg = ExeConfig(ExeMode.SimShots, num_shots=10)

if circ_name == "GHZ_state":
    fn = compile(task, params=(3,), qasm_fn=f"{circ_name}.qi")
elif circ_name == "test_ctrl_adder":
    fn = compile(task, params=(1, 1, 2, 3, 3), qasm_fn=f"{circ_name}.qi")
else:
    fn = compile(task, params=(), qasm_fn=f"{circ_name}.qi")

print(fn)