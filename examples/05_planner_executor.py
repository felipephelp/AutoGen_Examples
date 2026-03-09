from __future__ import annotations

import asyncio

from autogen_agentchat.teams import RoundRobinGroupChat

from _common import assert_standard_outputs, get_project_paths, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.model_client import tool_call_result
from autogen_infrastructure.orchestrators import run_agent_example
from autogen_infrastructure.tools_registry import file_explorer_tools


async def main() -> None:
    paths = get_project_paths()
    target_dir = str(paths.data)

    planner = build_replay_assistant(
        name="planner",
        responses=[
            "Plan: 1) enumerate text-like files in data, 2) return a concise inventory.",
        ],
        system_message="Create short executable plans.",
    )
    executor = build_replay_assistant(
        name="executor",
        responses=[
            tool_call_result(
                name="list_text_files",
                arguments={"path": target_dir, "recursive": True},
                call_id="list_text_files_1",
            ),
            "Execution complete: text-like files were listed from the data folder.",
        ],
        tools=file_explorer_tools(),
        system_message="Execute the planner's instructions using tools.",
    )

    team = RoundRobinGroupChat([planner, executor], max_turns=2)

    _, package = await run_agent_example(
        example_id="05_planner_executor",
        task=f"Run planner/executor workflow for {target_dir}",
        runner=team,
        metadata={"example_type": "planner_executor", "target_directory": target_dir},
    )
    write_extra_json(
        package,
        "plan_expectation.json",
        {
            "plan_steps": [
                "enumerate text files",
                "summarize inventory",
            ],
            "tool_expected": "list_text_files",
        },
    )
    missing = assert_standard_outputs("05_planner_executor")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
