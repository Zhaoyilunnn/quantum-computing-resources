from qiskit.providers.fake_provider import *
from qiskit.quantum_info import state_fidelity

from qiskit_aer import Aer 
from qiskit_aer.noise import NoiseModel
#from qiskit import Aer
#from qiskit.providers.aer.noise import NoiseModel

from qvm.manager.backend_manager import * 
from qvm.manager.process_manager import *
from qvm.util.circuit import BaseReliabilityCalculator, KlReliabilityCalculator
from qvm.util.backend import *
from qvm.test.base import *

from util import *


class TestBench(BaseTest):
    """
    Integration of backend manager and process manager
    """
    
    def setup_class(self):
        self._backend_manager = BfsBackendManager(self._backend)
        self._backend_manager.init_helpers()
        #self._backend_manager.cu_size = 2
        self._backend_manager.init_compute_units()
        self._process_manager = ProcessManagerFactory.get_manager("qvm", self._backend)

    def test_single_bench(self, bench):
        #circ = self.create_dummy_bell_state((0,1))  
        self._fid_calculator = KlReliabilityCalculator()
        circ = self.get_small_bench_circ(bench)
        cu = self._backend_manager.allocate(circ)
        fid_qvm = self.run_on_backend_and_get_fid(circ, cu.backend)
        fid_org = self.run_on_backend_and_get_fid(circ, self._backend)

        print("Fidelity Comparison\t{}\t{}".format(fid_qvm, fid_org))

    def test_two_bench(self, bench):
        shots = 2**20

        #circ0 = self.create_dummy_bell_state((0,1))
        #circ1 = self.create_dummy_bell_state((0,1))
        circ0 = self.get_small_bench_circ(bench)
        circ1 = self.get_small_bench_circ(bench)
        
        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        qvm_proc = QvmProcessManager(self._backend)
        #qvm_res = qvm_proc.run([process0, process1]).result()
        exe0, exe1 = qvm_proc._select([process0, process1])
        cu = self._backend_manager.merge_compute_units([exe0.resource, exe1.resource])
        #print(cu.real_qubits)
        #print(exe0.circ)
        #print(exe1.circ)
        exe = qvm_proc._merge_circuits([exe0.circ, exe1.circ])
        qvm_res = cu.backend.run(exe, shots=shots).result()

        base_proc = BaselineProcessManager(self._backend)
        base_res = base_proc.run([circ1, circ1], shots=shots).result()

        circ = base_proc._merge_circuits([circ0, circ1])
        #print(qvm_res.get_counts())
        #print(base_res.get_counts())

        # Calculate fidelity
        self._fid_calculator = KlReliabilityCalculator()
        fid_qvm = self._fid_calculator.calc_fidelity(circ, qvm_res.get_counts(), shots=shots)
        fid_base = self._fid_calculator.calc_fidelity(circ, base_res.get_counts(), shots=shots)
        print("Fid of qvm & baseline\t{}\t{}".format(fid_qvm, fid_base))


