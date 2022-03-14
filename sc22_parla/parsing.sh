#!/bin/bash

delim="_gpu_"
OUTPUT="parsed_results.out"

rm $OUTPUT

for fpath in profiling_results/*; do
  IFS="/"
  read -a fname <<< "$fpath"
  fname=${fname[1]}
  IFS="."
  read -a etype <<< "${fname}"
  unset IFS
  afname=$etype
  if [[ $etype == *"_gpu_"* ]]; then
    afname=( "${etype%%"$delim"*}" )
    etype=${etype#*"$delim"}
    IFS="g"
    read -a num_gpu <<< $etype
    afname=( "${afname%%"_"$num_gpu"g"*}" )
    afname+="_gpu.gph."$num_gpu".analysis"
    unset IFS
  else
    afname+=".gph.analysis"
  fi
  commands="python parser.py -actual "$fpath" -expect profiling_expects/"$afname" -output="$OUTPUT
  echo $commands
  $commands
done
