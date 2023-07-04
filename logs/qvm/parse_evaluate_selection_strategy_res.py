import sys

from typing import List, Any
from qutils.results import BaseParser


class QvmEvalSelectionParser(BaseParser):
    def parse_one(self, file_path, *args) -> List[Any]:
        compute_unit_lists = []
        b_names = []
        fid_brute_force, fid_naive = 0.0, 0.0
        time_brute_force, time_naive = 0.0, 0.0
        with open(file_path, "r") as f:
            for line in f:
                if line:
                    if line.startswith("/root/projects"):
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

        if len(compute_unit_lists) != 2:
            return []

        return [
            ",".join(b_names),
            "\t".join(compute_unit_lists),
            time_naive,
            time_brute_force,
            fid_naive,
            fid_brute_force,
        ]


def main():
    logs_path = sys.argv[1]

    parser = QvmEvalSelectionParser(logs_path)
    parser.run()


if __name__ == "__main__":
    main()
