import sys

from qiskit.circuit.parameterexpression import numpy
sys.path.insert(0, "../../../")

from qiskit import QuantumCircuit, QuantumRegister, \
                Aer, assemble, transpile
from math import pi
import json
import random
import argparse

from reorder import Reorder 
from bench import get_op_lists, get_op_list_without_measure

def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--nq', type=int, default=10, help='Number of qubits')
    parser.add_argument('--d', type=int, default=5, help='Depth')
    parser.add_argument('--rm', type=str, default="static-new-local", help="Reorder method")
    parser.add_argument('--np', type=str, default="4", help="Number of primary_qubits ")
    parser.add_argument('--nl', type=str, default="2", help="Number of local qubits, can be a list "\
            " and will generate qobj for each (reorder_method=static-new-local)")
    parser.add_argument('--tp', type=int, default=0, help="Whether to transpile")
    parser.add_argument('--pr', type=int, default=0, help="Whether to print sv real part")
    return parser.parse_args()


def gen_qobj_file(qc, qobj_name, qobj_inst_name, 
            reorder_method="static-new", 
            primary_qubits=4, local_qubits=2, 
            is_transpile=False, 
            is_print=False, 
            save_org_qobj_file=False,
            is_run=False):
    backend = Aer.get_backend("statevector_simulator")
    test = qc
    if is_transpile:
        test = transpile(qc, backend)
    qobj = assemble(test)
    if save_org_qobj_file:
        with open(qobj_name, 'w') as f:
            f.write(json.dumps(qobj.to_dict(), sort_keys=True, indent=4, separators=(',', ':')))
    
    if is_run:
        job = backend.run(qobj)
        outputstate = job.result().get_statevector(qc)
        if is_print:
            for d in outputstate.data.tolist():
                print(numpy.real(d))

    reo = Reorder.get_reorder(reorder_method)
    reo.local_qubits = primary_qubits
    if reorder_method == "static-new-local":
        reo.custom_local_qubits = local_qubits
    op_list = get_op_list_without_measure(get_op_lists(qobj.to_dict())[0]) 
    reo.run(op_list)
    reo.print_res()
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


def gen_random_unitary(num_qubits, depth=5, 
                    reorder_method="static-new-local", 
                    primary_qubits_list=[4],
                    local_qubits_list=[2]):
    """
    Generate a random circuit which contain only unitary single qubit gates
    """
    q = QuantumRegister(num_qubits)
    qc = QuantumCircuit(q)
    for _ in range(depth):
        for _ in range(num_qubits):
            qid = random.randint(0, num_qubits-1) 
            phi = random.random()
            lAmbda = random.random()
            qc.u(pi/2, phi, lAmbda, q[qid])

    for np in primary_qubits_list:
        for nl in local_qubits_list:
            gen_qobj_file(qc, 
                    "../data/unitary_random_{}.json".format(num_qubits),
                    "../data/unitary_random_{}_{}_{}_inst.json".format(
                                    num_qubits, np, nl),
                    reorder_method=reorder_method,
                    primary_qubits=np,
                    local_qubits=nl)


# ================= TODO: Legacy code to delete =================
#def main():
#    #gen_unitary()
#    #gen_unitary_new()
#    #gen_unitary_irregular()
#    #gen_unitary_irregular_tiny()
#    #gen_unitary_irregular_tiny_2()
#    #gen_unitary_irregular_tiny_3()
#    #gen_unitary_complete()
#    #gen_unitary_u3_test()
#    #gen_unitary_complete_new()
#    #gen_unitary_complete_new_1()
#    #gen_unitary_complete_new_2()
#    #gen_unitary_complete_new_3()
#    #gen_unitary_large()
#    #gen_unitary_large_2()
# ================= TODO: Legacy code to delete =================


def main():
    args = parse_args()
    num_qubits = args.nq
    depth = args.d
    reorder_method = args.rm

    num_local_list = [int(nlocal) for nlocal in args.nl.split(",")]
    num_primary_list = [int(nprimary) for nprimary in args.np.split(",")]
    gen_random_unitary(num_qubits, depth=depth, 
            reorder_method=reorder_method, 
            primary_qubits_list=num_primary_list,
            local_qubits_list=num_local_list)


if __name__ == '__main__':
    main()
