from numpy import average
from constants import QVM_SHOTS
from qvm.util.circuit import (
    KlReliabilityCalculator,
    KlReliabilityCalculatorForOracle,
    PSTCalculator,
)
from test.qvm import *

from qiskit import IBMQ
from qvm.util.quafu_helper import get_quafu_backend


class TestQvm(QvmBaseTest):
    def setup_class(self):
        self._backend_manager = BfsBackendManager(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()

    def test_qvm_run_v1(self):
        proc_manager = QvmProcessManagerV1(self._backend)
        circ0 = self.create_dummy_bell_state((0, 1))
        circ1 = self.create_dummy_bell_state((0, 1))

        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        proc_manager.run([process0, process1])

    def test_baseline_run(self):
        proc_manager = BaselineProcessManager(self._backend)

        circ0 = self.create_dummy_bell_state((0, 1))
        circ1 = self.create_dummy_bell_state((0, 1))

        proc_manager.run([circ0, circ1])


class TestQvmV2(QvmBaseTest):
    def setup_class(self):
        self._backend_manager = QvmFrpBackendManagerV2(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()

    def test_qvm_run_v2(self):
        proc_manager = QvmProcessManagerV2(self._backend)
        circ0 = self.create_dummy_bell_state((0, 1))
        circ0.draw(output="mpl")
        plt.tight_layout()
        plt.savefig("circ0.svg")
        plt.close()
        circ1 = self.get_qiskit_circ("random", num_qubits=6)
        circ1.draw(output="mpl")
        plt.tight_layout()
        plt.savefig("circ1.svg")
        plt.close()

        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        assert len(process0) > len(process1)

        data0 = copy.deepcopy(process0._data)
        data0.sort(key=lambda exe: exe.cost)
        data1 = copy.deepcopy(process1._data)
        data1.sort(key=lambda exe: exe.cost)

        # assert data0 == process0._data
        for i, exe in enumerate(data0):
            assert exe == data0[i]
        for i, exe in enumerate(data1):
            assert exe == data1[i]

        proc_manager.run([process0, process1])


class TestRealMachine(QvmBaseTest):
    def setup_class(self):
        provider = IBMQ.load_account()
        backend = provider.get_backend("ibmq_belem")
        self._backend_manager = QvmFrpBackendManagerV2(backend)
        self._backend_manager.cu_size = 2
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self.proc_manager = QvmProcessManagerV2(backend)

    def test_qvm_run_v2(self):
        circ0 = self.create_dummy_bell_state((0, 1))
        circ0.draw(output="mpl")
        plt.tight_layout()
        plt.savefig("circ0.svg")
        plt.close()
        circ1 = self.create_dummy_bell_state((0, 1))
        circ1.draw(output="mpl")
        plt.tight_layout()
        plt.savefig("circ1.svg")
        plt.close()

        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        # data0 = copy.deepcopy(process0._data)
        # data0.sort(key=lambda exe: exe.cost)
        # data1 = copy.deepcopy(process1._data)
        # data1.sort(key=lambda exe: exe.cost)

        ## assert data0 == process0._data
        # for i, exe in enumerate(data0):
        #    assert exe == data0[i]
        # for i, exe in enumerate(data1):
        #    assert exe == data1[i]

        self.proc_manager.run([process0, process1])


class TestQuafu(QvmBaseTest):
    def test_run_using_quafu_model(self):
        # P10
        quafu_backend_10 = get_quafu_backend("ScQ-P10")
        self._backend_manager = QvmFrpBackendManagerV2(quafu_backend_10)
        self._backend_manager.cu_size = 2
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self.proc_manager = QvmProcessManagerV2(quafu_backend_10)

        # P18
        quafu_backend_18 = get_quafu_backend("ScQ-P18")
        self._backend_manager = QvmFrpBackendManagerV2(quafu_backend_18)
        self._backend_manager.cu_size = 2
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self.proc_manager = QvmProcessManagerV2(quafu_backend_18)

    def test_run_on_quafu_machine(self):
        # P10
        quafu_backend_str = "ScQ-P18"
        quafu_backend = get_quafu_backend(quafu_backend_str)
        self._backend_manager = QvmFrpBackendManagerV2(quafu_backend)
        self._backend_manager.cu_size = 4
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()
        self.proc_manager = QuafuQvmProcessManager(
            quafu_backend, name=quafu_backend_str
        )

        circ0 = self.create_dummy_bell_state((0, 1))
        circ1 = self.create_dummy_bell_state((0, 1))

        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        res = self.proc_manager.run([process0, process1])
        print(res.counts)


class TestSelectMethods(QvmBaseTest):
    """Test the runtime of different select methods in qvm process manager"""

    def get_fidelity(self, circuit_list, executables):
        """Run simulation on each executable and calculate fidelity"""
        shots = QVM_SHOTS
        fid_calculator = KlReliabilityCalculator()
        results = []
        for exe in executables:
            res = exe.comp_unit.backend.run(exe.circ, shots=shots).result().get_counts()
            results.append(res)

        assert len(results) == len(circuit_list)
        fidelities = []
        for i, circ in enumerate(circuit_list):
            fid = fid_calculator.calc_fidelity(circ, results[i], shots=shots)
            fidelities.append(fid)
        return average(fidelities)

    def reconstruct_exes(self, exes, processes):
        """Reset selected exes to the original position is process list"""
        recons_exes = []
        for proc in processes:
            for exe in proc:
                if exe in exes:
                    recons_exes.append(exe)
        return recons_exes

    def prepare_for_test(self, qasm, backend, cu_size):
        """Preparation before running selection"""
        self._backend = globals().get(backend)()
        self.back_manager = QvmFrpBackendManagerV2(self._backend)
        self.back_manager.cu_size = int(cu_size)
        self.back_manager.init_helpers()
        self.back_manager.init_cus()
        self.proc_manager = QvmProcessManagerV2(self._backend)

        qasm_list = qasm.split(",")
        self.process_list = []
        self.circuit_list = []
        for qasm_path in qasm_list:
            # The format is "/path/to/the/qasm/file/name.qasm"
            qasm_name = qasm_path.split("/")[-1].split(".")[0]
            file_name = "_".join([backend, qasm_name, str(cu_size)]) + ".pkl"
            compilation_obj = os.path.join(self.data_dir, file_name)
            circ = self.get_qiskit_circ("qasm", qasm_path=qasm_path)
            self.circuit_list.append(circ)
            if not os.path.exists(compilation_obj):
                proc = self.back_manager.compile(circ)
                self.save_compilation_outcome(
                    self.data_dir, proc, qasm_name, backend, int(cu_size)
                )
            else:
                proc = self.load_compilation_outcome(
                    self.data_dir, qasm_name, backend, int(cu_size)
                )
            self.process_list.append(proc)

        print("\n==== Testing ===")
        print("\n==== qasm_list ===\n")
        print(qasm)

    def test_select_methods(self, qasm, backend, cu_size):
        """
        Test brute_force and naive method

        Args:
            bench: List of qasm file paths
            backend: Backend name
        """

        self.prepare_for_test(qasm, backend, cu_size)

        # Naive
        st_time = time.time()
        naive_exes = self.proc_manager._select_naive(self.process_list)
        self.debug_exes(naive_exes)
        print(f"naive selection time\t{time.time() - st_time}")
        naive_exes = self.reconstruct_exes(naive_exes, self.process_list)
        fid = self.get_fidelity(self.circuit_list, naive_exes)
        print(f"naive selection result\t{fid}")

        # Brute-force
        st_time = time.time()
        brute_force_exes = self.proc_manager._select_brute_force(self.process_list)
        self.debug_exes(brute_force_exes)
        print(f"brute_force selection time\t{time.time() - st_time}")
        fid = self.get_fidelity(self.circuit_list, brute_force_exes)
        print(f"brute_force selection result\t{fid}")

    def test_naive_reverse_select(self, qasm, backend, cu_size):
        """
        Test brute_force and naive method

        Args:
            bench: List of qasm file paths
            backend: Backend name
        """

        self.prepare_for_test(qasm, backend, cu_size)

        # Naive reverse
        st_time = time.time()
        naive_exes = self.proc_manager._select_naive(self.process_list, reverse=True)
        self.debug_exes(naive_exes)
        print(f"naive selection time\t{time.time() - st_time}")
        naive_exes = self.reconstruct_exes(naive_exes, self.process_list)
        fid = self.get_fidelity(self.circuit_list, naive_exes)
        print(f"naive selection result\t{fid}")


class TestOracle(QvmBaseTest):
    fid_calculator = KlReliabilityCalculatorForOracle()

    def run_oracle(self, circ, backend, metric):
        """Run circuit on aer_simulator and get fidelity"""
        shots = QVM_SHOTS
        backend = globals().get(backend)()
        circ = transpile(circ, backend)
        counts = backend.run(circ, shots=shots).result().get_counts()
        if metric == "pst":
            self.fid_calculator = PSTCalculator()
        return self.fid_calculator.calc_fidelity(circ, counts, shots=shots)

    def test_oracle(self, qasm, backend, metric):
        """Test sequential run result
        Use native qiskit transpile and run

        Args:
            qasm (str): qasm_file_list
            backend (str): backend name
        """
        print("\n ================ test_oracle ================ \n")
        if qasm.endswith(".qasm"):
            circ = self.get_qiskit_circ("qasm", qasm_path=qasm)
            fid = self.run_oracle(circ, backend)
            return

        with open(qasm, "r") as f:
            for line in f:
                qasm_path = line.strip()
                bench_name = os.path.basename(qasm_path)
                bench_name = bench_name.split(".")[0]
                circ = self.get_qiskit_circ("qasm", qasm_path=qasm_path)
                fid = self.run_oracle(circ, backend, metric)
                print(f"{bench_name}\t{fid}")


class TestFrpOracle(TestOracle):
    calculator = KlReliabilityCalculatorForOracle()

    def run_oracle(self, circ, backend, metric):
        """Run circuit on aer_simulator and get fidelity"""
        shots = QVM_SHOTS

        # First find a partition
        proc_manager = FrpProcessManager(backend)
        part = proc_manager.gen_partition(circ)
        # Then generate a compute unit
        cu = self.back_manager.extract_one_cu(part)
        # Run on cu
        circ = transpile(circ, cu.backend)
        counts = cu.backend.run(circ, shots=shots).result().get_counts()
        return self.calculator.calc_fidelity(circ, counts, shots=shots)

    def test_oracle(self, qasm, backend, metric):
        """Test sequential run result
        Use native qiskit transpile and run

        Args:
            qasm (str): qasm_file_list
            backend (str): backend name
        """
        backend = globals().get(backend)()
        self.back_manager = QvmFrpBackendManagerV2(backend)
        self.back_manager.init_helpers()
        super().test_oracle(qasm, backend, metric)

    def test_pst_oracle(self, qasm, backend, metric):
        """Test sequential run result
        Use native qiskit transpile and run

        Args:
            qasm (str): qasm_file_list
            backend (str): backend name
        """
        backend = globals().get(backend)()
        self.back_manager = QvmFrpBackendManagerV2(backend)
        self.back_manager.init_helpers()
        self.calculator = PSTCalculator()
        super().test_oracle(qasm, backend, metric)


class TestFrpBaseline(QvmBaseTest):
    def prepare_for_test(self, qasm, backend, cu_size):
        """Preparation before running selection"""
        self._backend = globals().get(backend)()
        self.back_manager = QvmFrpBackendManagerV2(self._backend)
        self.back_manager.init_helpers()
        self.proc_manager = FrpProcessManager(self._backend)

        qasm_list = qasm.split(",")
        self.process_list = []
        self.circuit_list = []
        for qasm_path in qasm_list:
            # The format is "/path/to/the/qasm/file/name.qasm"
            qasm_name = qasm_path.split("/")[-1].split(".")[0]
            circ = self.get_qiskit_circ("qasm", qasm_path=qasm_path)
            self.circuit_list.append(circ)

        print("\n==== Testing ===")
        print("\n==== qasm_list ===\n")
        print(qasm)

    def test_frp_baseline(self, qasm, backend, cu_size):
        """
        Test brute_force and naive method

        Args:
            bench: List of qasm file paths
            backend: Backend name
        """
        shots = QVM_SHOTS

        self.prepare_for_test(qasm, backend, cu_size)

        # Naive
        st_time = time.time()
        st_time = time.time()
        # Find reliable locations
        parts = [self.proc_manager.gen_partition(circ) for circ in self.circuit_list]
        # Gen comp units
        cus = [self.back_manager.extract_one_cu(part) for part in parts]
        # Compilation
        circs = [
            transpile(circ, cu.backend) for circ, cu in zip(self.circuit_list, cus)
        ]
        print(f"baseline selection time\t{time.time() - st_time}")
        # Execution
        counts_list = [
            cu.backend.run(c, shots=shots).result().get_counts()
            for c, cu in zip(circs, cus)
        ]
        # Calculate fidelity
        # fid_calculator = KlReliabilityCalculator()
        fid_calculator = KlReliabilityCalculatorForOracle()
        fids = [
            fid_calculator.calc_fidelity(circ, counts, shots=shots)
            for circ, counts in zip(circs, counts_list)
        ]
        fid = average(fids)
        print(f"baseline selection result\t{fid}")
