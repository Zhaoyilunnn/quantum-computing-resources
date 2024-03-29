if [ $# -ne 4 ]; then
    echo "Usage: bash $0 <backend: FakeCairo|FakeBrooklyn|...> <metric: kl|pst|hybrid> <version: vanilla|random|small_first|large_first|brute_force> <num_circ: 2~6>"
    exit 1
fi

backend=$1
metric=$2
version=$3
num_circ=$4
log_backend=brooklyn

test_class=TestBenchDiffBackendQvmFrpV2
quafu_backend_list=("ScQ-P10", "ScQ-P18", "ScQ-P136")

if [ ${backend} = "FakeCairo" ]; then
    log_backend="cairo"
elif [ ${backend} = "FakeBrooklyn" ]; then
    log_backend="brooklyn"
elif [ ${backend} = "FakeManhattan" ]; then
    log_backend="manhattan"
elif [[ "${quafu_backend_list[*]}" == *"${backend}"* ]]; then
    test_class=TestQuafuBackendRealMachineQvmFrpV2
    if [ ${backend} = "ScQ-P136" ]; then
        log_backend=quafu_136
    elif [ ${backend} = "ScQ-P18" ]; then
        log_backend=quafu_18
    elif [ ${backend} = "ScQ-P10" ]; then
        log_backend=quafu_10
    fi
fi

log_dir=logs/qvm/main_v2/${version}/${log_backend}/circ_${num_circ}_cu_4/${metric}
mkdir -p $log_dir


cat logs/qvm/benchmarks_v2/${num_circ}_circ_benchmarks.lst | while read idx qasm bench; do pytest -s -k "${test_class} and test_bench_diff_methods_diff_metric" tst/qvm/integration/bench_test.py --qasm $qasm --backend ${backend} --qvm_version ${version} --metric ${metric} | tee ${log_dir}/${idx}.log; done
