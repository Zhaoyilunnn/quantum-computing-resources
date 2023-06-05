import os

from qiskit.circuit import QuantumCircuit

from qiskit.circuit.random import random_circuit
from qiskit.pulse import Schedule

from qiskit_aer import Aer

from typing import Optional, Tuple, Union, List

from constants import QCS_BENCHMARKS_DIR


class BaseTest:
    # _sv_sim = Aer.get_backend("statevector_simulator")
    _sv_sim = Aer.get_backend("aer_simulator")
    # _sv_sim.set_options(method="statevector")
    _sv_sim.set_options(fusion_enable=False)

    def get_qiskit_circ(
        self,
        bench_name,
        num_qubits: int = 4,
        depth: int = 10,
        measure: bool = True,
        qasm_path: Optional[str] = None,
    ):
        circ = None
        if bench_name == "random":
            circ = random_circuit(num_qubits, depth, measure=measure)
        elif bench_name == "qasm":
            if not isinstance(qasm_path, str):
                raise ValueError("Qasm file path shoud be a string")
            if not os.path.isfile(qasm_path):
                raise ValueError("Please specify qasm file path!")
            circ = QuantumCircuit().from_qasm_file(qasm_path)
        else:
            raise NotImplementedError("Unsupported bench type!")

        return circ

    def get_quafu_circ_from_qasm(self, qasm_path):
        from quafu.circuits.quantum_circuit import QuantumCircuit

        with open(qasm_path, "r") as qasm:
            # FIXME(zhaoyilun): Quafu QuantumCircuit's num will be
            # read from qasm
            circ = QuantumCircuit(1)
            circ.from_openqasm(qasm.read())
            return circ

    def show_scheduled_debug_info(self, scheduled: Schedule) -> None:
        for inst in scheduled.instructions:
            print(inst)

    def create_dummy_bell_state(
        self,
        qubits: Union[List[Tuple[int, int]], Tuple[int, int]],
        num_qubits=None,
        is_measure=True,
        save_state=False,
    ) -> QuantumCircuit:
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
            if is_measure:
                dummy_circ.measure([q0, q1], [q0, q1])

        dummy_circ = None
        if isinstance(qubits, tuple):
            q0, q1 = qubits
            if q0 >= q1:
                raise ValueError("q0 should be smaller than q1")

            dummy_circ = QuantumCircuit(q1 + 1, q1 + 1)
            do_bell_state(dummy_circ, q0, q1)
        else:
            if not num_qubits:
                raise ValueError(
                    "Please specify the number of qubits if input is a set of qubit pairs"
                )

            dummy_circ = QuantumCircuit(num_qubits, num_qubits)
            for q0, q1 in qubits:
                if q0 >= num_qubits or q1 >= num_qubits:
                    raise ValueError(
                        "num_qubits must be larger than all involved qubits"
                    )
                do_bell_state(dummy_circ, q0, q1)

        if save_state:
            dummy_circ.save_state()

        return dummy_circ
