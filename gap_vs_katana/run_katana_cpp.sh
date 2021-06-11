#!/bin/bash

INPUTS=( "GAP-road" "GAP-kron" "GAP-twitter" "GAP-web" )
#INPUTS=( "GAP-twitter" )
#BENCH=( "bfs" "sssp" "cc" "bc" "pagerank" "tc" "jaccard"
#        "kcore" "louvain" )

#BENCH=( "bfs" )
#BENCH=( "cc" )
BENCH=( "bfs" "pagerank" "tc" "sssp"
        "bc" "sssp" )
#BENCH=( "tc" "sssp"
#        "bc" "sssp" )


#BENCH=("kcore")
#INPUTS=( "GAP-road" )
#BENCH=( "bfs" "sssp" )
#BENCH=( "louvain" "pagerank" )

INPUT_DIR="/data1/inputs-gill/"
OUTPUT_DIR="/home/hlee/benchmarking/katana.output"

export AWS_EC2_METADATA_DISABLED=true

for app in "${BENCH[@]}"
do
  for input in "${INPUTS[@]}"
  do
    export KATANA_BIND_MAIN_THREAD=0
    echo "Test katana-python-binding.. ${app} + ${input}"
    STDERR_FILE=${OUTPUT_DIR}"/"${app}_${input}.out
    echo "python bench_cpp_algos.py --input-dir ${INPUT_DIR} --threads 96  \
	    			     --graph ${input} --application ${app} \
    				     --trials 3 --source-nodes ${INPUT_DIR}/${input}.start \
				         2> $STDERR_FILE 1>> $STDERR_FILE"

    python bench_cpp_algos.py --input-dir ${INPUT_DIR} --threads 96  \
	    			     --graph ${input} --application ${app} \
    				     --trials 3 --source-nodes ${INPUT_DIR}/${input}.start \
				         2> $STDERR_FILE 1>> $STDERR_FILE
  done
done

