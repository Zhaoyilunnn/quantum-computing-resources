from test.qvm import *

from qiskit.compiler import schedule, transpile
from qiskit.providers.fake_provider import *
from qvm.manager.backend_manager import *
from qvm.util.backend import *
from qvm.util.misc import *

from constants import QCS_BENCHMARKS_DIR

# from qiskit import Aer
# from qiskit.providers.aer.noise import NoiseModel


BENCHES = ["random_8_5_max_operands_2_gen.qasm", "random_5_2_max_operands_2_gen.qasm"]

BENCH_PATHS = [
    os.path.join(os.path.curdir, QCS_BENCHMARKS_DIR, bench) for bench in BENCHES
]


class TestQvmProcManagerV2(QvmBaseTest):
    def brute_force_on_specific_backend(self, backend_obj):
        proc_manager = QvmProcessManagerV2(backend_obj, method="brute_force")
        back_manager = QvmFrpBackendManagerV2(backend_obj)
        back_manager.init_helpers()
        back_manager.init_cus()
        circuits = [
            QuantumCircuit.from_qasm_file(bench_path) for bench_path in BENCH_PATHS
        ]
        processes = [back_manager.compile(circ) for circ in circuits]
        exes = proc_manager._select(processes)
        for i, exe in enumerate(exes):
            print(f"exe:{i}, compute_unit_ids:{exe.comp_unit_ids}")

        lists = [proc.resource_list for proc in processes]
        best_combination = min_sum_indices_sets(*lists)
        assert best_combination == [exe.comp_unit_ids for exe in exes]

    def test_select_brute_force(self):
        # self.brute_force_on_specific_backend(FakeCairo())
        self.brute_force_on_specific_backend(FakeBrooklyn())


class TestProcessManager(QvmBaseTest):
    def test_qvm_manager(self):
        manager = ProcessManagerFactory.get_manager("qvm", FakeManila())

        test_eprs = [(0, 1), (2, 3)]

        dummy_circ = self.create_dummy_bell_state(test_eprs[0])
        transpiled = transpile(dummy_circ, manager._backend)
        sch_first = schedule(transpiled, manager._backend)
        print("===================== Schedule 0 ===========================")
        self.show_scheduled_debug_info(sch_first)
        # self.run_experiments(transpiled, sch_first, 'pulse')

        dummy_circ = self.create_dummy_bell_state(test_eprs[1])
        transpiled = transpile(dummy_circ, manager._backend)
        sch_second = schedule(transpiled, manager._backend)
        print("===================== Schedule 1 ===========================")
        self.show_scheduled_debug_info(sch_second)
        # self.run_experiments(transpiled, sch_second, 'pulse')

        sch_merged = manager._merge_schedules([sch_first, sch_second])
        print("===================== Merged Schedule ===========================")
        self.show_scheduled_debug_info(sch_merged)
        # self.run_experiments(transpiled, sch_merged, 'pulse')

        dummy_circ = self.create_dummy_bell_state(test_eprs, num_qubits=4)
        print("===================== Original Schedule ===========================")
        transpiled = transpile(dummy_circ, manager._backend)
        sch_original = schedule(transpiled, manager._backend)
        self.show_scheduled_debug_info(sch_original)
        # self.run_experiments(transpiled, sch_original, 'qasm')

        # assert sch_merged.instructions == sch_original.instructions

    def test_baseline_manager(self):
        manager = ProcessManagerFactory.get_manager("baseline", FakeManila())

        test_eprs = [(0, 1), (2, 3)]
        dummy_circ_first = self.create_dummy_bell_state(test_eprs[0])
        dummy_circ_second = self.create_dummy_bell_state(test_eprs[1])

        dummy_circ_original = self.create_dummy_bell_state(test_eprs, num_qubits=4)
        transpiled = transpile(dummy_circ_original, manager._backend)
        sch_original = schedule(transpiled, manager._backend)

        dummy_circ_merged = manager._merge_circuits(
            [dummy_circ_first, dummy_circ_first]
        )
        print(dummy_circ_original)
        print(dummy_circ_merged)

        transpiled = transpile(dummy_circ_merged, manager._backend)
        sch_merged = schedule(transpiled, manager._backend)

        assert sch_original.instructions == sch_merged.instructions
