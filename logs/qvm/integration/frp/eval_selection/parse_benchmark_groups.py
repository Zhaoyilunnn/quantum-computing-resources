import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} benchmark_groups.lst <num-circ> <cu-size>")
        print("Extract benchmark groups with given number of circuits")
        sys.exit(1)

    bench_file = sys.argv[1]
    num_circ = sys.argv[2]
    cu_size = sys.argv[3]
    idx = 0
    with open(bench_file, 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            b_id = items[0]
            cu_sz = items[-1]
            if "num_circ_"+num_circ in b_id and cu_sz == cu_size:
                bench_path_list = items[1].split(',')
                bench_names = [b.split('/')[-1].split('.')[0] for b in bench_path_list]
                bench_names = ",".join(bench_names)
                idx += 1
                print(f"{idx}\t{items[1]}\t{bench_names}")
