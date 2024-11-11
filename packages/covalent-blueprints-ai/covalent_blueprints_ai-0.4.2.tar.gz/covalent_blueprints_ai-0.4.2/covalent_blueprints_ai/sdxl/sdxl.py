# Copyright 2024 Agnostiq Inc.
"""Blueprint for an SDXL service that generates realistic images."""

from typing import Any, Dict, Optional

from covalent_blueprints import blueprint, get_blueprint
from covalent_blueprints.blueprints.templates import SingleServiceBlueprint

from covalent_blueprints_ai._prefix import PREFIX


@blueprint("Realistic SDXL Image Generator Service")
def sdxl(
    model_name: str = "SG161222/RealVisXL_V4.0",
    autoencoder_model_name: str = "madebyollin/sdxl-vae-fp16-fix",
    use_saved_model: bool = True,
    save_model_to_volume: bool = False,
    model_kwargs: Optional[Dict[str, Any]] = None,
    autoencoder_model_kwargs: Optional[Dict[str, Any]] = None,
):
    """A blueprint that deploys a service to host a Stable Diffusion
    image generator.

    Args:
        model_name: Hugging Face stable diffusion model name.
            Defaults to "SG161222/RealVisXL_V4.0".
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

    The service includes a single endpoint:
    - `/generate`: Generate an image based on a prompt.

    The endpoint accepts the following keyword-only parameters:
    - `prompt`: The prompt to generate an image from.
    - `negative_prompt`: The negative prompt that guides avoidance.
    - `seed`: Random seed.
    - `upscale`: Whether or not to use upscaling.
    - `upscale_factor`: Upscaling factor.
    - `**kwargs`: Additional keyword arguments for pipeline.

    The default executor has the following parameters:
    - `num_cpus`: 4
    - `memory`: '48GB'
    - `num_gpus`: 1
    - `gpu_type`: 'l40'
    - `time_limit`: '3 hours'

    The deployment will use its default environment unless an
    overriding executor specifies a new one.

    Returns:
        Covalent blueprint that deploys a Stable Diffusion image
        generator.

    Example:

        ```
        from covalent_blueprints_ai import sdxl

        sdxl_blueprint = sdxl()
        sdxl_client = sdxl_blueprint.run()

        prompt = "A beautiful sunset over the ocean."
        negative_prompt = "A dark and stormy night."

        # Generate an image based on a prompt.
        img_str = sdxl_client.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=42,
            num_inference_steps=20,
            upscale=True,
            strength=0.52,
            scale_factor=1.5,
        )

        # Display the image.
        import base64
        import io
        from PIL import Image

        buffer = io.BytesIO(base64.b64decode(img_str))
        Image.open(buffer)

        # Tear down the deployment.
        sdxl_client.teardown()
        ```
    """

    bp = get_blueprint(f"{PREFIX}/sdxl", _cls=SingleServiceBlueprint)
    bp.executors.set_executor_key("sdxl_backend")
    bp.set_default_inputs(
        model_name=model_name,
        autoencoder_model_name=autoencoder_model_name,
        use_saved_model=use_saved_model,
        save_model_to_volume=save_model_to_volume,
        model_kwargs=model_kwargs,
        autoencoder_model_kwargs=autoencoder_model_kwargs,
    )

    return bp
