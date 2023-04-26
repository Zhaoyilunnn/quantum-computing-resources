import sys
import os

def traverse_files(path, version):
    for root, dirs, files in os.walk(path):
        for f in files:
            file_path = os.path.join(root, f)
            parse_res(file_path, f, version)

def parse_res(file_path, file_name, version):
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
        print("\t".join([bench_name, res_qdao, res_quafu, str(runtime), str(overhead)]))


if __name__ == '__main__':
    logs_path = sys.argv[1]
    version = sys.argv[2]

    traverse_files(logs_path, version)

