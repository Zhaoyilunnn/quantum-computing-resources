import sys
import random
import itertools


def generate_combinations(elements, k):
    combinations = list(itertools.combinations(elements, k))
    return combinations


def main():
    if len(sys.argv) != 3:
        print(
            f"Usage: python {sys.argv[0]} <benchmarks.lst> <number of benchmarks in a group>"
        )
        sys.exit(1)

    b_list = []
    k = int(sys.argv[2])
    with open(sys.argv[1], "r") as f:
        for line in f:
            item = line.strip()
            b_list.append(item)

    combinations = generate_combinations(b_list, k)
    random.shuffle(combinations)
    idx = 0
    for b_comb in combinations:
        idx += 1
        b_names = [b.split("/")[-1].split(".")[0] for b in b_comb]
        b_name = ",".join(b_names)
        b_path = ",".join(b_comb)
        print(f"{idx}\t{b_path}\t{b_name}")


if __name__ == "__main__":
    main()
