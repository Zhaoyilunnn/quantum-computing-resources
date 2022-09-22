import sys
from util import print_op_list

class ReorderMethod:
    _n_primary = 5
    _result = {
        "clustered_insts": [],
        "n_cluster": None
    }

    def __init__(self):
        pass        
    
    @property
    def local_qubits(self):
        return self._n_primary
    
    @local_qubits.setter
    def local_qubits(self, n):
        self._n_primary = n
 
    @property
    def result(self):
        return self._result
    
    @staticmethod
    def get_op_name(op):
        return op["name"]

    @staticmethod
    def get_op_qubits(op):
        try:
            return op["qubits"]
        except KeyError:
            print(op)
            sys.exit(1)

    def run(self, op_list):
        pass

    def print_res(self):
        pass

class StaticReorder(ReorderMethod):
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
            if n_new + len(local_qubit_set) > self._n_primary:
                # Form a cluster
                local_qubit_set.clear()
                self._result["clustered_insts"].append(local_inst_list)
                local_inst_list = [] # Create a new list to store new cluster
            local_inst_list.append(op)
            for q in q_list:
                local_qubit_set.add(q)     
        self._result["clustered_insts"].append(local_inst_list)
        self._result["n_cluster"] = len(self._result["clustered_insts"]) 
    
    def print_res(self):
        for cluster in self._result["clustered_insts"]:
            print('-------------------------')
            print_op_list(cluster)
        print("Num ops after: {}".format(self._result["n_cluster"]))
        
    

class StaticReorderNew(ReorderMethod):
    """ 
    Simply traverse op list 
    Continues ops that reach the limit of local qubits form a cluster
    """

    def __init__(self):
        super().__init__()
        self._result = []

    def num_cluster(self):
        return self._n_primary

    def get_num_new_qubits(self, op_qubit_list, qubit_set):
        """ 
        Get the number of qubits that are not in set
        """
        num_new_qubits = 0
        for q in op_qubit_list:
            if q not in qubit_set:
                num_new_qubits += 1
        return num_new_qubits

    def is_cluster_limit_reached(self, new_qubits, qubit_set):
        """ Check if we need to move to another cluster """
        return new_qubits + len(qubit_set) > self.num_cluster()

    def run(self, op_list):
        cluster_qubit_set = set()
        cluster_inst_list = {"instructions": []}
        for op in op_list:
            q_list = self.get_op_qubits(op)
            n_new = self.get_num_new_qubits(q_list, cluster_qubit_set)
            if self.is_cluster_limit_reached(n_new, cluster_qubit_set):
                # Form a cluster
                cluster_qubit_set.clear()
                self._result.append(cluster_inst_list)
                cluster_inst_list = {"instructions": []} # Create a new list to store new cluster
            cluster_inst_list["instructions"].append(op)
            for q in q_list:
                cluster_qubit_set.add(q)     
        self._result.append(cluster_inst_list)

    def print_res(self):
        for cluster in self._result:
            print('-------------------------')
            print_op_list(cluster["instructions"])
        print("Num ops after: {}".format(len(self._result))) 


class StaticReorderNewWithLocal(StaticReorderNew):
    """ 
    Simply traverse op list 
    Continues ops that reach the limit of local qubits form a cluster
    Qubits within `local` qubits cannot be clustered
    """

    _n_local = 0

    @property
    def custom_local_qubits(self):
        return self._n_local

    @custom_local_qubits.setter
    def custom_local_qubits(self, n):
        self._n_local = n

    def __init__(self):
        super().__init__()
        self._result = []

    def get_op_qubits(self, op):
        """
        Qubits within `local` won't be considered when clustering
        """
        op_q_list = []
        for q in op["qubits"]:
            if q >= self._n_local:
                op_q_list.append(q)
        return op_q_list

    def num_cluster(self):
        return self._n_primary - self._n_local

class ReorderProvidor:
    _REORDERS = {
        'static': StaticReorder,
        'static-new': StaticReorderNew,
        'static-new-local': StaticReorderNewWithLocal
    }
    
    def get_reorder(self, method_name):
        return self._REORDERS[method_name]()


Reorder = ReorderProvidor()
