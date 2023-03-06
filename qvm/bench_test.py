from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile, schedule
from qiskit.providers.fake_provider import *
from qiskit.quantum_info import state_fidelity

from qiskit_aer import Aer 
from qiskit_aer.noise import NoiseModel
#from qiskit import Aer
#from qiskit.providers.aer.noise import NoiseModel

from qvm.manager.backend_manager import * 
from qvm.manager.process_manager import *
from qvm.util.circuit import BaseReliabilityCalculator
from qvm.util.backend import *
from qvm.test.base import *

from util import *


class TestQvm(BaseTest):
    """
    Integration of backend manager and process manager
    """
    
    def setup_class(self):
        self._backend_manager = BfsBackendManager(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_compute_units()
        self._process_manager = ProcessManagerFactory.get_manager("qvm", self._backend)

    def test_single_bench(self, bench):
        #circ = self.create_dummy_bell_state((0,1))  
        circ = self.get_small_bench_circ(bench)
        cu = self._backend_manager.allocate(circ)
        fid_qvm = self.run_on_backend_and_get_fid(circ, cu.backend)
        fid_org = self.run_on_backend_and_get_fid(circ, self._backend)

        print("Fidelity Comparison\t{}\t{}".format(fid_qvm, fid_org))
