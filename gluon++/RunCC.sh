#!/bin/bash

#INPUTS=( "rmat15_cleaned_symmetric" "road-USA" )
#INPUTS=( "road-USA" )
INPUTS=( "friendster" )
#INPUTS=( "road-USA" "rmat15_cleaned_symmetric" "friendster" )
#INPUTS=( "rmat15_cleaned_symmetric" "friendster" "road-USA" )
#INPUTS=( "road-USA" )
#INPUTS=( "rmat15_cleaned_symmetric" )
NUM_THS_AND_HOSTS_LIST=( "16;4" )
#NUM_THS_AND_HOSTS_LIST=( "56;1" )
BASE_INPUT_DIR="/net/ohm/export/cdgc/hlee/workspace/katana-enterprise.build/inputs/current/propertygraphs";
#VERSION_MODES=( "-use_kvstore=false" "-use_kvstore=true" )
#VERSION_NAMES=( "ExistingKatana" "Shortcutting" )
#ALGOS=( "DistPush" "DistKVStoreShortcutting" "DistKVStorePointerJumping" )
#ALGO_NAMES=( "DistPush" "Shortcutting" "PointerJumping" )
#ALGOS=("DistPush" "DistKVStoreShortcutting")
#ALGOS=( "DistKVStorePointerJumping" )
#ALGOS=( "DistKVStoreShortcutting" )
#ALGOS=( "DistKVStoreShortcutting" "DistKVStoreShortcuttingDirectAccess")
ALGOS=( "DistKVStoreShortcuttingDirectAccess")
#ALGOS=( "DistPush" "DistKVStoreShortcutting" "DistKVStoreShortcuttingDirectAccess" "DistKVStorePointerJumping" )
#ALGOS=( "DistPush" "DistKVStoreShortcutting")
#ALGO_NAMES=( "LabelProp-NonKV" "Shortcutting-KV" "Shortcutting-NodeDirectAccess-KV" "PJ-KV" )
ALGO_NAMES=( "LabelProp-NodeDirectAccess-KV-GS" )
#ALGO_NAMES=( "LabelProp-NonKV" "LabelProp-KV" )
#ALGO_NAMES=( "LabelProp-KV-GS" "LabelProp-NodeDirectAccess-KV-GS" )
#ALGOS=( "DistPush" )
#ALGO_NAMES=( "DistPush" "Shortcutting" )
#ALGOS=( "DistPush" "DistKVStorePointerJumping" )
#ALGO_NAMES=( "PointerJumping" )


EXEC_MODE="Sync"
NUM_RUNS=1

BASE_COMMANDS=" ./connected-components-cli-dist --exec=${EXEC_MODE} --symmetricGraph "

GET_INPUT_PATH () {
  if [[ "$1" =~ .*"road-USA".* ]]; then
    echo "gs://katana-demo-datasets/rdg-datasets/v3/gap_road"
  elif [[ "$1" =~ .*"friendster".* ]]; then
    echo $BASE_INPUT_DIR"/friendster"
  elif [[ "$1" =~ .*"rmat15_cleaned_symmetric"*. ]]; then
    echo $BASE_INPUT_DIR"/rmat15_cleaned_symmetric"
  else
    echo "Input should be provided."
    exit 1
  fi
}

for INPUT in "${INPUTS[@]}";
do
  for RUN in $(seq 1 $NUM_RUNS)
  do
    OUTPUT_PATH=$INPUT"-stats-LabelProp-MultiHost"
    mkdir $OUTPUT_PATH
    echo $INPUT
    INPUT_PATH=$(GET_INPUT_PATH $INPUT)
    echo $INPUT_PATH
    for NUM_THS_AND_HOSTS in "${NUM_THS_AND_HOSTS_LIST[@]}";
    do
      for i in "${!ALGOS[@]}";
      do
        IFS=';' read -a RES_OPTION <<< $NUM_THS_AND_HOSTS
        NUM_THREADS=${RES_OPTION[0]}
        NUM_HOSTS=${RES_OPTION[1]}
        echo "Thread:" $NUM_THREADS ", and Hosts:" $NUM_HOSTS
        COMPLETE_COMMANDS="mpirun -np ${NUM_HOSTS} "$BASE_COMMANDS"-t=${NUM_THREADS} --algo=${ALGOS[i]} "$INPUT_PATH
#COMPLETE_COMMANDS=$BASE_COMMANDS"-t=${NUM_THREADS} --algo=${ALGOS[i]} "$INPUT_PATH
        STAT_FILE=$INPUT".CC."${ALGO_NAMES[i]}"."$NUM_THREADS"Threads."$NUM_HOSTS"Hosts.$RUN.stats"
        COMPLETE_COMMANDS=${COMPLETE_COMMANDS}" --statFile=${OUTPUT_PATH}/"${STAT_FILE}
        echo $COMPLETE_COMMANDS
        $COMPLETE_COMMANDS
      done
    done
  done
  echo "PrintBarChart.sh $OUTPUT_PATH $INPUT"
  ./PrintBarChart.sh $OUTPUT_PATH $INPUT
done
