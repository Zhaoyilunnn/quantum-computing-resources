#!/bin/bash

BIN='/root/projects/qcs/sim-beta/build/bin/simulator'
DATA_PATH='/root/projects/qcs/sim-beta/test/data'
LOG_PATH='/root/projects/qcs/sim-beta/exp'

for i in 18 20 22 24 26; do
    ${BIN} -qobj_file ${DATA_PATH}/unitary_random_28_${i}_16_inst.json -nq 28 -np ${i} -nl 16 | 
        tee ${LOG_PATH}/random.28.${i}.16.log
done
