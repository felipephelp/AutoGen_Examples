from __future__ import annotations

from collections.abc import Callable
from typing import Any

from autogen_agentchat.agents import AssistantAgent

from .model_client import LiveBackend, create_live_client, create_replay_client


def build_replay_assistant(
    *,
    name: str,
    responses: list[Any],
    tools: list[Callable[..., Any]] | None = None,
    system_message: str | None = None,
    reflect_on_tool_use: bool = True,
) -> AssistantAgent:
    """Build deterministic replay assistant used in local didactic examples."""
    uses_tools = bool(tools)
    model_client = create_replay_client(responses, function_calling=uses_tools)
    return AssistantAgent(
        name=name,
        model_client=model_client,
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=reflect_on_tool_use if uses_tools else None,
    )


def build_live_assistant(
    *,
    name: str,
    backend: LiveBackend,
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
    ollama_host: str | None = None,
    tools: list[Callable[..., Any]] | None = None,
    system_message: str | None = None,
    reflect_on_tool_use: bool = True,
    temperature: float = 0.2,
    max_tokens: int = 1200,
    num_gpu: int | None = None,
    num_ctx: int | None = None,
    num_predict: int | None = None,
) -> AssistantAgent:
    """Build live assistant for API/vLLM/Ollama backends."""
    uses_tools = bool(tools)
    model_client = create_live_client(
        backend=backend,
        model=model,
        api_key=api_key,
        base_url=base_url,
        ollama_host=ollama_host,
        function_calling=uses_tools,
        temperature=temperature,
        max_tokens=max_tokens,
        num_gpu=num_gpu,
        num_ctx=num_ctx,
        num_predict=num_predict,
    )
    return AssistantAgent(
        name=name,
        model_client=model_client,
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=reflect_on_tool_use if uses_tools else None,
    )
