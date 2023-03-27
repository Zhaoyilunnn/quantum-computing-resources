from typing import Optional
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.states.statevector import Statevector
from qiskit_aer import Aer

from qdao.circuit import BasePartitioner, StaticPartitioner, VirtualCircuit
from qdao.manager import SvManager


class Engine:
    """Engine to execute a quantum circuit"""

    def __init__(
            self,
            partitioner: Optional[BasePartitioner] = None,
            manager: Optional[SvManager] = None,
            circuit: QuantumCircuit = QuantumCircuit(),
            **options
        ) -> None:
        if isinstance(partitioner, BasePartitioner):
            self._part = partitioner
        else:
            self._part = StaticPartitioner(**options)

        if isinstance(manager, SvManager):
            self._manager = manager
        else:
            self._manager = SvManager(**options)

        self._circ = circuit
        self._sim = Aer.get_backend("aer_simulator")
        self._sim.set_options(method="statevector")
        
        self._nq, self._np, self._nl = 6, 4, 2

        if "nq" in options:
            self._nq = options["nq"] 

        if "np" in options:
            self._np = options["np"] 

        if "nl" in options:
            self._nl = options["nl"] 

        self._num_chunks = 1 << (self._nq - self._np)
    
    @property
    def num_chunks(self):
        return self._num_chunks

    def _preprocess(
            self, 
            sub_circ: VirtualCircuit,
            isub: int,
            ichunk: int
        ) -> None:
        """Preprocessing before running a sub-simulation
        Args:
            sub_circ (VirtualCircuit):
            isub (int): Position in the sub-circuit sequence
            ichunk (int): For each sub-circuit, we need to 
                simulate chunk by chunk, (num_chunks = 1<<(nq-np))
        Comments:
            For the first sub_circuit we do not need to load
            statevector from secondary storage
        """
        if isub == 0:
            return
        self._manager.chunk_idx = ichunk
        sv = self._manager.load_sv(sub_circ.real_qubits)
        sub_circ.circ.initialize(sv)

    def _postprocess(
            self,
            sub_circ: VirtualCircuit,
            ichunk: int,
            sv: Statevector
        ) -> None:
        """Postprocessing after running a sub-simulation
        Args:
            sub_circ (VirtualCircuit):
            ichunk (int): For each sub-circuit, we need to 
                simulate chunk by chunk, (num_chunks = 1<<(nq-np))
            sv (Statevector): Statevector result of simulation
        """ 
        self._manager.chunk_idx = ichunk
        self._manager.chunk = sv.data
        self._manager.store_sv(sub_circ.real_qubits)

    def _run(
            self, 
            sub_circ: VirtualCircuit,
            isub: int
        ) -> None:
        """Run single sub-circuit

        Args:
            sub_circ (VirtualCircuit): Sub circuit with
                metadata recording the mapping between
                virtual and real qubits
            isub (int): Position of current sub-circ in 
                original sub-circ sequence
        """
        for ichunk in range(self._num_chunks):
            self._preprocess(sub_circ, isub, ichunk)
            res = self._sim.run(sub_circ.circ).result()
            sv = res.get_statevector()
            self._postprocess(sub_circ, ichunk, sv)

    def run(self):
        """Run simulation
        1. Partition the circuit into sub-circuits
        """
        sub_circs = self._part.run(self._circ)

        for isub, sub_circ in enumerate(sub_circs):
            self._run(sub_circ, isub)


