import sys
import numpy as np


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <oracle> <bench_name_list>")
        sys.exit(1)

    oracle_res = {}
    oracle_res_file = sys.argv[1]
    with open(oracle_res_file, 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            b_name, fid = items[0], float(items[1])
            oracle_res[b_name] = fid

    bench_name_list = sys.argv[2].split(',')
    try:
        fid = np.average([oracle_res[b] for b in bench_name_list])
        print(f"{sys.argv[2]}\t{fid}")
    except KeyError:
        print(f"{sys.argv[2]}\tnot_found")


if __name__ == '__main__':
    main()
