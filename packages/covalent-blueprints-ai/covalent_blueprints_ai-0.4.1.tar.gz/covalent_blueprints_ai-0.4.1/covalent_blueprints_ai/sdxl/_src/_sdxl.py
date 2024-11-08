"""Deploy a Stable Diffusion service that generates realistic
images."""

import shutil

import covalent_cloud as cc

from covalent_blueprints_ai._versions import covalent_blueprints_pkg, covalent_cloud_pkg

# cc.save_api_key("your-api-key")

SD_ENV = "sdxl@blueprints"

volume = cc.volume("sdxl")

cc.create_env(
    name=SD_ENV,
    pip=[
        "torch",
        "diffusers",
        "transformers",
        "peft",
        "huggingface_hub",
        covalent_cloud_pkg,
        covalent_blueprints_pkg,
    ],
    wait=True,
)

gpu_executor = cc.CloudExecutor(
    env=SD_ENV,
    num_cpus=4,
    memory="48GB",
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.L40,
    time_limit="3 hours",
)


@cc.service(executor=gpu_executor, name="Realistic SDXL Image Generator")
def sdxl_backend(
    model_name="SG161222/RealVisXL_V4.0",
    autoencoder_model_name="madebyollin/sdxl-vae-fp16-fix",
    model_kwargs=None,
    autoencoder_model_kwargs=None,
    use_saved_model=True,
    save_model_to_volume=False,
):
    """Backend service for a Stable Diffusion image generator model.

    Args:
        model_name: Hugging Face stable diffusion model name. Defaults
            to "SG161222/RealVisXL_V4.0".
        autoencoder_model_name: Hugging Face autoencoder model name.
            Defaults to "madebyollin/sdxl-vae-fp16-fix".
        model_kwargs: Keyword arguments passed to the stable diffusion
            model. Defaults listed below.
        autoencoder_model_kwargs: Keyword arguments passed to the
            autoencoder model. Defaults listed below.
        use_saved_model: Load the saved model from the cloud volume,
            if available. Defaults to True.
        save_model_to_volume: Save the pretrained model to the cloud
            volume, overwriting if a copy already exists. Defaults to
            False.

    Default model_kwargs:
        "torch_dtype": torch.float16,
        "custom_pipeline": "lpw_stable_diffusion_xl",
        "use_safetensors": True,
        "add_watermarker": False,
        "use_auth_token": None,
        "variant": "fp16",

    Default autoencoder_model_kwargs:
        "torch_dtype": torch.float16
    """

    import torch
    from covalent_blueprints.blueprints.utilities import pick_largest_fs
    from diffusers import StableDiffusionXLPipeline
    from diffusers.models import AutoencoderKL

    saved_model_name = str(model_name).replace("/", "--")
    saved_model_path = volume / saved_model_name
    if use_saved_model and saved_model_path.exists():
        model_name = str(saved_model_path)

    saved_autoencoder_model_name = str(autoencoder_model_name).replace("/", "--")
    saved_autoencoder_model_path = volume / saved_autoencoder_model_name
    if use_saved_model and saved_autoencoder_model_path.exists():
        autoencoder_model_name = str(saved_autoencoder_model_path)

    local_cache_dir = pick_largest_fs("/scratch", "/tmp")

    # Load autoencoder.
    default_autoencoder_model_kwargs = {"torch_dtype": torch.float16}
    autoencoder_model_kwargs = {
        **default_autoencoder_model_kwargs,
        **(autoencoder_model_kwargs or {}),
    }
    autoencoder_model_kwargs["cache_dir"] = str(local_cache_dir)
    vae = AutoencoderKL.from_pretrained(
        autoencoder_model_name,
        **autoencoder_model_kwargs,
    )

    # Load model.
    default_model_kwargs = {
        "torch_dtype": torch.float16,
        "custom_pipeline": "lpw_stable_diffusion_xl",
        "use_safetensors": True,
        "add_watermarker": False,
        "use_auth_token": None,
        "variant": "fp16",
    }
    model_kwargs = {**default_model_kwargs, **(model_kwargs or {})}
    model_kwargs["cache_dir"] = str(local_cache_dir)
    pipe = StableDiffusionXLPipeline.from_pretrained(
        model_name,
        vae=vae,
        **model_kwargs,
    )

    # Optionally, store the model on a cloud volume.
    if save_model_to_volume:

        print(f"💾 Saving model to {saved_model_path}")
        shutil.rmtree(saved_model_path, ignore_errors=True)
        pipe.save_pretrained(saved_model_path)

        print(f"💾 Saving autoencoder model to {saved_model_path}")
        shutil.rmtree(saved_autoencoder_model_path, ignore_errors=True)
        vae.save_pretrained(saved_autoencoder_model_path)

    if torch.cuda.is_available():
        pipe.to("cuda")

    return {"pipe": pipe}


@sdxl_backend.endpoint("/generate")
def generate_image(
    pipe=None,
    *,
    prompt="A beautiful sunset over the ocean.",
    negative_prompt="(face asymmetry, eyes asymmetry, deformed eyes, open mouth)",
    seed=0,
    upscale=False,
    scale_factor=1.5,
    **kwargs,
):
    """Generate an image based on a prompt. Image is returned as a
    base64-encoded string.

    Kwargs:
        prompt: The prompt to generate the image from. Defaults to
            "A beautiful sunset over the ocean.".
        negative_prompt: The negative prompt to generate the image
            from. See below for default value.
        seed: Random seed. Defaults to 0.
        upscale: Whether or not to use upscaling. Defaults to False.
        scale_factor: Upscaling scale factor. Defaults to 1.5.

    Any additional keyword arguments are passed directly to the
    pipeline.

    The default negative prompt is:
        "(face asymmetry, eyes asymmetry, deformed eyes, open mouth)"

    This negative prompt is recommended for "SG161222/RealVisXL_V4.0"

    Returns:
        A base64-encoded string of the generated image.
    """
    import base64
    import io
    import random

    import numpy as np
    import torch
    from diffusers import StableDiffusionXLImg2ImgPipeline

    # Seed everything.
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    generator = torch.Generator().manual_seed(seed)

    if upscale:
        # Upscale the image using an upscaler pipeline.
        upscaler_pipe = StableDiffusionXLImg2ImgPipeline(**pipe.components)
        latents = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            generator=generator,
            output_type="latent",
            **kwargs,
        ).images

        upscaled_latents = torch.nn.functional.interpolate(
            latents, scale_factor=scale_factor, mode="nearest"
        )
        images = upscaler_pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=upscaled_latents,
            generator=generator,
            output_type="pil",
            **kwargs,
        ).images

    else:
        # Generate the image using the original pipeline.
        images = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            generator=generator,
            output_type="pil",
            **kwargs,
        ).images

    # Convert image to base64 string
    image = images[0]
    bytes_io = io.BytesIO()
    image.save(bytes_io, format="PNG")
    image_as_str = base64.b64encode(bytes_io.getvalue()).decode("utf-8")

    return image_as_str


# Deploy the function service
sd_client = cc.deploy(sdxl_backend, volume=volume)(model_name="SG161222/RealVisXL_V4.0")
sd_client = cc.get_deployment(sd_client, wait=True)
print(sd_client)
