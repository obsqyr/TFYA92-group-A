#!/bin/bash
#
#SBATCH -J testjob
#SBATCH -A liu-compute-2020-20
#SBATCH -t 00:05:00
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH -n 32
#
module load impi/.2018.3.222-eb

time mpirun python3 main.py

echo "job completed"
