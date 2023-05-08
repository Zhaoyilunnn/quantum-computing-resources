for q in $(seq 28 32); do
    for p in $(seq 2 2 10); do
        for l in $(seq 2 2 10); do
            pytest -s -k test_run_quafu_random_basic tst/qdao/engine.py \
                --nq ${q} \
                --np $((q-p)) \
                --nl $((q-p-l)) |
                tee logs/qdao/shuguang/no_parallel/nl_impact/rqc.${q}.${p}.${l}.log
        done
    done
done
