from test.qvm import *

from qiskit.providers.fake_provider import *
from qutils.plot import plot_bar
from qvm.manager.backend_manager import *
from qvm.manager.process_manager import *
from qvm.util.backend import *
from qvm.util.circuit import KlReliabilityCalculator, PSTCalculator, merge_circuits_v2
from qvm.util.quafu_helper import get_quafu_backend, to_qiskit_backend_v1

from constants import *


class TestBenchQvmBfs(QvmBaseTest):
    """
    Integration of backend manager and process manager
    """

    def setup_class(self):
        self._backend_manager = BfsBackendManager(self._backend)
        self._backend_manager.init_helpers()
        # self._backend_manager.cu_size = 2
        self._backend_manager.init_cus()
        self._process_manager = ProcessManagerFactory.get_manager("qvm", self._backend)

    def test_single_bench(self, bench):
        # circ = self.create_dummy_bell_state((0,1))
        self._fid_calculator = KlReliabilityCalculator()
        circ = self.get_qiskit_circ(bench)
        cu = self._backend_manager._allocate(circ)
        fid_qvm = self.run_on_backend_and_get_fid(circ, cu.backend)
        fid_org = self.run_on_backend_and_get_fid(circ, self._backend)

        print("Fidelity Comparison\t{}\t{}".format(fid_qvm, fid_org))

    def test_two_bench_native(self, bench):
        """Testing qvm vs. baseline (native QISKIT)"""
        shots = QVM_SHOTS

        # circ0 = self.create_dummy_bell_state((0,1))
        # circ1 = self.create_dummy_bell_state((0,1))
        circ0 = self.get_qiskit_circ(bench)
        circ1 = self.get_qiskit_circ(bench)

        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        qvm_proc = QvmProcessManagerV1(self._backend)
        # qvm_res = qvm_proc.run([process0, process1]).result()
        exe0, exe1 = qvm_proc._select([process0, process1])
        cu = self._backend_manager.merge_cus([exe0.comp_unit, exe1.comp_unit])
        # print(cu.real_qubits)
        # print(exe0.circ)
        # print(exe1.circ)
        exe = qvm_proc._merge_circuits([exe0.circ, exe1.circ])
        qvm_res = cu.backend.run(exe, shots=shots).result()

        base_proc = BaselineProcessManager(self._backend)
        base_res = base_proc.run([circ1, circ1], shots=shots).result()

        circ = base_proc._merge_circuits([circ0, circ1])
        # print(qvm_res.get_counts())
        # print(base_res.get_counts())

        # Calculate fidelity
        self._fid_calculator = KlReliabilityCalculator()
        fid_qvm = self._fid_calculator.calc_fidelity(
            circ, qvm_res.get_counts(), shots=shots
        )
        fid_base = self._fid_calculator.calc_fidelity(
            circ, base_res.get_counts(), shots=shots
        )
        print("Fid of qvm & baseline\t{}\t{}".format(fid_qvm, fid_base))

    def run_frp(self, circ_list: List[QuantumCircuit], **kwargs):
        """Run using FRP process manager
        Here we temporarily use backend manager to extract compute units and compile on
        compute units, a better implementation should be in FrpProcessManager->run() method
        """
        proc = FrpProcessManager(self._backend)
        if "is_low_cmr" in kwargs:
            is_low_cmr = kwargs["is_low_cmr"]
            proc._partitioner.is_low_cmr = is_low_cmr

        part_list = [proc.gen_partition(circ) for circ in circ_list]
        cu_list = [self._backend_manager.extract_one_cu(part) for part in part_list]
        trans_list = [
            transpile(circ_list[i], cu_list[i].backend) for i in range(len(circ_list))
        ]
        cu = self._backend_manager.merge_cus(cu_list)
        exe = proc._merge_circuits(trans_list)
        res = cu.backend.run(exe, **kwargs).result()
        return res

    def run_qvm(self, circ_list: List[QuantumCircuit], **kwargs):
        """Run using qvm process manager

        Here we temporarily use backend manager to extract compute units and compile on
        compute units, a better implementation should be in QvmProcessManager->run() method
        """

        qvm_proc = QvmProcessManagerV1(self._backend)
        processes = [self._backend_manager.compile(circ) for circ in circ_list]
        exes = qvm_proc._select(processes)
        cus = [exe.comp_unit for exe in exes]
        cu = self._backend_manager.merge_cus(cus)
        circs = [exe.circ for exe in exes]
        circ = qvm_proc._merge_circuits(circs)
        res = cu.backend.run(circ, **kwargs).result()
        return res

    def test_two_bench_frp(self, bench):
        """Testing qvm vs. FRP (MICRO-2019)"""
        shots = QVM_SHOTS

        # circ0 = self.create_dummy_bell_state((0,1))
        # circ1 = self.create_dummy_bell_state((0,1))
        circ0 = self.get_qiskit_circ(bench)
        circ1 = self.get_qiskit_circ(bench)
        circ = merge_circuits([circ0, circ1])

        qvm_res = self.run_qvm([circ0, circ1], shots=shots)
        frp_res = self.run_frp([circ0, circ1], shots=shots)

        # Calculate fidelity
        self._fid_calculator = KlReliabilityCalculator()
        fid_qvm = self._fid_calculator.calc_fidelity(
            circ, qvm_res.get_counts(), shots=shots
        )
        fid_frp = self._fid_calculator.calc_fidelity(
            circ, frp_res.get_counts(), shots=shots
        )
        print(f"Fid of qvm & frp\t{fid_qvm}\t{fid_frp}")

    def test_two_n4_qasm_bench_wo_cmr(self):
        """Test two 4-qubit programs, compare qvm and frp"""
        shots = QVM_SHOTS
        fids_qvm = []
        fids_frp = []
        labels = []
        self._fid_calculator = KlReliabilityCalculator()
        for b in SMALL_BENCHES:
            if b.endswith("_n4"):
                try:
                    b_file = QASMBENCH_SMALL_DIR + "/" + b + "/" + b + ".qasm"
                    circ = self.get_qiskit_circ("qasm", qasm_path=b_file)
                    circ_merged = merge_circuits([circ, circ])
                except Exception as e:
                    print("Error: {}, when running benchmark: {}".format(e, b))
                    continue
                qvm_res = self.run_qvm([circ, circ], shots=shots)
                frp_res = self.run_frp([circ, circ], shots=shots)
                fid_qvm = self._fid_calculator.calc_fidelity(
                    circ_merged, qvm_res.get_counts(), shots=shots
                )
                fid_frp = self._fid_calculator.calc_fidelity(
                    circ_merged, frp_res.get_counts(), shots=shots
                )
                fids_qvm.append(fid_qvm)
                fids_frp.append(fid_frp)
                labels.append(b)
        print("Fid of QVM:\t{}".format("\t".join([str(f) for f in fids_qvm])))
        print("Fid of FRP:\t{}".format("\t".join([str(f) for f in fids_frp])))
        print("Benches: {}".format("\t".join(labels)))

        plot_bar(
            [fids_qvm, fids_frp],
            labels,
            data_labels=["QVM", "FRP"],
            figname="fid_qvm_frp_qasm_n4_two.png",
            figsize=(20, 6),
        )

    def test_two_n4_qasm_bench_with_cmr(self):
        """Test two 4-qubit programs, compare qvm and frp
        Here we introduce CMR to graph partition in FRP
        """
        shots = QVM_SHOTS
        fids_qvm = []
        fids_frp = []
        labels = []
        self._fid_calculator = KlReliabilityCalculator()
        for b in SMALL_BENCHES:
            if b.endswith("_n4"):
                try:
                    b_file = QASMBENCH_SMALL_DIR + "/" + b + "/" + b + ".qasm"
                    circ = self.get_qiskit_circ("qasm", qasm_path=b_file)
                    # circ_merged = merge_circuits_v2([circ, circ])
                    circ_merged = merge_circuits([circ, circ])
                    cmr = calc_cmr(circ)
                    is_low_cmr = True if cmr < 10 else False
                except Exception:
                    continue
                print(
                    "Bench Name: {}, is_low_cmr: {}, cmr: {}".format(b, is_low_cmr, cmr)
                )
                qvm_res = self.run_qvm([circ, circ], shots=shots)
                frp_res = self.run_frp([circ, circ], shots=shots, is_low_cmr=is_low_cmr)
                fid_qvm = self._fid_calculator.calc_fidelity(
                    circ_merged, qvm_res.get_counts(), shots=shots
                )
                fid_frp = self._fid_calculator.calc_fidelity(
                    circ_merged, frp_res.get_counts(), shots=shots
                )
                fids_qvm.append(fid_qvm)
                fids_frp.append(fid_frp)
                labels.append(b)
        print("Fid of QVM:\t{}".format("\t".join([str(f) for f in fids_qvm])))
        print("Fid of FRP:\t{}".format("\t".join([str(f) for f in fids_frp])))
        print("Benches: {}".format("\t".join(labels)))

        plot_bar(
            [fids_qvm, fids_frp],
            labels,
            data_labels=["QVM", "FRP"],
            figname="fid_qvm_frp_qasm_n4_two.png",
            figsize=(20, 6),
        )


class TestBenchQvmFrpV1(TestBenchQvmBfs):
    def setup_class(self):
        self._backend_manager = QvmFrpBackendManagerV1(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self._process_manager = ProcessManagerFactory.get_manager("qvm", self._backend)


class TestBenchQvmFrpV2(TestBenchQvmBfs):
    def setup_class(self):
        self._backend_manager = QvmFrpBackendManagerV2(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self._process_manager = ProcessManagerFactory.get_manager("qvm", self._backend)
        self.fid_calculator = KlReliabilityCalculator()

    def test_single_bench(self, bench):
        pass

    def run_exes_independent(self, exes: List[BaseExecutable], **kwargs):
        """Run each exe on its own backend
        This is used for run_qvm"""
        counts_list = [
            exe.comp_unit.backend.run(exe.circ, **kwargs).result().get_counts()
            for exe in exes
        ]
        return counts_list

    def run_exes_merge(self, exes: List[BaseExecutable], **kwargs):
        """Merge each exe and run on merged cu
        Used for run_qvm"""
        cus = [exe.comp_unit for exe in exes]
        cu = self._backend_manager.merge_cus(cus)
        circs = [exe.circ for exe in exes]
        # circ = qvm_proc._merge_circuits(circs)
        circ = merge_circuits_v2(circs)
        res = cu.backend.run(circ, **kwargs).result()
        return res.get_counts()

    def run_qvm(
        self,
        circ_list: List[QuantumCircuit],
        is_run=True,
        independent=False,
        method="random",
        **kwargs,
    ):
        """Run using qvm process manager

        Here we temporarily use backend manager to extract compute units and compile on
        compute units, a better implementation should be in QvmProcessManager->run() method
        """

        qvm_proc = QvmProcessManagerV2(self._backend)
        qvm_proc.method = method
        processes = [self._backend_manager.compile(circ) for circ in circ_list]
        start = time.time()
        exes = qvm_proc._select(processes)
        print(f"QVM::selection::costs::\t{time.time() - start}")

        if not is_run:
            # If we just want to test the online compilation time
            return None

        if independent:
            return self.run_exes_independent(exes, **kwargs)
        return self.run_exes_merge(exes, **kwargs)

    def run_frp_exes(self, trans_list, cu_list, independent=False, **kwargs):
        """merge and run on merged backend, or run independently
        Used for run_frp

        Args:
            trans_list: transpiled quantum circuits
            cu_list: allocated compute units from frp manager
            independent: whether run independently
        """
        if independent:
            return [
                cu.backend.run(c, **kwargs).result().get_counts()
                for c, cu in zip(trans_list, cu_list)
            ]

        # Merge each comp_unit and run
        cu = self._backend_manager.merge_cus(cu_list)
        # exe = proc._merge_circuits(trans_list)
        exe = merge_circuits_v2(trans_list)

        res = cu.backend.run(exe, **kwargs).result()
        return res.get_counts()

    def run_frp(
        self, circ_list: List[QuantumCircuit], is_run=True, independent=False, **kwargs
    ):
        """Run using FRP process manager
        Here we temporarily use backend manager to extract compute units and compile on
        compute units, a better implementation should be in FrpProcessManager->run() method
        """
        proc = FrpProcessManager(self._backend)
        if "is_low_cmr" in kwargs:
            is_low_cmr = kwargs["is_low_cmr"]
            proc._partitioner.is_low_cmr = is_low_cmr

        start = time.time()
        part_list = [proc.gen_partition(circ) for circ in circ_list]
        cu_list = [self._backend_manager.extract_one_cu(part) for part in part_list]
        trans_list = [
            transpile(circ_list[i], cu_list[i].backend) for i in range(len(circ_list))
        ]
        print(f"FRP::online_compilation::costs::\t{time.time() - start}")

        if not is_run:
            # We just want to test the online compilation time
            return None

        return self.run_frp_exes(trans_list, cu_list, independent=independent, **kwargs)

    def test_two_bench_frp(self, bench, nq, qasm, independent=False):
        """Testing qvm vs. FRP (MICRO-2019)

        Args:
            bench (str): `qasm` or `random`. If `qasm`, construct circuit
                from qasm file, otherwise create random circuit
            nq (str): int(nq) is the number of qubits, this is only useful when
                getting random circuit
            qasm (str): QASM files, should be <qasm-0>;<qasm-1> format
        """
        shots = QVM_SHOTS
        nq = int(nq)
        if qasm:
            items = qasm.split(",")
            assert len(items) == 2 and bench == "qasm"
            qasm0 = items[0]
            qasm1 = items[1]
            circ0 = self.get_qiskit_circ(bench, qasm_path=qasm0)
            circ1 = self.get_qiskit_circ(bench, qasm_path=qasm1)
        else:
            circ0 = self.get_qiskit_circ(bench, num_qubits=nq)
            circ1 = self.get_qiskit_circ(bench, num_qubits=nq)

        circ = merge_circuits_v2([circ0, circ1])

        qvm_res = None
        try:
            qvm_res = self.run_qvm([circ0, circ1], independent=independent, shots=shots)
        except Exception as e:
            print(f"run qvm error: {e}")

        frp_res = None
        try:
            frp_res = self.run_frp([circ0, circ1], independent=independent, shots=shots)
        except Exception as e:
            print(f"run frp error: {e}")

        # Calculate fidelity
        if independent:
            circ_list = [circ0, circ1]
        else:
            circ_list = circ

        fid_qvm = None
        if qvm_res:
            fid_qvm = self.fid_calculator.calc_fidelity(circ_list, qvm_res, shots=shots)
        fid_frp = None
        if frp_res:
            fid_frp = self.fid_calculator.calc_fidelity(circ_list, frp_res, shots=shots)
        print(f"Fid of qvm & frp\t{fid_qvm}\t{fid_frp}")


class TestBenchDiffBackendQvmFrpV2(TestBenchQvmFrpV2):
    fid_calculator = KlReliabilityCalculator()

    def setup_class(self):
        pass

    def prepare_for_test(self, backend, cu_size, vs="random"):
        self._backend = globals().get(backend)()
        self._backend_manager = QvmFrpBackendManagerV2(self._backend)
        if vs == "vanilla":
            self._backend_manager.method = "vanilla"
        self.cu_size = int(cu_size)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()

        # FIXME(): self._process_manager may have no use
        self._process_manager = ProcessManagerFactory.get_manager("qvm", self._backend)

    def test_two_bench_runtime_overhead(self, bench, nq, qasm, backend, cu_size):
        self.prepare_for_test(backend, cu_size)
        shots = QVM_SHOTS
        nq = int(nq)
        if qasm:
            items = qasm.split(",")
            assert len(items) == 2 and bench == "qasm"
            qasm0 = items[0]
            qasm1 = items[1]
            circ0 = self.get_qiskit_circ(bench, qasm_path=qasm0)
            circ1 = self.get_qiskit_circ(bench, qasm_path=qasm1)
        else:
            circ0 = self.get_qiskit_circ(bench, num_qubits=nq)
            circ1 = self.get_qiskit_circ(bench, num_qubits=nq)

        circ = merge_circuits_v2([circ0, circ1])

        qvm_res = None
        try:
            qvm_res = self.run_qvm([circ0, circ1], is_run=False, shots=shots)
        except Exception as e:
            print(f"run qvm error: {e}")

        frp_res = None
        try:
            frp_res = self.run_frp([circ0, circ1], is_run=False, shots=shots)
        except Exception as e:
            print(f"run frp error: {e}")

    def test_two_bench_frp(self, bench, nq, qasm, backend, cu_size):
        self.prepare_for_test(backend, cu_size)
        super().test_two_bench_frp(bench, nq, qasm)

    def test_kl_independent_two_bench_frp(self, bench, nq, qasm, backend, cu_size):
        """Execute qvm/frp exes on their own backend"""
        self.prepare_for_test(backend, cu_size)
        super().test_two_bench_frp(bench, nq, qasm, independent=True)

    def test_pst_independent_two_bench_frp(self, bench, nq, qasm, backend, cu_size):
        """Execute qvm/frp exes on their own backend

        Use PST as reliability metric"""
        self.prepare_for_test(backend, cu_size)
        self.fid_calculator = PSTCalculator()
        super().test_two_bench_frp(bench, nq, qasm, independent=True)

    def test_bench_diff_methods_diff_metric(self, qasm, backend, cu_size, qvm_version, metric):
        """Given a list of qasm benchmarks, run on QvmFrpBackendManagerV2
        and QvmProcessManagerV2.

        Support setting qvm versions or baseline
        - vanilla: randomly select exe
        - random: sort exes, greedily select without sorting processes
        - small_first: sort exes, sort processes (small circ first) and greedily select
        - large_first: sort exes, sort processes (large circ first) and greedily select
        - brute_force: sort exes, sort processes, and find optimal solution minimizing sum of idxes
        - baseline: online compilation

        Support different metric:
        - kl: KL divergence
        - pst: Percentage of successful trials
        """
        self.prepare_for_test(backend, cu_size, vs=qvm_version)

        if metric == "pst":
            self.fid_calculator = PSTCalculator()

        shots = QVM_SHOTS
        qasms = qasm.split(",")
        circ_list = [self.get_qiskit_circ("qasm", qasm_path=q) for q in qasms]
        if qvm_version in ["random", "vanilla"]:
            res = self.run_qvm(
                circ_list, independent=True, method="random", shots=shots
            )
        elif qvm_version == "small_first":
            res = self.run_qvm(circ_list, independent=True, method="naive", shots=shots)
        elif qvm_version == "large_first":
            res = self.run_qvm(
                circ_list, independent=True, method="naive_reverse", shots=shots
            )
        elif qvm_version == "brute_force":
            res = self.run_qvm(
                circ_list, independent=True, method="brute_force", shots=shots
            )
        elif qvm_version == "baseline":
            res = self.run_frp(circ_list, independent=True, shots=shots)
        else:
            raise ValueError(
                "Unsupported version, should be in one of "\
                "[vanilla, random, small_first, large_first, brute_force, baseline]"
            )

        fid = self.fid_calculator.calc_fidelity(circ_list, res, shots=shots)
        print(f"Fid of {qvm_version}\t{fid}")


class TestQuafuBackendQvmFrpV2(TestBenchDiffBackendQvmFrpV2):
    def setup_class(self):
        pass

    def prepare_for_test(self, backend, cu_size):
        from quafu.users.userapi import User

        user = User()
        user.get_backends_info()
        BACKENDS = user.get_available_backends()
        try:
            quafu_backend = BACKENDS[backend]
        except KeyError as ex:
            print("Backend not found in quafu backend")
            exit(1)
        self._backend = to_qiskit_backend_v1(quafu_backend.get_chip_info())
        self._backend_manager = QvmFrpBackendManagerV2(self._backend)
        self.cu_size = int(cu_size)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self._process_manager = ProcessManagerFactory.get_manager("qvm", self._backend)


class TestQuafuBackendRealMachineQvmFrpV2(TestBenchDiffBackendQvmFrpV2):
    def setup_class(self):
        pass

    def prepare_for_test(self, backend, cu_size):
        quafu_backend_str = backend
        quafu_backend = get_quafu_backend(quafu_backend_str)
        self._backend_manager = QvmFrpBackendManagerV2(quafu_backend)
        self._backend_manager.cu_size = int(cu_size)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self.qvm_proc_manager = QuafuQvmProcessManager(
            quafu_backend, name=quafu_backend_str
        )
        self.frp_proc_manager = QuafuFrpProcessManager(
            quafu_backend, name=quafu_backend_str
        )

    def test_two_bench_frp(self, bench, nq, qasm, backend, cu_size):
        self.prepare_for_test(backend, cu_size)

        shots = QVM_SHOTS
        nq = int(nq)
        if qasm:
            items = qasm.split(",")
            assert len(items) == 2 and bench == "qasm"
            qasm0 = items[0]
            qasm1 = items[1]
            circ0 = self.get_qiskit_circ(bench, qasm_path=qasm0)
            circ1 = self.get_qiskit_circ(bench, qasm_path=qasm1)
        else:
            circ0 = self.get_qiskit_circ(bench, num_qubits=nq)
            circ1 = self.get_qiskit_circ(bench, num_qubits=nq)

        # FIXME() test purpose
        # circ0 = self.create_dummy_bell_state((0,1))
        # circ1 = self.create_dummy_bell_state((0,1))
        # FIXME() test purpose

        circ = merge_circuits_v2([circ0, circ1])

        # run qvm
        processes = [
            self._backend_manager.compile(circ0),
            self._backend_manager.compile(circ1),
        ]
        qvm_res = self.qvm_proc_manager.run(processes)
        qvm_counts = qvm_res.counts

        # run online compilation
        frp_res = self.frp_proc_manager.run([circ0, circ1])
        frp_counts = frp_res.counts

        # Calculate fidelity
        self._fid_calculator = KlReliabilityCalculator()

        fid_qvm = self._fid_calculator.calc_fidelity(circ, qvm_counts, shots=shots)
        fid_frp = self._fid_calculator.calc_fidelity(circ, frp_counts, shots=shots)
        print(f"Fid of qvm & frp\t{fid_qvm}\t{fid_frp}")


# FIXME(): directly using QvmProcessManagerV2.run cannot calculate fidelity
class TestBenchDiffBackendUseNativeQvmFrpV2(TestBenchDiffBackendQvmFrpV2):
    """Use native QvmProcessManagerV2.run method to execute multiple circuits"""

    def run_qvm(self, circ_list: List[QuantumCircuit], is_run=True, **kwargs):
        """Run using qvm process manager

        Here we temporarily use backend manager to extract compute units and compile on
        compute units, a better implementation should be in QvmProcessManager->run() method
        """

        qvm_proc = QvmProcessManagerV2(self._backend)
        processes = [self._backend_manager.compile(circ) for circ in circ_list]
        # start = time.time()
        # exes = qvm_proc._select(processes)
        # print(f"QVM::selection::costs::\t{time.time() - start}")
        # cus = [exe.comp_unit for exe in exes]
        # cu = self._backend_manager.merge_cus(cus)
        # circs = [exe.circ for exe in exes]
        # # circ = qvm_proc._merge_circuits(circs)
        # circ = merge_circuits_v2(circs)
        # if is_run:
        #     res = cu.backend.run(circ, **kwargs).result()
        #     return res
        if is_run:
            res = qvm_proc.run(processes)
            return res
