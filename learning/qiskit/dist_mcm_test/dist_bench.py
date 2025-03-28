"""
A simple dynamic circuit program to test how runtime change with the number of qubits increases


Environment:

  qiskit==1.1.1
  qiskit-aer==0.14.1
  qiskit-ibm-runtime==0.25.0
  qiskit-qasm3-import==0.5.0

"""

from typing import Tuple
from numpy import random
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

service = QiskitRuntimeService()


def apply_mcm_block(qc: QuantumCircuit, qubits: Tuple[int, int]):
    """
    Apply a measurement-feedback block on two given qubits
    """
    q0 = qubits[0]
    q1 = qubits[1]

    # generate a random int value between 1 and 10
    delay = random.randint(1, 10)
    qc.delay(delay, q0, "ns")
    qc.x(q0)
    qc.h(q1)
    qc.measure(q0, q0)
    qc.z(q1).c_if(q0, 0)
    qc.reset(q0)


def dist_test_qc(num_qubit: int):
    qc = QuantumCircuit(num_qubit, num_qubit)
    assert num_qubit % 2 == 0, "The number of qubits should be even."

    for i in range(0, num_qubit, 2):
        apply_mcm_block(qc, (i, i + 1))

    # apply a layer of randomized cnot on the qubits
    for i in range(0, num_qubit, 2):
        # generate two random qubit id
        q0 = random.randint(0, num_qubit)
        q1 = random.randint(0, num_qubit)
        # make sure q0 != q1
        while q0 == q1:
            q1 = random.randint(0, num_qubit)
        # apply cnot
        qc.cx(q0, q1)

    qc.measure_all()
    return qc


# 1. A quantum circuit for preparing the quantum state (|00> + |11>)/rt{2}
# qc = QuantumCircuit(2)
# qc.h(0)
# qc.cx(0, 1)
# qc.measure_all()

for i in range(4, 106, 10):

    qc = dist_test_qc(i)

    # 2: Optimize problem for quantum execution.
    backend = service.least_busy(operational=True, simulator=False)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(qc)

    # 3. Execute using the Sampler primitive
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = 1  # Options can be set using auto-complete.
    job = sampler.run([isa_circuit])
    print(f"Job ID is {job.job_id()}")
    # pub_result = job.result()[0]
    # print(f"Counts for the meas output register: {pub_result.data.meas.get_counts()}")
