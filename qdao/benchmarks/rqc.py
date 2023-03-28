import time
from qiskit.circuit import QuantumCircuit

from qiskit.compiler import transpile

from qdao.test import QdaoBaseTest
from qdao.engine import Engine

from utils.misc import profile

TEST_BASE = QdaoBaseTest()


@profile
def run_base(circ: QuantumCircuit):
    TEST_BASE._sv_sim.run(circ)

@profile
def run_qdao(circ: QuantumCircuit):
    eng = Engine(circuit=circ, num_primary=circ.num_qubits-2, num_local=20)
    eng.run()

def main():
    circ = TEST_BASE.get_small_bench_circ("random", num_qubits=30, depth=10, measure=False)
    circ = transpile(circ, TEST_BASE._sv_sim)

    run_base(circ)

    run_qdao(circ)



if __name__ == '__main__':
    main()
