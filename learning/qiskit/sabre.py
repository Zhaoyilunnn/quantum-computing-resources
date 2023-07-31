import sys
from qiskit import QuantumCircuit
from qiskit.converters.circuit_to_dag import circuit_to_dag
from qiskit.dagcircuit import DAGCircuit
from qiskit.transpiler.passes.routing import SabreSwap
from qiskit.circuit.random.utils import random_circuit
from qiskit.providers.fake_provider import FakeCairo
from qiskit.transpiler import CouplingMap

if len(sys.argv) != 2:
    print("test SABRE mapping and routing algorithm")
    print(f"Usage: python {sys.argv[0]} <qasm>")
    sys.exit(1)

qasm = sys.argv[1]


circ = random_circuit(4, 4, max_operands=2)
# circ = QuantumCircuit.from_qasm_file(qasm)
backend = FakeCairo()
c_map = backend.configuration().coupling_map
c_map = CouplingMap(c_map)

sabre = SabreSwap(c_map)
dag = circuit_to_dag(circ)
dag.draw(filename="input.svg")

dag = sabre.run(dag)
dag.draw(filename="output.svg")
