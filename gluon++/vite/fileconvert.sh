salloc -N 1 -n 1 --cpus-per-task 32 --ntasks-per-node 1 mpirun --bind-to none -np 1 ./bin/fileConvert -z -u -i -f friendster.el -o friendster.bin 2>&1 converting.log 
