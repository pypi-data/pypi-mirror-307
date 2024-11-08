# Copyright 2024 Agnostiq Inc.
"""Blueprint for a Llama-like LLM service that generates/streams text
based on a prompt."""

from typing import Any, Dict, Optional

from covalent_blueprints import blueprint, get_blueprint
from covalent_blueprints.blueprints.templates import SingleServiceBlueprint

from covalent_blueprints_ai._prefix import PREFIX


@blueprint("Llama Chatbot Backend")
def llama_chatbot(
    model_name: str = "unsloth/llama-3-8b-Instruct-bnb-4bit",
    device_map: str = "auto",
    use_saved_model: bool = True,
    save_model_to_volume: bool = False,
    model_kwargs: Optional[Dict[str, Any]] = None,
) -> SingleServiceBlueprint:
    """A blueprint that deploys a service to host a Llama-like LLM
    chatbot.

    Args:
        model_name: Name of the pretrained LLM. Defaults to
            "unsloth/llama-3-8b-Instruct-bnb-4bit".
        device_map: Device map for the pretrained LLM. Defaults to
            "auto".
        use_saved_model: Load the saved model from the cloud volume,
            if available. Defaults to True.
        save_model_to_volume: Save the pretrained model to the cloud
            volume, overwriting if a copy already exists. Defaults to
            False.
        model_kwargs: Additional keyword arguments for the model.

    The deployed service includes three endpoints:
    - `/generate`: Generate a response to a prompt.
    - `/generate_message`: Generate a response to a list of messages.
    - `/stream`: Generate a response to a prompt, streaming tokens.

    The endpoints accept the following keyword-only parameters:
    - `prompt` or `messages`: The prompt or messages to respond to.
    - `max_new_tokens`: The maximum number of tokens to generate.
    - `temperature`: The temperature for sampling.
    - `top_p`: The top-p value for sampling.
    - `do_sample`: Whether to sample from the output distribution.

    The default executor has the following parameters:
    - `num_cpus`: 8
    - `num_gpus`: 1
    - `gpu_type`: 'l40'
    - `memory`: '15GB'
    - `time_limit`: '3 hours'

    The deployment will use its default environment unless an
    overriding executor specifies a new one.

    Returns:
        Covalent blueprint that deploys a Llama-like LLM chatbot.

    Example:

        ```
        from covalent_blueprints_ai import llama_chatbot

        chatbot_blueprint = llama_chatbot()
        chatbot_client = chatbot_blueprint.run()

        prompt = "Sometimes I think about "
        max_new_tokens = 50

        # Generate a response to a prompt.
        chatbot_client.generate(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
        )

        # Generate a response to a prompt, streaming tokens.
        for token in chatbot_client.stream(prompt=prompt):
            print(token.decode(), end="")

        # Tear down the deployment.
        chatbot_client.teardown()
        ```
    """
    bp = get_blueprint(f"{PREFIX}/llama_chatbot", _cls=SingleServiceBlueprint)
    bp.executors.set_executor_key("chatbot_backend")
    bp.set_default_inputs(
        model_name=model_name,
        device_map=device_map,
        use_saved_model=use_saved_model,
        save_model_to_volume=save_model_to_volume,
        model_kwargs=model_kwargs,
    )

    return bp
