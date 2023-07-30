import pickle
import sys


def main():
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <backend-name: FakeCairo | FakeBrooklyn> <bench-name> <cu-size>")
        sys.exit(1)

    backend_name = sys.argv[1]
    bench_name = sys.argv[2]
    cu_size = sys.argv[3]
    cache_proc_name = "_".join([backend_name, bench_name, cu_size]) + ".pkl"
    obj = None
    with open("data/qvm/" + cache_proc_name, "rb") as f:
        obj = f.read()
    proc = pickle.loads(obj)
    print(len(proc))


if __name__ == '__main__':
    main()
