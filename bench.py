import sys
import numpy as np
from qiskit import *
from qiskit.circuit.random import random_circuit
import argparse
import json
from util import profile
from reorder import Reorder

def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--num-qubits', type=int, default=10, help='number of qubits')
    parser.add_argument('--backend', type=str, default='aer_simulator', help='simulation method')
    parser.add_argument('--mode', type=str, default='qasm', help='How to construct a circuit')
    parser.add_argument('--qasm-file', type=str, default='', help='The qasm file path')
    parser.add_argument('--depth', type=int, default=10, help='Depth of a circuit')
    parser.add_argument('--analysis', type=int, default=0, help='Whether perform static circuit analysis')
    parser.add_argument('--run', type=int, default=1, help='Whether run experiments')
    parser.add_argument('--fusion', type=int, default=0, help='Whether enable fusion')
    parser.add_argument('--local-qubits', type=int, default=10, help='Max qubits within a cluster')
    return parser.parse_args()

def get_op_list(qobj_dict):
    """
    Get operation list from Qobj
    """
    op_lists = []
    try:
        exps = qobj_dict["experiments"]
        for exp_id, exp in enumerate(exps):
            op_list = exp["instructions"]
            op_lists.append(op_list)
    except Exception:
        print("Error processing qobj dictionary: no instructions!")
        sys.exit(1)
    return op_lists

def get_n_qubits(qobj_dict):
    n_qubits = None
    try:
        n_qubits = qobj_dict["config"]["n_qubits"]
    except KeyError:
        print("Error processing qobj dictionary: no n_qubits!")
        sys.exit(1)
    return n_qubits

def print_qobj(qobj):
    qobj_dict = qobj.to_dict()
    qobj_json = json.dumps(qobj_dict, sort_keys=True, indent=4, separators=(',', ':'))
    print(qobj_json)

def analysis(qobj, local_qubits=10):
    qobj_dict = qobj.to_dict()
    op_lists = get_op_list(qobj_dict) 
    n_qubits = get_n_qubits(qobj_dict)
    reorder = Reorder.get_reorder('static')
    reorder.local_qubits = local_qubits
    for op_list in op_lists:
        print(json.dumps(op_list, sort_keys=True, indent=4, separators=(',', ':')))
        print("Num ops before: {}".format(len(op_list)))
        reorder.run(op_list)
        result = reorder.result
        # for cluster in result["clustered_insts"]:
        #     print(cluster)
        #print(json.dumps(result["clustered_insts"], sort_keys=True, indent=4, separators=(',', ':')))
        print("Num ops after: {}".format(result["n_cluster"]))
        
#@profile
def run(qobj, backend):
    backend.run(qobj)

def main():
    args = parse_args()
    
    circ = None
    if args.mode == 'qasm':
        if not args.qasm_file:
            raise Exception("Should set the qasm file path when using qasm mode")
        circ = QuantumCircuit().from_qasm_file(args.qasm_file)
    elif args.mode == 'random':
        num_qubits = int(args.num_qubits)
        depth = int(args.depth)
        circ = random_circuit(num_qubits, depth, measure=True)
    else:
        raise NotImplementedError("Unsupported circuit constructing mode!")
        
    backend = Aer.get_backend(args.backend)
    backend.set_options(fusion_enable=(False if args.fusion == 0 else True))
    test = transpile(circ, backend)
    qobj = assemble(test)
    
    if args.analysis == 1:
        analysis(qobj, args.local_qubits)
    if args.run == 1:
        run(qobj, backend) 

if __name__ == '__main__':
    main()
