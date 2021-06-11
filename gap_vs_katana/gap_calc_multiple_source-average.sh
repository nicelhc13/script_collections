#!/bin/bash

NUM_START_POINT=64

#for file in sssp*.out; do
for input in "kron" "road" "urand" "twitter" "web"; do 
  total_str="("
  for file in bfs/bfs-${input}*; do
    ALLTIME=(`grep -Po '(?<=Trial Time:).*' $file`)
    for line in ${ALLTIME[@]}; do
      line=`echo $line | xargs`
      IFS=" "
      read -ra line <<< $line
      for time in "${line[@]}"; do
        total_str+=${time}" + "
      done
    done
  done
  total_str+=" 0)/(3*${NUM_START_POINT})"
  echo $total_str
  total=`echo "scale=5; ${total_str}" | bc`
  echo $file"+"$input":"$total >> time.out
done
