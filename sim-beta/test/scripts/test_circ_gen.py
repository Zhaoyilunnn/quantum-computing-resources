from qiskit import QuantumCircuit, QuantumRegister, \
                Aer, assemble, transpile
from math import pi
import json

from qiskit.result import result


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
    

def main():
    gen_unitary()


if __name__ == '__main__':
    main()
