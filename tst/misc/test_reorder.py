from reorder import Reorder
from bench import get_op_list_without_measure, get_op_lists
import json

test_input = [{"name": "u2", "params": [1.8661487719578789, 0.9139730132963093], "qubits": [2]}, {"name": "ccx", "qubits": [0, 3, 1]}, {"name": "ccx", "qubits": [3, 1, 0]}, {"name": "cswap", "qubits": [0, 3, 2]}, {"name": "rz", "params": [3.7076558050008965], "qubits": [0]}, {"name": "u1", "params": [-2.3561944901923457], "qubits": [1]}, {"name": "cu1", "params": [3.3698812961910276], "qubits": [2, 3]}, {"name": "u3", "params": [2.2241824136041903, 1.9155819994517396, 1.9208439411554306], "qubits": [2]}, {"name": "cswap", "qubits": [3, 0, 1]}]
test_output = [[{"name": "u2", "params": [1.8661487719578789, 0.9139730132963093], "qubits": [2]}], [{"name": "ccx", "qubits": [0, 3, 1]}, {"name": "ccx", "qubits": [3, 1, 0]}], [{"name": "cswap", "qubits": [0, 3, 2]}, {"name": "rz", "params": [3.7076558050008965], "qubits": [0]}], [{"name": "u1", "params": [-2.3561944901923457], "qubits": [1]}, {"name": "cu1", "params": [3.3698812961910276], "qubits": [2, 3]}, {"name": "u3", "params": [2.2241824136041903, 1.9155819994517396, 1.9208439411554306], "qubits": [2]}], [{"name": "cswap", "qubits": [3, 0, 1]}]]

CASE_STATIC_LOCAL = "test_data/archive/random.6.qobj.json"

class TestReorder:

    def test_run(self):
        reo = Reorder.get_reorder("static")
        reo.local_qubits = 3
        reo.run(test_input)
        result = reo.result
        assert result["clustered_insts"] == test_output

    def test_run_reorder_local(self):
        reo = Reorder.get_reorder("static-new-local")
        test_qobj = None
        with open(CASE_STATIC_LOCAL, "r") as fr:
            test_qobj = json.load(fr)
        op_lists = get_op_lists(test_qobj)
        test_input = get_op_list_without_measure(op_lists[0])
        reo.custom_local_qubits = 2
        reo.local_qubits = 4
        reo.run(test_input)
        res = reo.result
        assert res[0]["instructions"][0]["qubits"] == [1]
        assert res[0]["instructions"][1]["qubits"] == [3]
        assert res[0]["instructions"][2]["qubits"] == [3,1]
        assert res[0]["instructions"][3]["qubits"] == [1]
        assert res[1]["instructions"][0]["qubits"] == [4,2]
        assert res[1]["instructions"][1]["qubits"] == [4]
        assert res[2]["instructions"][0]["qubits"] == [0,5]
        assert res[2]["instructions"][1]["qubits"] == [0,2]
        assert res[2]["instructions"][2]["qubits"] == [5]
