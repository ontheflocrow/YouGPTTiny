lightning run model \
    --node-rank=0  \
    --main-address=192.168.48.36 \
    --accelerator=cuda \
    --devices=8 \
    --num-nodes=1 \
    pretrain/csg_tiny_1B_llama_wanjuancc.py --devices 8 --train_data_dir /data/datasets/processed/llama2_tokenize_data/wanjuancc_train  --val_data_dir /data/datasets/processed/llama2_tokenize_data/slimpajama_validation
