#!/bin/bash

logs_dir=logs/qvm/model/observ_cost_exe/$(date +%s)
mkdir -p ${logs_dir}

for i in $(seq 2 8); do
    for j in $(seq 1 5); do
        pytest -s -k test_get_cost tst/qvm/model/executable.py --nq ${i} >> ${logs_dir}/rqc.${i}.log
    done
done
