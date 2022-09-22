import sys, os, psutil
import subprocess
import time

from qiskit.visualization.qcstyle import json

def profile(func):
    def wrapper(*args, **kwargs):
        pid = os.getpid()
        subprocess.Popen(["./tools/monitor_mem.sh", str(pid)])
        time_before = time.time()
        result = func(*args, **kwargs)
        time_after = time.time()
        print("{}:consumed time:\t{:,}".format(
            func.__name__,
            time_after - time_before))
        return result
    return wrapper

def get_op_lists(qobj_dict):
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

def get_op_list_without_measure(op_list):
    op_list_wo_meas = []
    for op in op_list:
        if op["name"] == "measure":
            continue
        if "qubits" not in op:
            continue
        op_list_wo_meas.append(op)
    return op_list_wo_meas

def get_n_qubits(qobj_dict):
    n_qubits = None
    try:
        n_qubits = qobj_dict["config"]["n_qubits"]
    except KeyError:
        print("Error processing qobj dictionary: no n_qubits!")
        sys.exit(1)
    return n_qubits

def print_op_list(op_list):
    for op in op_list:
        name = op["name"]
        qubits = op["qubits"]
        print("{}:{}".format(name, ','.join([str(q) for q in qubits])))

def print_qobj(qobj):
    qobj_dict = qobj.to_dict()
    qobj_json = json.dumps(qobj_dict, sort_keys=True, indent=4, separators=(',', ':'))
    print(qobj_json)

def load_qobj_from_path(qobj_path):
    qobj_dict = None
    with open(qobj_path, 'r') as fr:
        qobj_dict = json.load(fr)
    return qobj_dict 
