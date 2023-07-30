import sys


def main():
    if len(sys.argv) != 3:
        print(f"python {sys.argv[0]} <n-bench-list> <bench-list>")
        print("example: python logs/qvm/gen_benchmark_group_idx.py logs/qvm/benchmarks_v2/2_circ_benchmarks.lst logs/qvm/benchmark_names.lst")
        sys.exit(1)

    bench_names_file = sys.argv[2]
    bench_names_list = []
    with open(bench_names_file, 'r') as f:
        for line in f:
            bench_names_list.append(line.strip())

    bench_names_idx = {b: (i+1) for i, b in enumerate(bench_names_list)}

    n_bench_list_file = sys.argv[1]
    with open(n_bench_list_file, 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            b_list = items[-1].split(',')
            idx_list = [str(bench_names_idx[b]) for b in b_list]
            print("_".join(idx_list))


if __name__ == '__main__':
    main()
