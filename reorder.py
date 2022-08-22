
class ReroderMethod:
    _n_local = 5
    _result = {
        "clustered_insts": [],
        "n_cluster": None
    }

    def __init__(self):
        pass        
    
    @property
    def local_qubits(self):
        return self._n_local
    
    @local_qubits.setter
    def local_qubits(self, n):
        self._n_local = n
 
    @property
    def result(self):
        return self._result
    
    @staticmethod
    def get_op_name(op):
        return op["name"]

    @staticmethod
    def get_op_qubits(op):
        return op["qubits"]

    def run(self, op_list):
        pass

class StaticReorder(ReroderMethod):
    """ 
    Simply traverse op list 
    Continues ops that reach the limit of local qubits form a cluster
    """

    def __init__(self):
        super().__init__()

    def run(self, op_list):
        local_qubit_set = set()
        local_inst_list = []
        for op in op_list:
            q_list = self.get_op_qubits(op)
            n_new = 0
            for q in q_list:
                if q not in local_qubit_set:
                    n_new += 1
            if n_new + len(local_qubit_set) > self._n_local:
                # Form a cluster
                local_qubit_set.clear()
                self._result["clustered_insts"].append(local_inst_list)
                local_inst_list = [] # Create a new list to store new cluster
            local_inst_list.append(op)
            for q in q_list:
                local_qubit_set.add(q)     
        self._result["clustered_insts"].append(local_inst_list)
        self._result["n_cluster"] = len(self._result["clustered_insts"]) 
    

class ReorderProvidor:
    _REORDERS = {
        'static': StaticReorder
    }
    
    def get_reorder(self, method_name):
        return self._REORDERS[method_name]()


Reorder = ReorderProvidor()
