import sys
sys.path.insert(0, "../../../")

from qiskit import QuantumCircuit, QuantumRegister, \
                Aer, assemble, transpile
from math import pi
import json

from qiskit.result import result
from reorder import Reorder 
from bench import get_op_lists, get_op_list_without_measure


def gen_unitary():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi, 0.5, 0.5, q[0])
    qc.u(pi, 0.2, 0.3, q[1])
    qc.u(pi, 0.5, 0.5, q[2])
    qc.u(pi, 0.5, 0.5, q[3])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    print(outputstate.data.tolist())
    #with open("../data/unitary_res.json", "w") as f:
    #    f.write(json.dumps(outputstate.data.tolist()))


def gen_unitary_new():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[3])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_new.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    print(outputstate.data.tolist())


def gen_unitary_complete():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[3])
    qc.u(pi/2, 1.5, 0.5, q[4])
    qc.u(pi/2, 1.5, 0.5, q[5])
    qc.u(pi/2, 1.5, 0.5, q[4])
    qc.u(pi/2, 1.5, 0.5, q[2])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_complete.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    print(outputstate.data.tolist())
    reo = Reorder.get_reorder('static-new')
    reo.local_qubits = 4
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    with open("../data/unitary_complete_inst.json", "w") as f:
        f.write(json.dumps(reo.result, sort_keys=True, indent=4, separators=(',', ':')))
    #with open("../data/unitary_res.json", "w") as f:
    #    f.write(json.dumps(outputstate.data.tolist()))
    

def main():
    gen_unitary()
    gen_unitary_new()
    gen_unitary_complete()


if __name__ == '__main__':
    main()
