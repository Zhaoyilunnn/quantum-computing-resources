time=$(date +%s)
python benchmarks/qiskit_test.py $1
time_2=$(date +%s)
echo $((time_2-time))
