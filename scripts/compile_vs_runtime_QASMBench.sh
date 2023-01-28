#!/bin/bash

benchmarks_list=/root/projects/qcs/scripts/benchmarks.lst
benchmarks_path=/root/projects/QASMBench/large

cat $benchmarks_list | while read benchmark_name; do
    python bench.py \
        --mode qasm \
        --qasm-file ${benchmarks_path}/${benchmark_name}/${benchmark_name}.qasm \
        --run 0 \
        --backend fake
    done

