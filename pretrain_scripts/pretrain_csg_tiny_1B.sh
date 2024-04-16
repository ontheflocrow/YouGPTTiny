lightning run model \
    --node-rank=0  \
    --main-address=192.168.48.36 \
    --accelerator=cuda \
    --devices=8 \
    --num-nodes=1 \
    pretrain/csg_tiny_1B.py --devices 8 --train_data_dir /data/datasets/processed/deepseek_llama2_tokenize_data/slim_star_combined  --val_data_dir /data/datasets/processed/deepseek_llama2_tokenize_data/slim_star_combined_validation
