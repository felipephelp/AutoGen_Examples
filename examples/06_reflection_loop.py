from __future__ import annotations

import asyncio

from _common import assert_standard_outputs, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.orchestrators import run_agent_example


def _last_content(task_result: object) -> str:
    messages = getattr(task_result, "messages", [])
    if not messages:
        return ""
    return str(getattr(messages[-1], "content", ""))


async def main() -> None:
    assistant = build_replay_assistant(
        name="reflection_agent",
        responses=[
            "Draft v1: Build a document explorer with basic listing and summaries.",
            "Critique: Add deterministic outputs and explicit validation for each example.",
            "Draft v2: Build explorer + deterministic sample outputs + validation checklist.",
        ],
        system_message="Use a reflection loop to improve your own output.",
    )

    draft = await assistant.run(task="Write a first draft plan for this project.")
    critique = await assistant.run(task="Critique your own draft and list one weakness.")
    final_result, package = await run_agent_example(
        example_id="06_reflection_loop",
        task="Produce a revised final plan after reflection.",
        runner=assistant,
        metadata={"example_type": "reflection_loop"},
    )

    write_extra_json(
        package,
        "reflection_cycles.json",
        {
            "cycle_1_draft": _last_content(draft),
            "cycle_2_critique": _last_content(critique),
            "cycle_3_final": _last_content(final_result),
        },
    )
    missing = assert_standard_outputs("06_reflection_loop")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
