for i in $(seq 1 9); do
    for j in $(seq 0 9); do
        rm -rf data/sv${i}${j}*
    done
done
rm -rf data/*
