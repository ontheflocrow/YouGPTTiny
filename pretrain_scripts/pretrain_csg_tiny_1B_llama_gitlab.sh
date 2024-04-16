lightning run model \
    --node-rank=0 \
    --main-address=192.168.48.36 \
    --accelerator=cuda \
    --devices=8 \
    --num-nodes=2 \
    pretrain/csg_tiny_1B_llama_gitlab.py --devices 8 --train_data_dir /data/datasets/processed/llama2_tokenize_data/gitlab_train
