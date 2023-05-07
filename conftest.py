import logging


## Logging configuration
#logging.basicConfig(filename='qvm_test.log', encoding='utf-8', level=logging.DEBUG,
#                format='%(asctime)s %(message)s')
#logger = logging.getLogger("qvm_pytest_logger")


def pytest_addoption(parser):
    parser.addoption("--verify", action="store", default="pulse")
    parser.addoption("--bench", action="store", default="random")
    parser.addoption("--qasm", action="store", default="")
    parser.addoption("--alpha", action="store", default=0)
    parser.addoption("--beta", action="store", default=0)
    parser.addoption("--nq", action="store", default=10)
    parser.addoption("--np", action="store", default=0)
    parser.addoption("--nl", action="store", default=0)
    parser.addoption("--mode", action="store", default="QDAO")
    parser.addoption("--parallel", action="store", default=1)
    parser.addoption("--diff", action="store", default=1)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.verify
    if 'verify' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("verify", [option_value])

    option_value = metafunc.config.option.bench
    if 'bench' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("bench", [option_value])

    option_value = metafunc.config.option.qasm
    if 'qasm' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("qasm", [option_value])

    # Alpha paramter in FRP
    option_value = metafunc.config.option.alpha
    if 'alpha' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("alpha", [option_value])

    # Beta paramter in FRP
    option_value = metafunc.config.option.beta
    if 'beta' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("beta", [option_value])

    option_value = metafunc.config.option.nq
    if 'nq' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("nq", [option_value])

    option_value = metafunc.config.option.np
    if 'np' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("np", [option_value])

    option_value = metafunc.config.option.nl
    if 'nl' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("nl", [option_value])

    option_value = metafunc.config.option.mode
    if 'mode' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("mode", [option_value])

    option_value = metafunc.config.option.parallel
    if 'parallel' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("parallel", [option_value])

    option_value = metafunc.config.option.diff
    if 'diff' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("diff", [option_value])
