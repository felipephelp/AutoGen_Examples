from __future__ import annotations

from collections.abc import Callable
from typing import Any

from autogen_agentchat.agents import AssistantAgent

from .model_client import create_replay_client


def build_replay_assistant(
    *,
    name: str,
    responses: list[Any],
    tools: list[Callable[..., Any]] | None = None,
    system_message: str | None = None,
    reflect_on_tool_use: bool = True,
) -> AssistantAgent:
    uses_tools = bool(tools)
    model_client = create_replay_client(responses, function_calling=uses_tools)
    return AssistantAgent(
        name=name,
        model_client=model_client,
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=reflect_on_tool_use if uses_tools else None,
    )
