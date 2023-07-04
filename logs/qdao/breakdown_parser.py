import sys
import os
from typing import List, Any

from qutils.results import BaseParser


class QdaoBreakParser(BaseParser):
    def parse_one(self, file_path, *args) -> List[Any]:
        version = args[0]

        bench_name = None
        res_qdao, res_init, res_load, res_store = None, None, None, None
        with open(file_path, "r") as f:
            items = os.path.basename(file_path).split(".")
            bench_name = items[-3]
            for line in f:
                if line and line.startswith("Qdao runs"):
                    res_qdao = float(line.strip().split()[-1])
                if line and line.startswith("_initialize"):
                    res_init = float(line.strip().split()[-1])
                if line and line.startswith("load_sv"):
                    res_load = float(line.strip().split()[-1])
                if line and line.startswith("store_sv"):
                    res_store = float(line.strip().split()[-1])

        if res_qdao and res_init and res_load and res_store:
            res_io = res_init + res_load + res_store
            res_compute = res_qdao - res_io
            prop_io = res_io / res_qdao
            prop_compute = res_compute / res_qdao
            return [
                bench_name,
                res_qdao,
                res_init,
                res_load,
                res_store,
                prop_compute,
                prop_io,
            ]

        return []


if __name__ == "__main__":
    logs_path = sys.argv[1]
    version = sys.argv[2]

    parser = QdaoBreakParser(logs_path, version)
    parser.run()

    # traverse_files(logs_path, version)
