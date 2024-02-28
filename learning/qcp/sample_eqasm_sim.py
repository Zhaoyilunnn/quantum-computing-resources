import logging
import sys
import argparse
from pyqcas.quantum_coprocessor import Quantum_coprocessor


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("exe_file_name", type=str)

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_options()

    qcas = Quantum_coprocessor()
    qcas.upload_program(args.exe_file_name)
    qcas.set_log_level(log_level=logging.DEBUG)
    qcas.execute()
    result = qcas.read_result()
