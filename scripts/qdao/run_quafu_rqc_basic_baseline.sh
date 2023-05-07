for q in $(seq 28 32); do pytest -s -k test_run_quafu_random_basic tst/qdao/engine.py --nq ${q} --mode BASELINE | tee logs/qdao/shuguang/baseline.rqc.${q}.log; done
