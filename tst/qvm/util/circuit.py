from test.qvm import *

from qutils.plot import plot_bar
from qvm.util.circuit import (
    BaseReliabilityCalculator,
    PSTCalculator,
    SvFidReliabilityCalculator,
    calc_cmr,
    merge_circuits_v2,
    reset_circuit_layout,
)

from constants import *


class TestBaseReliabilityCalculator(QvmBaseTest):
    _calculator = BaseReliabilityCalculator()

    def test_calc_fidelity(self):
        print("================ Test fidelity calculation =====================")
        circ = self.create_dummy_bell_state((0, 1))
        counts_noise = self._backend.run(circ).result().get_counts(circ)
        print(counts_noise)
        fidelity = self._calculator.calc_fidelity(circ, counts_noise)
        print("Test fidelity: {}".format(fidelity))


class TestPSTCalculator(TestBaseReliabilityCalculator):
    _calculator = PSTCalculator()


class TestSvFidReliabilityCalculator(QvmBaseTest):
    _calculator = SvFidReliabilityCalculator()

    def test_calc_fidelity(self):
        # TODO(zhaoyilun): Currently vqe runs too slow
        shots = 2**1
        is_trans = False

        b = "vqe_uccsd_n4"
        b_file = QASMBENCH_SMALL_DIR + "/" + b + "/" + b + ".qasm"
        circ = self.get_qiskit_circ("qasm", qasm_path=b_file)
        trans = circ
        if is_trans:
            trans = transpile(circ, self._backend)
        trans.save_state()
        res = self._backend.run(trans, shots=shots).result()
        sv_noise = res.get_statevector()
        fid = self._calculator.calc_fidelity(
            trans, sv_noise, is_trans=is_trans, shots=shots
        )
        print("TestSvFidReliabilityCalculator fid of {}: {}".format(b, fid))

    def test_calc_fidelity_bell_state(self):
        shots = 2**10
        circ = self.create_dummy_bell_state((0, 1), is_measure=False)
        circ.save_state()
        print(circ)
        self._backend.set_options(method="statevector")
        res = self._backend.run(circ, shots=shots).result()
        print(res.data())
        # sv_noise = res.data()["density_matrix"]
        sv_noise = res.get_statevector()
        fid = self._calculator.calc_fidelity(
            circ, sv_noise, is_trans=False, shots=shots
        )
        print("TestSvFidReliabilityCalculator fid of bell state: {}".format(fid))


class TestUtilCircuitMisc(QvmBaseTest):
    def test_calc_cmr(self):
        circ = self.create_dummy_bell_state((0, 1))
        cmr = calc_cmr(circ)
        assert cmr == 0.5

    def test_calc_cmr_single_bench(self, bench, qasm):
        print("===== Testing Bench: {}, Qasm: {}".format(bench, qasm))
        circ = self.get_qiskit_circ(bench, qasm_path=qasm)
        print(calc_cmr(circ))

    def test_calc_cmr_multi_benches(self):
        cmrs = []
        labels = []
        for b in SMALL_BENCHES:
            try:
                b_file = QASMBENCH_SMALL_DIR + "/" + b + "/" + b + ".qasm"
                circ = self.get_qiskit_circ("qasm", qasm_path=b_file)
            except Exception:
                continue
            cmrs.append(calc_cmr(circ))
            labels.append(b)
        plot_bar(cmrs, labels, figname="cmr_multi_benches.png", figsize=(20, 6))

    def test_calc_cmr_multi_benches_n4(self):
        cmrs = []
        labels = []
        for b in SMALL_BENCHES:
            if not b.endswith("_n4"):
                continue
            try:
                b_file = QASMBENCH_SMALL_DIR + "/" + b + "/" + b + ".qasm"
                circ = self.get_qiskit_circ("qasm", qasm_path=b_file)
            except Exception:
                continue
            cmrs.append(calc_cmr(circ))
            labels.append(b)
        plot_bar(cmrs, labels, figname="cmr_multi_benches_n4.png", figsize=(20, 6))

    def test_merge_circuits_v2(self):
        b = "vqe_uccsd_n4"
        b_file = QASMBENCH_SMALL_DIR + "/" + b + "/" + b + ".qasm"
        circ = self.get_qiskit_circ("qasm", qasm_path=b_file)
        print("clbits: {}".format(circ.clbits))
        print("clbits: {}".format(circ.num_clbits))
        print("qubits: {}".format(circ.qubits))
        print(circ)
        circ_merged = merge_circuits_v2([circ, circ], save_state=True)
        print(circ_merged)
        sim = Aer.get_backend("aer_simulator")
        res = sim.run(circ_merged, shots=2**20).result()
        print(res.get_counts())
        print(res.get_statevector())

        # Test correctness
        # 1. Create two bell state circuit and merge them
        bs = self.create_dummy_bell_state((0, 1), is_measure=False)
        bs_4_merged = merge_circuits_v2([bs, bs], save_state=True)
        bs_4_orig = self.create_dummy_bell_state(
            [(0, 1), (2, 3)], num_qubits=4, is_measure=False, save_state=True
        )
        sim = Aer.get_backend("aer_simulator")
        sim.set_options(method="statevector")
        res_merged = sim.run(bs_4_merged).result()
        res_orig = sim.run(bs_4_orig).result()
        sv_merged = res_merged.get_statevector()
        sv_orig = res_orig.get_statevector()
        assert sv_merged.equiv(sv_orig)
        print(sv_merged)
        print(sv_orig)

    def test_set_circuit_layout(self):
        circ = self.get_qiskit_circ("random", depth=4)
        trans = transpile(circ, FakeCairo())
        reset_circuit_layout(circ, [2, 3, 4, 7])
