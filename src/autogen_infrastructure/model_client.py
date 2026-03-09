from __future__ import annotations

import json
import os
from typing import Any, Literal, Sequence

from autogen_core import FunctionCall
from autogen_core.models import CreateResult, RequestUsage
from autogen_ext.models.replay import ReplayChatCompletionClient

LiveBackend = Literal["api", "vllm", "ollama"]

DEFAULT_MODEL_INFO = {
    "vision": False,
    "function_calling": False,
    "json_output": True,
    "structured_output": True,
    "family": "unknown",
    "multiple_system_messages": False,
}


def _build_model_info(*, function_calling: bool) -> dict[str, Any]:
    """Create model capabilities used for custom/non-canonical model names."""
    model_info = dict(DEFAULT_MODEL_INFO)
    model_info["function_calling"] = function_calling
    return model_info


def apply_local_gpu_config(*, cuda_visible_devices: str | None = None) -> None:
    """Apply local GPU visibility for backends that honor CUDA_VISIBLE_DEVICES."""
    if cuda_visible_devices:
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda_visible_devices


def create_replay_client(
    responses: Sequence[str | CreateResult],
    *,
    function_calling: bool = False,
) -> ReplayChatCompletionClient:
    """Create deterministic replay model client for offline/example runs."""
    return ReplayChatCompletionClient(
        responses,
        model_info=_build_model_info(function_calling=function_calling),
    )


def create_openai_compatible_client(
    *,
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
    function_calling: bool = False,
    temperature: float = 0.2,
    max_tokens: int = 1200,
    include_name_in_message: bool | None = None,
) -> Any:
    """Create OpenAI-compatible live client (OpenAI/Groq/vLLM endpoint)."""
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise ImportError(
            "Live API mode requires OpenAI-compatible dependencies. "
            "Install with: pip install openai tiktoken"
        ) from exc

    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    if not resolved_api_key:
        raise ValueError(
            "Missing API key for live mode. Set OPENAI_API_KEY/GROQ_API_KEY or pass --api-key."
        )

    resolved_base_url = base_url or os.getenv("OPENAI_BASE_URL")

    if include_name_in_message is None:
        lowered = (resolved_base_url or "").lower()
        include_name_in_message = "groq" not in lowered

    kwargs: dict[str, Any] = {
        "model": model,
        "api_key": resolved_api_key,
        "model_info": _build_model_info(function_calling=function_calling),
        "temperature": temperature,
        "max_tokens": max_tokens,
        "include_name_in_message": include_name_in_message,
    }
    if resolved_base_url:
        kwargs["base_url"] = resolved_base_url

    return OpenAIChatCompletionClient(**kwargs)


def create_vllm_client(
    *,
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
    function_calling: bool = False,
    temperature: float = 0.2,
    max_tokens: int = 1200,
) -> Any:
    """Create vLLM client through OpenAI-compatible endpoint.

    Note: GPU allocation for vLLM is done on the vLLM server process itself.
    The client can still set CUDA_VISIBLE_DEVICES for local single-process setups.
    """
    resolved_base_url = base_url or os.getenv("VLLM_BASE_URL") or "http://localhost:8000/v1"
    resolved_api_key = api_key or os.getenv("VLLM_API_KEY") or "local-vllm"
    return create_openai_compatible_client(
        model=model,
        api_key=resolved_api_key,
        base_url=resolved_base_url,
        function_calling=function_calling,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def create_ollama_client(
    *,
    model: str,
    host: str | None = None,
    function_calling: bool = False,
    temperature: float = 0.2,
    num_gpu: int | None = None,
    num_ctx: int | None = None,
    num_predict: int | None = None,
) -> Any:
    """Create Ollama client for local inference.

    `num_gpu` controls local GPU allocation in Ollama options.
    """
    try:
        from autogen_ext.models.ollama import OllamaChatCompletionClient
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise ImportError(
            "Ollama backend requires dependencies. Install with: pip install ollama tiktoken"
        ) from exc

    resolved_host = host or os.getenv("OLLAMA_HOST") or "http://localhost:11434"
    kwargs: dict[str, Any] = {
        "model": model,
        "host": resolved_host,
        "model_info": _build_model_info(function_calling=function_calling),
        "temperature": temperature,
    }
    if num_gpu is not None:
        kwargs["num_gpu"] = num_gpu
    if num_ctx is not None:
        kwargs["num_ctx"] = num_ctx
    if num_predict is not None:
        kwargs["num_predict"] = num_predict

    return OllamaChatCompletionClient(**kwargs)


def create_live_client(
    *,
    backend: LiveBackend,
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
    ollama_host: str | None = None,
    function_calling: bool = False,
    temperature: float = 0.2,
    max_tokens: int = 1200,
    num_gpu: int | None = None,
    num_ctx: int | None = None,
    num_predict: int | None = None,
) -> Any:
    """Create live model client for API, vLLM, or Ollama backends."""
    if backend == "api":
        return create_openai_compatible_client(
            model=model,
            api_key=api_key,
            base_url=base_url,
            function_calling=function_calling,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    if backend == "vllm":
        return create_vllm_client(
            model=model,
            api_key=api_key,
            base_url=base_url,
            function_calling=function_calling,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    return create_ollama_client(
        model=model,
        host=ollama_host,
        function_calling=function_calling,
        temperature=temperature,
        num_gpu=num_gpu,
        num_ctx=num_ctx,
        num_predict=num_predict,
    )


def tool_call_result(
    *,
    name: str,
    arguments: dict[str, Any],
    call_id: str = "call_1",
    prompt_tokens: int = 25,
    completion_tokens: int = 8,
) -> CreateResult:
    """Create deterministic function-call message for replay tool-calling runs."""
    return CreateResult(
        finish_reason="function_calls",
        content=[
            FunctionCall(
                id=call_id,
                name=name,
                arguments=json.dumps(arguments),
            )
        ],
        usage=RequestUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens),
        cached=False,
    )
