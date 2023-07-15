import sys
import math


def main():
    if len(sys.argv) != 2:
        print(f"cat <qasm_list> | python {sys.argv[0]} <pst-res>")
        sys.exit(1)

    pst_res = sys.argv[1]
    nondetermine_set = set()

    with open(pst_res, "r") as f:
        for line in f:
            items = line.strip().split("\t")
            assert len(items) == 2
            qasm, pst = items
            pst = float(pst)
            if math.isclose(pst, 1):
                nondetermine_set.add(qasm)
    print(nondetermine_set)

    for line in sys.stdin:
        qasms = line.strip().split(",")
        if any([qasm in nondetermine_set for qasm in qasms]):
            print("PST applicable ")
            continue
        print(line.strip())


if __name__ == "__main__":
    main()
