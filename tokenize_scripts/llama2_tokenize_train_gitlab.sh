python scripts/prepare_gitlab.py \
    --source_path /data/datasets/gitlab_model/train \
    --tokenizer_path /data/datasets/tokenizers/Llama2Tokenizer \
    --destination_path /data/datasets/processed/llama2_tokenize_data/gitlab_train \
    --split train --percentage 1.0