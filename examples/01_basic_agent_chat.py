from __future__ import annotations

import asyncio

from _common import assert_standard_outputs, write_extra_markdown
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.orchestrators import run_agent_example


async def main() -> None:
    assistant = build_replay_assistant(
        name="basic_assistant",
        responses=[
            "AutoGen can orchestrate autonomous agents, tools, and workflows in a reusable way.",
        ],
        system_message="You explain AutoGen examples in concise language.",
    )

    _, package = await run_agent_example(
        example_id="01_basic_agent_chat",
        task="Explain what this repository demonstrates.",
        runner=assistant,
        metadata={"example_type": "single_agent"},
    )

    write_extra_markdown(
        package,
        "expected_behavior.md",
        "- One assistant reply is generated.\n- No tool calls are required.\n",
    )
    missing = assert_standard_outputs("01_basic_agent_chat")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
