import sys
import time
sys.path.append('.')

from qiskit.circuit import QuantumCircuit
from qiskit_aer import Aer
from qutils.misc import profile


#@profile(t=2)
def main(qasm_file: str):
    sim = Aer.get_backend('aer_simulator')
    #sim.set_options(fusion_enable=False)
    sim.set_options(fusion_max_qubit=2)
    circ = QuantumCircuit.from_qasm_file(qasm_file)
    circ.save_state()
    sim.run(circ)


if __name__ == '__main__':
    qasm_file = sys.argv[1]
    start = time.time()
    main(qasm_file)
    print(f"consume::{time.time() - start}")
