bench_list=(\
    #head_1000_circuit_n28_m14_s5_e6_pEFGH.qasm
    head_1000_circuit_n30_m14_s7_e6_pEFGH.qasm
    #random_28_25_max_operands_2_gen.qasm
    random_30_27_max_operands_2_gen.qasm
    #qnn_n31.qasm
    qnn_n29.qasm
    graph_state-30.qasm
    hidden_linear_function-30.qasm
    qft-30.qasm
    iqp-30.qasm
    #graph_state-28.qasm
    #hidden_linear_function-28.qasm
    #qft-28.qasm
    #iqp-28.qasm
    #vqe_n28.qasm
    vqe_n30.qasm\
)

n_list=(\
    #28
    30
    #28
    30
    #31
    29
    30
    30
    30
    30
    #28
    #28
    #28
    #28
    #28
    30\
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
    NL=22
    bench_name=${bench_list[$i]}
    pytest -s -k test_run_${version}_any_qasm \
        tst/qdao/engine.py \
        --nq $NQ \
        --np $NP \
        --nl $NL \
        --qasm ${bench_name} \
        --parallel ${parallel}|
        tee ${res_dir}/${bench_name}.log
done
