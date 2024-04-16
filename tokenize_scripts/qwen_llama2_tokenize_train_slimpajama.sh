python scripts/prepare_slimpajama.py \
    --source_path /data/datasets/cerebras/SlimPajama-627B \
    --tokenizer_path /data/datasets/tokenizers/qwenLlamaTokenizer \
    --destination_path /data/datasets/processed/qwen_llama2_tokenize_data/slimpajama_train \
    --split train --percentage 1.0