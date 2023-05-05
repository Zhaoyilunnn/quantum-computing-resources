import sys
import os
from typing import List, Any

from utils.results import BaseParser


class QdaoResParser(BaseParser):

    def parse_one(self, file_path, *args) -> List[Any]:
        version = args[0]

        bench_name = None
        res_qdao, res_quafu = None, None
        with open(file_path, 'r') as f:
            items = os.path.basename(file_path).split('.')
            bench_name = items[-3]
            for line in f:
                if line and line.startswith("Qdao runs"):
                    res_qdao = float(line.strip().split()[-1])
                if line and line.startswith(f"{version} runs"):
                    res_quafu = float(line.strip().split()[-1])

        if res_qdao and res_quafu:
            runtime = float(res_qdao) / float(res_quafu)
            overhead0 = (float(res_qdao) - float(res_quafu)) / float(res_qdao)
            overhead1 = float(res_qdao) - float(res_quafu)
            #print("\t".join([bench_name, res_qdao, res_quafu, str(runtime), str(overhead)]))
            return [bench_name, res_qdao, res_quafu, runtime, overhead0, overhead1]

        return []


if __name__ == '__main__':
    logs_path = sys.argv[1]
    version = sys.argv[2]

    parser = QdaoResParser(logs_path, version)
    parser.run()

    #traverse_files(logs_path, version)

