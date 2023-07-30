"""Script for `sim-beta` project to generate qobj json file and analyze reorder algorithms"""

import argparse
import json
import logging
import pickle

from qiskit_aer.noise import NoiseModel

from qutils.misc import *
from reorder import Reorder
from noise import Noise
from qiskit import *
from qiskit.circuit.random import random_circuit
from qiskit.providers import Backend, BackendV1, BackendV2, provider, fake_provider
from qiskit.providers.jobstatus import JobStatus
from qiskit.providers.fake_provider import *
from qiskit.transpiler import CouplingMap

# from qvm.util import *
# from qvm.manager.backend_manager import *


# Logging configuration
logging.basicConfig(
    filename="bench.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


# IBMQ.save_account("036d2bca315b21dc9525cd05217943de9eab08326f37d652ac23aed075ea3e32ea3a983602b728e1b7c3e5e2a157959dcd0b834eb34ce607b3ec1d6401e9594d", overwrite=True)
DEVICE_LIST = [
    "ibm_oslo",
    "ibmq_manila",
    "ibm_nairobi",
    "ibmq_quito",
    "ibmq_belem",
    "ibmq_lima",
]
# provider = IBMQ.load_account()
provider = None

#### For json format
# sort_keys=True, indent=4, separators=(',', ':')
#### For json format

FAKE_BACKEND = "fake"
USE_BACKEND_NOISE = "backend"


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--fusion", type=int, default=0, help="Whether enable fusion (Default: 0)"
    )
    parser.add_argument(
        "--num-qubits", type=int, default=10, help="Number of qubits (Default: 10)"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="aer_simulator",
        help="Execution environment,"
        " if set to IBM device name, [ibm_oslo, ibmq_manila, ibm_nairobi, ibmq_quito, ibmq_belem, ibmq_lima]"
        " use real device. Can be a list (',' seperated), will execute the same circuit on each backend, "
        " if set to fake, use fake backend (Default: aer_simulator)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="qasm",
        help="How to construct a circuit, qasm | random | analysis (Default: qasm)",
    )
    parser.add_argument(
        "--qasm-file", type=str, default="", help="The qasm file path Default: empty"
    )
    parser.add_argument(
        "--depth", type=int, default=10, help="Depth of a circuit (Default: 10)"
    )
    parser.add_argument(
        "--run", type=int, default=1, help="Whether run experiments (Default: 1)"
    )
    parser.add_argument(
        "--analysis",
        type=int,
        default=0,
        help="Whether perform static circuit analysis, (Default: 0)",
    )
    parser.add_argument(
        "--save-qobj",
        type=int,
        default=0,
        help="Whether save qobj file(analysis==1), (Default: 0)",
    )
    parser.add_argument(
        "--qobj-file",
        type=str,
        default="qobj",
        help="qobj file path(analysis==1 && save_qobj==1), (Default: qobj)",
    )
    parser.add_argument(
        "--local-qubits",
        type=int,
        default=10,
        help="Max qubits within a cluster. (analysis==1), (Default: 10)",
    )
    parser.add_argument(
        "--draw-circ",
        type=int,
        default=0,
        help="Whether print circuit diagram. (Default: 0)",
    )
    parser.add_argument(
        "--reorder-method",
        type=str,
        default="static-new-local",
        help="Method for reordering (clustering), (Default: static-new-local)",
    )
    parser.add_argument(
        "--nl",
        type=int,
        default=2,
        help="Number of local qubits (reorder_method=static-new-local), (Default: 2)",
    )
    parser.add_argument(
        "--noise",
        type=str,
        default="backend",
        help="Noise model name: device_name | backend | <customized>, "
        "if this is set to IBM device name, use noise model from the deivice, (Default: backend)",
    )
    parser.add_argument(
        "--save-sv",
        dest="save_sv",
        type=int,
        default=0,
        help="Whether to save statevector, (Default 0)",
    )
    return parser.parse_args()


# TODO: Make is_complete_prog optional from command line
def do_analysis(
    qobj_dict,
    local_qubits=10,
    save_qobj=False,
    qobj_file=None,
    reorder_method="static-new-local",
    nl=2,
    is_complete_prog=True,
):
    if save_qobj:
        if qobj_file is None:
            raise ValueError("Set qobj file name when save_qobj is True!")
        with open(qobj_file, "w") as f:
            f.write(
                json.dumps(qobj_dict, sort_keys=True, indent=4, separators=(",", ":"))
            )

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


def analysis(
    qobj,
    local_qubits=10,
    save_qobj=False,
    qobj_file=None,
    reorder_method="static-new-local",
    nl=2,
):
    qobj_dict = qobj.to_dict()
    do_analysis(
        qobj_dict,
        local_qubits=local_qubits,
        save_qobj=save_qobj,
        qobj_file=qobj_file,
        reorder_method=reorder_method,
        nl=2,
    )


def construct_circuit(args):
    circ = QuantumCircuit()
    if args.mode == "qasm":
        if not args.qasm_file:
            raise Exception("Should set the qasm file path when using qasm mode")
        circ = QuantumCircuit().from_qasm_file(args.qasm_file)
    elif args.mode == "random":
        num_qubits = int(args.num_qubits)
        depth = int(args.depth)
        circ = random_circuit(num_qubits, depth, measure=True)
    return circ


def get_backend_list(args):
    backend_list = []
    backend_name_list = args.backend.split(",")
    for backend_name in backend_name_list:
        if backend_name in DEVICE_LIST:
            backend = provider.get_backend(backend_name)
        elif backend_name == FAKE_BACKEND:
            # backend = FakeWashingtonV2()
            # backend = FakeWashington()
            # backend = FakeCairo()
            backend = FakeBrooklyn()
        else:
            backend = Aer.get_backend(backend_name)
            backend.set_options(fusion_enable=(False if args.fusion == 0 else True))
        backend_list.append(backend)
    return backend_list


def run_all_backends():
    pass


def run_circ(args, circ):
    backend_list = get_backend_list(args)

    for backend in backend_list:
        coupling_map = None
        basis_gates = None
        if args.noise == USE_BACKEND_NOISE:
            # Use noise model from backend
            noise_model = NoiseModel.from_backend(backend)
            if isinstance(backend, BackendV1):
                coupling_map = backend.configuration().coupling_map
            elif isinstance(backend, BackendV2):
                coupling_map = backend.coupling_map
            else:
                raise ValueError("Unsupported backend type")
            basis_gates = noise_model.basis_gates
        elif args.noise in DEVICE_LIST:
            # Use noise model from a specific IBM device
            # Note that:
            #  If use specific device, this will override actual backend's configuration!
            noise_device = provider.get_backend(args.noise)
            noise_model = NoiseModel.from_backend(noise_device)
            coupling_map = noise_device.configuration().coupling_map
            basis_gates = noise_model.basis_gates
        else:
            noise_model = Noise.get_noise_model(args.noise)

        # logging.info('zyl-qcs-running::NoiseModel:%s, Backend:%s, CouplingMap:%s', noise_model, backend, coupling_map)
        # qobj = compile_circ(circ, backend, coupling_map, basis_gates)
        # transpiled = gate_compile(circ, backend, coupling_map, basis_gates)
        transpiled = gate_compile(circ, backend)
        print("#Inst at gate level: {}".format(len(transpiled)))
        scheduled = pulse_compile(transpiled, backend)
        print("#Inst at pulse level: {}".format(len(scheduled.instructions)))
        qobj = assemble(transpiled)
        # qobj = scheduled
        # qobj = circ
        print(
            "dt: {}, duration: {}".format(
                backend.configuration().dt, scheduled.duration
            )
        )

        if args.analysis == 1:
            analysis(
                qobj,
                local_qubits=args.local_qubits,
                save_qobj=(False if args.save_qobj == 0 else True),
                qobj_file=args.qobj_file,
                reorder_method=args.reorder_method,
                nl=args.nl,
            )

        if args.run == 1:
            run(qobj, backend, noise_model=noise_model, save_sv=args.save_sv)


@profile
def compile_circ(circ, backend, coupling_map=None, basis_gates=None):
    transpiled = transpile(
        circ, backend, coupling_map=coupling_map, basis_gates=basis_gates
    )
    scheduled = schedule(transpiled, backend)
    qobj = assemble(transpiled)
    print("dt: {}, duration: {}".format(backend.configuration().dt, scheduled.duration))
    return qobj


@profile
def gate_compile(circ, backend, coupling_map=None, basis_gates=None):
    transpiled = transpile(
        circ, backend, coupling_map=coupling_map, basis_gates=basis_gates
    )
    return transpiled


@profile
def pulse_compile(circ, backend):
    scheduled = schedule(circ, backend)
    return scheduled


def run_analysis_only(args):
    if args.qobj_file == "":
        raise ValueError("Please provide qobj_file")
    qobj_dict = load_qobj_from_path(args.qobj_file)
    do_analysis(qobj_dict)


@profile
def run(qobj, backend, noise_model=None, save_sv=False):
    # TODO: `noise_model` is not an option for IBMQ and will be ignored
    #       Be careful if version changed
    job = backend.run(qobj, noise_model=noise_model)
    if backend.name() in DEVICE_LIST:
        return
    # if job.status() is not JobStatus.DONE:
    #    print("Job is running")
    counts = job.result().get_counts()
    # print(counts)

    if save_sv:
        sv = job.result().get_statevector(0)
        with open("temp.txt", "wb") as fw:
            pickle.dump(sv.data.tolist()[1:2], fw)


def main():
    args = parse_args()

    if args.mode in ("qasm", "random"):
        circ = construct_circuit(args)
        if args.draw_circ == 1:
            print(circ.draw(output="text"))
        run_circ(args, circ)
    elif args.mode == "analysis":
        run_analysis_only(args)
    else:
        raise NotImplementedError("Unsupported mode")


if __name__ == "__main__":
    main()
