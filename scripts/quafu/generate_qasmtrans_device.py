from collections import OrderedDict
from quafu import Task, User
import sys
import random
import json


version = "0.1"


def generate_config(backend_name, chip_info):

    mapping = chip_info["mapping"]
    mapping_reversed = {v: k for k, v in mapping.items()}
    num_qubits = len(mapping)
    full_info = chip_info["full_info"]

    config = OrderedDict()

    config['name'] = backend_name
    config['version']  = version
    config['num_qubits'] = num_qubits

    two_qubits_gate = "cx"

    config['basis_gates'] = ["cz", "rx", "ry", "rz", "h"]

    config["T1"] = OrderedDict()
    config["T2"] = OrderedDict()
    config["freq"] = OrderedDict()
    config["readout_length"] = OrderedDict()
    config["prob_meas0_prep1"] = OrderedDict()
    config["prob_meas1_prep0"] = OrderedDict()
    config["gate_lens"] = OrderedDict()
    config["gate_errs"] = OrderedDict()
    for i in range(int(num_qubits)):
        config["T1"][str(i)] = random.uniform(0, 0.00001)
        config["T2"][str(i)] = random.uniform(0, 0.00001)
        config["freq"][str(i)] = random.uniform(5000000000, 5300000000)
        config["readout_length"][str(i)] = random.uniform(0,0.0000006)
        config["prob_meas0_prep1"][str(i)] = random.uniform(0,0.1)
        config["prob_meas1_prep0"][str(i)] = random.uniform(0,0.1)
        for gate in config['basis_gates']:
            if gate != two_qubits_gate:
                config["gate_lens"][gate+str(i)] = random.uniform(0,0.00000001)
                config["gate_errs"][gate+str(i)] = random.uniform(0,0.00000001)
        config["gate_lens"]["reset"+str(i)] = random.uniform(0,0.00000001)
        config["gate_errs"]["reset"+str(i)] = random.uniform(0,0.00000001)

    config[two_qubits_gate+"_coupling"] = []
    for link in full_info["topological_structure"]:
        qubits = link.split("_")
        assert len(qubits) == 2
        i, j = mapping_reversed[qubits[0]], mapping_reversed[qubits[1]]
        if i != j:
            config["gate_lens"][two_qubits_gate+str(i)+"_"+str(j)] = random.uniform(0,0.00000001)
            config["gate_errs"][two_qubits_gate+str(i)+"_"+str(j)] = random.uniform(0,0.00000001)
            config[two_qubits_gate+"_coupling"].append(str(i)+"_"+str(j))

    with open('quafu'+"_"+backend_name + '.json', 'w') as outfile:
        json.dump(config, outfile)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <backend-name>")
        sys.exit(1)

    backend_name = sys.argv[1]
    user = User()
    backends = user.get_available_backends()
    chip_info = backends[backend_name].get_chip_info()
    generate_config(backend_name, chip_info)


if __name__ == '__main__':
    main()
