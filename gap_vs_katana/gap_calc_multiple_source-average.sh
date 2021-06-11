#!/bin/bash

NUM_START_POINT=3

#for file in sssp*.out; do
for file in bfs/*; do
  ALLTIME=(`grep -Po '(?<=Trial Time:).*' $file`)
  total_str="("
  for line in ${ALLTIME[@]}; do
    line=`echo $line | xargs`
    IFS=" "
    read -ra line <<< $line
    for time in "${line[@]}"; do
      total_str+=${time}" + "
    done
  done
  total_str+=" 0)/${NUM_START_POINT}"
  total=`echo "scale=5; ${total_str}" | bc`
  echo $file":"$total >> time.out
done
