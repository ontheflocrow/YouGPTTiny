#!/bin/bash -l

#SBATCH --nodes=1        # This needs to match Fabric(num_nodes=...)
### SBATCH --gpus-per-node=8
#SBATCH --ntasks-per-node=8     # This needs to match Fabric(devices=...)
#SBATCH --gres=gpu:8            # Request N GPUs per machine
### SBATCH --gpus-per-task=1
#SBATCH --mem=0
#SBATCH --time=0-02:00:00

#SBATCH --output=/data/home/akokolis/myWorkspace/TinyLlama/results/slurm-%j.out
#SBATCH --error=/data/home/akokolis/myWorkspace/TinyLlama/results/slurm-%j.err

# Activate conda environment
# module load anaconda3/2023.03-1
# module load cuda/11.8

conda activate tinyllama
conda env list

echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
echo "PATH $PATH"

# Debugging flags (optional)
export NCCL_DEBUG=INFO
export PYTHONFAULTHANDLER=1

# LD_PRELOAD=/usr/local/cuda-11.8/lib/libnccl.so.2.16.2
LD_PRELOAD=/opt/aws-ofi-nccl/lib/libnccl-net.so
# On your cluster you might need this:
# export NCCL_SOCKET_IFNAME=^docker0,lo

# Run your training script
srun python /data/home/akokolis/myWorkspace/TinyLlama/pretrain/tinyllama.py --nodes 2 --devices 8 --train_data_dir /fsx-checkpoints/akokolis/data  --val_data_dir /fsx-checkpoints/akokolis/data
