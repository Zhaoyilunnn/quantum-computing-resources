from quingo import *
from pathlib import Path
import qututor.runtime.result_format as rf
import qututor.global_config as gc


kernel_file = gc.quingo_dir / "utils.qu"


class Test_Utils:
    def test_individual(self):
        circ_name = "get_bin"
        task = Quingo_task(kernel_file, circ_name, qisa=Qisa.QUIET)
        cfg = ExeConfig(ExeMode.SimShots, 1)
        for i in range(7):
            fn = compile(task, params=(i, 4), qasm_fn=f"{circ_name}_{i}.qi")
            print(fn)
            ## res = call(
            ##     task,
            ##     (
            ##         i,
            ##         4,
            ##     ),
            ##     BackendType.QUANTUM_SIM,
            ##     cfg,
            ## )
            ## assert i == rf.get_first_non_zero_res(res)


if __name__ == "__main__":
    Test_Utils().test_individual()

    print("All tests passed")
