# Copyright Lightning AI. Licensed under the Apache License 2.0, see LICENSE file.

import json
import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

import lightning as L
import torch
from lightning.fabric.plugins import BitsandbytesPrecision
from lm_eval import base, evaluator, tasks
from lm_eval.base import BaseLM
from multiprocessing import Pool


wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))

from lit_gpt import GPT, Config, Tokenizer
from lit_gpt.generate.base import generate
from lit_gpt.utils import CLI, check_valid_checkpoint_dir, get_default_supported_precision, load_checkpoint
import glob
import os
import numpy as np
import time
from multiprocessing import Process, cpu_count


class EvalHarnessBase(BaseLM):
    # Credits:
    # https://github.com/EleutherAI/gpt-neox/blob/main/eval_tasks/eval_adapter.py
    def __init__(self, fabric: L.Fabric, model: GPT, tokenizer: Tokenizer, batch_size: int):
        super().__init__()
        self.fabric = fabric
        self.model = model
        self.tokenizer = tokenizer
        self.batch_size_per_gpu = batch_size
        # with fabric.init_tensor():
        #     model.set_kv_cache(batch_size=batch_size)

    @classmethod
    def create_from_arg_string(cls, arg_string, additional_config=None):
        kwargs = {el.split("=")[0]: el.split("=")[1] for el in arg_string.split(",")}
        return cls(**kwargs, **additional_config)

    @property
    def eot_token_id(self):
        # we use EOT because end of *text* is more accurate for what we're doing than end of *sentence*
        return self.tokenizer.eos_id

    @property
    def max_length(self):
        # return self.model.max_seq_length
        return self.model.config.block_size

    @property
    def vocab_size(self):
        return self.tokenizer.vocab_size

    @property
    def max_gen_toks(self):
        return 256

    @property
    def batch_size(self):
        return self.batch_size_per_gpu * self.fabric.world_size

    @property
    def device(self):
        return self.fabric.device

    def tok_encode(self, string: str) -> List[int]:
        return self.tokenizer.encode(string, bos=False, eos=False).tolist()

    def tok_decode(self, tokens: List[int]) -> str:
        t = torch.tensor(tokens)
        return self.tokenizer.decode(t)

    @torch.inference_mode()
    def _model_call(self, inps):
        return self.model(inps)

    @torch.inference_mode()
    def _model_generate(self, context, max_length, eos_token_id) -> torch.Tensor:
        # this only supports batch size 1
        assert context.shape[0] == 1
        out = generate(self.model, context[0], max_length, eos_id=eos_token_id)
        for block in self.model.transformer.h:
            block.attn.kv_cache.reset_parameters()
        return out.unsqueeze(0)

    @torch.inference_mode()
    def run_eval_single(
            self, eval_tasks: List[str], num_fewshot: int, limit: Optional[int], bootstrap_iters: int, no_cache: bool
    ) -> Dict:

        print("global_rank:", self.fabric.global_rank)
        # Returns a list containing all values of the task registry that
        # match at least one of the patterns
        import fnmatch

        def pattern_match(patterns, source_list):
            task_names = set()
            for pattern in patterns:
                for matching in fnmatch.filter(source_list, pattern):
                    task_names.add(matching)
            return list(task_names)

        eval_tasks = pattern_match(eval_tasks, tasks.ALL_TASKS)
        print(f"Found tasks: {eval_tasks}")

        # **HACK INCOMING**:
        # first get task dict on local main rank
        # the tasks are downloaded *as they are initialized*, and the downloads don't like multithreading.
        # so we download them once on the local main rank, wait, and then initialize them on all other ranks, which *should* load from the cache.
        # if self.fabric.local_rank == 0:
        tasks.get_task_dict(eval_tasks)
        # torch barrier
        # self.fabric.barrier()
        # tasks.get_task_dict(eval_tasks)

        lm = self
        if not no_cache:
            lm = base.CachingLM(lm, "lm_cache/litgpt.db")
        results = evaluator.evaluate(
            lm=lm,
            task_dict=tasks.get_task_dict(eval_tasks),
            num_fewshot=num_fewshot,
            limit=limit,
            bootstrap_iters=bootstrap_iters,
        )
        results["config"] = dict(
            model=self.model.config.name,
            batch_size=self.batch_size,
            device=str(self.device),
            num_fewshot=num_fewshot,
            limit=limit,
            bootstrap_iters=bootstrap_iters,
            no_cache=no_cache,
        )
        return results

    @torch.inference_mode()
    def run_eval(
            self, eval_tasks: List[str], num_fewshot: int, limit: Optional[int], bootstrap_iters: int, no_cache: bool
    ) -> Dict:
        # Returns a list containing all values of the task registry that
        # match at least one of the patterns
        import fnmatch

        def pattern_match(patterns, source_list):
            task_names = set()
            for pattern in patterns:
                for matching in fnmatch.filter(source_list, pattern):
                    task_names.add(matching)
            return list(task_names)

        eval_tasks = pattern_match(eval_tasks, tasks.ALL_TASKS)
        print(f"Found tasks: {eval_tasks}")

        # **HACK INCOMING**:
        # first get task dict on local main rank
        # the tasks are downloaded *as they are initialized*, and the downloads don't like multithreading.
        # so we download them once on the local main rank, wait, and then initialize them on all other ranks, which *should* load from the cache.
        if self.fabric.local_rank == 0:
            tasks.get_task_dict(eval_tasks)
        # torch barrier
        self.fabric.barrier()
        tasks.get_task_dict(eval_tasks)

        lm = self
        if not no_cache:
            lm = base.CachingLM(lm, "lm_cache/litgpt.db")
        results = evaluator.evaluate(
            lm=lm,
            task_dict=tasks.get_task_dict(eval_tasks),
            num_fewshot=num_fewshot,
            limit=limit,
            bootstrap_iters=bootstrap_iters,
        )
        results["config"] = dict(
            model=self.model.config.name,
            batch_size=self.batch_size,
            device=str(self.device),
            num_fewshot=num_fewshot,
            limit=limit,
            bootstrap_iters=bootstrap_iters,
            no_cache=no_cache,
        )
        return results


@torch.inference_mode()
def run_eval_harness(
        checkpoint_dir: Path,
        tokenizer_dir: Path,
        precision: Optional[str] = None,
        quantize: Optional[Literal["bnb.nf4", "bnb.nf4-dq", "bnb.fp4", "bnb.fp4-dq", "bnb.int8"]] = None,
        eval_tasks: List[str] = ["arc_challenge", "piqa", "hellaswag", "hendrycksTest-*"],
        save_filepath: Optional[Path] = None,
        num_fewshot: int = 0,
        limit: Optional[int] = None,
        bootstrap_iters: int = 100000,
        no_cache: bool = True,
        devices: Union[int, list] = 1,
):  
    if precision is None:
        precision = get_default_supported_precision(training=False)

    plugins = None
    if quantize is not None and quantize.startswith("bnb."):
        if "mixed" in precision:
            raise ValueError("Quantization and mixed precision is not supported.")
        dtype = {"16-true": torch.float16, "bf16-true": torch.bfloat16, "32-true": torch.float32}[precision]
        plugins = BitsandbytesPrecision(quantize[4:], dtype)
        precision = None
    fabric = L.Fabric(devices=devices, precision=precision, plugins=plugins)

    # check_valid_checkpoint_dir(checkpoint_dir)
    tokenizer = Tokenizer(tokenizer_dir)

    model_name = "csg-wukong-1B"
    config = Config.from_name(model_name)

    # config = Config.from_name(checkpoint_dir / "model_config.yaml")
    # config = Config.from_file(checkpoint_dir / "model_config.yaml")

    # checkpoint_path = checkpoint_dir / "lit_model.pth"
    # for i, checkpoint_path in enumerate(checkpoint_dir):
    checkpoint_path = checkpoint_dir
    print("checkpoint_path", checkpoint_path)
    print(f"Loading model {str(checkpoint_path)!r} with {config.__dict__}", file=sys.stderr)
    with fabric.init_module(empty_init=False):
        model = GPT(config)

    model.eval()

    # model = fabric.setup(model)
    model = fabric.setup_module(model)
    # model = fabric.load(resume, state)

    # load_checkpoint(fabric, model, checkpoint_path)
    fabric.load(checkpoint_path, {"model": model})

    eval_harness = EvalHarnessBase(fabric, model, tokenizer, 128)

    results = eval_harness.run_eval(eval_tasks, num_fewshot, limit, bootstrap_iters, no_cache)
    print(results)
    if save_filepath is None:
        # print(results)
        pass
    else:
        print(f"Saving results to {str(save_filepath)!r}")
        save_filepath.parent.mkdir(parents=True, exist_ok=True)
        data = json.dumps(results)
        with open(save_filepath, "w") as fw:
            fw.write(data)


if __name__ == "__main__":
    torch.set_float32_matmul_precision("high")

    # CLI(run_eval_harness)
    
    checkpoint_dir = Path("/data/train/csg-tiny-1B/out_20240217/tinyllama_1b")
    tokenizer_dir = Path("/data/datasets/tokenizers/Llama2Tokenizer")
    precision = "bf16-true"
    eval_tasks = ["hellaswag", "openbookqa", "winogrande",  "arc_challenge", "arc_easy", "boolq", "piqa"]
    # eval_tasks = ["hellaswag"]

    save_filepath = "/data/train/csg-tiny-1B/out_20240217/result"
    filenames = sorted(glob.glob(str(checkpoint_dir / f"{'iter-'}*")))
    # filenames = ["/data/train/csg-tiny-1B/out_20240217/tinyllama_1b/iter-920000-ckpt.pth"]
    # filenames = sorted(glob.glob(checkpoint_dir + "/*", recursive=True), reverse=True)
    # only retrain subsets that follow the prefix in filenames_subset
    print("filenames:", filenames)

    # num_processes = 8
    # chunked_filenames = np.array_split(filenames, num_processes)
    batch_size = 128
    processes = []
    start_time = time.time()
    
    # async def 
    for i, filename in enumerate(filenames):
        # for j in range(i, i+8):
        # subset = filenames[i]
        # print("subset:", subset)
        print("filename:", filename)
        if 1:
            save_filepath_now = save_filepath + filename.split("/data/train/csg-tiny-1B/out_20240217/tinyllama_1b")[-1].split(".pth")[0] + ".json"
            print("save_filepath_now", save_filepath_now)
            # os.environ["CUDA_VISIBLE_DEVICES"] = "1"
            run_eval_harness(checkpoint_dir=filename, tokenizer_dir=tokenizer_dir, precision=precision,
                             eval_tasks=eval_tasks, save_filepath=Path(save_filepath_now), devices=[2])
        else:
            continue
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

    # print("checkpoint_dir:", checkpoint_dir)
    # # output_dir = Path("/data_share/train/tinyllama")
    
    # run_eval_harness(checkpoint_dir=checkpoint_dir, tokenizer_dir=tokenizer_dir,
    #                  precision=precision, eval_tasks=eval_tasks,
    #                  save_filepath=save_filepath, batch_size=128)
