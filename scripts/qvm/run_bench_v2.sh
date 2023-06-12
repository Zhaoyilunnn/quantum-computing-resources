#!/bin/bash

if [ $# -ne 4 ]; then
    echo "Usage: ./$0 <QASMBench-directory> <number-of-benches> <BackendName> <comp_unit_size>"
    echo "FakeBrooklyn: 65-q"
    echo "FakeCairo: 27-q"
    exit 1
fi

# Specify the directory to search in
search_dir=$1
num_select=$2

# Get the list of all subdirectories
sub_dirs=$(ls -d -l $search_dir/*/ | awk '{print $NF}')

# Count the number of subdirectories
num_dirs=$(echo "$sub_dirs" | wc -l)

# Check if the number of subdirectories is less than the specified count
if [ "$num_dirs" -lt "$num_select" ]; then
    echo "Insufficient number of subdirectories to select $num_select directories."
    exit 1
fi

# Generate an array of indices for shuffling
indices=($(seq 1 $(($num_dirs))))
shuf_indices=($(shuf -e "${indices[@]}"))

# Select the first n shuffled indices
random_indices=("${shuf_indices[@]:0:$num_select}")

# Extract the randomly selected subdirectories
random_subdirs=()
for index in "${random_indices[@]}"; do
    random_subdirs+=($(echo "$sub_dirs" | sed -n "${index}p"))
done

# Find the matching files in the selected subdirectories
files=()
for subdir in "${random_subdirs[@]}"; do
    matching_files=$(find "$subdir" -type f -name "$(basename "$subdir").qasm")
    if [ -n "$matching_files" ]; then
        files+=("$matching_files")
    fi
done

# Join the files' paths with comma as separator
files_string=$(IFS=,; echo "${files[*]}")

echo "Randomly selected files:"
echo "$files_string"

pytest -s -k "TestBenchDiffBackendQvmFrpV2 and test_two_bench_frp" tst/qvm/integration/bench_test.py --bench qasm --qasm ${files_string} --backend $3 --cu_size $4
