import os
import sys

from typing import List, Any
from qutils.results import BaseParser
from qutils.misc import check_equiv_two_list


def check_prefix_and_update_list(prefix_list: List[str], line: str, lst: List[Any]):
    """check if line starts with any prefix in prefix_list and append last item to lst"""
    for prefix in prefix_list:
        if line.startswith(prefix):
            items = line.strip().split("\t")
            val = float(items[-1])
            lst.append(val)


class QvmEvalSelectionParser(BaseParser):
    def parse_one(self, file_path, *args) -> List[Any]:
        diff_only = args[0]
        methods_list = args[1]
        time_log_prefix_list = [method + " selection time" for method in methods_list]
        fid_log_prefix_list = [method + " selection result" for method in methods_list]

        compute_unit_lists = []
        b_names = []

        file_name = os.path.basename(file_path).split(".")[0]
        file_name_items = file_name.split("_")
        bench_qasm_path = ""

        fidelities = []
        times = []

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
                    else:
                        check_prefix_and_update_list(time_log_prefix_list, line, times)
                        check_prefix_and_update_list(
                            fid_log_prefix_list, line, fidelities
                        )

        compute_unit_lists = [eval(cu_list) for cu_list in compute_unit_lists]

        if len(compute_unit_lists) != len(methods_list):
            return []

        if diff_only and len(compute_unit_lists) == 2:
            if check_equiv_two_list(compute_unit_lists[0], compute_unit_lists[1]):
                return []

        return [
            ",".join(b_names),
            file_name,
            bench_qasm_path,
            *file_name_items,
            *compute_unit_lists,
            *times,
            *fidelities,
        ]


def main():
    if len(sys.argv) not in [2, 3, 4]:
        print(f"Usage: python {sys.argv[0]} logs_path diff_only selection_method_list")
        print(
            "\tdiff_only is optional, if set 1, only results with different selection outcome will be printed"
        )
        print("\tselection_method_list is optional, default: naive,brute_force")
        sys.exit(1)

    logs_path = sys.argv[1]
    diff_only = False
    methods_list = ["naive", "brute_force"]
    if len(sys.argv) == 3:
        diff_only = True if int(sys.argv[2]) == 1 else False
    elif len(sys.argv) == 4:
        diff_only = True if int(sys.argv[2]) == 1 else False
        methods_list = sys.argv[3].split(",")

    parser = QvmEvalSelectionParser(logs_path, diff_only, methods_list)
    parser.run()


if __name__ == "__main__":
    main()
