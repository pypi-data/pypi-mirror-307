# Copyright 2024 Agnostiq Inc.
"""Blueprint for fine-tuning a model using the PEFT-LoRA method and
deploying it as a text generation service."""

import warnings
from pathlib import Path
from typing import Any, Callable, Optional, Union

from covalent_blueprints import blueprint, get_blueprint
from covalent_blueprints.blueprints.templates import ServiceWorkflowBlueprint

from covalent_blueprints_ai._prefix import PREFIX
from covalent_blueprints_ai.lora_fine_tuning.utilities import (
    load_local_dataset_from_file,
)


@blueprint("LLM LoRA Fine-Tuning and Service Deployment")
def lora_fine_tuning(
    model_id: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    data: Union[str, Path, Any] = "imdb",
    dataset_map_func: Optional[Callable] = None,
    split: str = "train[:20%]",
    device_map: Union[str, dict] = "auto",
    model_kwargs: Optional[dict] = None,
    deploy: bool = True,
    use_saved_model: bool = True,
    save_model_to_volume: bool = False,
    *,
    use_quantization: bool = False,
    load_in_4bit: bool = True,
    bnb_4bit_quant_type: str = "nf4",
    bnb_4bit_compute_dtype: str = "float16",
    bnb_4bit_use_double_quant: bool = False,
    output_dir: str = "./outputs",
    learning_rate: float = 2e-3,
    num_train_epochs: int = 5,
    save_total_limit: int = 1,
    save_strategy: str = "epoch",
    per_device_train_batch_size: int = 2,
    gradient_accumulation_steps: int = 1,
    optim: str = "paged_adamw_32bit",
    weight_decay: float = 0.001,
    fp16: bool = False,
    bf16: bool = False,
    max_grad_norm: float = 0.3,
    max_steps: int = -1,
    warmup_ratio: float = 0.03,
    group_by_length: bool = True,
    lr_scheduler_type: str = "cosine",
    report_to: str = "none",
    lora_alpha: int = 32,
    lora_dropout: float = 0.05,
    r: int = 32,
    bias: str = "none",
    task_type: str = "CAUSAL_LM",
    target_modules: Union[str, list, None] = "linear",
    dataset_text_field: str = "text",
    max_seq_length: int = 1024,
    packing: bool = True,
    dataset_batch_size: int = 10,
) -> ServiceWorkflowBlueprint:
    """A blueprint that fine-tunes a model using the PEFT-LoRA method
    and (by default) deploys it as a text generation service.

    Args:
        model_id: Name of the model to fine-tune. Defaults to
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0".
        data: The identifier passed to `load_dataset`, or the path to
            a local dataset, or a `Dataset` object. Defaults to
            "imdb". Please note that a data argument that refers to a
            local dataset cannot be overridden at runtime (i.e. when
            calling `.run()` on the blueprint returned by this
            function).
        dataset_map_func: An arbitrary function that accepts a dataset
            as its only argument and returns a dataset. Defaults to
            None.
        split: Split to use for the fine-tuning data. Defaults to
            "all".
        device_map: Model device map for Pytorch. Defaults to "auto".
        model_kwargs: An optional dictionary of additional keyword
            arguments for `AutoModelForCausalLM.from_pretrained()`.
            Defaults to None.
        deploy: Whether to deploy the fine-tuned model as a function
            service or to save it on the volume. Defaults to True.
        use_saved_model: Load the saved base model from the cloud
            volume, if available. Defaults to True.
        save_model_to_volume: Save the pretrained base model to the
            cloud volume, overwriting if a copy already exists.
            Defaults to False.

    Args for BitAndBytesConfig:
        use_quantization: Whether to use quantization. Defaults to
            False.
        load_in_4bit: Whether to load the model in 4-bit. Defaults to
            True.
        bnb_4bit_quant_type: The quantization type for 4-bit. Defaults
            to "nf4".
        bnb_4bit_compute_dtype: The compute dtype for 4-bit. Defaults
            to "float16".
        bnb_4bit_use_double_quant: Whether to use double quantization
            for 4-bit. Defaults to False.

    Args for TrainingArguments:
        output_dir: The output directory for the fine-tuned model.
            Defaults to "./outputs".
        learning_rate: The learning rate for the fine-tuning. Defaults
            to 2e-3.
        num_train_epochs: The number of training epochs.
            Defaults to 5.
        save_total_limit: The total number of checkpoints to save.
            Defaults to 1.
        save_strategy: The strategy for saving checkpoints. Defaults
            to "epoch".
        per_device_train_batch_size: The training batch size per
            device. Defaults to 2.
        gradient_accumulation_steps: The number of gradient
            accumulation steps. Defaults to 1.
        optim: The optimizer to use. Defaults to "paged_adamw_32bit".
        weight_decay: The weight decay for the optimizer. Defaults to
            0.001.
        fp16: Whether to use FP16. Defaults to False.
        bf16: Whether to use BF16. Defaults to False.
        max_grad_norm: The maximum gradient norm. Defaults to 0.3.
        max_steps: The maximum number of training steps.
            Defaults to -1.
        warmup_ratio: The warmup ratio for the learning rate
            scheduler. Defaults to 0.03.
        group_by_length: Whether to group the data by length. Defaults
            to True.
        lr_scheduler_type: The type of learning rate scheduler.
            Defaults to "cosine".
        report_to: The type of reporting. Defaults to "none".

    Args for LoraConfig:
        lora_alpha: The alpha value for LoRA. Defaults to 32.
        lora_dropout: The dropout rate for LoRA. Defaults to 0.05.
        r: The r value for LoRA. Defaults to 32.
        bias: The bias type for LoRA. Defaults to "none".
        task_type: The task type for LoRA. Defaults to "CAUSAL_LM".
        target_modules: The target modules for LoRA. Passing None
            relies on the model being recognized. Passing the string
            "linear" targets all linear modules. An explicit list of
            target modules is also accepted. Defaults to "linear".

    Args for SFTTrainer:
        dataset_text_field: The text field in the dataset. Defaults to
            "text".
        max_seq_length: The maximum sequence length. Defaults to 1024.
        packing: Whether to pack the data. Defaults to True.
        dataset_batch_size: The batch size for the dataset.
            Defaults to 10.

    When deploy is True, the deployed service includes two endpoints:
    - `/generate`: Generate a response to a prompt.
    - `/stream`: Generate a response to a prompt, streaming tokens.

    The service endpoints accept the following keyword-only params:
    - `prompt`: The prompt to generate a response to.
    - `max_new_tokens`: The maximum number of tokens to generate.
    - `temperature`: The temperature for sampling.
    - `truncation`: Whether to truncate the generated text.
        (`/generate` only)

    The default service executor has the following parameters:
    - `num_cpus`: 6
    - `num_gpus`: 1
    - `gpu_type`: 'a100'
    - `memory`: '64GB'
    - `time_limit`: '4 hours'

    Returns:
        Covalent blueprint that fine-tunes a model using the PEFT-LoRA
        method and either saves it on a volume or deploys it as a text
        generation service.

    Example:

        ```
        from covalent_blueprints_ai import lora_fine_tuning

        bp = lora_fine_tuning(
            model_id="Qwen/Qwen2-0.5B",
            data="./imdb_sample.json",  # sample local dataset
            split="train",
            num_train_epochs=3,
        )

        # Fine tune and deploy the new model.
        llm_client = bp.run()

        # Generate a response to a prompt.
        response = llm_client.generate(prompt="Once upon a time ")
        print(response)

        # Tear down the deployment.
        llm_client.teardown()
        ```
    """

    bp = get_blueprint(f"{PREFIX}/lora_fine_tuning", _cls=ServiceWorkflowBlueprint)

    bp.executors.set_executor_key(
        electron_key="peft_fine_tuning",
        service_key="llm_service",
    )

    if (
        isinstance(data, (str, Path))
        and (local_dataset := Path(data).expanduser().absolute()).exists()
    ):
        if split == "all":
            warnings.warn(
                "split='all' is not supported for local datasets. "
                "Will use split='train'."
            )
            split = "train"

        data = load_local_dataset_from_file(local_dataset, split)

    bp.set_default_inputs(
        model_id=model_id,
        data=data,
        split=split,
        device_map=device_map,
        # BitAndBytesConfig
        use_quantization=use_quantization,
        load_in_4bit=load_in_4bit,
        bnb_4bit_quant_type=bnb_4bit_quant_type,
        bnb_4bit_compute_dtype=bnb_4bit_compute_dtype,
        bnb_4bit_use_double_quant=bnb_4bit_use_double_quant,
        # TrainingArguments
        output_dir=output_dir,
        learning_rate=learning_rate,
        num_train_epochs=num_train_epochs,
        save_total_limit=save_total_limit,
        save_strategy=save_strategy,
        per_device_train_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        optim=optim,
        weight_decay=weight_decay,
        fp16=fp16,
        bf16=bf16,
        max_grad_norm=max_grad_norm,
        max_steps=max_steps,
        warmup_ratio=warmup_ratio,
        group_by_length=group_by_length,
        lr_scheduler_type=lr_scheduler_type,
        report_to=report_to,
        # LoraConfig
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        r=r,
        bias=bias,
        task_type=task_type,
        target_modules=target_modules,
        # SFTTrainer
        dataset_text_field=dataset_text_field,
        max_seq_length=max_seq_length,
        packing=packing,
        dataset_batch_size=dataset_batch_size,
        model_kwargs=model_kwargs or {},
        deploy=deploy,
        dataset_map_func=dataset_map_func,
        use_saved_model=use_saved_model,
        save_model_to_volume=save_model_to_volume,
    )

    return bp
