import torch
import transformers
import os
import argparse
from pathlib import Path
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline

def load_model_and_maybe_tokenizer(out_dir, tokenizer_path = None):
    model_path = os.path.join(out_dir, "pytorch_model.bin")
    state_dict = torch.load(model_path)

    model = LlamaForCausalLM.from_pretrained(
        out_dir, local_files_only=True, state_dict=state_dict
    )
    model = model.to("cuda")

    if tokenizer_path is not None:
        # tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
        tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
        return model, tokenizer
    
    return model, None

def generate_text(prompt, model, tokenizer):
    text_generator = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
        tokenizer=tokenizer
    )

    formatted_prompt = f"Question: {prompt} Answer:"

    sequences = text_generator(
        formatted_prompt,
        do_sample=True,
        top_k=5,
        top_p=0.9,
        num_return_sequences=1,
        repetition_penalty=1.5,
        max_new_tokens=128,
    )

    for seq in sequences:
        print(f"Result: {seq['generated_text']}")

def main():
    parser = argparse.ArgumentParser(description="Generate text with LLaMA model.")
    parser.add_argument("--in_dir", type=str,
                                    help="Directory for the pretrained model converted from saved checkpoint using convert_pytorch_to_hf.sh",
                                    default=str(Path("out") / "pretrained_300M_515000"))
    parser.add_argument("--out_dir", type=str,
                                     help="Output directory for the pretrained model.",
                                     default=str(Path("out") / "pretrained_300M_515000" / "huggingface"))
    parser.add_argument("--tokenizer_path", type=str,
                                            help="Path to the tokenizer.",
                                            default="llama-tokenizer")
    parser.add_argument("--inference_only", action='store_true',
                                            help="Only run inference without saving and uploading the model.")

    args = parser.parse_args()

    model, tokenizer = load_model_and_maybe_tokenizer(args.in_dir, args.tokenizer_path)

    if not args.inference_only:
        if not os.path.exists(args.out_dir):
            os.mkdir(args.out_dir)
        model.save_pretrained(args.out_dir)
        model.push_to_hub("keeeeenw/MicroLlama")
        # reload model from huggingface
        model = LlamaForCausalLM.from_pretrained(
            "keeeeenw/MicroLlama"
        )

    # reload model from huggingface
    model = LlamaForCausalLM.from_pretrained(
        "keeeeenw/MicroLlama")
    generate_text("Who are you?", model, tokenizer)

if __name__ == "__main__":
    main()