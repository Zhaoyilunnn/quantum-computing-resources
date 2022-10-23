"""
Ref:
    1. https://qiskit.org/documentation/apidoc/aer_noise.html
    2. https://qiskit.org/documentation/stubs/qiskit.providers.ibmq.IBMQBackend.html#qiskit.providers.ibmq.IBMQBackend
"""


import argparse
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, execute
from qiskit import IBMQ, Aer, transpile
from qiskit.providers import provider
from qiskit.result import counts
from qiskit.visualization import plot_histogram, plot_distribution
from qiskit_aer.noise import NoiseModel

#IBMQ.save_account("036d2bca315b21dc9525cd05217943de9eab08326f37d652ac23aed075ea3e32ea3a983602b728e1b7c3e5e2a157959dcd0b834eb34ce607b3ec1d6401e9594d", overwrite=True)
provider = IBMQ.load_account()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sys-name', type=str, default='ibmq_lima', help="Quantum Processor Name")
    parser.add_argument('--sim', type=str, default=1, help="Whether run simulator")
    parser.add_argument('--real', type=str, default=0, help="Whether run on real machine")
    parser.add_argument('--job-id', type=str, default="", help="Job id to retrieve")
    return parser.parse_args()


def build_circ():
    # Make a circuit
    circ = QuantumCircuit(3, 3)
    circ.h(0)
    circ.cx(0, 1)
    circ.cx(1, 2)
    circ.measure([0, 1, 2], [0, 1, 2])
    return circ


def run_sim(backend, circ, is_run=True):
    noise_model = NoiseModel.from_backend(backend)
    # Get coupling map from backend
    coupling_map = backend.configuration().coupling_map
    
    # Get basis gates from noise model
    basis_gates = noise_model.basis_gates
    
    if is_run:
        # Perform a noise simulation
        result = execute(circ, Aer.get_backend('qasm_simulator'),
                         coupling_map=coupling_map,
                         basis_gates=basis_gates,
                         noise_model=noise_model).result()
        #counts = result.get_counts(0)
        #counts = result.get_counts(circ)
        counts = result.get_counts()
        print(counts)
        #plot_histogram(counts)
        plot_distribution(counts)
        plt.savefig("simulation_res.png", dpi=1024)


def run_real(backend, circ, is_run=False, job_id=None):
    transpiled = transpile(circ, backend=backend)
    status = backend.status()
    is_operational = status.operational
    jobs_in_queue = status.pending_jobs
    job_limit = backend.job_limit()

    if job_id:
        retrieve_job = backend.retrieve_job(job_id)
        #print(retrieve_job.result().get_counts(0))
        #print(retrieve_job.result().get_counts(circ))
        counts = retrieve_job.result().get_counts()
        print(counts)
        plot_distribution(counts)
        plt.savefig("real_result.png", dpi=1024)

    if is_run:
        job = backend.run(transpiled)
        counts = job.result()

    print("is_operational:{} jobs_in_queue:{} job_limit:{}".format(is_operational, jobs_in_queue, job_limit))


def main():
    args = parse_args()
    #backend = provider.get_backend('ibmq_vigo')
    backend = provider.get_backend(args.sys_name)
    #backend = provider.backend.ibmq_lima
    circ = build_circ()
    run_sim(backend, circ, is_run=(True if args.sim == 1 else False))
    run_real(backend, circ, 
            is_run=(True if args.real == 1 else False),
            job_id=args.job_id)


if __name__ == '__main__':
    main()
