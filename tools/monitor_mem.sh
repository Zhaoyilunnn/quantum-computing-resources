#!/bin/sh

if [ $# -ne 2 ]; then
    echo "Usage: bash ./$0 <process-id> <profile-interval>"
    exit 1
fi

pid=$1
interval=$2

file="/proc/${pid}/status"
while ((test -f ${file})); do
  cat ${file} | grep VmRSS
  sleep $interval
done
