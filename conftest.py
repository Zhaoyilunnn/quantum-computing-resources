
def pytest_addoption(parser):
    parser.addoption("--verify", action="store", default="pulse")
    parser.addoption("--bench", action="store", default="random")
    parser.addoption("--alpha", action="store", default=0)
    parser.addoption("--beta", action="store", default=0)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.verify
    if 'verify' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("verify", [option_value])

    option_value = metafunc.config.option.bench
    if 'bench' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("bench", [option_value])

    option_value = metafunc.config.option.alpha
    if 'alpha' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("alpha", [option_value])

    option_value = metafunc.config.option.beta
    if 'beta' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("beta", [option_value])
