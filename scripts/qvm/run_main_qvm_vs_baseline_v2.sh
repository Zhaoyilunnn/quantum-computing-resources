if [ $# -ne 4 ]; then
    echo "Usage: bash $0 <backend: FakeCairo|FakeBrooklyn|...> <metric: kl|pst> <num_circ: 2~6> <cu_size>"
    exit 1
fi

backend=$1
metric=$2
num_circ=$3
cu_size=$4
log_backend=brooklyn

if [ ${backend} = "FakeCairo" ]; then
    log_backend="cairo"
elif [ ${backend} = "FakeBrooklyn" ]; then
    log_backend="brooklyn"
elif [ ${backend} = "FakeManhattan" ]; then
    log_backend="manhattan"
fi

log_dir=logs/qvm/main_v2/random/${log_backend}/circ_${num_circ}_cu_${cu_size}/${metric}
mkdir -p $log_dir


cat logs/qvm/benchmarks_v2/${num_circ}_circ_benchmarks.lst | while read idx qasm bench; do pytest -s -k "TestBenchDiffBackendQvmFrpV2 and test_${metric}_independent_two_bench_frp" tst/qvm/integration/bench_test.py --bench qasm --qasm $qasm --backend ${backend} --cu_size ${cu_size} | tee ${log_dir}/${idx}.log; done
