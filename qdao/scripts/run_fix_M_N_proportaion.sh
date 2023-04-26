for i in $(seq 22 32); do
    pytest -s -k test_run_quafu_random_basic tst/qdao/engine.py \
        --nq ${i} \
        --np $((i-2)) \
        --nl $((i-6)) |
        tee logs/qdao/shuguang/parallel/fix_M_to_N/rqc.${i}.qasm.log
done
