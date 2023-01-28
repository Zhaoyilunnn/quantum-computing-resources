#!/bin/bash

d=10
for nq in $(seq 5 25); do
    python bench.py \
        --mode random \
        --num-qubits ${nq} \
        --depth ${d} \
        --run 0 \
        --backend fake;
    echo "random::num_qubits: ${nq}, ::depth: ${d}"
done

nq=25
for d in 10 20 30 40 50; do
    python bench.py \
        --mode random \
        --num-qubits ${nq} \
        --depth ${d} \
        --run 0 \
        --backend fake
    echo "random::num_qubits: ${nq}, ::depth: ${d}"
done

