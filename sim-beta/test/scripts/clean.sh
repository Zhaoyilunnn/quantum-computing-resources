#!/bin/bash

for i in $(seq 1 9); do
    for j in $(seq 0 9); do
        rm -rf sv${i}${j}*.bin
    done
done
