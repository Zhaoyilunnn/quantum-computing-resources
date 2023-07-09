if [ $# -ne 4 ]; then
    echo "Usage: bash $0 <backend: FakeCairo|FakeBrooklyn|...> <metric: kl|pst> <version: vanilla|random|small_first|large_first|brute_force> <num_circ: 2~6>"
    exit 1
fi

backend=$1
metric=$2
version=$3
num_circ=$4
log_backend=brooklyn

if [ ${backend} = "FakeCairo" ]; then
    log_backend="cairo"
elif [ ${backend} = "FakeBrooklyn" ]; then
    log_backend="brooklyn"
elif [ ${backend} = "FakeManhattan" ]; then
    log_backend="manhattan"
fi

log_dir=logs/qvm/main/${version}/${log_backend}/circ_${num_circ}_cu_4/${metric}
mkdir -p $log_dir


cat logs/qvm/${num_circ}_circ_benchmarks.lst | while read idx qasm bench; do pytest -s -k "TestBenchDiffBackendQvmFrpV2 and test_bench_diff_methods_diff_metric" tst/qvm/integration/bench_test.py --qasm $qasm --backend ${backend} --qvm_version ${version} --metric ${metric} | tee ${log_dir}/${idx}.log; done
