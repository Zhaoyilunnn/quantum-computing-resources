from qiskit.compiler import transpile, schedule
from qiskit.providers.fake_provider import *

#from qiskit import Aer
#from qiskit.providers.aer.noise import NoiseModel

from qvm.manager.backend_manager import * 
from qvm.util.backend import *
from qvm.util.misc import *
from qvm.test.base import *

from util import *


class TestProcessManager(QvmBaseTest):

    def test_qvm_manager(self):

        manager = ProcessManagerFactory.get_manager("qvm", FakeManila()) 
        
        test_eprs = [(0,1), (2,3)]

        dummy_circ = self.create_dummy_bell_state(test_eprs[0])
        transpiled = transpile(dummy_circ, manager._backend)
        sch_first = schedule(transpiled, manager._backend)
        print("===================== Schedule 0 ===========================")
        self.show_scheduled_debug_info(sch_first)
        #self.run_experiments(transpiled, sch_first, 'pulse')

        dummy_circ = self.create_dummy_bell_state(test_eprs[1])
        transpiled = transpile(dummy_circ, manager._backend)
        sch_second = schedule(transpiled, manager._backend)
        print("===================== Schedule 1 ===========================")
        self.show_scheduled_debug_info(sch_second) 
        #self.run_experiments(transpiled, sch_second, 'pulse')

        sch_merged = manager._merge_schedules([sch_first, sch_second])
        print("===================== Merged Schedule ===========================")
        self.show_scheduled_debug_info(sch_merged)
        #self.run_experiments(transpiled, sch_merged, 'pulse')

        dummy_circ = self.create_dummy_bell_state(test_eprs, num_qubits=4)
        print("===================== Original Schedule ===========================")
        transpiled = transpile(dummy_circ, manager._backend)
        sch_original = schedule(transpiled, manager._backend)
        self.show_scheduled_debug_info(sch_original)
        #self.run_experiments(transpiled, sch_original, 'qasm')

        #assert sch_merged.instructions == sch_original.instructions


    def test_baseline_manager(self):
        
        manager = ProcessManagerFactory.get_manager("baseline", FakeManila())

        test_eprs = [(0,1), (2,3)]
        dummy_circ_first = self.create_dummy_bell_state(test_eprs[0])
        dummy_circ_second = self.create_dummy_bell_state(test_eprs[1])
        
        dummy_circ_original = self.create_dummy_bell_state(test_eprs, num_qubits=4)
        transpiled = transpile(dummy_circ_original, manager._backend)
        sch_original = schedule(transpiled, manager._backend)

        dummy_circ_merged = manager._merge_circuits([dummy_circ_first, dummy_circ_first])
        print(dummy_circ_original)
        print(dummy_circ_merged)

        transpiled = transpile(dummy_circ_merged, manager._backend)
        sch_merged = schedule(transpiled, manager._backend)

        assert sch_original.instructions == sch_merged.instructions


