# for q in $(seq 3 10); do for i in $(seq 1 20); do bash scripts/qvm/run_eval_selection_methods.sh /root/projects/QASMBench/small/ $q FakeBrooklyn 4; done | tee logs/qvm/integration/frp/eval_selection/${q}-q_20_times.log; done

for q in $(seq 2 8); do
    for i in $(seq 1 50); do
        for c in 4 6 8; do
            bash scripts/qvm/run_eval_selection_methods.sh /root/projects/QASMBench/small/ $q FakeBrooklyn $c | tee logs/qvm/integration/frp/eval_selection/brooklyn/num_circ_${q}_group_${i}_cu_${c}.log
        done
    done
done
