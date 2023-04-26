import sys
import os

from utils.plot import plot_bar_3d

def traverse_files(path):
    res_dict = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            file_path = os.path.join(root, f)
            parse_res(file_path, f, res_dict)

    #print(res_dict)
    for q in res_dict:
        plot_bar_3d(
            res_dict[q],
            labels=(r'$K$', r'$M$', 'Normalized Overhead'),
            figname=f"params_rqc_{q}.pdf",
            normalize=True,
            integer=True
        )

def parse_res(file_path, file_name, res_dict):

    items = file_name.split('.')
    NQ = int(items[1])
    NP = NQ - int(items[2])
    NL = NP - int(items[3])

    res_qdao, res_quafu = None, None
    with open(file_path, 'r') as f:
        for line in f:
            if line and line.startswith("Qdao runs"):
                res_qdao = line.strip().split()[-1]
            if line and line.startswith("Quafu runs"):
                res_quafu = line.strip().split()[-1]

    if res_qdao and res_quafu:
        runtime = float(res_qdao) / float(res_quafu)
        memory = 2**(NQ-NP)
        print("\t".join([str(NQ), str(NP), str(NL), res_qdao, res_quafu, str(memory), str(runtime)]))
        res_dict.setdefault(NQ, [])
        res_dict[NQ].append((NL, NP, runtime))



if __name__ == '__main__':
    file_path = sys.argv[1]
    traverse_files(file_path)
