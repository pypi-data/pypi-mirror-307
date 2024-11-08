# Copyright 2024 Agnostiq Inc.
"""Fine tune an LLM on a local or public dataset using LoRA.

Optionally deploy the fine-tuned model as a text generation service.
"""

import shutil
from pathlib import Path
from typing import Any, Callable, Union
from uuid import uuid4

import covalent as ct
import covalent_cloud as cc
from covalent_cloud.function_serve.deployment import Deployment

from covalent_blueprints_ai._versions import covalent_blueprints_pkg, covalent_cloud_pkg

# cc.save_api_key("you-api-key")

FT_ENV = "lora-fine-tuning@blueprints"

ft_volume = cc.volume("lora-fine-tuning")

cc.create_env(
    name=FT_ENV,
    pip=[
        "accelerate==0.29.1",
        "bitsandbytes==0.43.0",
        "datasets==2.18.0",
        "peft==0.10.0",
        "scipy==1.12.0",
        "sentencepiece==0.2.0",
        "torch==2.2.2",
        "transformers==4.39.3",
        "trl==0.8.1",
        "tiktoken==0.7.0",
        "einops==0.8.0",
        "pytest==8.2.2",
        "protobuf==5.27.2",
        covalent_cloud_pkg,
        covalent_blueprints_pkg,
    ],
    wait=True,
)

service_executor = cc.CloudExecutor(
    env=FT_ENV,
    num_cpus=6,
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.L40,
    memory="48GB",
    time_limit="3 hours",
    volume_id=ft_volume.id,
)

fine_tuning_executor = cc.CloudExecutor(
    env=FT_ENV,
    num_cpus=6,
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.L40,
    memory="48GB",
    time_limit="3 hours",
    volume_id=ft_volume.id,
)


@ct.electron(executor=fine_tuning_executor)
def peft_fine_tuning(
    model_id,
    data,
    dataset_map_func,
    split,
    ft_args,
    device_map,
    model_kwargs,
    use_saved_model,
    save_model_to_volume,
):
    """Fine tune a model using the PEFT-LoRA method and save it to a
    volume."""
    # pylint: disable=import-outside-toplevel, import-error

    import torch
    from covalent_blueprints.blueprints.utilities import pick_largest_fs
    from datasets import Dataset, DatasetDict, load_dataset, load_from_disk
    from peft import LoraConfig
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TrainingArguments,
    )
    from trl import SFTTrainer

    local_cache_dir = pick_largest_fs("/scratch", "/tmp")
    saved_model_name = str(model_id).replace("/", "--")
    saved_model_path = ft_volume / saved_model_name

    if use_saved_model and saved_model_path.exists():
        model_id = str(saved_model_path)

    if not ft_args.get("use_quantization", False):
        quantization_config = None
    else:
        bnb_4bit_compute_dtype = getattr(torch, ft_args["bnb_4bit_compute_dtype"])
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=ft_args["load_in_4bit"],
            bnb_4bit_quant_type=ft_args["bnb_4bit_quant_type"],
            bnb_4bit_compute_dtype=bnb_4bit_compute_dtype,
            bnb_4bit_use_double_quant=ft_args["bnb_4bit_use_double_quant"],
        )

    # Load and configure the downloaded model from pretrained
    print("💿 Loading base model:", model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=quantization_config,
        device_map=device_map,
        trust_remote_code=True,
        cache_dir=local_cache_dir,
        **model_kwargs,
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # Load and configure the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    if save_model_to_volume:
        shutil.rmtree(saved_model_path, ignore_errors=True)
        print("💾 Saving base model to volume:", saved_model_path)
        model.save_pretrained(saved_model_path)
        tokenizer.save_pretrained(saved_model_path)

    # Try download dataset else try to load from disk
    if isinstance(data, (Dataset, DatasetDict)):
        dataset = data
    else:
        try:
            dataset = load_dataset(data, split=split)
        except Exception:
            dataset = load_from_disk(data, keep_in_memory=True)

    if dataset_map_func:
        dataset = dataset.map(dataset_map_func)

    # Find linear layers in the model
    if ft_args["target_modules"] == "linear":
        unique_layers = set()
        for name, module in model.named_modules():
            if "Linear" in str(type(module)):
                layer_type = name.split(".")[-1]
                unique_layers.add(layer_type)
        ft_args["target_modules"] = list(unique_layers)

    # Set up supervised fine-tuning trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=LoraConfig(
            lora_alpha=ft_args["lora_alpha"],
            lora_dropout=ft_args["lora_dropout"],
            r=ft_args["r"],
            bias=ft_args["bias"],
            task_type=ft_args["task_type"],
            target_modules=ft_args["target_modules"],
        ),
        tokenizer=tokenizer,
        args=TrainingArguments(
            output_dir=ft_args["output_dir"],
            num_train_epochs=ft_args["num_train_epochs"],
            per_device_train_batch_size=ft_args["per_device_train_batch_size"],
            gradient_accumulation_steps=ft_args["gradient_accumulation_steps"],
            optim=ft_args["optim"],
            save_strategy=ft_args["save_strategy"],
            save_total_limit=ft_args["save_total_limit"],
            learning_rate=ft_args["learning_rate"],
            weight_decay=ft_args["weight_decay"],
            fp16=ft_args["fp16"],
            bf16=ft_args["bf16"],
            max_grad_norm=ft_args["max_grad_norm"],
            max_steps=ft_args["max_steps"],
            warmup_ratio=ft_args["warmup_ratio"],
            group_by_length=ft_args["group_by_length"],
            lr_scheduler_type=ft_args["lr_scheduler_type"],
            report_to=ft_args["report_to"],
        ),
        dataset_text_field=ft_args["dataset_text_field"],
        max_seq_length=ft_args["max_seq_length"],
        packing=ft_args["packing"],
        dataset_batch_size=ft_args["dataset_batch_size"],
    )

    # Run training
    trainer.train()

    # Save trained model
    new_model_filename = model_id.split("/")[-1] + f"_{uuid4()}"
    ft_model_path = ft_volume / new_model_filename
    trainer.model.save_pretrained(ft_model_path)
    trainer.tokenizer.save_pretrained(ft_model_path)
    print(f"📦 Saving fine-tuned model to {ft_model_path}")

    return ft_model_path


@cc.service(executor=service_executor, name="LoRA Fine-Tuned LLM", volume=ft_volume)
def llm_service(ft_model_path, device_map):
    """Serves a LoRA fine-tuned LLM for text generation."""
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    # Load model and tokenizer
    print(f"💿 loading model from: {ft_model_path}")
    model = AutoModelForCausalLM.from_pretrained(
        str(ft_model_path),
        device_map=device_map,
        trust_remote_code=True,
        cache_dir=ft_model_path.parent,
    )
    print(f"💿 loading tokenizer from: {ft_model_path}")
    tokenizer = AutoTokenizer.from_pretrained(
        str(ft_model_path),
        trust_remote_code=True,
        cache_dir=ft_model_path.parent,
    )
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    return {"pipe": pipe}


@llm_service.endpoint("/generate", name="Generate Response")
def generate(
    pipe=None,
    *,
    prompt=None,
    max_new_tokens=200,
    truncation=True,
    temperature=0.9,
):
    """Generate a response to a prompt.

    Kwargs:
        prompt: The prompt to generate a response to.
        max_new_tokens: Maximum number of new tokens to generate.
            Defaults to 200.
        truncation: Whether to truncate the generated text.
            Defaults to True.
        temperature: The temperature for sampling. Defaults to 0.9.

    Returns:
        The generated text.
    """
    if prompt is None:
        return "Please provide a prompt."

    output = pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        truncation=truncation,
        temperature=temperature,
    )
    return output[0]["generated_text"]


@llm_service.endpoint("/stream", name="Stream Response")
def generate_stream(
    pipe=None,
    *,
    prompt=None,
    max_new_tokens=200,
    temperature=0.9,
):
    """Generate and stream a response to a prompt.

    Kwargs:
        prompt: The prompt to generate a response to.
        max_new_tokens: Maximum number of new tokens to generate.
            Defaults to 200.
        temperature: The temperature for sampling. Defaults to 0.9.

    Yields:
        Tokens of the generated text.
    """

    if prompt is None:
        yield "Please provide a prompt."

    else:
        import torch

        def _starts_with_space(tokenizer, token_id):
            token = tokenizer.convert_ids_to_tokens(token_id)
            return token.startswith("▁")

        model = pipe.model
        tokenizer = pipe.tokenizer
        _input = tokenizer(prompt, return_tensors="pt").to("cuda")

        for output_length in range(max_new_tokens):
            # Generate next token
            output = model.generate(
                **_input,
                max_new_tokens=1,
                temperature=temperature,
                pad_token_id=tokenizer.eos_token_id,
            )
            # Check for stopping condition
            current_token_id = output[0][-1]
            if current_token_id == tokenizer.eos_token_id:
                break
            # Decode token
            current_token = tokenizer.decode(current_token_id, skip_special_tokens=True)
            if (
                _starts_with_space(tokenizer, current_token_id.item())
                and output_length > 1
            ):
                current_token = " " + current_token

            yield current_token

            # Update input for next iteration.
            # Output grows in size with each iteration.
            _input = {
                "input_ids": output.to("cuda"),
                "attention_mask": torch.ones(1, len(output[0])).to("cuda"),
            }


lattice_executor = cc.CloudExecutor(
    env=FT_ENV,
    num_cpus=2,
    memory="12GB",
    time_limit="3 hours",
    volume_id=ft_volume.id,
)


@ct.lattice(
    executor=lattice_executor,
    workflow_executor=lattice_executor,
)
def workflow_fine_tune_and_deploy_service(
    model_id: str,
    data: Union[str, Path, Any],
    split: str,
    device_map: Union[str, dict],
    use_quantization: bool,
    load_in_4bit: bool,
    bnb_4bit_quant_type: str,
    bnb_4bit_compute_dtype: str,
    bnb_4bit_use_double_quant: bool,
    output_dir: str,
    learning_rate: float,
    num_train_epochs: int,
    save_total_limit: int,
    save_strategy: str,
    per_device_train_batch_size: int,
    gradient_accumulation_steps: int,
    optim: str,
    weight_decay: float,
    fp16: bool,
    bf16: bool,
    max_grad_norm: float,
    max_steps: int,
    warmup_ratio: float,
    group_by_length: bool,
    lr_scheduler_type: str,
    report_to: str,
    target_modules: Union[str, list],
    lora_alpha: int,
    lora_dropout: float,
    r: int,
    bias: str,
    task_type: str,
    dataset_text_field: str,
    max_seq_length: int,
    packing: bool,
    dataset_batch_size: int,
    model_kwargs: dict,
    deploy: bool,
    dataset_map_func: Union[Callable, None],
    use_saved_model: bool,
    save_model_to_volume: bool,
) -> Union[Deployment, str]:
    """Fine-tune a model using the PEFT-LoRA method and serve it as a
    text generation service."""

    ft_args = {
        "use_quantization": use_quantization,
        "load_in_4bit": load_in_4bit,
        "bnb_4bit_quant_type": bnb_4bit_quant_type,
        "bnb_4bit_compute_dtype": bnb_4bit_compute_dtype,
        "bnb_4bit_use_double_quant": bnb_4bit_use_double_quant,
        "output_dir": output_dir,
        "learning_rate": learning_rate,
        "num_train_epochs": num_train_epochs,
        "save_total_limit": save_total_limit,
        "save_strategy": save_strategy,
        "per_device_train_batch_size": per_device_train_batch_size,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "optim": optim,
        "weight_decay": weight_decay,
        "fp16": fp16,
        "bf16": bf16,
        "max_grad_norm": max_grad_norm,
        "max_steps": max_steps,
        "warmup_ratio": warmup_ratio,
        "group_by_length": group_by_length,
        "lr_scheduler_type": lr_scheduler_type,
        "report_to": report_to,
        "target_modules": target_modules,
        "lora_alpha": lora_alpha,
        "lora_dropout": lora_dropout,
        "r": r,
        "bias": bias,
        "task_type": task_type,
        "dataset_text_field": dataset_text_field,
        "max_seq_length": max_seq_length,
        "packing": packing,
        "dataset_batch_size": dataset_batch_size,
    }

    ft_model_path = peft_fine_tuning(
        model_id=model_id,
        data=data,
        dataset_map_func=dataset_map_func,
        split=split,
        ft_args=ft_args,
        device_map=device_map,
        model_kwargs=model_kwargs,
        use_saved_model=use_saved_model,
        save_model_to_volume=save_model_to_volume,
    )
    if deploy:
        return llm_service(ft_model_path, device_map)

    return ft_model_path


dispatch_func = cc.dispatch(
    workflow_fine_tune_and_deploy_service,
    volume=ft_volume,
)

dispatch_id = dispatch_func(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    data="imdb",
    dataset_map_func=None,
    split="train[:5%]",
    use_quantization=False,
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=False,
    output_dir="./outputs",
    learning_rate=2e-3,
    num_train_epochs=5,
    save_total_limit=1,
    save_strategy="epoch",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    weight_decay=0.001,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="cosine",
    report_to="none",
    target_modules="linear",
    lora_alpha=32,
    lora_dropout=0.05,
    r=32,
    bias="none",
    task_type="CAUSAL_LM",
    dataset_text_field="text",
    max_seq_length=1024,
    packing=True,
    dataset_batch_size=10,
    device_map="auto",
    model_kwargs={},
    use_saved_model=True,
    save_model_to_volume=False,
    deploy=True,
)

res = cc.get_result(dispatch_id, wait=True)
res.result.load()
print(res.result.value)
