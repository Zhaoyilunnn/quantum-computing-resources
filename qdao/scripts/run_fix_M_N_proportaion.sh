# Usage: ./$0 $mode $version
# mode = parallel or no_parallel
# version = quafu or qiskit

if [ $# -ne 3 ]; then
    echo "Usage: bash $0 <mode (no_parallel | parallel)> <version (qiskit | quafu)> <system (shuguang | macos)>"
    exit 1
else
    mode=$1
    version=$2
    system=$3
fi

if [ ${mode} = "no_parallel" ]; then
    parallel=0
elif [ ${mode} = "parallel" ]; then
    parallel=1
else
    echo "Unsupported mode"
    exit 1
fi

res_dir=logs/qdao/${system}/${mode}/fix_M_to_N/${version}/$(date +%s)
mkdir -p $res_dir

for i in $(seq 12 28); do
    np=$((i-2))
    if [ $i -le 29 ]; then
        nl=$((i-6))
    else
        nl=24
    fi
    pytest -s -k test_run_${version}_random_basic tst/qdao/engine.py \
        --nq ${i} \
        --np ${np} \
        --nl ${nl} \
        --parallel ${parallel} |
        tee ${res_dir}/rqc.${i}-${np}-${nl}.qasm.log
done
