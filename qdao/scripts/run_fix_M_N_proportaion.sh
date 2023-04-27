# Usage: ./$0 $mode $version
# mode = parallel or no_parallel
# version = quafu or qiskit

if [ $# -eq 2 ]; then
    mode=$1
    version=$2
else
    mode=parallel
    version=quafu
fi


res_dir=logs/qdao/shuguang/${mode}/fix_M_to_N/${version}/$(date +%s)
mkdir $res_dir

for i in $(seq 22 32); do
    np=$((i-2))
    if [ $i -le 29 ]; then
        nl=$((i-6))
    else
        nl=24
    fi
    pytest -s -k test_run_${version}_random_basic tst/qdao/engine.py \
        --nq ${i} \
        --np ${np} \
        --nl ${nl} |
        tee ${res_dir}/rqc.${i}-${np}-${nl}.qasm.log
done
