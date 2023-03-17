from qvm.util.circuit import \
        BaseReliabilityCalculator, \
        calc_cmr
from qvm.test.base import *
from util.plot import plot_bar


SMALL_BENCH_PATH="/root/projects/QASMBench/small/"

SMALL_BENCHES = [
    "adder_n4",
    "basis_change_n3",
    "basis_test_n4",
    "basis_trotter_n4",
    "bell_n4",
    "cat_state_n4",
    "deutsch_n2",
    "dnn_n2",
    "error_correctiond3_n5",
    "fredkin_n3",
    "grover_n2",
    "hs4_n4",
    "inverseqft_n4",
    "ipea_n2",
    "iswap_n2",
    "linearsolver_n3",
    "lpn_n5",
    "pea_n5",
    "qaoa_n3",
    "qec_en_n5",
    "qec_sm_n5",
    "qft_n4",
    "qrng_n4",
    "quantumwalks_n2",
    "shor_n5",
    "teleportation_n3",
    "toffoli_n3",
    "variational_n4",
    "vqe_uccsd_n4",
    "wstate_n3"
]


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
