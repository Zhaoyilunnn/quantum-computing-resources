import sys
import os

sys.path.append('.')

from typing import List, Any
from qutils.plot import plot_bar_3d
from qutils.results import BaseParser


class QdaoLVsMAndK(BaseParser):

    def parse_one(self, file_path, *args) -> List[Any]:

        bench_name = None
        num_sub_circ, num_ops = None, None
        with open(file_path, 'r') as f:
            items = os.path.basename(file_path).split('.')
            bench_name = items[-3]
            _, NQ, NP, NL = items[-2].split('-')
            NQ, NP, NL = int(NQ), int(NP), int(NL)
            for line in f:
                if line and "sub-circuits" in line:
                    num_sub_circ = int(line.strip().split()[-1])
                if line and "original circuit" in line:
                    num_ops = int(line.strip().split()[-1])

        if num_sub_circ and num_ops:
            return [bench_name, NL, NP, num_sub_circ]

        return []

    def post_process(self):
        res_dict = {}
        for r in self.results:
            bench_name = r[0]
            res_dict.setdefault(bench_name, [])
            res_dict[bench_name].append(r[1:])

        for b in res_dict:
            plot_bar_3d(
                res_dict[b],
                labels=(r'$t$', r'$m$', r'$l$'),
                figname=f"L_vs_M_K_{b}.pdf",
                normalize=False,
                integer=True
            )


if __name__ == '__main__':
    logs_path = sys.argv[1]
    version = sys.argv[2]

    parser = QdaoLVsMAndK(logs_path, version)
    parser.run()
    parser.post_process()
