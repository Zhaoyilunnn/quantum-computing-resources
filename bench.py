import argparse
import json
import logging

from qiskit_aer.noise import NoiseModel

from util import *
from reorder import Reorder
from noise import Noise
from qiskit import *
from qiskit.circuit.random import random_circuit
from qiskit.providers import provider


# Logging configuration
logging.basicConfig(filename='bench.log', encoding='utf-8', level=logging.DEBUG,
                format='%(asctime)s %(message)s')


#IBMQ.save_account("036d2bca315b21dc9525cd05217943de9eab08326f37d652ac23aed075ea3e32ea3a983602b728e1b7c3e5e2a157959dcd0b834eb34ce607b3ec1d6401e9594d", overwrite=True)
DEVICE_LIST = ['ibm_oslo', 'ibmq_manila', 'ibm_nairobi', 'ibmq_quito', 'ibmq_belem', 'ibmq_lima']
provider = IBMQ.load_account()

#### For json format
# sort_keys=True, indent=4, separators=(',', ':')
#### For json format


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--fusion', type=int, default=0, help='Whether enable fusion (Default: 0)')
    parser.add_argument('--num-qubits', type=int, default=10, help='Number of qubits (Default: 10)')
    parser.add_argument('--backend', type=str, default='aer_simulator', help='Execution environment," \
            " if set to IBM device name, [ibm_oslo, ibmq_manila, ibm_nairobi, ibmq_quito, ibmq_belem, ibmq_lima]" \
            " use real device (Default: aer_simulator)')
    parser.add_argument('--mode', type=str, default='qasm', help='How to construct a circuit, qasm | random | analysis (Default: qasm)')
    parser.add_argument('--qasm-file', type=str, default='', help='The qasm file path Default: empty')
    parser.add_argument('--depth', type=int, default=10, help='Depth of a circuit (Default: 10)')
    parser.add_argument('--run', type=int, default=1, help='Whether run experiments (Default: 1)')
    parser.add_argument('--analysis', type=int, default=0, help='Whether perform static circuit analysis, (Default: 0)')
    parser.add_argument('--save-qobj', type=int, default=0, help='Whether save qobj file(analysis==1), (Default: 0)')
    parser.add_argument('--qobj-file', type=str, default='qobj', help='qobj file path(analysis==1 && save_qobj==1), (Default: qobj)')
    parser.add_argument('--local-qubits', type=int, default=10, help='Max qubits within a cluster. (analysis==1), (Default: 10)')
    parser.add_argument('--draw-circ', type=int, default=0, help='Whether print circuit diagram. (analysis==1), (Default: 0)')
    parser.add_argument('--reorder-method', type=str, default="static-new-local", help="Method for reordering (clustering), (Default: static-new-local)")
    parser.add_argument('--nl', type=int, default=2, help="Number of local qubits (reorder_method=static-new-local), (Default: 2)")
    parser.add_argument('--noise', type=str, default='depolarizing', help="Noise model name, if this is set to IBM device name,"\
            " use noise model from the deivice, (Default: depolarizing)")
    return parser.parse_args()


# TODO: Make is_complete_prog optional from command line
def do_analysis(qobj_dict,
        local_qubits=10,
        save_qobj=False,
        qobj_file=None,
        reorder_method="static-new-local",
        nl=2, is_complete_prog=True):

    if save_qobj:
        if qobj_file is None:
            raise ValueError("Set qobj file name when save_qobj is True!")
        with open(qobj_file, 'w') as f:
            f.write(json.dumps(qobj_dict, sort_keys=True, indent=4, separators=(',', ':')))

    op_lists = get_op_lists(qobj_dict) 
    reorder = Reorder.get_reorder(reorder_method)
    reorder.local_qubits = local_qubits

    if reorder_method == "static-new-local":
        reorder.custom_local_qubits = nl

    for op_list in op_lists:
        print_op_list(op_list)
        if not is_complete_prog:
            op_list = get_op_list_without_measure(op_list) 
        print("Num ops before: {}".format(len(op_list)))
        reorder.run(op_list)
        reorder.print_res()


def analysis(qobj, 
        local_qubits=10, 
        save_qobj=False, 
        qobj_file=None,
        reorder_method='static-new-local',
        nl=2):
    qobj_dict = qobj.to_dict()
    do_analysis(qobj_dict, 
            local_qubits=local_qubits,
            save_qobj=save_qobj,
            qobj_file=qobj_file,
            reorder_method=reorder_method,
            nl=2)


def construct_circuit(args):
    circ = None
    if args.mode == 'qasm':
        if not args.qasm_file:
            raise Exception("Should set the qasm file path when using qasm mode")
        circ = QuantumCircuit().from_qasm_file(args.qasm_file)
    elif args.mode == 'random':
        num_qubits = int(args.num_qubits)
        depth = int(args.depth)
        circ = random_circuit(num_qubits, depth, measure=True)
    return circ


def run_circ(args, circ):
    logging.info('Running!!NoiseModel:%s, Backend:%s', args.noise, args.backend)
    noise_model = None
    coupling_map = None
    basis_gates = None
    backend = None # The execution engine
    if args.noise in DEVICE_LIST:
        # The noise name is the same as the device name
        # Now use noise model from real-device
        device = provider.get_backend(args.noise)
        noise_model = NoiseModel.from_backend(device)
        coupling_map = device.configuration().coupling_map
        basis_gates = noise_model.basis_gates
    else:
        noise_model = Noise.get_noise_model(args.noise) 
    print(noise_model, coupling_map, basis_gates)

    if args.backend in DEVICE_LIST:
        backend = provider.get_backend(args.backend)
    else:
        backend = Aer.get_backend(args.backend)
        backend.set_options(fusion_enable=(False if args.fusion == 0 else True))
    test = transpile(circ, backend, coupling_map=coupling_map,
            basis_gates=basis_gates)
    qobj = assemble(test)

    if args.analysis == 1:
        if args.draw_circ == 1:
            print(circ.draw(output='text'))
        analysis(qobj, 
                local_qubits=args.local_qubits,
                save_qobj=(False if args.save_qobj == 0 else True),
                qobj_file=args.qobj_file,
                reorder_method=args.reorder_method,
                nl=args.nl)
    
    if args.run == 1:
        run(qobj, backend, noise_model=noise_model) 


def run_analysis_only(args):
    if args.qobj_file == "":
        raise ValueError("Please provide qobj_file")
    qobj_dict = load_qobj_from_path(args.qobj_file)
    do_analysis(qobj_dict)
        

@profile
def run(qobj, backend,
        noise_model=None):
    backend.run(qobj, noise_model=noise_model)


def main():
    args = parse_args()
    
    if args.mode in ('qasm', 'random'):
        circ = construct_circuit(args)
        run_circ(args, circ)
    elif args.mode == 'analysis':
        run_analysis_only(args)
    else:
        raise NotImplementedError("Unsupported mode")
        

if __name__ == '__main__':
    main()
