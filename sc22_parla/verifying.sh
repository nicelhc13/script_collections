#!/bin/bash

INPUT_DIR="profiling_results_2022_0313"
GRAPH_INPUT_DIR="inputs_new"

export PYTHONPATH="../Parla.py"
for gpath in ${INPUT_DIR}/*; do
  commands="python verify.py -input "$gpath 
#if [[ $gpath == *".dm." ]]; then
#  fi  
  IFS="/"
  read -a gpath_split <<< "$gpath"
  IFS="."
  read -a gfname <<< "${gpath_split[1]}"
  unset IFS 
  gfname=${gfname[0]}
  if [[ $gfname == *"_gpu_"* ]]; then
    if [[ $gfname == *"_lazydm"* ]]; then
      gfname=${gfname::-16}
    elif [[ $gfname == *"_eagerdm"* ]]; then
      gfname=${gfname::-17}
    fi
  fi
  gfname=${gfname}".gph"
  commands+=" -graph "$GRAPH_INPUT_DIR"/"$gfname
  echo $commands
  $commands
done
