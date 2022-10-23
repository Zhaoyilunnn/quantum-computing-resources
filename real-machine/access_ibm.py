"""
Ref:
    1. https://qiskit.org/documentation/apidoc/aer_noise.html
    2. https://qiskit.org/documentation/stubs/qiskit.providers.ibmq.IBMQBackend.html#qiskit.providers.ibmq.IBMQBackend
"""


from qiskit import QuantumCircuit, execute
from qiskit import IBMQ, Aer, transpile
from qiskit.providers import provider
from qiskit.result import counts
from qiskit.visualization import plot_histogram
from qiskit_aer.noise import NoiseModel

#IBMQ.save_account("036d2bca315b21dc9525cd05217943de9eab08326f37d652ac23aed075ea3e32ea3a983602b728e1b7c3e5e2a157959dcd0b834eb34ce607b3ec1d6401e9594d", overwrite=True)
provider = IBMQ.load_account()


def build_circ():
    # Make a circuit
    circ = QuantumCircuit(3, 3)
    circ.h(0)
    circ.cx(0, 1)
    circ.cx(1, 2)
    circ.measure([0, 1, 2], [0, 1, 2])
    return circ


def run_sim(backend, circ):
    noise_model = NoiseModel.from_backend(backend)
    # Get coupling map from backend
    coupling_map = backend.configuration().coupling_map
    
    # Get basis gates from noise model
    basis_gates = noise_model.basis_gates
    
    # Perform a noise simulation
    result = execute(circ, Aer.get_backend('qasm_simulator'),
                     coupling_map=coupling_map,
                     basis_gates=basis_gates,
                     noise_model=noise_model).result()
    counts = result.get_counts(0)
    print(counts)


def run_real(backend, circ):
    transpiled = transpile(circ, backend=backend)
    #job = backend.run(transpiled)
    #counts = job.result()
    status = backend.status()
    is_operational = status.operational
    jobs_in_queue = status.pending_jobs
    job_limit = backend.job_limit()

    print("is_operational:{} jobs_in_queue:{} job_limit:{}".format(is_operational, jobs_in_queue, job_limit))


def main():
    #backend = provider.get_backend('ibmq_vigo')
    backend = provider.backend.ibmq_lima
    circ = build_circ()
    run_sim(backend, circ)
    run_real(backend, circ)


if __name__ == '__main__':
    main()
