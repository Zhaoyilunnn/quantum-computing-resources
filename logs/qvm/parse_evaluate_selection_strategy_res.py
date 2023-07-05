import os
import sys

from typing import List, Any
from qutils.results import BaseParser


def check_equiv_two_list(first: List[set], second: List[set]):
    if len(first) != len(second):
        return False
    for s in first:
        if s not in second:
            return False
    return True


class QvmEvalSelectionParser(BaseParser):
    def parse_one(self, file_path, *args) -> List[Any]:
        compute_unit_lists = []
        b_names = []
        fid_brute_force, fid_naive = 0.0, 0.0
        time_brute_force, time_naive = 0.0, 0.0

        diff_only = args[0]

        file_name = os.path.basename(file_path).split('.')[0]
        file_name_items = file_name.split('_')
        bench_qasm_path = ""
        with open(file_path, "r") as f:
            for line in f:
                if line:
                    if line.startswith("/root/projects"):
                        bench_qasm_path = line.strip()
                        items = line.strip().split(",")
                        b_names = [b.split("/")[-1].split(".")[0] for b in items]
                    elif line.startswith("compute_unit_list"):
                        items = line.strip().split("\t")
                        compute_unit_list = items[-1]
                        compute_unit_lists.append(compute_unit_list)
                    elif line.startswith("naive selection time"):
                        items = line.strip().split("\t")
                        time_naive = float(items[-1])
                    elif line.startswith("brute_force selection time"):
                        items = line.strip().split("\t")
                        time_brute_force = float(items[-1])
                    elif line.startswith("naive selection result"):
                        items = line.strip().split("\t")
                        fid_naive = float(items[-1])
                    elif line.startswith("brute_force selection result"):
                        items = line.strip().split("\t")
                        fid_brute_force = float(items[-1])

        compute_unit_lists = [eval(cu_list) for cu_list in compute_unit_lists]

        if len(compute_unit_lists) != 2:
            return []

        if diff_only:
            if check_equiv_two_list(compute_unit_lists[0], compute_unit_lists[1]):
                return []

        return [
            ",".join(b_names),
            file_name,
            bench_qasm_path,
            *file_name_items,
            *compute_unit_lists,
            time_naive,
            time_brute_force,
            fid_naive,
            fid_brute_force,
        ]


def main():
    if len(sys.argv) not in [2, 3]:
        print(f"Usage: python {sys.argv[0]} logs_path diff_only")
        print("diff_only is optional, if set 1, only results with different selection outcome will be printed")
        sys.exit(1)

    logs_path = sys.argv[1]
    diff_only = False
    if len(sys.argv) == 3:
        diff_only = True if int(sys.argv[2]) == 1 else False

    parser = QvmEvalSelectionParser(logs_path, diff_only)
    parser.run()


if __name__ == "__main__":
    main()
