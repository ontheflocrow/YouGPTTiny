fabric run model \
    --node-rank=0  \
    --main-address=192.168.48.36 \
    --accelerator=cuda \
    --devices=8 \
    --num-nodes=2 \
    pretrain/tinyllama_continue_train.py --devices 8 --train_data_dir /data/datasets/processed/llama2_tokenize_data/cosmopedia_train --val_data_dir /data/datasets/processed/llama2_tokenize_data/slimpajama_validation --resume /data/train/csg-tiny-1B/iter-220000-ckpt.pth