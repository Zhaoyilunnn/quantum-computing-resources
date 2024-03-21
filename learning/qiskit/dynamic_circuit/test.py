from qiskit import QuantumCircuit, schedule, transpile
from qiskit.providers.fake_provider import FakeWashington

import argparse

from qiskit.pulse import Schedule


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("qasm_file", type=str, help="File path of OpenQASM3 benchmark file")

    return parser.parse_args()


def num_condition_ops(circ: QuantumCircuit):
    """Get the number of operations that is conditioned on classical bits"""
    num_cond_ops = 0
    for i in range(len(circ.data)):
        op = circ.data[i].operation
        if op.condition:
            num_cond_ops += 1
    return num_cond_ops



def main():
    args = parse_args()
    # For OpenQASM2
    circ = QuantumCircuit.from_qasm_file(args.qasm_file)
    # circ = qasm3.load(args.qasm_file)

    # backend = Fake127QPulseV1()
    backend = FakeWashington()
    transpiled_circ = transpile(circ, backend=backend)
    scheduled_pulses = schedule(transpiled_circ, backend=backend)

    print(f"\n------------------ Original Circuit ------------------\n")
    print(circ)
    print(f"\n------------------ Transpiled Circuit ------------------\n")
    print(transpiled_circ)
    print(f"\n------------------ Transpiled QASM ------------------\n")
    #print(qasm2.dumps(transpiled_circ))
    print(transpiled_circ.qasm())
    print(f"\n------------------ Duration ------------------\n")
    assert isinstance(scheduled_pulses, Schedule)
    print(f"dt:\t{backend.configuration().dt}\tduration:\t{scheduled_pulses.duration}")
    print(f"\n------------------ Number of conditioned operations ------------------\n")
    print(f"num-of-cond-ops:\t{num_condition_ops(transpiled_circ)}")



if __name__ == '__main__':
    main()
