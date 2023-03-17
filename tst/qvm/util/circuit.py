from qvm.util.circuit import \
        BaseReliabilityCalculator, \
        calc_cmr
from qvm.test.base import *


class TestUtilCircuit(BaseTest):

    _calculator = BaseReliabilityCalculator()

    def test_calc_fidelity(self):

        print("================ Test fidelity calculation =====================")
        circ = self.create_dummy_bell_state((0,1))
        counts_noise = self._backend.run(circ).result().get_counts(circ)
        print(counts_noise) 
        fidelity = self._calculator.calc_fidelity(circ, counts_noise)
        print("Test fidelity: {}".format(fidelity))

    def test_calc_cmr(self):

        circ = self.create_dummy_bell_state((0,1))
        cmr = calc_cmr(circ)
        assert cmr == 0.5
