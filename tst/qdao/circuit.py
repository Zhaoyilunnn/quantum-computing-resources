from qdao.circuit import BasePartitioner
from qdao.test import QdaoBaseTest


class TestBasePartitioner(QdaoBaseTest):
    
    _part = BasePartitioner()

    def test_gen_sub_circ(self):
        """Testing generation of sub-circuits"""
        circ = self.get_small_bench_circ("random")
        print(circ)
        sub_instrs = circ.data[0:4]
        sub_circ = self._part._gen_sub_circ(circ, sub_instrs)
        print(sub_circ)
