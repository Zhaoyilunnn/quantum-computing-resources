import os
import pickle
from test.base import BaseTest

from qiskit.circuit import QuantumCircuit
from qiskit.circuit.random import random_circuit
from qiskit.compiler import transpile
from qiskit.providers.fake_provider import *
from qiskit.quantum_info import state_fidelity
from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel

from qvm.manager import *
from qvm.util.backend import *
from qvm.util.circuit import BaseReliabilityCalculator

# from qiskit import Aer
# from qiskit.providers.aer.noise import NoiseModel


class QvmBaseTest(BaseTest):
    # _backend = FakeLagos()
    # _backend = FakeManila()
    _backend = FakeCairo()
    # _sv_sim = Aer.get_backend("aer_simulator")
    _fid_calculator = BaseReliabilityCalculator()

    data_dir = "data/qvm"

    def run_experiments(self, transpiled, scheduled, verify):
        # Fisrt run ideal simulation on simulator
        res_ideal = self._sv_sim.run(transpiled, shots=1024).result()
        sv_ideal = res_ideal.get_statevector(transpiled)

        # Then run noisy simulation on simulator
        # The noise model is extracted from backend
        noise_model = NoiseModel.from_backend(self._backend)
        res_noise = self._sv_sim.run(
            transpiled, noise_model=noise_model, shots=1024
        ).result()
        sv_noise = res_noise.get_statevector(transpiled)
        print("==================== SV::noise ==================")
        print(sv_noise)
        print(res_noise.get_counts())
        print("==================== SV::ideal ==================")
        print(sv_ideal)
        print(res_ideal.get_counts())
        print("==================== SV::fidelity ==================")
        print(state_fidelity(sv_noise, sv_ideal))

        if verify == "pulse":
            res_noise = self._backend.run(scheduled).result()
            print("==================== COUNTS::pulse ==================")
            print(res_noise.get_counts())
        elif verify == "qasm":
            res_noise = self._backend.run(transpiled).result()
            print("==================== COUNTS::qasm ==================")
            print(res_noise.get_counts())
        else:
            raise NotImplementedError(
                "Unsupported verfication level, please choose either `pulse` or `qasm`"
            )

    def run_on_backend_and_get_fid(self, circ, backend: BackendV1, **kwargs):
        """
        1. Transpile
        2. Run on backend
        3. Get counts
        4. Calculate fidelity/reliability
        """
        trans = transpile(circ, backend)
        res = backend.run(trans, **kwargs).result()
        counts = res.get_counts()
        print("================= Counts after running on backend =====================")
        print(counts)
        fid = self._fid_calculator.calc_fidelity(trans, counts, **kwargs)
        print("=================== Reliability =======================")
        print(fid)
        return fid

    def debug_exes(self, executables: List[BaseExecutable]):
        """Print executables compute unit ids list"""
        compute_unit_lists = [exe.comp_unit_ids for exe in executables]
        print(f"compute_unit_list\t{compute_unit_lists}")

    def reconstruct_exes(self, exes: List[BaseExecutable], processes: List[Process]):
        """Reset selected exes to the original position is process list"""
        recons_exes = []
        for proc in processes:
            for exe in proc:
                if exe in exes:
                    recons_exes.append(exe)
        return recons_exes

    def save_compilation_outcome(
        self, data_dir, process: Process, qasm_name: str, backend: str, cu_size: int = 4
    ):
        """Save compilation result (Process object) to disk

        Args:
            data_dir (str): Directory to save this object
            process (Process): Compiled outcome on given backend
            qasm_name (str): QASM benchmark name
            backend (str): Backend name
            cu_size (int): Number of qubits within a compute unit
        """
        file_name = "_".join([backend, qasm_name, str(cu_size)]) + ".pkl"
        file_name = os.path.join(data_dir, file_name)

        serialized_obj = pickle.dumps(process)
        with open(file_name, "wb") as f:
            f.write(serialized_obj)

    def load_compilation_outcome(
        self, data_dir, qasm_name: str, backend: str, cu_size: int = 4
    ):
        """Save compilation result (Process object) to disk

        Args:
            data_dir (str): Directory to save this object
            qasm_name (str): QASM benchmark name
            backend (str): Backend name
            cu_size (int): Number of qubits within a compute unit
        """
        file_name = "_".join([backend, qasm_name, str(cu_size)]) + ".pkl"
        file_name = os.path.join(data_dir, file_name)

        serialized_obj = None
        with open(file_name, "rb") as f:
            serialized_obj = f.read()
        if serialized_obj:
            return pickle.loads(serialized_obj)
        return None
