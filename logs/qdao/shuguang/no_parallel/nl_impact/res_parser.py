import sys


if __name__ == '__main__':
    res_log = sys.argv[1]

    items = res_log.split('.')
    NQ = int(items[1])
    NP = NQ - int(items[2])
    NL = NP - int(items[3])

    res_qdao, res_quafu = None, None
    with open(res_log, 'r') as f:
        for line in f:
            if line and line.startswith("Qdao runs"):
                res_qdao = line.strip().split()[-1]
            if line and line.startswith("Quafu runs"):
                res_quafu = line.strip().split()[-1]

    if res_qdao and res_quafu:
        runtime = float(res_qdao) / float(res_quafu)
        memory = 2**(NQ-NP)
        print("\t".join([str(NQ), str(NP), str(NL), res_qdao, res_quafu, str(memory), str(runtime)]))
