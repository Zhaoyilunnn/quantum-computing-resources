bench_path=qdao/benchmarks/qasm/

bench_list_cirq=(\
    vqe_n27_with_measure.qasm
    vqe_n28_with_measure.qasm
    vqe_n29_with_measure.qasm
    vqe_n30_with_measure.qasm
    vqe_n31_with_measure.qasm
    vqe_n32_with_measure.qasm
)

bench_list=(\
    vqe_n27.qasm
    vqe_n28.qasm
    vqe_n29.qasm
    vqe_n30.qasm
    vqe_n31.qasm
    vqe_n32.qasm
)

bench_list_qdao=(\
    vqe_n29.qasm
    vqe_n30.qasm
    vqe_n31.qasm
    vqe_n32.qasm
)

n_list=(\
    29
    30
    31
    32
)

logs_path=logs/qdao/winpc/comparison/
mkdir -p ${logs_path}
for b in ${bench_list_cirq[@]}; do
    python qdao/benchmarks/qsimcirq_test.py ${bench_path}${b} | tee ${logs_path}/qsimcirq.${b}.log
done
for b in ${bench_list[@]}; do
    python qdao/benchmarks/qiskit_test.py ${bench_path}${b} | tee ${logs_path}/qiskit.${b}.log
    python qdao/benchmarks/quafu_test.py ${bench_path}${b} | tee ${logs_path}/quafu.${b}.log
done

parallel=0
N=${#n_list[@]}
for i in $(seq 0 $((N-1))); do
    NQ=${n_list[${i}]}
    NP=$((NQ-2))
    NL=$((NQ-8))
    bench_name=${bench_list_qdao[$i]}
    pytest -s -k test_run_quafu_any_qasm \
        tst/qdao/engine.py \
        --nq $NQ \
        --np $NP \
        --nl $NL \
        --qasm ${bench_name} \
        --diff 0 \
        --parallel ${parallel}|
        tee ${logs_path}/qdao_quafu.${bench_name}.log
    pytest -s -k test_run_qiskit_any_qasm \
        tst/qdao/engine.py \
        --nq $NQ \
        --np $NP \
        --nl $NL \
        --qasm ${bench_name} \
        --diff 0 \
        --parallel ${parallel}|
        tee ${logs_path}/qdao_qiskit.${bench_name}.log
done
