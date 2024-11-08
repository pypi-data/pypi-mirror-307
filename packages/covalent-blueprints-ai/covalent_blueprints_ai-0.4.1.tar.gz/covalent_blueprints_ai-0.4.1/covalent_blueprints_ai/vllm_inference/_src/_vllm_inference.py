# Copyright 2024 Agnostiq Inc.
"""Deploy an LLM text generation service using vLLM."""
# pylint: disable=import-outside-toplevel, import-error

import covalent_cloud as cc

from covalent_blueprints_ai._versions import covalent_blueprints_pkg

# cc.save_api_key("your-api-key")

VLLM_ENV = "vllm-inference@blueprints"

volume = cc.volume("vllm-inference")

cc.create_env(
    name=VLLM_ENV,
    pip=["vllm==0.5.1", "torch==2.3.0", covalent_blueprints_pkg],
    wait=True,
)

service_executor = cc.CloudExecutor(
    env="vllm-inference@blueprints",
    num_cpus=6,
    memory="25GB",
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.A5000,
    time_limit="3 hours",
    volume_id=volume.id,
)


@cc.service(executor=service_executor, name="vLLM Inference")
# gpu_memory_utilization: float):
def vllm_service(
    model_name="facebook/opt-125m",
    dtype="auto",
    **llm_kwargs,
):
    """Backend service for a vLLM model.

    Args:
        model: The name or path of a Hugging Face Transformers
            model, e.g. "facebook/opt-125m".
        dtype: The data type for the model weights and activations.
            Defaults to "auto".
        **llm_kwargs: Additional keyword arguments for the vllm.LLM
            constructor.
    """
    from vllm import LLM

    return {"llm": LLM(model=model_name, dtype=dtype, **llm_kwargs)}


@vllm_service.endpoint(route="/generate", name="Generate Text")
def generate(
    llm=None,
    *,
    prompt=None,
    n=1,
    best_of=None,
    presence_penalty=0.0,
    frequency_penalty=0.0,
    repetition_penalty=1.0,
    temperature=1.0,
    top_p=1.0,
    top_k=-1,
    min_p=0.0,
    seed=None,
    use_beam_search=False,
    length_penalty=1.0,
    early_stopping=False,
    stop=None,
    stop_token_ids=None,
    include_stop_str_in_output=False,
    ignore_eos=False,
    max_tokens=16,
    min_tokens=0,
    logprobs=None,
    prompt_logprobs=None,
    detokenize=True,
    skip_special_tokens=True,
    spaces_between_special_tokens=True,
    truncate_prompt_tokens=None,
) -> str:
    """Generate text based on a prompt.

    Kwargs:
        prompt: The prompt to generate text from.

    Additional keyword arguments below are initialization parameters
    for vllm.SamplingParams.

        n: Number of output sequences to return for the given prompt.
        best_of: Number of output sequences that are generated from
            the prompt. From these `best_of` sequences, the top `n`
            sequences are returned. `best_of` must be greater than or
            equal to `n`. This is treated as the beam width when
            `use_beam_search` is True. By default, `best_of` is set to
            `n`.
        presence_penalty: Float that penalizes new tokens based on
            whether they appear in the generated text so far. Values
            > 0 encourage the model to use new tokens, while values
            < 0 encourage the model to repeat tokens.
        frequency_penalty: Float that penalizes new tokens based on
            their frequency in the generated text so far. Values > 0
            encourage the model to use new tokens, while values < 0
            encourage the model to repeat tokens.
        repetition_penalty: Float that penalizes new tokens based on
            whether they appear in the prompt and the generated text
            so far. Values > 1 encourage the model to use new tokens,
            while values < 1 encourage the model to repeat tokens.
        temperature: Float that controls the randomness of the
            sampling. Lower values make the model more
            deterministic, while higher values make the model
            more random. Zero means greedy sampling.
        top_p: Float that controls the cumulative probability of the
            top tokens to consider. Must be in (0, 1]. Set to 1 to
            consider all tokens.
        top_k: Integer that controls the number of top tokens to
            consider. Set to -1 to consider all tokens.
        min_p: Float that represents the minimum probability for a
            token to be considered, relative to the probability of the
            most likely token. Must be in [0, 1]. Set to 0 to disable
            this.
        seed: Random seed to use for the generation.
        use_beam_search: Whether to use beam search instead of
            sampling.
        length_penalty: Float that penalizes sequences based on their
            length. Used in beam search.
        early_stopping: Controls the stopping condition for beam
            search. It accepts the following values: `True`, where
            the generation stops as soon as there are `best_of`
            complete candidates; `False`, where a heuristic is
            applied and the generation stops when it is very
            unlikely to find better candidates; `"never"`, where
            the beam search procedure only stops when there
            cannot be better candidates (canonical beam search
            algorithm).
        stop: List of strings that stop the generation when they are
            generated. The returned output will not contain the stop
            strings.
        stop_token_ids: List of tokens that stop the generation when
            they are generated. The returned output will contain the
            stop tokens unless the stop tokens are special tokens.
        include_stop_str_in_output: Whether to include the stop strings
            in output text. Defaults to False.
        ignore_eos: Whether to ignore the EOS token and continue
            generating tokens after the EOS token is generated.
        max_tokens: Maximum number of tokens to generate per output
            sequence.
        min_tokens: Minimum number of tokens to generate per output
            sequence before EOS or stop_token_ids can be generated.
        logprobs: Number of log probabilities to return per output
            token. Note that the implementation follows the OpenAI API:
            The return result includes the log probabilities on the
            `logprobs` most likely tokens, as well as the chosen
            tokens. The API will always return the log probability of
            the sampled token, so there may be up to `logprobs+1`
            elements in the response.
        prompt_logprobs: Number of log probabilities to return per
            prompt token.
        detokenize: Whether to detokenize the output. Defaults to True.
        skip_special_tokens: Whether to skip special tokens in the
            output.
        spaces_between_special_tokens: Whether to add spaces between
            special tokens in the output. Defaults to True.
        truncate_prompt_tokens: If set to an integer k, will use only
            the last k tokens from the prompt (i.e., left truncation).
            Defaults to None (i.e., no truncation).

    Returns:
        The generated text.
    """
    from vllm import SamplingParams

    sampling_params = SamplingParams(
        n=n,
        best_of=best_of,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        repetition_penalty=repetition_penalty,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        min_p=min_p,
        seed=seed,
        use_beam_search=use_beam_search,
        length_penalty=length_penalty,
        early_stopping=early_stopping,
        stop=stop,
        stop_token_ids=stop_token_ids,
        include_stop_str_in_output=include_stop_str_in_output,
        ignore_eos=ignore_eos,
        max_tokens=max_tokens,
        min_tokens=min_tokens,
        logprobs=logprobs,
        prompt_logprobs=prompt_logprobs,
        detokenize=detokenize,
        skip_special_tokens=skip_special_tokens,
        spaces_between_special_tokens=spaces_between_special_tokens,
        truncate_prompt_tokens=truncate_prompt_tokens,
    )
    return llm.generate(prompt, sampling_params)[0].outputs[0].text


vllm_client = cc.deploy(vllm_service)(gpu_memory_utilization=0.9)
vllm_client = cc.get_deployment(vllm_client, wait=True)
print(vllm_client)
