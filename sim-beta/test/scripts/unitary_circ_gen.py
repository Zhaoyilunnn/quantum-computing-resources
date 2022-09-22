import sys

from qiskit.circuit.parameterexpression import numpy
sys.path.insert(0, "../../../")

from qiskit import QuantumCircuit, QuantumRegister, \
                Aer, assemble, transpile
from math import pi
import json

from reorder import Reorder 
from bench import get_op_lists, get_op_list_without_measure


def gen_qobj_file(qc, qobj_name, qobj_inst_name):
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open(qobj_name, 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    #print(outputstate.data.tolist())
    for d in outputstate.data.tolist():
        print(numpy.real(d))
    reo = Reorder.get_reorder('static-new')
    reo.local_qubits = 4
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    with open(qobj_inst_name, "w") as f:
        f.write(json.dumps(reo.result, sort_keys=True, indent=4, separators=(',', ':')))



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


def gen_unitary_irregular():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 1.5, 0.5, q[4])
    qc.u(pi/2, 1.5, 0.5, q[5])
    qc.u(pi/2, 1.5, 0.5, q[4])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_irregular.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    print(outputstate.data.tolist())


def gen_unitary_irregular_tiny():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 1.5, 0.5, q[4])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_irregular_tiny.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    print(outputstate.data.tolist())


def gen_unitary_irregular_tiny_2():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 1.5, 0.5, q[4])
    qc.u(pi/2, 1.5, 0.5, q[5])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_irregular_tiny_2.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    print(outputstate.data.tolist())

def gen_unitary_irregular_tiny_3():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[3])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_irregular_tiny_3.json", 'w') as f:
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
    gen_qobj_file(qc, "../data/unitary_complete.json", "../data/unitary_complete_inst.json")


def gen_unitary_u3_test():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(1.1415926535897933, 3.0707963267948966, 2.0707963267948966, q[0])
    gen_qobj_file(qc, "../data/unitary_u3_test.json", "../data/unitary_u3_test_inst.json")

    

def gen_unitary_complete_new():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[3])
    qc.u(pi/2, 1.5, 0.5, q[4])
    qc.u(pi/2, 1.5, 0.5, q[5])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_complete_new.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    print(outputstate.data.tolist())
    #for d in outputstate.data.tolist():
    #    print(numpy.real(d))
    reo = Reorder.get_reorder('static-new')
    reo.local_qubits = 4
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    with open("../data/unitary_complete_new_inst.json", "w") as f:
        f.write(json.dumps(reo.result, sort_keys=True, indent=4, separators=(',', ':')))
    #with open("../data/unitary_res.json", "w") as f:
    #    f.write(json.dumps(outputstate.data.tolist()))


def gen_unitary_complete_new_1():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[3])
    qc.u(pi/2, 1.5, 0.5, q[5])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_complete_new_1.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    #print(outputstate.data.tolist())
    #for d in outputstate.data.tolist():
    #    print(numpy.real(d))
    reo = Reorder.get_reorder('static-new')
    reo.local_qubits = 4
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    with open("../data/unitary_complete_new_1_inst.json", "w") as f:
        f.write(json.dumps(reo.result, sort_keys=True, indent=4, separators=(',', ':')))
    #with open("../data/unitary_res.json", "w") as f:
    #    f.write(json.dumps(outputstate.data.tolist()))


def gen_unitary_complete_new_2():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[3])
    qc.u(pi/2, 1.5, 0.5, q[4])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_complete_new_2.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    #print(outputstate.data.tolist())
    #for d in outputstate.data.tolist():
    #    print(numpy.real(d))
    reo = Reorder.get_reorder('static-new')
    reo.local_qubits = 4
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    with open("../data/unitary_complete_new_2_inst.json", "w") as f:
        f.write(json.dumps(reo.result, sort_keys=True, indent=4, separators=(',', ':')))
    #with open("../data/unitary_res.json", "w") as f:
    #    f.write(json.dumps(outputstate.data.tolist()))


def gen_unitary_complete_new_3():
    q = QuantumRegister(6)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(1.1415926535897933, 3.0707963267948966, 2.0707963267948966, q[2])
    qc.u(pi/2, 1.5, 0.5, q[3])
    qc.u(1.1415926535897933, 3.0707963267948966, 2.0707963267948966, q[4])
    qc.u(pi/2, 1.5, 0.5, q[5])
    gen_qobj_file(qc, "../data/unitary_complete_new_3.json", "../data/unitary_complete_new_3_inst.json")


def gen_unitary_large():
    q = QuantumRegister(10)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(pi/2, 1.5, 0.5, q[3])
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[4])
    qc.u(pi/2, 0.2, 0.3, q[5])
    qc.u(pi/2, 0.2, 0.3, q[6])
    qc.u(pi/2, 0.2, 0.3, q[7])
    qc.u(pi/2, 0.2, 0.3, q[9])
    qc.u(pi/2, 0.2, 3.5, q[8])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_large.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    #print(outputstate.data.tolist())
    for d in outputstate.data.tolist():
        print(numpy.real(d))
    print(qc.draw(output='text'))
    reo = Reorder.get_reorder('static-new')
    reo.local_qubits = 8
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    with open("../data/unitary_large_inst.json", "w") as f:
        f.write(json.dumps(reo.result, sort_keys=True, indent=4, separators=(',', ':')))
    #with open("../data/unitary_res.json", "w") as f:
    #    f.write(json.dumps(outputstate.data.tolist()))

def gen_unitary_large_2():
    q = QuantumRegister(20)
    qc = QuantumCircuit(q)
    qc.u(pi/2, 0.5, 0.5, q[0])
    qc.u(pi/2, 0.2, 0.3, q[1])
    qc.u(pi/2, 1.5, 0.5, q[3])
    qc.u(pi/2, 1.5, 0.5, q[2])
    qc.u(pi/2, 1.5, 0.5, q[4])
    qc.u(pi/2, 0.2, 0.3, q[5])
    qc.u(pi/2, 0.2, 0.3, q[6])
    qc.u(pi/2, 0.2, 0.3, q[7])
    qc.u(pi/2, 0.2, 0.3, q[9])
    qc.u(pi/2, 0.2, 3.5, q[8])
    qc.u(pi/2, 2.0, 3.5, q[10])
    qc.u(pi/2, 0.2, 3.5, q[11])
    qc.u(pi/2, 0.2, 3.5, q[12])
    qc.u(pi/2, 0.2, 3.5, q[13])
    qc.u(pi/2, 1.2, 3.5, q[14])
    qc.u(pi/2, 0.2, 3.5, q[15])
    qc.u(pi/2, 0.2, 3.5, q[16])
    qc.u(pi/2, 0.2, 3.0, q[17])
    qc.u(pi/2, 0.2, 3.5, q[19])
    qc.u(pi/2, 0.2, 3.5, q[18])
    backend = Aer.get_backend("statevector_simulator")
    test = transpile(qc, backend)
    qobj = assemble(test)
    job = backend.run(qobj)
    outputstate = job.result().get_statevector(qc)
    with open("../data/unitary_large_2.json", 'w') as f:
        f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    #print(outputstate.data.tolist())
    #for d in outputstate.data.tolist():
    #    print(numpy.real(d))
    print(qc.draw(output='text'))
    reo = Reorder.get_reorder('static-new')
    reo.local_qubits = 18
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    with open("../data/unitary_large_2_inst.json", "w") as f:
        f.write(json.dumps(reo.result, sort_keys=True, indent=4, separators=(',', ':')))
    #with open("../data/unitary_res.json", "w") as f:
    #    f.write(json.dumps(outputstate.data.tolist()))


def main():
    #gen_unitary()
    #gen_unitary_new()
    #gen_unitary_irregular()
    #gen_unitary_irregular_tiny()
    #gen_unitary_irregular_tiny_2()
    #gen_unitary_irregular_tiny_3()
    #gen_unitary_complete()
    #gen_unitary_u3_test()
    #gen_unitary_complete_new()
    #gen_unitary_complete_new_1()
    #gen_unitary_complete_new_2()
    gen_unitary_complete_new_3()
    #gen_unitary_large()
    #gen_unitary_large_2()


if __name__ == '__main__':
    main()