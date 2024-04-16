import logging
import re

from lit_gpt.model import GPT
from lit_gpt.config import Config
from lit_gpt.prompts import PromptStyle
from lit_gpt.tokenizer import Tokenizer
from lit_gpt.fused_cross_entropy import FusedCrossEntropyLoss
from lightning_utilities.core.imports import RequirementCache

if not bool(RequirementCache("torch>=2.1.0dev")):
    raise ImportError(
        "Lit-GPT requires torch nightly (future torch 2.1). Please follow the installation instructions in the"
        " repository README.md"
    )
_LIGHTNING_AVAILABLE = RequirementCache("lightning>=2.1.0.dev0")
if not bool(_LIGHTNING_AVAILABLE):
    raise ImportError(
        "Lit-GPT requires Lightning nightly (future lightning 2.1). Please run:\n"
        f" pip uninstall -y lightning; pip install -r requirements.txt\n{str(_LIGHTNING_AVAILABLE)}"
    )

# Suppress excessive warnings, see https://github.com/pytorch/pytorch/issues/111632
pattern = re.compile(".*Profiler function .* will be ignored")
logging.getLogger("torch._dynamo.variables.torch").addFilter(lambda record: not pattern.search(record.getMessage()))

# __all__ = ["GPT", "Config", "Tokenizer"]
__all__ = ["GPT", "Config", "Tokenizer", "PromptStyle"]

