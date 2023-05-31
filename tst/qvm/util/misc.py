from qvm.util.misc import *
from test.qvm import *


class TestUtilMisc(QvmBaseTest):

    def test_split_list(self):
        lst = [1,2,3,4,5,6,7,8,9,10]
        res = split_list(lst, 3)
        assert res == [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]] 
