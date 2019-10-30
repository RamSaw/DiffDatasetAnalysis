#!/bin/bash
#SBATCH --gres=gpu
#SBATCH --cpus-per-task=22
#SBATCH --exclusive
module add singularity
srun singularity run --bind output/e003/output:/mnt msrc_mining.sif
