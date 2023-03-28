import logging
import numpy as np

from typing import Optional
from qiskit.circuit import CircuitInstruction, QuantumCircuit
from qiskit.quantum_info.states.statevector import QiskitError, Statevector
from qiskit_aer import Aer

from qdao.circuit import BasePartitioner, StaticPartitioner, VirtualCircuit
from qdao.manager import SvManager
from qdao.util import retrieve_sv, generate_secondary_file_name
from qdao.qiskit.initializer import initialize

from utils.misc import print_statistics, time_it

QuantumCircuit.initialize = initialize

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
        #self._sim.set_options(method="statevector")

    @property
    def num_chunks(self):
        return self._num_chunks

    @time_it
    def _preprocess(
            self,
            sub_circ: VirtualCircuit,
            ichunk: int
        ):
        """Preprocessing before running a sub-simulation
        Args:
            sub_circ (VirtualCircuit):
            ichunk (int): For each sub-circuit, we need to
                simulate chunk by chunk, (num_chunks = 1<<(nq-np))
        Comments:
            1. Currently qiskit QuantumCircuit.initialize will
               append an initialize instruction at the end of
               the circuit, we need create a new instance and
               init from statevector at the begining
        """
        self._manager.chunk_idx = ichunk
        sv = self._manager.load_sv(sub_circ.real_qubits)
        logging.debug("loaded sv: {}".format(sv))
        nq = sub_circ.circ.num_qubits
        circ = QuantumCircuit(nq)
        circ.initialize(sv, range(nq))
        circ.print_statistics()
        circ.compose(sub_circ.circ, inplace=True)
        logging.debug(circ)
        return Statevector(sv), circ

    @time_it
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

    @time_it
    def _run(
            self,
            sub_circ: VirtualCircuit,
        ) -> None:
        """Run single sub-circuit

        Args:
            sub_circ (VirtualCircuit): Sub circuit with
                metadata recording the mapping between
                virtual and real qubits
        """
        for ichunk in range(self._num_chunks):
            _, circ = self._preprocess(sub_circ, ichunk)
            res = self._sim.run(circ).result()
            sv = res.get_statevector()
            self._postprocess(sub_circ, ichunk, sv)

    def debug(self, sub_circ: VirtualCircuit):
        """
        After running a sub-circuit,
        test the result statevector is correct
        """
        NQ = self._circ.num_qubits
        circ = QuantumCircuit(NQ)
        qubit_map = {
            sub_circ.circ.qubits[i]: circ.qubits[q]
            for i, q in enumerate(sub_circ.real_qubits)
        }
        for instr in sub_circ.circ.data[:-1]: # Omit last save_state
            op = instr.operation.copy()
            qubits = [qubit_map[i] for i in instr.qubits]
            new_instr = CircuitInstruction(op, qubits=qubits)
            circ.append(new_instr)
        circ.save_state()

        print(circ)
        sv = self._sim.run(circ).result().get_statevector(-1)
        sv_res = Statevector(retrieve_sv(NQ, self._nl))
        print(sv)
        print(sv_res)
        assert sv.equiv(sv_res)

    @time_it
    def _initialize(self):
        # Calc number of storage units
        num_sus = (1 << (self._circ.num_qubits - self._nl))
        for i in range(num_sus):
            # Init a storage unit
            su = np.zeros(1<<self._nl, dtype=complex)
            if i == 0:
                su[0] = 1.
            fn = generate_secondary_file_name(i)
            np.save(fn, su)

    def run(self):
        """Run simulation
        1. Partition the circuit into sub-circuits
        2. For each sub-circuit, run for 1<<(nq-np) times of
           simulations. Each simulation will init from a
           different part of statevector
        """
        sub_circs = self._part.run(self._circ)
        self._initialize()
        for sub_circ in sub_circs:
            self._run(sub_circ)
            #self.debug(sub_circ)

Engine.print_statistics = print_statistics
