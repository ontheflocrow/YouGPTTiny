lightning run model \
    --node-rank=0  \
    --main-address=192.168.48.36 \
    --accelerator=cuda \
    --devices=8 \
    --num-nodes=1 \
    pretrain/csg_tiny_120m_deepseek.py --devices 8 --train_data_dir /data/datasets_bak/processed/deepseek_llama2_tokenize_data/slim_star_combined --val_data_dir /data/datasets_bak/processed/deepseek_llama2_tokenize_data/slimpajama_validation
