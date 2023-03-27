from qiskit.compiler import transpile, schedule
from qiskit.providers.fake_provider import *

#from qiskit import Aer
#from qiskit.providers.aer.noise import NoiseModel

from qvm.manager.backend_manager import * 
from qvm.util.backend import *
from qvm.util.misc import *
from qvm.test.base import *

from utils.misc import *


class TestBaseBackendManager(QvmBaseTest):
    
    def setup_class(self):
        self._manager = BaseBackendManager(self._backend)
        self._manager.init_helpers()
        self._manager.init_compute_units()
        self._conf = self._backend.configuration()
        self._props = self._backend.properties() 

    def test_allocate(self):
        circ = self.create_dummy_bell_state([(0,1),(2,3)], num_qubits=4)
        cu = self._manager.allocate(circ)
        #virt_trans = transpile(circ, cu.backend)
        real_trans = transpile(circ, self._backend)
        #print(cu.backend.run(virt_trans).result().get_counts())
        print(self._backend.run(real_trans).result().get_counts())

    def test_extract_compute_unit(self):

        sub_graph = [1, 2]

        compute_unit = self._manager.extract_single_compute_unit(sub_graph) 
        
        cu_conf = compute_unit.backend.configuration()
        cu_props = compute_unit.backend.properties()
        
        assert cu_conf.coupling_map == [[0, 1], [1, 0]]
        assert len(cu_props.qubits) == 2
        assert compute_unit.real_qubits == [1, 2]
        assert compute_unit.real_to_virtual == {1:0, 2:1}

        for gate in cu_props.gates:

            # Create a test gate coping from 
            # gate in compute unit, the only
            # difference should be qubits
            test_gate = copy.deepcopy(gate)
            real_q = compute_unit.real_qubits
            
            for i, q in enumerate(gate.qubits):
                vq = gate.qubits[i] # Virtual qubit id in compute unit gate
                test_gate.qubits[i] = real_q[vq] # Remap to real qubit id

            # Then the test gate should be the same as the original one
            assert test_gate in self._props.gates

    
    def test_compilation_on_compute_unit(self, verify):


        # Defined the qubits in compute unit
        sub_graph = [1,4,7]
        #sub_graph = [0,1,5]
        vq0, vq1 = 0, 1 # virtual qubit id
        rq0, rq1 = sub_graph[vq0], sub_graph[vq1]
        
        # Extract a compute unit from backend
        compute_unit = self._manager.extract_single_compute_unit(sub_graph) 

        plot_error(self._backend, figname="backend.png")
        plot_error(compute_unit.backend, figname="compute_unit.png")

        dummy_circ = self.create_dummy_bell_state((vq0, vq1))

        fig = dummy_circ.draw(output='mpl')
        fig.savefig("bell_state.png")

        transpiled = transpile(dummy_circ, compute_unit.backend)
        print(transpiled._data) 
        real_transpiled = self._manager.circuit_virtual_to_real(transpiled, compute_unit)
        print(real_transpiled._data)
        sch_cu = schedule(real_transpiled, self._backend)
        self.show_scheduled_debug_info(sch_cu)
        #self.run_experiments(transpiled, sch_cu, verify)

        print("================== Original ========================")
        dummy_circ = self.create_dummy_bell_state((rq0, rq1))
        transpiled = transpile(dummy_circ, self._backend)
        print(transpiled)
        sch_original = schedule(transpiled, self._backend)
        self.show_scheduled_debug_info(sch_original)
        #self.run_experiments(transpiled, sch_original, verify)

        assert sch_cu.instructions == sch_original.instructions 

    def test_compile(self):
        circ = self.create_dummy_bell_state((0,1))
        
        res = self._manager.compile(circ)
        for rid in res:
            print(rid, res[rid].resource.real_qubits, res[rid].resource_id)
            print(res[rid].circ)


class TestKlBackendManager(QvmBaseTest):

    def setup_class(self):
        self._manager = KlBackendManager(self._backend)
        self._manager.init_helpers()
        self._manager.init_compute_units()

    def test_allocate(self):
        circ = self.create_dummy_bell_state((0,1))
        cu = self._manager.allocate(circ)
        #print(cu.real_qubits, cu.real_to_virtual)
        plot_error(cu.backend, figname="compute_unit_kl.png")

        for i, cu in enumerate(self._manager._compute_units):
            cu.draw_nx_cmap(figname="cu_nx_cmap_{}.png".format(i))


class TestBfsBackendManager(QvmBaseTest):

    def setup_class(self):
        self._manager = BfsBackendManager(self._backend)
        self._manager.init_helpers()
        self._manager.init_compute_units()

    def test_allocate(self):
        circ = self.create_dummy_bell_state((0,1))
        cu = self._manager.allocate(circ)
        #print(cu.real_qubits, cu.real_to_virtual)
        plot_error(cu.backend, figname="compute_unit_bfs.png")

        for i, cu in enumerate(self._manager._compute_units):
            cu.draw_nx_cmap(figname="cu_nx_cmap_{}.png".format(i))


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

