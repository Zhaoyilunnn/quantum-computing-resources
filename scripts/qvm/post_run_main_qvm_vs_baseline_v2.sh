# log_dir=logs/qvm/main/random/cairo/circ_2_cu_4/
# if [ $# -ne 2 ]; then
#     echo "Usage: bash $0 <log-dir> <key>"
#     exit 1
# fi
#
# log_dir=$1
# key=$2
#
# cd ${log_dir} && ls -l *.log | awk '{print $NF}' | sort -k1,1n | while read line; do log=$line; res=$(grep ${key} $line); echo -e "${log}\t${res}"; done && cd -
log_dir=logs/qvm/main/random/cairo/circ_2_cu_4/
if [ $# -lt 2 ]; then
    echo "Usage: bash $0 <log-dir> <key1,key2,key3...>"
    exit 1
fi

log_dir=$1
keys=$2

cd ${log_dir} && ls -l *.log | awk '{print $NF}' | sort -k1,1n | while read line; do
    log=$line
    res=""
    for key in $(echo ${keys} | tr ',' ' '); do
        result=$(grep ${key} $line)
        res="${res}\t${result}"
    done
    echo -e "${log}${res}"
done

cd -
