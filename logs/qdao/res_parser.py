import sys
import os


bench_list = [
    'random_28_25_max_operands_2_gen',
    'random_30_27_max_operands_2_gen',
    'head_1000_circuit_n28_m14_s5_e6_pEFGH',
    'head_1000_circuit_n30_m14_s7_e6_pEFGH',
    'qnn_n29',
    'qnn_n31',
    'vqe_n28',
    'vqe_n30',
    'graph_state-30',
    'hidden_linear_function-30',
    'iqp-30',
    'qft-30'
]


def traverse_files(path, version):
    res = {}

    for root, dirs, files in os.walk(path):
        for f in files:
            file_path = os.path.join(root, f)
            parse_res(file_path, f, version, res)

    try:
        for b in bench_list:
            print("\t".join([b] + res[b]))
    except Exception:
        for k, v in res.items():
            print("\t".join([k] + v))

def parse_res(
        file_path,
        file_name,
        version,
        res
    ):
    version = sys.argv[2]

    items = file_name.split('.')
    bench_name = items[-3]

    res_qdao, res_quafu = None, None
    with open(file_path, 'r') as f:
        for line in f:
            if line and line.startswith("Qdao runs"):
                res_qdao = line.strip().split()[-1]
            if line and line.startswith(f"{version} runs"):
                res_quafu = line.strip().split()[-1]

    if res_qdao and res_quafu:
        runtime = float(res_qdao) / float(res_quafu)
        overhead = (float(res_qdao) - float(res_quafu)) / float(res_qdao)
        #print("\t".join([bench_name, res_qdao, res_quafu, str(runtime), str(overhead)]))
        res[bench_name] = [res_qdao, res_quafu, str(runtime), str(overhead)]


if __name__ == '__main__':
    logs_path = sys.argv[1]
    version = sys.argv[2]

    traverse_files(logs_path, version)

