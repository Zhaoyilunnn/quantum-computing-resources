import sys
import os

sys.path.append('.')

from typing import List, Any
from utils.plot import plot_bar_3d
from utils.results import BaseParser


class QdaoPerfVsMAndK(BaseParser):

    def parse_one(self, file_path, *args) -> List[Any]:

        res_qdao, res_quafu = None, None
        with open(file_path, 'r') as f:
            items = os.path.basename(file_path).split('.')
            NQ = int(items[1].split('-')[0])
            NP = NQ - int(items[2])
            NL = NP - int(items[3])
            for line in f:
                if line and line.startswith("Qdao runs"):
                    res_qdao = line.strip().split()[-1]
                if line and line.startswith("Quafu runs"):
                    res_quafu = line.strip().split()[-1]

        if res_qdao and res_quafu:
            runtime = float(res_qdao) / float(res_quafu)
            memory = 2**(NQ-NP)
            print("\t".join([str(NQ), str(NP), str(NL), res_qdao, res_quafu, str(memory), str(runtime)]))

            return [NQ, NL, NP, runtime]

        return []

    def post_process(self):
        res_dict = {}
        for r in self.results:
            NQ = r[0]
            res_dict.setdefault(NQ, [])
            res_dict[NQ].append(r[1:])

        for q in res_dict:
            plot_bar_3d(
                res_dict[q],
                labels=(r'$t$', r'$m$', 'Normalized Overhead'),
                figname=f"params_rqc_{q}.pdf",
                normalize=True,
                integer=True
            )


if __name__ == '__main__':
    logs_path = sys.argv[1]
    version = sys.argv[2]

    parser = QdaoPerfVsMAndK(logs_path, version)
    parser.run()
    parser.post_process()
