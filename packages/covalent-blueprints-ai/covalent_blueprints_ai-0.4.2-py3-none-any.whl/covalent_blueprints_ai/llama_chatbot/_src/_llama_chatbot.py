# Copyright 2024 Agnostiq Inc.
"""Deploy a Llama model as an LLM service for text generation and
streaming."""

import shutil
from pathlib import Path

import covalent_cloud as cc

from covalent_blueprints_ai._versions import covalent_blueprints_pkg, covalent_cloud_pkg

# cc.save_api_key("your-api-key")

CB_ENV = "llama-chatbot@blueprints"

volume = cc.volume("llama-chatbot")

cc.create_env(
    name=CB_ENV,
    pip=[
        "accelerate",
        "bitsandbytes",
        "sentencepiece",
        "transformers",
        covalent_cloud_pkg,
        covalent_blueprints_pkg,
    ],
    wait=True,
)

gpu_executor = cc.CloudExecutor(
    env=CB_ENV,
    num_cpus=8,
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.L40,
    memory="15 GB",
    time_limit="3 hours",
    volume_id=volume.id,
)


@cc.service(executor=gpu_executor, name="LLM Chatbot Server")
def chatbot_backend(
    model_name="unsloth/llama-3-8b-Instruct-bnb-4bit",
    device_map="auto",
    use_saved_model=True,
    save_model_to_volume=False,
    model_kwargs=None,
):
    """Backend service for a Llama-like chatbot.

    Args:
        model_path: Hugging Face model name, e.g.
            "unsloth/llama-3-8b-Instruct-bnb-4bit".
        device_map: PyTorch device map for model sub-modules. Defaults
            to "auto".
        use_saved_model: Load the saved model from the cloud volume,
            if available. Defaults to True.
        save_model_to_volume: Save the pretrained model to the cloud
            volume, overwriting if a copy already exists. Defaults to
            False.
        model_kwargs: Additional keyword arguments for the model.
    """
    import torch
    from covalent_blueprints.blueprints.utilities import pick_largest_fs
    from transformers import pipeline

    saved_model_name = str(model_name).replace("/", "--")
    saved_model_path = volume / saved_model_name

    local_cache_dir = pick_largest_fs("/scratch", "/tmp")

    if use_saved_model and saved_model_path.exists():
        model_name = str(saved_model_path)

    default_kwargs = {
        "torch_dtype": torch.bfloat16,
        "cache_dir": str(local_cache_dir),
    }

    model_kwargs = model_kwargs or {}
    model_kwargs = {**default_kwargs, **model_kwargs}

    print(f"🤖 Loading model '{model_name}' with kwargs '{model_kwargs}")

    pipe_kwargs = {
        "task": "text-generation",
        "model": model_name,
        "device_map": device_map,
        "model_kwargs": model_kwargs,
    }
    try:
        pipe = pipeline(**pipe_kwargs)
    except PermissionError:
        if model_kwargs.get("cache_dir") != "/tmp" and Path("/tmp").exists():
            print(
                f"❌ PermissionError: with pipe kwargs '{pipe_kwargs}'. "
                "Attempting to cache in '/tmp' instead..."
            )
            model_kwargs["cache_dir"] = "/tmp"
            pipe = pipeline(**pipe_kwargs)
        else:
            raise

    terminators = [
        pipe.tokenizer.eos_token_id,
        pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
    ]

    if save_model_to_volume:
        shutil.rmtree(saved_model_path, ignore_errors=True)
        print("💾 Saving model to", saved_model_path)
        pipe.model.save_pretrained(saved_model_path)
        pipe.tokenizer.save_pretrained(saved_model_path)

    return {"pipe": pipe, "terminators": terminators}


@chatbot_backend.endpoint("/generate", name="Generate Response to Prompt")
def generate(
    pipe=None,
    terminators=None,
    *,
    prompt=None,
    max_new_tokens=200,
    temperature=0.6,
    top_p=0.9,
    do_sample=True,
):
    """Generate a response to a prompt.

    Kwargs:
        prompt: The prompt to generate a response to.
        max_new_tokens: Maximum number of new tokens to generate.
            Defaults to 200.
        temperature: The temperature for sampling. Defaults to 0.6.
        top_p: The nucleus sampling threshold. Defaults to 0.9.
        do_sample: Whether to sample from the output distribution.

    Returns:
        The generated text.
    """

    if prompt is None:
        return "Please provide a prompt."

    if do_sample:
        outputs = pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            eos_token_id=terminators,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
        )
    else:
        outputs = pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            eos_token_id=terminators,
            do_sample=False,
        )

    if isinstance(prompt[0], list):
        return [output[0]["generated_text"] for output in outputs]

    return outputs[0]["generated_text"]


@chatbot_backend.endpoint("/generate_message", name="Generate Response to Messages")
def generate_message(
    pipe=None,
    terminators=None,
    *,
    messages=None,
    max_new_tokens=200,
    temperature=0.6,
    top_p=0.9,
    do_sample=True,
):
    """Generate a response to a list of messages.

    Kwargs:
        messages: A list of messages to generate a response to.
        max_new_tokens: Maximum number of new tokens to generate.
            Defaults to 200.
        temperature: The temperature for sampling. Defaults to 0.6.
        top_p: The nucleus sampling threshold. Defaults to 0.9.
        do_sample: Whether to sample from the output distribution.

    Returns:
        The generated message.
    """

    if messages is None:
        return "Please provide a list of messages."

    if do_sample:
        outputs = pipe(
            messages,
            max_new_tokens=max_new_tokens,
            eos_token_id=terminators,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
        )
    else:
        outputs = pipe(
            messages,
            max_new_tokens=max_new_tokens,
            eos_token_id=terminators,
            do_sample=False,
        )

    if isinstance(messages[0], list):
        return [output[0]["generated_text"][-1] for output in outputs]

    return outputs[0]["generated_text"][-1]


@chatbot_backend.endpoint("/stream", name="Stream Response", streaming=True)
def generate_stream(
    pipe=None,
    *,
    prompt=None,
    max_new_tokens=200,
    temperature=0.6,
    top_p=0.9,
    do_sample=True,
):
    """Generate and stream a response to a prompt.

    Kwargs:
        prompt: The prompt to generate a response to.
        max_new_tokens: Maximum number of new tokens to generate.
            Defaults to 200.
        temperature: The temperature for sampling. Defaults to 0.6.
        top_p: The nucleus sampling threshold. Defaults to 0.9.
        do_sample: Whether to sample from the output distribution.

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
            if do_sample:
                output = model.generate(
                    **_input,
                    max_new_tokens=1,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                )
            else:
                output = model.generate(
                    **_input,
                    max_new_tokens=1,
                    do_sample=False,
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


info = cc.deploy(chatbot_backend, volume=volume)(
    model_name="unsloth/llama-3-8b-Instruct-bnb-4bit"
)
info = cc.get_deployment(info.function_id, wait=True)
print(info)
