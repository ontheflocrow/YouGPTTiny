python scripts/prepare_slimpajama.py \
    --source_path /data/datasets/cerebras/SlimPajama-627B \
    --tokenizer_path /data/datasets/tokenizers/deepseekLlamaTokenizer \
    --destination_path /data/datasets_bak/processed/deepseek_llama2_tokenize_data/slimpajama_validation \
    --split validation --percentage 1.0