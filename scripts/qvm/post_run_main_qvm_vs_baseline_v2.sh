log_dir=logs/qvm/main/random/cairo/circ_2_cu_4/
if [ $# -ne 1 ]; then
    echo "Usage: bash $0 <log-dir>"
    exit 1
fi

log_dir=$1

cd ${log_dir} && ls -l *.log | awk '{print $NF}' | sort -k1,1n | while read line; do log=$line; res=$(grep Fid $line); echo -e "${log}\t${res}"; done && cd -
