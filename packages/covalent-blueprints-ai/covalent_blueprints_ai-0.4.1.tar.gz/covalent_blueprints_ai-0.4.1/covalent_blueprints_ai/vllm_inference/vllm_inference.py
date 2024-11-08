# Copyright 2024 Agnostiq Inc.
"""Blueprint for an LLM service using vLLM."""

from covalent_blueprints import blueprint, get_blueprint
from covalent_blueprints.blueprints.templates import SingleServiceBlueprint

from covalent_blueprints_ai._prefix import PREFIX


@blueprint("vLLM Inference Service")
def vllm_inference(
    model_name: str = "facebook/opt-125m",
    dtype: str = "auto",
    **llm_kwargs,
) -> SingleServiceBlueprint:
    """A blueprint that deploys a service to host an LLM model using
    vLLM.

    Args:
        model_name: The name of the model to deploy. Defaults to
            "facebook/opt-125m".
        dtype: The data type to use. Defaults to "auto".
        **llm_kwargs: Additional keyword arguments to pass to
            `vllm.LLM` model.

    The service includes a single endpoint:
    - `/generate`: Generate text based on a prompt.

    The endpoint accepts a `prompt` as a key-word only parameter in
    addition to various initialization parameters for
    vllm.SamplingParams.

    The default executor has the following parameters:
    - `num_cpus`: 6
    - `num_gpus`: 1
    - `gpu_type`: 'a5000'
    - `memory`: '25GB'
    - `time_limit`: '3 hours'

    The deployment will use its default environment unless an
    overriding executor specifies a new one.

    Returns:
        Covalent blueprint that deploys an LLM model using vLLM.

    Example:

        ```
        from covalent_blueprints_ai import vllm_inference

        vllm_blueprint = vllm_inference(
            model_name="unsloth/llama-3-8b-Instruct"
        )
        vllm_client = vllm_blueprint.run(gpu_memory_utilization=0.9)

        prompt = "Once upon a time, in a land far, far away..."
        temperature = 0.8
        top_p = 0.95

        # Generate text based on a prompt.
        generated_text = vllm_client.generate(
            prompt=prompt,
            temperature=temperature,
            top_p=top_p,
        )
        print(generated_text)

        # Tear down the deployment.
        vllm_client.teardown()
        ```
    """
    bp = get_blueprint(f"{PREFIX}/vllm_inference", _cls=SingleServiceBlueprint)
    bp.executors.set_executor_key("vllm_service")
    bp.set_default_inputs(
        model_name=model_name,
        dtype=dtype,
        **llm_kwargs,
    )

    return bp
