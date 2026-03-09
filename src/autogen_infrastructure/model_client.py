from __future__ import annotations

import json
from typing import Any, Sequence

from autogen_core import FunctionCall
from autogen_core.models import CreateResult, RequestUsage
from autogen_ext.models.replay import ReplayChatCompletionClient

DEFAULT_MODEL_INFO = {
    "vision": False,
    "function_calling": False,
    "json_output": True,
    "structured_output": True,
    "family": "unknown",
    "multiple_system_messages": False,
}


def create_replay_client(
    responses: Sequence[str | CreateResult],
    *,
    function_calling: bool = False,
) -> ReplayChatCompletionClient:
    model_info = dict(DEFAULT_MODEL_INFO)
    model_info["function_calling"] = function_calling
    return ReplayChatCompletionClient(responses, model_info=model_info)


def tool_call_result(
    *,
    name: str,
    arguments: dict[str, Any],
    call_id: str = "call_1",
    prompt_tokens: int = 25,
    completion_tokens: int = 8,
) -> CreateResult:
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
