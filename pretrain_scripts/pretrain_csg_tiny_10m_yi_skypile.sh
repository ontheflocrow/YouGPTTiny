lightning run model \
    --node-rank=0  \
    --main-address=192.168.48.36 \
    --accelerator=cuda \
    --devices=8 \
    --num-nodes=1 \
    pretrain/csg_tiny_10m_yi_skypile.py --devices 8 --train_data_dir /data/datasets_bak/processed/yi_llama2_tokenize_data/skypile_train --resume /data/project/TinyLlama/out/csg_tiny_10M_yi/iter-320000-ckpt.pth
