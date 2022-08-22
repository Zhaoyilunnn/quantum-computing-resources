from reorder import Reorder

test_input = [{"name": "u2", "params": [1.8661487719578789, 0.9139730132963093], "qubits": [2]}, {"name": "ccx", "qubits": [0, 3, 1]}, {"name": "ccx", "qubits": [3, 1, 0]}, {"name": "cswap", "qubits": [0, 3, 2]}, {"name": "rz", "params": [3.7076558050008965], "qubits": [0]}, {"name": "u1", "params": [-2.3561944901923457], "qubits": [1]}, {"name": "cu1", "params": [3.3698812961910276], "qubits": [2, 3]}, {"name": "u3", "params": [2.2241824136041903, 1.9155819994517396, 1.9208439411554306], "qubits": [2]}, {"name": "cswap", "qubits": [3, 0, 1]}]
test_output = [[{"name": "u2", "params": [1.8661487719578789, 0.9139730132963093], "qubits": [2]}], [{"name": "ccx", "qubits": [0, 3, 1]}, {"name": "ccx", "qubits": [3, 1, 0]}], [{"name": "cswap", "qubits": [0, 3, 2]}, {"name": "rz", "params": [3.7076558050008965], "qubits": [0]}], [{"name": "u1", "params": [-2.3561944901923457], "qubits": [1]}, {"name": "cu1", "params": [3.3698812961910276], "qubits": [2, 3]}, {"name": "u3", "params": [2.2241824136041903, 1.9155819994517396, 1.9208439411554306], "qubits": [2]}], [{"name": "cswap", "qubits": [3, 0, 1]}]]  

class TestReorder:

    def test_run(self):
        reo = Reorder.get_reorder("static")
        reo.local_qubits = 3
        reo.run(test_input)
        result = reo.result
        print(result["clustered_insts"])
        assert result["clustered_insts"] == test_output
        
