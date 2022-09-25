#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: sh $0 <log-file>"
    echo "E.g., sh $0 top.random.28.26.24.log"
    exit 1
fi

cat $1 | grep simulator | 
    awk 'BEGIN{
        sum=0;cnt=0
    }
    {
        if($(NF-4)>10) {
            sum+=$(NF-4);cnt+=1
        }
    }; END {print sum/cnt}'
