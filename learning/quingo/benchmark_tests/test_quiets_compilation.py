from quingo import *
from quingo.backend.qisa import Qisa
import qututor.global_config as gc
import argparse

import logging

logger = logging.getLogger("compile")
logger.setLevel("DEBUG")
logger.disabled = False

parser = argparse.ArgumentParser()
parser.add_argument("qu", help="quingo source file name")
parser.add_argument("func", help="function name in the source file")
parser.add_argument("--isa", default="QUIET", help="ISA type, QCIS or QUIET")

args = parser.parse_args()

qu_file = gc.quingo_dir / args.qu

circ_name = args.func

if args.isa == "QUIET":
    isa_type = Qisa.QUIET
    suffix = ".qi"
elif args.isa == "QCIS":
    isa_type = Qisa.QCIS
    suffix = ".qcis"
else:
    raise NotImplementedError("Unsupported QISA type, please choose QCIS or QUIET")

task = Quingo_task(qu_file, circ_name, qisa=isa_type, debug_mode=True)
cfg = ExeConfig(ExeMode.SimShots, num_shots=10)

if circ_name == "GHZ_state":
    fn = compile(task, params=(3,), qasm_fn=f"{circ_name}{suffix}")
elif circ_name == "test_ctrl_adder":
    fn = compile(task, params=(1, 1, 2, 3, 3), qasm_fn=f"{circ_name}{suffix}")
else:
    fn = compile(task, params=(), qasm_fn=f"{circ_name}{suffix}")

print(fn)
