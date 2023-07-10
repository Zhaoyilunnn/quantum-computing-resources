if [ $# -ne 3 ]; then
    echo "Usage: bash $0 <frp-oracle-res-file> <native-oracle-res-file> <metric: pst|kl>"
    exit 1
fi

frp_oracle=$1
native_oracle=$2
metric=$3

# awk -F '\t' '{print $NF}' logs/qvm/oracle/brooklyn/frp_oracle_results.txt | paste logs/qvm/oracle/brooklyn/results.txt - | awk -F'\t' '{if($2>$3){a=$3;} else {a=$2;} print $1"\t"a}'
if [ $metric = "kl" ]; then
    awk -F '\t' '{print $NF}' ${frp_oracle} | paste ${native_oracle} - | awk -F'\t' '{if($2>$3){a=$3;} else {a=$2;} print $1"\t"a}'
elif [ $metric = "pst" ]; then
    awk -F '\t' '{print $NF}' ${frp_oracle} | paste ${native_oracle} - | awk -F'\t' '{if($2<$3){a=$3;} else {a=$2;} print $1"\t"a}'
else
    echo "metric should be either `pst` or `kl`"
    exit 1
fi
