#!/bin/bash

#INPUTS=( "rmat15_cleaned_symmetric" "road-USA" )
#INPUTS=( "road-USA" )
#INPUTS=( "friendster" )
#INPUTS=( "road-USA" "rmat15_cleaned_symmetric" "friendster" )
INPUTS=( "road-USA" "ldbc_1" "ldbc_10" "twitter40" )
#INPUTS=( "rmat15_cleaned_symmetric" )
#NUM_THS_AND_HOSTS_LIST=( "16;4" )
NUM_THS_AND_HOSTS_LIST=( "56;1" )
BASE_INPUT_DIR="/net/ohm/export/cdgc/hlee/workspace/katana-enterprise.build/inputs/current/propertygraphs";
#VERSION_MODES=( "-use_kvstore=false" "-use_kvstore=true" )
#VERSION_NAMES=( "ExistingKatana" "Shortcutting" )
ALGOS=( "-use_kvstore=false" "-use_kvstore=true" )
ALGO_NAMES=("Louvain-NonKV" "Louvain-KV")

NUM_RUNS=1

BASE_COMMANDS=" ./louvain-clustering-cli-dist --symmetricGraph --modularity_threshold_total=0.0001 --modularity_threshold_per_round=0.0001 --max_iterations=1000 --min_graph_size=100 --partition=blocked-oec "

GET_INPUT_PATH () {
  if [[ "$1" =~ .*"road-USA".* ]]; then
    echo "gs://katana-demo-datasets/rdg-datasets/v3/gap_road"
  elif [[ "$1" =~ .*"friendster".* ]]; then
    echo $BASE_INPUT_DIR"/friendster"
  elif [[ "$1" =~ .*"rmat15_cleaned_symmetric"*. ]]; then
    echo $BASE_INPUT_DIR"/rmat15_cleaned_symmetric"
  elif [[ "$1" =~ .*"ldbc_10".* ]]; then
    echo "gs://katana-demo-datasets/rdg-datasets/v3/ldbc_10_"
  elif [[ "$1" =~ .*"ldbc_1".* ]]; then
    echo "gs://katana-demo-datasets/rdg-datasets/v3/ldbc_1_"
  elif [[ "$1" =~ .*"twitter40".* ]]; then
    echo "gs://katana-demo-datasets/rdg-datasets/v3/twitter40"
  else
    echo "Input should be provided."
    exit 1
  fi
}

for INPUT in "${INPUTS[@]}";
do
  for RUN in $(seq 1 $NUM_RUNS)
  do
    OUTPUT_PATH=$INPUT"-stats"
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
        COMPLETE_COMMANDS=$BASE_COMMANDS"-t=${NUM_THREADS} ${ALGOS[i]} "$INPUT_PATH
        STAT_FILE=$INPUT".LV."${ALGO_NAMES[i]}"."$NUM_THREADS"Threads."$NUM_HOSTS"Hosts.$RUN.stats"
        COMPLETE_COMMANDS=${COMPLETE_COMMANDS}" --statFile=${OUTPUT_PATH}/"${STAT_FILE}
        echo $COMPLETE_COMMANDS
        $COMPLETE_COMMANDS
      done
    done
  done
  echo "PrintBarChart.sh $OUTPUT_PATH $INPUT"
  ./PrintBarChart.sh $OUTPUT_PATH $INPUT
done
