import sys

from typing import List, Any
from qutils.results import BaseParser


class QvmTwoBenchParser(BaseParser):
    def parse_one(self, file_path, *args) -> List[Any]:
        b0_name, b1_name, fid0, fid1 = "", "", 0, 0
        with open(file_path, 'r') as f:
            for line in f:
                if line:
                    if line.startswith('/root/projects'):
                        items = line.strip().split(',')
                        if len(items) != 2:
                            continue
                        b0, b1 = items[0], items[1]
                        b0_name = b0.split('/')[-1].split('.')[0]
                        b1_name = b1.split('/')[-1].split('.')[0]
                    elif line.startswith("Fid of qvm"):
                        items = line.strip().split('\t')
                        fid0, fid1 = items[1], items[2]

        return [b0_name+','+b1_name, float(fid0), float(fid1)]


def main():
    logs_path = sys.argv[1]

    parser = QvmTwoBenchParser(logs_path)
    parser.run()


if __name__ == '__main__':
    main()
