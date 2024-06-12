import logging
from quingo import *
from pathlib import Path
import qututor.runtime.result_format as rf
from qututor.adder.classical_behavior import adder_behavior, subtracter_behavior
from qututor.tools import *
import qututor.global_config as gc

import termcolor as tc

logger = get_logger("compile")
logger.setLevel(logging.DEBUG)
logger.disabled = False

kernel_file = gc.quingo_dir / "draper_test.qu"


class Test_Draper_adder:
    def add_or_sub(i, j, num_qubits, subtract=False):
        task = Quingo_task(kernel_file, "test_sc_adder", qisa=Qisa.QUIET, debug_mode=True)
        i_bits = int2bit_list(i, num_qubits)
        j_bits = int2bit_list(j, num_qubits)
        logger.debug("a: {} '{}'   b: {} '{}'".format(i, bin(i), j, bin(j)))

        fn = compile(task, params=(i_bits, j_bits, subtract), qasm_fn=f"draper_test_{i_bits}_{j_bits}_{subtract}.qi")
        print(fn)
        # sim_result = call(task, (i_bits, j_bits, subtract))
        
        # logger.debug(sim_result)
        # res = rf.get_first_non_zero_res(sim_result)
        # logger.debug("res: {}".format(res))
        # logger.debug(" {}  {}  {}".format(i, j, res))

        # if subtract:
        #     assert res == subtracter_behavior(i, j, num_qubits)
        # else:
        #     assert res == adder_behavior(i, j, num_qubits)

        # logger.info(
        #     tc.colored("passed:", "green")
        #     + " {} {} {} = {}".format(i, "-" if subtract else "+", j, res)
        # )

    def test_adder(self, subtract=False):
        num_qubits = 2
        for i in range(1 << num_qubits):
            for j in range(1 << num_qubits):
                trigger_task(Test_Draper_adder.add_or_sub, (i, j, num_qubits), False)

    def test_subtracter(self):
        num_qubits = 2
        for i in range(1 << num_qubits):
            for j in range(1 << num_qubits):
                trigger_task(
                    Test_Draper_adder.add_or_sub, (i, j, num_qubits, True), False
                )


if __name__ == "__main__":
    Test_Draper_adder().test_adder()
    Test_Draper_adder().test_subtracter()
