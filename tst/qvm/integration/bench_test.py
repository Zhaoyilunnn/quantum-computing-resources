from test.qvm import *

from qiskit.result import Counts
from qiskit.providers.fake_provider import *
from qutils.plot import plot_bar
from qvm.manager.backend_manager import *
from qvm.manager.process_manager import *
from qvm.util.backend import *
from qvm.util.circuit import (
    KlReliabilityCalculator,
    PstCalculator,
    merge_circuits_v2,
    QvmFidCalculator,
)
from qvm.util.quafu_helper import get_quafu_backend, to_qiskit_backend_v1

from constants import *


# qvm_version to ochestration method mappings
V2M = {
    "random": "random",
    "vanilla": "random",
    "small_first": "naive",
    "large_first": "naive_reverse",
    "brute_force": "brute_force",
}


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
    shots = QVM_SHOTS

    def setup_class(self):
        self._backend_manager = QvmFrpBackendManagerV2(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self.fid_calculator = KlReliabilityCalculator()
        self.qvm_proc = QvmProcessManagerV2(self._backend)
        self.frp_proc = FrpProcessManager(self._backend)

    def test_single_bench(self, bench):
        pass

    def run_exes_independent(self, exes: List[BaseExecutable], **kwargs):
        """Run each exe on its own backend
        This is used for run_qvm"""
        counts_list = []
        for exe in exes:
            res = exe.comp_unit.backend.run(exe.circ, **kwargs).result()
            cnts = Counts(res.get_counts())
            counts_list.append(cnts)
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
        return Counts(res.get_counts())

    def do_run_qvm_orch_method(
        self,
        processes: List[Process],
        is_run=True,
        independent=False,
        method: str = "random",
        **kwargs,
    ):
        self.qvm_proc.method = method
        start = time.time()
        exes = self.qvm_proc._select(processes)
        end = time.time()
        consumed = end - start
        print(f"QVM::selection::costs::\t{method}\t{consumed}")

        exes = self.reconstruct_exes(exes, processes)
        self.debug_exes(exes)
        if not is_run:
            # If we just want to test the online compilation time
            return None

        if independent:
            res = self.run_exes_independent(exes, **kwargs)
        else:
            res = self.run_exes_merge(exes, **kwargs)
        return res, consumed

    def do_run_qvm_orch(
        self,
        processes: List[Process],
        is_run=True,
        independent=False,
        method: str | List[str] = "random",
        **kwargs,
    ):
        if isinstance(method, str):
            res, _ = self.do_run_qvm_orch_method(
                processes,
                is_run=is_run,
                independent=independent,
                method=method,
                **kwargs,
            )
            return res

        # If we run multiple methods together, record the consumed times
        results = []
        for m in method:
            res, consumed = self.do_run_qvm_orch_method(
                processes, is_run=is_run, independent=independent, method=m, **kwargs
            )
            results.append((res, consumed))
        return results

    def run_qvm(
        self,
        circ_list: List[QuantumCircuit],
        is_run=True,
        independent=False,
        method: str | List[str] = "random",
        **kwargs,
    ):
        """Run using qvm process manager

        Here we temporarily use backend manager to extract compute units and compile on
        compute units, a better implementation should be in QvmProcessManager->run() method

        Args:
            circ_list: List of quantum circuits (without transpilation)
            is_run: Whether run simulation/experiment
            independent: Whether merge each exe and run on merged backend
            method: Method of ochestration (selection) in QVM process manager
            **kwargs: Other options
        """

        processes = [self._backend_manager.compile(circ) for circ in circ_list]
        return self.do_run_qvm_orch(
            processes, is_run=is_run, independent=independent, method=method, **kwargs
        )

    def run_frp_exes(self, trans_list, cu_list, independent=False, **kwargs):
        """merge and run on merged backend, or run independently
        Used for run_frp

        Args:
            trans_list: transpiled quantum circuits
            cu_list: allocated compute units from frp manager
            independent: whether run independently
        """
        if independent:
            res = []
            for c, cu in zip(trans_list, cu_list):
                cnts = cu.backend.run(c, **kwargs).result().get_counts()
                res.append(Counts(cnts))
            return res

        # Merge each comp_unit and run
        cu = self._backend_manager.merge_cus(cu_list)
        # exe = proc._merge_circuits(trans_list)
        exe = merge_circuits_v2(trans_list)

        res = cu.backend.run(exe, **kwargs).result()
        return Counts(res.get_counts())

    def run_frp(
        self, circ_list: List[QuantumCircuit], is_run=True, independent=False, **kwargs
    ):
        """Run using FRP process manager
        Here we temporarily use backend manager to extract compute units and compile on
        compute units, a better implementation should be in FrpProcessManager->run() method
        """
        if "is_low_cmr" in kwargs:
            is_low_cmr = kwargs["is_low_cmr"]
            self.frp_proc._partitioner.is_low_cmr = is_low_cmr

        start = time.time()
        part_list = [self.frp_proc.gen_partition(circ) for circ in circ_list]
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
            qvm_res = self.run_qvm(
                [circ0, circ1], independent=independent, shots=self.shots
            )
        except Exception as e:
            print(f"run qvm error: {e}")

        frp_res = None
        try:
            frp_res = self.run_frp(
                [circ0, circ1], independent=independent, shots=self.shots
            )
        except Exception as e:
            print(f"run frp error: {e}")

        # Calculate fidelity
        if independent:
            circ_list = [circ0, circ1]
        else:
            circ_list = circ

        fid_qvm = None
        if qvm_res:
            fid_qvm = self.fid_calculator.calc_fidelity(
                circ_list, qvm_res, shots=self.shots
            )
        fid_frp = None
        if frp_res:
            fid_frp = self.fid_calculator.calc_fidelity(
                circ_list, frp_res, shots=self.shots
            )
        print(f"Fid of qvm & frp\t{fid_qvm}\t{fid_frp}")


class TestBenchDiffBackendQvmFrpV2(TestBenchQvmFrpV2):
    fid_calculator = KlReliabilityCalculator()

    def setup_class(self):
        pass

    def init_back_manager(self, cu_size, vs="random"):
        """Initialize backend manager"""
        self._backend_manager = QvmFrpBackendManagerV2(self._backend)
        if vs == "vanilla":
            self._backend_manager.method = "vanilla"
        self.cu_size = int(cu_size)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()

    def init_proc_managers(self):
        """Initialize process managers"""
        self.qvm_proc = QvmProcessManagerV2(self._backend)
        self.frp_proc = FrpProcessManager(self._backend)

    def init_backend(self, backend):
        """Initialize backend"""
        self._backend = globals().get(backend)()

    def prepare_for_test(self, backend, cu_size, vs="random"):
        """Create backend manager, should be run at the begining of each single test,
        this is used to replace `setup_class`

        Must call in following order,
        1. init_backend
        2. init_back_manager
        3. init_proc_managers
        """
        self.init_backend(backend)
        self.init_back_manager(cu_size, vs=vs)
        self.init_proc_managers()

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
            qvm_res = self.run_qvm([circ0, circ1], is_run=False, shots=self.shots)
        except Exception as e:
            print(f"run qvm error: {e}")

        frp_res = None
        try:
            frp_res = self.run_frp([circ0, circ1], is_run=False, shots=self.shots)
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
        self.fid_calculator = PstCalculator()
        super().test_two_bench_frp(bench, nq, qasm, independent=True)

    def test_bench_diff_methods_diff_metric(
        self, qasm, backend, cu_size, qvm_version, metric
    ):
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
        print("\n------------------- Testing --------------\n")

        self.prepare_for_test(backend, cu_size, vs=qvm_version)

        if metric == "pst":
            self.fid_calculator = PstCalculator()

        # Prepare circuits
        shots = QVM_SHOTS
        qasms = qasm.split(",")
        circ_list = [self.get_qiskit_circ("qasm", qasm_path=q) for q in qasms]

        # Execution
        if qvm_version in V2M:
            res = self.run_qvm(
                circ_list, independent=True, method=V2M[qvm_version], shots=self.shots
            )
        elif qvm_version == "baseline":
            res = self.run_frp(circ_list, independent=True, shots=self.shots)
        else:
            raise ValueError(
                "Unsupported version, should be in one of "
                "[vanilla, random, small_first, large_first, brute_force, baseline]"
            )

        fid = self.fid_calculator.calc_fidelity(circ_list, res, shots=self.shots)
        print(f"Fid of {qvm_version}\t{fid}")

    def test_bench_multi_methods_multi_metrics(
        self, qasm, backend, cu_size, qvm_version
    ):
        """Test a bench group using different qvm ochestration methods"""

        print("\n------------------- Testing --------------\n")

        self.prepare_for_test(backend, cu_size, vs=qvm_version)

        # Prepare circuits
        shots = QVM_SHOTS
        qasms = qasm.split(",")
        circ_list = [self.get_qiskit_circ("qasm", qasm_path=q) for q in qasms]

        # Parse versions
        versions = qvm_version.split(",")
        methods = [V2M[v] for v in versions]

        # Execution
        results = self.run_qvm(
            circ_list, independent=True, method=methods, shots=self.shots
        )

        # Calc fidelity for each circuit, reuse ideal simulation results
        calculator = QvmFidCalculator()
        counts_ideal_list = [
            calculator.get_ideal_counts(circ, shots=self.shots) for circ in circ_list
        ]

        for idx_method, (counts, consumed) in enumerate(results):
            kls = []
            psts = []
            for idx_circ, counts_ideal in enumerate(counts_ideal_list):
                kl = calculator.calc_kl(
                    counts_ideal, counts[idx_circ], circ_list[idx_circ].num_qubits
                )
                kls.append(kl)
                pst = calculator.calc_pst(counts_ideal, counts[idx_circ])
                psts.append(pst)
            avg_kl = np.average(kls)
            avg_pst = np.average(psts)
            print(f"{versions[idx_method]}\t{consumed}\t{avg_kl}\t{avg_pst}")


class TestQuafuBackendQvmFrpV2(TestBenchDiffBackendQvmFrpV2):
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
    shots = 1000

    def init_backend(self, backend):
        self._backend_name = backend
        self._backend = get_quafu_backend(backend)

    def init_proc_managers(self):
        self.qvm_proc = QuafuQvmProcessManager(
            self._backend, name=self._backend_name, method="random"
        )
        self.frp_proc = QuafuFrpProcessManager(self._backend, name=self._backend_name)

    def prepare_for_test(self, backend, cu_size, vs="random"):
        self.init_backend(backend)
        self.init_back_manager(cu_size, vs=vs)
        self.init_proc_managers()

    def do_run_qvm_orch_method(
        self,
        processes: List[Process],
        is_run=True,
        independent=False,
        method: str = "random",
        **kwargs,
    ):
        self.qvm_proc.method = method
        qvm_res = self.qvm_proc.run(processes)
        qvm_counts = Counts(qvm_res.counts)
        return qvm_counts, 0

    def run_frp_exes(self, trans_list, cu_list, independent=False, **kwargs):
        """merge and run on merged backend
        Used for run_frp

        Args:
            trans_list: transpiled quantum circuits
            cu_list: allocated compute units from frp manager
            independent: whether run independently
        """
        frp_res = self.frp_proc.run_transpiled(trans_list)
        frp_counts = Counts(frp_res.counts)
        return frp_counts


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
