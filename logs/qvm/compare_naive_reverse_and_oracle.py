import sys
import numpy as np


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <naive_reverse_res> <oracle>")
        sys.exit(1)

    oracle_res = {}
    oracle_res_file = sys.argv[2]
    with open(oracle_res_file, "r") as f:
        for line in f:
            items = line.strip().split("\t")
            b_name, fid = items[0], float(items[1])
            oracle_res[b_name] = fid

    naive_reverse_file = sys.argv[1]
    fids_1, fids_2 = [], []
    with open(naive_reverse_file, "r") as f:
        for line in f:
            items = line.strip().split("\t")
            if items[0] == "avg":
                continue
            b_names = items[0].split(",")
            fid = float(items[-1])
            oracle_fid = 0.0
            try:
                for b in b_names:
                    oracle_fid += oracle_res[b]
                oracle_fid /= len(b_names)
            except KeyError as ex:
                raise KeyError("Some benches not found in oracle result") from ex
            fids_1.append(fid)
            fids_2.append(oracle_fid)
            print(f"{','.join(b_names)}\t{fid}\t{oracle_fid}")
    avg_fid_1 = np.average(fids_1)
    avg_fid_2 = np.average(fids_2)
    print(f"avg\t{avg_fid_1}\t{avg_fid_2}")


if __name__ == "__main__":
    main()
