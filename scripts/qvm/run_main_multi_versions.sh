if [ $# -ne 3 ]; then
    echo "Usage: bash $0 <backend: FakeCairo|FakeBrooklyn|...> <version: list of vanilla|random|small_first|large_first|brute_force> <num_circ: 2~6>"
    echo "This script will calculate both PST and KL"
    exit 1
fi

backend=$1
version=$2
num_circ=$3
log_backend=brooklyn

if [ ${backend} = "FakeCairo" ]; then
    log_backend="cairo"
elif [ ${backend} = "FakeBrooklyn" ]; then
    log_backend="brooklyn"
elif [ ${backend} = "FakeManhattan" ]; then
    log_backend="manhattan"
fi

log_dir=logs/qvm/main_v2/multi_versions/${log_backend}/circ_${num_circ}_cu_4/
mkdir -p $log_dir


cat logs/qvm/benchmarks_v2/${num_circ}_circ_benchmarks.lst | while read idx qasm bench; do  pytest -s -k "TestBenchDiffBackendQvmFrpV2 and test_bench_multi_methods_multi_metrics" tst/qvm/integration/bench_test.py --qasm ${qasm} --backend ${backend} --qvm_version ${version} | tee ${log_dir}/${idx}.log; done
