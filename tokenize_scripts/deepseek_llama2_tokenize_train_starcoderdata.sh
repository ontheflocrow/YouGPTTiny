python scripts/prepare_starcoder.py \
    --source_path /data/datasets/starcoderdata \
    --tokenizer_path /data/datasets/tokenizers/deepseekLlamaTokenizer \
     --destination_path /data/datasets_bak/processed/deepseek_llama2_tokenize_data/starcoder_train \
     --split train --percentage 1.0
