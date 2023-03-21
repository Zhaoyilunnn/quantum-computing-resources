from qvm.util.circuit import \
        BaseReliabilityCalculator, \
        calc_cmr
from qvm.constants import *
from qvm.test.base import *
from util.plot import plot_bar


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

    def test_calc_cmr_single_bench(self,
                                   bench,
                                   qasm):
        print("===== Testing Bench: {}, Qasm: {}".format(bench, qasm))
        circ = self.get_small_bench_circ(bench, qasm_path=qasm)
        print(calc_cmr(circ))

    def test_calc_cmr_multi_benches(self):
        cmrs = []
        labels = []
        for b in SMALL_BENCHES:
            try:
                b_file = SMALL_BENCH_PATH + "/" + b + "/" + b + ".qasm"
                circ = self.get_small_bench_circ("qasm", qasm_path=b_file)
            except Exception:
                continue
            cmrs.append(calc_cmr(circ))
            labels.append(b)
        plot_bar(cmrs, 
                 labels, 
                 figname="cmr_multi_benches.png",
                 figsize=(20,6)) 
