
class ReroderMethod:

    def __init__(self):
        pass        


class StaticReorder(ReroderMethod):
    def __init__(self):
        super().__init__()

    def run(self, op_list):
        for op in op_list:
            print(op)

    def get_num_clusters(self):
        pass


class ReorderProvidor:
    _REORDERS = {
        'static': StaticReorder
    }
    
    def get_reorder(self, method_name):
        return self._REORDERS[method_name]()


Reorder = ReorderProvidor()
