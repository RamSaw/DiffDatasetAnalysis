#!/bin/bash
#SBATCH --gres=gpu
#SBATCH --cpus-per-task=22
#SBATCH --exclusive
module add singularity
srun singularity run --bind /home/mpravilov:/mnt msrc_mining.sif
