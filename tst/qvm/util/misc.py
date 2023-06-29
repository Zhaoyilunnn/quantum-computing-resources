from test.qvm import *

from qvm.util.misc import *


class TestUtilMisc(QvmBaseTest):
    def test_split_list(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        res = split_list(lst, 3)
        assert res == [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]

    def test_min_sum_indices_sets(self):
        list1 = [{1, 2}, {3, 4}, {5, 6}]
        list2 = [{1, 5}, {3, 4}, {5, 6}]
        list3 = [{2, 6}, {3, 4}, {5, 6}]

        res = min_sum_indices_sets(list1, list2, list3)

        assert res == [{3, 4}, {1, 5}, {2, 6}]
