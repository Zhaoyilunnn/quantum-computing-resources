#!/bin/bash
cat test_data/qasms.list | while read line; do python bench.py --qasm-file $line --local-qubits 10 --analysis 1 --run 0; done
