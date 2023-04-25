import sys


if __name__ == '__main__':
    res_log = sys.argv[1]
    version = sys.argv[2]

    items = res_log.split('.')
    bench_name = items[-3]

    res_qdao, res_quafu = None, None
    with open(res_log, 'r') as f:
        for line in f:
            if line and line.startswith("Qdao runs"):
                res_qdao = line.strip().split()[-1]
            if line and line.startswith(f"{version} runs"):
                res_quafu = line.strip().split()[-1]

    if res_qdao and res_quafu:
        runtime = float(res_qdao) / float(res_quafu)
        print("\t".join([bench_name, res_qdao, res_quafu, str(runtime)]))
