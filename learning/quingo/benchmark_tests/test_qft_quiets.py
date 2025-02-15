import logging
from quingo import *
from pathlib import Path
import qututor.global_config as gc
import argparse


qu_file = gc.quingo_dir / "test_qft.qu"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--isa", default="QUIET", help="QUIET or QCIS")
    return parser.parse_args()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_bin(x, n):
    if not is_number(x):
        raise ValueError("get_bin: parameter is not a number.")

    return "{0:{fill}{width}b}".format((int(x) + 2**n) % 2**n, fill="0", width=n)


def to_int(x):
    a = 0
    for i in range(len(x)):
        if x[i] == 1:
            a += 2**i
    return a


def get_first_non_zero_res(qcis_result):
    if qcis_result is None:
        print("No measure results found")
    qubit_list, msmt_count = qcis_result
    return to_int(msmt_count[0])


cfg = ExeConfig(ExeMode.SimShots, 1)


class Test_QFT_BB:
    def test_qft_bb(self, isa):
        if isa == "QUIET":
            isa_type = Qisa.QUIET
            suffix = ".qi"
        elif isa == "QCIS":
            isa_type = Qisa.QCIS
            suffix = ".qcis"
        else:
            raise NotImplementedError("Unsupported ISA type")
        num_qubits = 2
        for i in range(1 << num_qubits):
            str_bin = get_bin(i, num_qubits)
            blist = [int(b) for b in str_bin]
            print("input :", str_bin)
            blist.reverse()
            task = Quingo_task(qu_file, "test_qft_bb", qisa=isa_type)
            fn = compile(task, params=(blist,), qasm_fn=f"test_qft_bb_{blist}{suffix}")
            print(fn)


if __name__ == "__main__":
    args = get_args()
    Test_QFT_BB().test_qft_bb(args.isa)
