import numpy as np

from quafu.simulators.simulator import simulate


class QuafuSimulator:

    def __init__(self) -> None:
        pass

    def run(self, simobj) -> np.ndarray:

        return simulate(
                simobj.circ,
                psi=simobj.objs[0],
                output="state_vector"
            ).get_statevector()
