#!/bin/bash

for fname in $1/*.stats; do
  echo "Rscript AddOneMetric.R -i $fname -o $2.tmp"
  Rscript AddOneMetric.R -i $fname -o $2.tmp
done
Rscript PrintBarChart.R -i $2.tmp -o $2
mv $2 $1

rm $2.tmp
