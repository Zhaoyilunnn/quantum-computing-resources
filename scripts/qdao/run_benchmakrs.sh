bench_list=(\
    #a.rqc_30_0.qasm
    #a.rqc_30_1.qasm
    #a.vqa.qnn_29_0.qasm
    #a.vqa.qnn_29_1.qasm
    #a.vqa.vqe_29.qasm
    #a.vqa.vqe_30.qasm
    #b.gs_30.qasm
    #b.hlf_30.qasm
    #b.iqp_30.qasm
    #b.qft_30.qasm
    a.rqc_28_0.qasm
    a.rqc_28_1.qasm
    a.vqa.qnn_27_0.qasm
    a.vqa.qnn_27_1.qasm
    a.vqa.vqe_27.qasm
    a.vqa.vqe_28.qasm
    b.gs_28.qasm
    b.hls_28.qasm
    b.iqp_28.qasm
    b.qft_28.qasm
)

n_list=(\
    #30
    #30
    #29
    #29
    #29
    #30
    #30
    #30
    #30
    #30
    28
    28
    27
    27
    27
    28
    28
    28
    28
    28
)

N=${#n_list[@]}


mode=no_parallel # no_parallel or parallel
version=qiskit
system=shuguang

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


res_dir=logs/qdao/${system}/${mode}/${version}/$(date +%s)
mkdir -p $res_dir

for i in $(seq 0 $((N-1))); do
    NQ=${n_list[${i}]}
    NP=$((NQ-2))
    NL=20
    bench_name=${bench_list[$i]}
    pytest -s -k test_run_${version}_any_qasm \
        tst/qdao/engine.py \
        --nq $NQ \
        --np $NP \
        --nl $NL \
        --qasm ${bench_name} \
        --diff 0 \
        --parallel ${parallel}|
        tee ${res_dir}/${bench_name}.log
done
