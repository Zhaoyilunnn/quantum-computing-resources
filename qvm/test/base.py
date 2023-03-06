from qiskit.circuit import QuantumCircuit
from qiskit.circuit.random import random_circuit
from qiskit.compiler import transpile
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

from util import *


class BaseTest:

    #_backend = FakeLagos()
    #_backend = FakeManila()
    _backend = FakeCairo()
    _sv_sim = Aer.get_backend("statevector_simulator")
    #_sv_sim = Aer.get_backend("aer_simulator")
    _fid_calculator = BaseReliabilityCalculator()

    def get_small_bench_circ(self, bench_name):
        circ = None
        if bench_name == "random":
            circ = random_circuit(4, 10, measure=True) 

        return circ
        
    def show_scheduled_debug_info(self, scheduled: Schedule) -> None:
        for inst in scheduled.instructions:
            print(inst)
    
    def run_experiments(self, transpiled, scheduled, verify):
        # Fisrt run ideal simulation on simulator
        res_ideal = self._sv_sim.run(transpiled, shots=1024).result()
        sv_ideal = res_ideal.get_statevector(transpiled)

        # Then run noisy simulation on simulator 
        # The noise model is extracted from backend
        noise_model = NoiseModel.from_backend(self._backend)
        res_noise = self._sv_sim.run(transpiled, noise_model=noise_model, shots=1024).result()
        sv_noise = res_noise.get_statevector(transpiled)
        print("==================== SV::noise ==================")
        print(sv_noise)
        print(res_noise.get_counts())
        print("==================== SV::ideal ==================")
        print(sv_ideal)
        print(res_ideal.get_counts())
        print("==================== SV::fidelity ==================")
        print(state_fidelity(sv_noise, sv_ideal))

        if verify == 'pulse':
            res_noise = self._backend.run(scheduled).result()
            print("==================== COUNTS::pulse ==================")
            print(res_noise.get_counts())
        elif verify == 'qasm':
            res_noise = self._backend.run(transpiled).result()
            print("==================== COUNTS::qasm ==================")
            print(res_noise.get_counts())
        else:
            raise NotImplementedError("Unsupported verfication level, please choose either `pulse` or `qasm`")

    def run_on_backend_and_get_fid(self, 
            circ, 
            backend: BackendV1,
            shots=4096):
        """ 
        1. Transpile
        2. Run on backend
        3. Get counts
        4. Calculate fidelity/reliability
        """
        trans = transpile(circ, backend)
        res = backend.run(trans, shots=shots).result()
        counts = res.get_counts()
        print("================= Counts after running on backend =====================")
        print(counts)
        fid = self._fid_calculator.calc_fidelity(trans, counts)
        print("=================== Reliability =======================")
        print(fid)
        return fid

    def create_dummy_bell_state(self, 
            qubits: Union[List[Tuple[int, int]], Tuple[int, int]],
            num_qubits=None) -> QuantumCircuit:
        """
        Create a bell state circuit for test
        q0: the first qubit id to operate on
        q1: the second qubit id to operate on

        The circuit size will be q1+1, which is 
        useful to emulate virtualization
        """
        def do_bell_state(dummy_circ, q0, q1):
            dummy_circ.h(q0)
            dummy_circ.cx(q0, q1)
            dummy_circ.measure([q0, q1], [q0, q1])


        dummy_circ = None
        if isinstance(qubits, tuple):
            q0, q1 = qubits
            if q0 >= q1:
                raise ValueError("q0 should be smaller than q1")

            dummy_circ = QuantumCircuit(q1+1, q1+1)
            do_bell_state(dummy_circ, q0, q1)
        else:
            if not num_qubits:
                raise ValueError("Please specify the number of qubits if input is a set of qubit pairs")

            dummy_circ = QuantumCircuit(num_qubits, num_qubits)
            for (q0, q1) in qubits:
                if q0 >= num_qubits or q1 >= num_qubits:
                    raise ValueError("num_qubits must be larger than all involved qubits")
                do_bell_state(dummy_circ, q0, q1)

        return dummy_circ

