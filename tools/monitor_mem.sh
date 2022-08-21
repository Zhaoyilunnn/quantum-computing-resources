#!/bin/sh

pid=$1

file="/proc/${pid}/status"
while ((test -f ${file})); do
  cat ${file} | grep VmRSS
  sleep 2
done
