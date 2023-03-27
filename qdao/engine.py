import copy
import logging

from typing import Optional
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.states.statevector import QiskitError, Statevector
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
            num_primary: int=4,
            num_local: int=2
        ) -> None:
        if isinstance(partitioner, BasePartitioner):
            self._part = partitioner
        else:
            self._part = StaticPartitioner(np=num_primary, nl=num_local)

        self._circ = circuit
        self._nq = circuit.num_qubits
        if isinstance(manager, SvManager):
            self._manager = manager
        else:
            self._manager = SvManager(
                num_qubits=self._nq,
                num_primary=num_primary,
                num_local=num_local
            )

        self._np, self._nl = num_primary, num_local
        self._num_chunks = 1 << (self._nq - self._np)

        self._sim = Aer.get_backend("aer_simulator")
        self._sim.set_options(method="statevector")

    @property
    def num_chunks(self):
        return self._num_chunks

    def _preprocess(
            self,
            sub_circ: VirtualCircuit,
            isub: int,
            ichunk: int
        ):
        """Preprocessing before running a sub-simulation
        Args:
            sub_circ (VirtualCircuit):
            isub (int): Position in the sub-circuit sequence
            ichunk (int): For each sub-circuit, we need to
                simulate chunk by chunk, (num_chunks = 1<<(nq-np))
        Comments:
            1. For the first sub_circuit we do not need to load
               statevector from secondary storage
            2. Currently qiskit QuantumCircuit.initialize will
               append an initialize instruction at the end of
               the circuit, we need create a new instance and
               init from statevector at the begining
        """
        if isub == 0:
            return
        self._manager.chunk_idx = ichunk
        sv = self._manager.load_sv(sub_circ.real_qubits)
        nq = sub_circ.circ.num_qubits
        circ = QuantumCircuit(nq)
        circ.initialize(sv, range(nq))
        circ.compose(sub_circ.circ, inplace=True)
        sub_circ.circ = circ
        return Statevector(sv)

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
            try:
                self._preprocess(sub_circ, isub, ichunk)
            except QiskitError as e:
                assert e.message == "Sum of amplitudes-squared does not equal one."
                logging.info("Skipping all-zero chunk: {}, "\
                        "for sub-circuit: {}".format(ichunk, sub_circ.circ))
                continue
            #self._preprocess(sub_circ, isub, ichunk)
            res = self._sim.run(sub_circ.circ).result()
            sv = res.get_statevector()
            self._postprocess(sub_circ, ichunk, sv)

    def run(self):
        """Run simulation
        1. Partition the circuit into sub-circuits
        2. For each sub-circuit, run for 1<<(nq-np) times of
           simulations. Each simulation will init from a
           different part of statevector
        """
        sub_circs = self._part.run(self._circ)

        # TODO(zhaoyilun): delete this
        circ = copy.deepcopy(self._circ)
        circ.save_state()
        print(circ)
        print(sub_circs[0].circ)
        assert sub_circs[0].circ == circ
        # TODO(zhaoyilun): delete this

        for isub, sub_circ in enumerate(sub_circs):
            self._run(sub_circ, isub)


