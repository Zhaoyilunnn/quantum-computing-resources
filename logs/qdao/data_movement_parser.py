import sys
import os
from typing import List, Any

from utils.results import BaseParser


class QdaoDataMoveParser(BaseParser):

    def parse_one(self, file_path, *args) -> List[Any]:
        version = args[0]

        bench_name = None
        num_sub_circ, num_ops = None, None
        with open(file_path, 'r') as f:
            items = os.path.basename(file_path).split('.')
            bench_name = items[-3]
            bench_conf = [int(c) for c in items[-2].split('-')[1:]]
            for line in f:
                if line and "sub-circuits" in line:
                    num_sub_circ = int(line.strip().split()[-1])
                if line and "original circuit" in line:
                    num_ops = int(line.strip().split()[-1])

        if num_sub_circ and num_ops:
            if bench_conf:
                return [bench_name, *bench_conf, num_sub_circ, num_ops, num_ops/num_sub_circ]
            return [bench_name, num_sub_circ, num_ops, num_ops/num_sub_circ]

        return []


if __name__ == '__main__':
    logs_path = sys.argv[1]
    version = sys.argv[2]

    parser = QdaoDataMoveParser(logs_path, version)
    parser.run()

    #traverse_files(logs_path, version)

