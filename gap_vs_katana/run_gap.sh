GAPBS_DIR=/home/hlee/gapbs
GRAPH_DIR=/data2/gap-inputs
OUT_DIR=/home/hlee/benchmarking/gap.output/
START_DIR=/data1/inputs-gill

THREADS=96
#THREAD_LIMIT=$THREADS-1
export OMP_NUM_THREADS=${THREADS}
#export GOMP_CPU_AFFINITY="0-55"
#PRE="numactl -N 0 -m 0"
#PRE="numactl -N 0,1 -m 0,1"
PRE=""

for input in "kron" "urand" "twitter" "web" "road"; do
  echo $input
  cat $START_DIR"/GAP-${input}.start" | while read SNODE; do
    $PRE $GAPBS_DIR/bfs -f $GRAPH_DIR/${input}.sg -n3 -r${SNODE} -a > $OUT_DIR/bfs/bfs-${input}-t$THREADS-s$SNODE.out
  done
done
echo "DON>..."
: '
$PRE $GAPBS_DIR/bfs -f $GRAPH_DIR/kron.sg -n3 -a > $OUT_DIR/bfs-kron-t$THREADS.out
echo "urand-bfs"
$PRE $GAPBS_DIR/bfs -f $GRAPH_DIR/urand.sg -n3 -a > $OUT_DIR/bfs-urand-t$THREADS.out
echo "twitter-bfs"
$PRE $GAPBS_DIR/bfs -f $GRAPH_DIR/twitter.sg -n3 -a > $OUT_DIR/bfs-twitter-t$THREADS.out
echo "web-bfs"
$PRE $GAPBS_DIR/bfs -f $GRAPH_DIR/web.sg -n3 -a > $OUT_DIR/bfs-web-t$THREADS.out
echo "road-bfs"
$PRE $GAPBS_DIR/bfs -f $GRAPH_DIR/road.sg -n3 -a > $OUT_DIR/bfs-road-t$THREADS.out
'

: '
# cc
echo "kron-cc"
$PRE $GAPBS_DIR/cc -f $GRAPH_DIR/kron.sg -n3 -a > $OUT_DIR/cc-kron-t$THREADS.out
echo "urand-cc"
$PRE $GAPBS_DIR/cc -f $GRAPH_DIR/urand.sg -n3 -a > $OUT_DIR/cc-urand-t$THREADS.out
echo "twitter-cc"
$PRE $GAPBS_DIR/cc -f $GRAPH_DIR/twitter.sg -n3 -a > $OUT_DIR/cc-twitter-t$THREADS.out
echo "web-cc"
$PRE $GAPBS_DIR/cc -f $GRAPH_DIR/web.sg -n3 -a > $OUT_DIR/cc-web-t$THREADS.out
echo "road-cc"
$PRE $GAPBS_DIR/cc -f $GRAPH_DIR/road.sg -n3 -a > $OUT_DIR/cc-road-t$THREADS.out
'

: '
# pr
echo "kron-pr"
$PRE $GAPBS_DIR/pr -f $GRAPH_DIR/kron.sg -i1000 -t1e-4 -n3 -a > $OUT_DIR/pr-kron-t$THREADS.out
echo "urand-pr"
$PRE $GAPBS_DIR/pr -f $GRAPH_DIR/urand.sg -i1000 -t1e-4 -n3 -a > $OUT_DIR/pr-urand-t$THREADS.out
echo "twitter-pr"
$PRE $GAPBS_DIR/pr -f $GRAPH_DIR/twitter.sg -i1000 -t1e-4 -n3 -a > $OUT_DIR/pr-twitter-t$THREADS.out
echo "web-pr"
$PRE $GAPBS_DIR/pr -f $GRAPH_DIR/web.sg -i1000 -t1e-4 -n3 -a > $OUT_DIR/pr-web-t$THREADS.out
echo "road-pr"
$PRE $GAPBS_DIR/pr -f $GRAPH_DIR/road.sg -i1000 -t1e-4 -n3 -a > $OUT_DIR/pr-road-t$THREADS.out
'

: '
# bc
echo "kron-bc"
$PRE $GAPBS_DIR/bc -f $GRAPH_DIR/kron.sg -i4 -n16 -a > $OUT_DIR/bc-kron-t$THREADS.out
echo "urand-bc"
$PRE $GAPBS_DIR/bc -f $GRAPH_DIR/urand.sg -i4 -n16 -a > $OUT_DIR/bc-urand-t$THREADS.out
echo "twitter-bc"
$PRE $GAPBS_DIR/bc -f $GRAPH_DIR/twitter.sg -i4 -n16 -a > $OUT_DIR/bc-twitter-t$THREADS.out
echo "web-bc"
$PRE $GAPBS_DIR/bc -f $GRAPH_DIR/web.sg -i4 -n16 -a > $OUT_DIR/bc-web-t$THREADS.out
echo "road-bc"
OMP_NUM_THREADS=16 $GAPBS_DIR/bc -f $GRAPH_DIR/road.sg -i4 -n16 -a > $OUT_DIR/bc-road-t$THREADS.out
'


: '
echo "kron-tc"
$PRE $GAPBS_DIR/tc -f $GRAPH_DIR/kronU.sg -n3 -a > $OUT_DIR/tc-kron-t$THREADS.out
echo "urand-tc"
$PRE $GAPBS_DIR/tc -f $GRAPH_DIR/urandU.sg -n3 -a > $OUT_DIR/tc-urand-t$THREADS.out
echo "twitter-tc"
$PRE $GAPBS_DIR/tc -f $GRAPH_DIR/twitterU.sg -n3 -a > $OUT_DIR/tc-twitter-t$THREADS.out
echo "web-tc"
$PRE $GAPBS_DIR/tc -f $GRAPH_DIR/webU.sg -n3 -a > $OUT_DIR/tc-web-t$THREADS.out
echo "road-tc"
$PRE $GAPBS_DIR/tc -f $GRAPH_DIR/roadU.sg -n3 -a > $OUT_DIR/tc-road-t$THREADS.out
'

: '
echo "kron-sssp"
$PRE $GAPBS_DIR/sssp -f $GRAPH_DIR/kron.wsg -n64 -d1 -a > $OUT_DIR/sssp-kron-t$THREADS.out
echo "urand-sssp"
$PRE $GAPBS_DIR/sssp -f $GRAPH_DIR/urand.wsg -n64 -d1 -a > $OUT_DIR/sssp-urand-t$THREADS.out
echo "twitter-sssp"
$PRE $GAPBS_DIR/sssp -f $GRAPH_DIR/twitter.wsg -n64 -d1 -a > $OUT_DIR/sssp-twitter-t$THREADS.out
echo "web-sssp"
$PRE $GAPBS_DIR/sssp -f $GRAPH_DIR/web.wsg -n64 -d1 -a > $OUT_DIR/sssp-web-t$THREADS.out
echo "road-sssp"
$GAPBS_DIR/sssp -f $GRAPH_DIR/road.wsg -n64 -d13 -a > $OUT_DIR/sssp-road-t$THREADS.out
'
