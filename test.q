#!/bin/bash
#
#SBATCH -J testjob
#SBATCH -A liu-compute-2020-20
#SBATCH -t 00:05:00
#SBATCH -N 1
#SBATCH --exclusive
#
module load impi/.2018.1.163
mpirun echo "Hello world!"
echo "job completed"
