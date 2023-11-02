#!/bin/bash -l

# SLURM SUBMIT SCRIPT
#SBATCH --nodes=2        # This needs to match Fabric(num_nodes=...)
#SBATCH --ntasks-per-node=8     # This needs to match Fabric(devices=...)
#SBATCH --gres=gpu:8            # Request N GPUs per machine
#SBATCH --mem=0
#SBATCH --time=0-02:00:00

#SBATCH --output=/private/home/akokolis/myWorkspace/TinyLlama/results/slurm-%j.out
#SBATCH --error=/private/home/akokolis/myWorkspace/TinyLlama/results/slurm-%j.err

# Activate conda environment
# module load anaconda3/2023.03-1
module load cuda/11.8

conda activate tinyllama
conda env list


# Debugging flags (optional)
export NCCL_DEBUG=INFO
export PYTHONFAULTHANDLER=1

# On your cluster you might need this:
# export NCCL_SOCKET_IFNAME=^docker0,lo

# Run your training script
srun python /private/home/akokolis/myWorkspace/TinyLlama/pretrain/tinyllama.py --nodes 2 --devices 8 --train_data_dir /checkpoint/akokolis/tinyllama_datasets/data/slim_star_combined  --val_data_dir /checkpoint/akokolis/tinyllama_datasets/data/slim_star_combined