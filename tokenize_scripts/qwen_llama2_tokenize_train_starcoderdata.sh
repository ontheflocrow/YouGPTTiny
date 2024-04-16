python scripts/prepare_starcoder.py \
    --source_path /data/datasets/starcoderdata \
    --tokenizer_path /data/datasets/tokenizers/qwenLlamaTokenizer \
     --destination_path /data/datasets/processed/qwen_llama2_tokenize_data/starcoder_train \
     --split train --percentage 1.0
