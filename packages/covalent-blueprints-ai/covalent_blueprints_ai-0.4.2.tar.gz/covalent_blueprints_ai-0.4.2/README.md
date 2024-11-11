# AI Blueprints for Covalent

A collection of AI blueprints for Covalent, built using the [`covalent-blueprints`](https://github.com/AgnostiqHQ/covalent-blueprints) library.

## Installation

```bash
pip install -U covalent-blueprints-ai
```

## Contents

This repository currently contains the following blueprints.

| name | description |
|----------|----------|
| `llama_chatbot()` | Deploys a Llama-like chatbot service. |
| `sdxl()` | Deploys a realistic image generator using basic on SDXL. |
| `sdxl_turbo()` | Deploys a fast image generator using SDXL-turbo. |
| `vllm_inference()` | Deploys an LLM service using vLLM. |
| `lora_fine_tuning()` | Fine-tunes and deploys a new LLM. |
| `nvidia_llama_rag()` | Deploys a RAG service using NVIDIA NIMs. |

See the [`/examples`](./examples) directory for usage examples.
