from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector

import sys
import quafu


def main():
    if len(sys.argv) != 2:
        print("Compare quafu simulation result with qiskit")
        print(f"Usage: python {sys.argv[0]} <qasm_file>")
        sys.exit(1)

    sim = Aer.get_backend("aer_simulator")
    sim.set_options(method="statevector")
    qasm = sys.argv[1]
    with open(qasm, 'r') as f:
        qasm_str = f.read()
        quafu_circ = quafu.QuantumCircuit(1)
        quafu_circ.from_openqasm(qasm_str)
        qiskit_circ = QuantumCircuit.from_qasm_str(qasm_str)
        qiskit_circ.save_state()
        sv_qiskit = sim.run(qiskit_circ).result().get_statevector()
        sv_quafu = quafu.simulate(quafu_circ, output="state_vector").get_statevector()
        print(Statevector(sv_qiskit).equiv(Statevector(sv_quafu)))


if __name__ == '__main__':
    main()
