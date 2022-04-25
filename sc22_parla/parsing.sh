#!/bin/bash

delim="_gpu_"
OUTPUT="parsed_results.out"

rm $OUTPUT

INPUT=$1

for fpath in $INPUT/*; do
  IFS="/"
  read -a fname <<< "$fpath"
  fname=${fname[1]}
  IFS="."
  read -a etype <<< "${fname}"
  unset IFS
  afname=$etype

  echo ">>>>>>>> "$fpath

  ptype="user"
  if [[ $fname == *"policy"* ]]; then
    ptype="policy"
  fi

  if [[ $etype == *"_gpu_"* ]]; then
    afname=( "${etype%%"$delim"*}" ) # independent_80%
    etype=${etype#*"$delim"}
    IFS="_" # 100KB_1g_eagerdm
    read -a etype <<< "${etype}"
    dsize=${etype[0]}
    etype=${etype[1]}
    IFS="g"
    read -a num_gpu <<< $etype # 

    afname=( "${afname%%"_"$num_gpu"g"*}" )
    afname+="_gpu."$ptype".gph."$num_gpu".analysis"
    unset IFS
  else
    afname+="."$ptype".gph.analysis"
  fi

#commands="python parser.py -actual "$fpath" -expect inputs/"$afname" -output="$OUTPUT
  commands="python parser_extract_median.py -actual "$fpath" -expect inputs/"$afname" -output="$OUTPUT" -branch=$2"
#commands="python parser_withoutexp.py -actual "$fpath" -output="$OUTPUT
#echo $commands
  $commands
done
