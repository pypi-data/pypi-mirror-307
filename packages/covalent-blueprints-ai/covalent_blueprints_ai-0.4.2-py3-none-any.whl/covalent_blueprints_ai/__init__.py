# Copyright 2024 Agnostiq Inc.
from pathlib import Path

from covalent_blueprints import register_blueprints_dir

from ._prefix import PREFIX
from .llama_chatbot import llama_chatbot
from .lora_fine_tuning import lora_fine_tuning
from .nvidia_llama_rag import nvidia_llama_rag
from .sdxl import sdxl
from .sdxl_turbo import sdxl_turbo
from .vllm_inference import vllm_inference

__all__ = [
    "llama_chatbot",
    "lora_fine_tuning",
    "nvidia_llama_rag",
    "sdxl",
    "sdxl_turbo",
    "vllm_inference",
]


register_blueprints_dir(
    name=PREFIX,
    install_dir=Path(__file__).parent,
    overwrite=True,
)
