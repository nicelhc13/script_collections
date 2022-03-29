OMP_NUM_THREADS=32
echo $OMP_NUM_THREADS
salloc -N 1 -n 1 --cpus-per-task 32 --ntasks-per-node 1 mpirun --bind-to none -np 32 bin/./graphClustering -i -t 4 -a 0.75 -f friendster.bin
