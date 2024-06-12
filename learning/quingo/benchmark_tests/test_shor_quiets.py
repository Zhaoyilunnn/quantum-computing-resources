import logging
from quingo import *
import qututor.runtime.result_format as rf
import qututor.global_config as gc
from qututor.tools import *
import termcolor as tc

logger = get_logger("add_N_back")
logger.setLevel(logging.DEBUG)
logger.disabled = True

mod_adder_module = gc.quingo_dir / "modular_adder.qu"


class Test_Addback:
    def add_back(params):
        task = Quingo_task(mod_adder_module, "test_mod_add_back_nc", qisa=Qisa.QUIET)
        a, b, N, w = params
        logger.debug("add_back: a: {}, b: {}, N: {}, w: {}".format(a, b, N, w))
        exp_res = a + b
        fn = compile(task, params=(a, b, N, w), qasm_fn=f"test_mod_add_back_nc_{a}_{b}_{N}_{w}.qi")
        print(fn)
        ## sim_result = call(task, params=(a, b, N, w))
        ## res = sim_result[1][0][::-1][1:]
        ## res = int("".join(list(map(str, res))), 2)

        ## logger.info(
        ##     "add_back "
        ##     + (
        ##         tc.colored("passed:", "green")
        ##         if res == exp_res
        ##         else tc.colored("failed:", "red")
        ##     )
        ##     + "a: {}, b: {}, N: {}, w: {}, acutal: {}, expect: {}".format(
        ##         a, b, N, w, res, exp_res
        ##     )
        ## )
        ## assert res == exp_res

    def mod_adder_nc(params):
        task = Quingo_task(mod_adder_module, "test_mod_adder_nc")
        a, b, N, w = params
        logger.debug("add_back_nc: a: {}, b: {}, N: {}, w: {}".format(a, b, N, w))
        exp_res = (a + b) % N
        sim_result = call(task, params=(a, b, N, w))
        # print("sim_result: ", sim_result)
        res = rf.get_first_non_zero_res(sim_result)
        logger.info(
            "mod_adder_nc "
            + (
                tc.colored("passed:", "green")
                if res == exp_res
                else tc.colored("failed:", "red")
            )
            + "a: {}, b: {}, N: {}, w: {}, acutal: {}, expect: {}".format(
                a, b, N, w, res, exp_res
            )
        )
        assert res == exp_res

    def test_add_backs(self):
        def single_test(params):
            trigger_task(Test_Addback.add_back, (params,), False)
            trigger_task(Test_Addback.mod_adder_nc, (params,), False)

        # a, b, N, width
        # N > a,b
        single_test((2, 2, 3, 2))
        single_test((1, 1, 3, 2))
        single_test((0, 1, 3, 2))
        single_test((0, 0, 5, 3))
        single_test((2, 3, 8, 3))
        single_test((7, 3, 8, 3))

    def mod_adder(params):
        task = Quingo_task(mod_adder_module, "test_mod_adder")
        c0, c1, a, b, N, w = params
        exp_res = (a + b) % N if (c0 == 1 and c1 == 1) else b
        logger.debug(
            "mod_adder: c0:{}, c1:{}, a: {}, b: {}, N: {}, w: {}, exp_res: {}".format(
                c0, c1, a, b, N, w, exp_res
            )
        )

        sim_result = call(task, params)
        # print("sim_result: ", sim_result)
        res = rf.get_first_non_zero_res(sim_result)
        # print("res: ", res)
        logger.info(
            "mod_adder_nc "
            + (
                tc.colored("passed:", "green")
                if res == exp_res
                else tc.colored("failed:", "red")
            )
            + "c0: {}, c1: {}, a: {}, b: {}, N: {}, w: {}, acutal: {}, expect: {}".format(
                c0, c1, a, b, N, w, res, exp_res
            )
        )
        assert res == exp_res

    def test_mod_adder(self):
        def single_test(params):
            trigger_task(Test_Addback.mod_adder, (params,), True)

        single_test((1, 1, 2, 3, 8, 3))
        single_test((1, 0, 2, 3, 8, 3))


if __name__ == "__main__":
    test = Test_Addback()
    test.test_add_backs()
    test.test_mod_adder()
    print("All tests passed")
