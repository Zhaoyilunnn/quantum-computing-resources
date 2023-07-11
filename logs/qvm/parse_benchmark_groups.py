import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} benchmark_groups.lst <num-circ> <cu-size>")
        print("Extract benchmark groups with given number of circuits")
        sys.exit(1)

    bench_file = sys.argv[1]
    with open(bench_file, "r") as f:
        for line in f:
            items = line.strip().split("\t")
            bench_path_list = items[1].split(",")
            bench_names = [b.split("/")[-1].split(".")[0] for b in bench_path_list]
            bench_names = ",".join(bench_names)
            print(f"{items[0]}\t{items[1]}\t{bench_names}")
