#!/bin/bash

for nq in 10 20 30 40 50 60 70 80; do
    python bench.py \
        --mode random \
        --num-qubits ${nq} \
        --depth ${nq} \
        --run 0 \
        --backend fake;
    echo "random::num_qubits: ${nq}, ::depth: ${d}"
done
