#!/bin/bash
#
#SBATCH -J testjob
#SBATCH -A liu-compute-2020-20
#SBATCH -t 03:00:00
#SBATCH -N 2
#SBATCH --exclusive
#SBATCH -n 64
#
module load Python/3.8.3-anaconda-2020.07-extras-nsc1
module load impi/.2018.1.163-eb
source activate tfya92
pip install chemparse
time mpirun ~/.conda/envs/tfya92/bin/python3 main.py

echo "job completed"
