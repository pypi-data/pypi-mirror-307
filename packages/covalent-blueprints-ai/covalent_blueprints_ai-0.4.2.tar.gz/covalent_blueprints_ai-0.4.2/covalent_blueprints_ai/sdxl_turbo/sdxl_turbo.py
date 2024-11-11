# Copyright 2024 Agnostiq Inc.
"""Blueprint for an SDXL-turbo service that generates images based on a
prompt."""

from covalent_blueprints import blueprint, get_blueprint
from covalent_blueprints.blueprints.templates import SingleServiceBlueprint

from covalent_blueprints_ai._prefix import PREFIX


@blueprint("Fast SDXL Image Generator Service")
def sdxl_turbo(
    model_name: str = "stabilityai/sdxl-turbo",
    torch_dtype: str = "float16",
    variant: str = "fp16",
    use_saved_model: bool = True,
    save_model_to_volume: bool = False,
) -> SingleServiceBlueprint:
    """A blueprint that deploys a service to host an SDXL-turbo image
    generator.

    Args:
        model_name: The name of the model to deploy. Defaults to
            "stabilityai/sdxl-turbo".
        torch_dtype: PyTorch data type (as string) for model
            parameters. Defaults to "float16".
        variant: Model variant. Defaults to "fp16".
        use_saved_model: Load the saved model from the cloud volume, if
            available. Defaults to True.
        save_model_to_volume: Save the pretrained model to the cloud
            volume, overwriting if a copy already exists. Defaults to
            False.

    The service includes a single endpoint:
    - `/generate`: Generate an image based on a prompt.

    The endpoint accepts the following keyword-only parameters:
    - `prompt`: The prompt to generate an image from.
    - `num_inference_steps`: The number of SDXL-turbo inference steps.
    - `guidance_scale`: The guidance scale for the SDXL-turbo model.

    The default executor has the following parameters:
    - `num_cpus`: 25
    - `num_gpus`: 1
    - `gpu_type`: 'l40'
    - `memory`: '56GB'
    - `time_limit`: '3 hours'

    The deployment will use its default environment unless an
    overriding executor specifies a new one.

    Returns:
        Covalent blueprint that deploys an SDXL-turbo image generator.

    Example:

        ```
        from covalent_blueprints_ai import sdxl_turbo

        sdxl_blueprint = sdxl_turbo()
        sdxl_client = sdxl_blueprint.run()

        prompt = "A beautiful sunset over the ocean."
        num_inference_steps = 1

        # Generate an image based on a prompt.
        img_str = sdxl_client.generate(
            prompt=prompt,
            num_inference_steps=num_inference_steps,
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

    bp = get_blueprint(f"{PREFIX}/sdxl_turbo", _cls=SingleServiceBlueprint)
    bp.executors.set_executor_key("text_to_image_service")
    bp.set_default_inputs(
        model_name=model_name,
        torch_dtype=torch_dtype,
        variant=variant,
        use_saved_model=use_saved_model,
        save_model_to_volume=save_model_to_volume,
    )

    return bp
