# Copyright 2024 Agnostiq Inc.
"""Deploy a text-to-image pipeline as a service, using 'sdxl-turbo' by
default."""

import base64
import io
import shutil
from pathlib import Path

import covalent_cloud as cc

from covalent_blueprints_ai._versions import covalent_blueprints_pkg, covalent_cloud_pkg

# cc.save_api_key("your-api-key")

SDXL_ENV = "sdxl-turbo@blueprints"

volume = cc.volume("sdxl-turbo")

cc.create_env(
    name=SDXL_ENV,
    pip=[
        "torch",
        "transformers[sentencepiece]",
        "accelerate",
        "diffusers",
        covalent_cloud_pkg,
        covalent_blueprints_pkg,
    ],
    wait=True,
)

gpu_executor = cc.CloudExecutor(
    env=SDXL_ENV,
    num_cpus=25,
    memory="56 GB",
    time_limit="3 hours",
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.L40,
    volume_id=volume.id,
)


@cc.service(executor=gpu_executor, name="Fast SDXL Image Generator")
def text_to_image_service(
    model_name="stabilityai/sdxl-turbo",
    torch_dtype="float16",
    variant="fp16",
    use_saved_model=True,
    save_model_to_volume=False,
):
    """Backend service for an SDXL-like image generator.

    Args:
        model_name: Hugging face model name, e.g. "stabilityai/
            sdxl-turbo".
        torch_dtype: PyTorch data type (as string) for model
            parameters. Defaults to "float16".
        variant: Model variant. Defaults to "fp16".
        use_saved_model: Load the saved model from the cloud volume,
            if available. Defaults to True.
        save_model_to_volume: Save the pretrained model to the cloud
            volume, overwriting if a copy already exists. Defaults to
            False.
    """

    import torch
    from covalent_blueprints.blueprints.utilities import pick_largest_fs
    from diffusers import AutoPipelineForText2Image

    saved_model_name = str(model_name).replace("/", "--")
    saved_model_path = volume / saved_model_name

    local_cache_dir = pick_largest_fs("/scratch", "/tmp")

    if use_saved_model and saved_model_path.exists():
        print("💿 Loading saved model from", saved_model_path)
        model_name = str(saved_model_path)

    pipe_kwargs = {
        "pretrained_model_or_path": model_name,
        "torch_dtype": getattr(torch, torch_dtype),
        "variant": variant,
        "cache_dir": str(local_cache_dir),
    }
    try:
        pipe = AutoPipelineForText2Image.from_pretrained(**pipe_kwargs)
    except (PermissionError, OSError) as e:
        if pipe_kwargs.get("cache_dir") != "/tmp" and Path("/tmp").exists():
            print(
                f"❌ {e.__class__.__name__}: with pipe kwargs '{pipe_kwargs}'. "
                "Attempting to cache in '/tmp' instead..."
            )
            pipe_kwargs["cache_dir"] = "/tmp"
            pipe = AutoPipelineForText2Image.from_pretrained(**pipe_kwargs)
        else:
            raise

    pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    if save_model_to_volume:
        print("💾 Saving model to", saved_model_path)
        shutil.rmtree(saved_model_path, ignore_errors=True)
        pipe.save_pretrained(saved_model_path)

    return {"pipe": pipe}


@text_to_image_service.endpoint("/generate", name="Generate Image")
def generate_image(
    pipe=None,
    *,
    prompt=None,
    num_inference_steps=1,
    guidance_scale=0.0,
):
    """Generate an image based on a prompt. Image is returned as a
    base64-encoded string.

    Kwargs:
        prompt: The prompt to generate the image from. Defaults to
            "A beautiful sunset over the ocean."
        num_inference_steps: Number of inference steps. Defaults to 1.
        guidance_scale: The strength of guidance provided by the
            prompt. Defaults to 0.0.

    Returns:
        A base64-encoded string of the generated image.
    """
    if prompt is None:
        prompt = "A beautiful sunset over the ocean."

    image = pipe(
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
    ).images[0]

    bytes_io = io.BytesIO()
    image.save(bytes_io, format="PNG")
    image_as_str = base64.b64encode(bytes_io.getvalue()).decode("utf-8")
    return image_as_str


info = cc.deploy(text_to_image_service)(model_name="stabilityai/sdxl-turbo")
info = cc.get_deployment(info.function_id, wait=True)
print(info)
print(info.address)
