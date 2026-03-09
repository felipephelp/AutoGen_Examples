from __future__ import annotations

import json
import os
import time
from typing import Any

from autogen_agentchat.base import TaskResult

from .output_writer import export_task_result


async def run_agent_example(
    *,
    example_id: str,
    task: str,
    runner: Any,
    metadata: dict[str, Any] | None = None,
) -> tuple[TaskResult, dict[str, Any]]:
    """Run an example task, persist outputs, and print concise run summary."""
    started = time.perf_counter()
    result: TaskResult = await runner.run(task=task)
    elapsed_s = round(time.perf_counter() - started, 4)
    package = export_task_result(
        example_id=example_id,
        task=task,
        result=result,
        metadata={
            "elapsed_seconds": elapsed_s,
            **(metadata or {}),
        },
    )

    # Console summary for individual runs (can be disabled by AUTOGEN_EXAMPLE_CONSOLE=0).
    show_console = os.getenv("AUTOGEN_EXAMPLE_CONSOLE", "1").strip().lower() not in {
        "0",
        "false",
        "no",
        "off",
    }
    if show_console:
        final_content: Any = ""
        if result.messages:
            final_content = getattr(result.messages[-1], "content", "")
        if not isinstance(final_content, str):
            final_content = json.dumps(final_content, ensure_ascii=False, indent=2)

        print(f"[{example_id}] INPUT: {task}")
        print(f"[{example_id}] OUTPUT: {final_content}")
        print(f"[{example_id}] OUTPUT_DIR: {package['output_dir']}")
    return result, package
