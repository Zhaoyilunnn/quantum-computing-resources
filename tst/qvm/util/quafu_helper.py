from test.qvm import QvmBaseTest

from qvm.util.quafu_helper import (
    FakeCairo,
    extract_quafu_qubit_mapping,
    to_qiskit_backend_v1,
)
from qiskit import transpile

from quafu.users.userapi import User

user = User()
user.get_backends_info()
BACKENDS = user.get_available_backends()


class TestQuafuHelper(QvmBaseTest):
    def test_extract_quafu_qubit_mapping(self):
        mock_chip_info = {"mapping": {"0": "Q1", "1": "Q2", "2": "Q3", "3": "Q4"}}
        mapping, inv_mapping = extract_quafu_qubit_mapping(mock_chip_info)
        assert mapping == {"0": "Q1", "1": "Q2", "2": "Q3", "3": "Q4"}
        assert inv_mapping == {"Q1": "0", "Q2": "1", "Q3": "2", "Q4": "3"}

    def test_to_qiskit_backend_v1(self):
        chip_info = BACKENDS["ScQ-P10"].get_chip_info()
        backend = to_qiskit_backend_v1(chip_info)
        # Test compilation
        circ = self.get_qiskit_circ("random", num_qubits=4, depth=3)
        # trans_circ = transpile(circ, backend=FakeCairo())
        trans_circ = transpile(circ, backend=backend)
        print(trans_circ)
        print("\nCompilation on ScQ-P10 succeeded!!!!!!!!!\n")

        chip_info = BACKENDS["ScQ-P18"].get_chip_info()
        backend = to_qiskit_backend_v1(chip_info)
        # Test compilation
        trans_circ = transpile(circ, backend=backend)
        print("\nCompilation on ScQ-P18 succeeded!!!!!!!!!\n")

        chip_info = BACKENDS["ScQ-P136"].get_chip_info()
        backend = to_qiskit_backend_v1(chip_info)
        # Test compilation
        trans_circ = transpile(circ, backend=backend)
        print("\nCompilation on ScQ-P136 succeeded!!!!!!!!!\n")
