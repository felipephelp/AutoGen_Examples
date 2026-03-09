from __future__ import annotations

import asyncio

from _common import assert_standard_outputs, get_project_paths, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.model_client import tool_call_result
from autogen_infrastructure.orchestrators import run_agent_example
from autogen_infrastructure.tools_registry import file_explorer_tools


async def main() -> None:
    """Run tool-calling example for directory exploration."""
    paths = get_project_paths()
    target_dir = str(paths.data / "documents")

    assistant = build_replay_assistant(
        name="file_explorer_agent",
        responses=[
            tool_call_result(
                name="list_directory",
                arguments={"path": target_dir},
                call_id="list_docs",
            ),
            "The folder contains two project files. Both are ready for downstream analysis.",
        ],
        tools=file_explorer_tools(),
        system_message="Use tools to inspect folders before answering.",
    )

    _, package = await run_agent_example(
        example_id="02_tools_file_explorer",
        task=f"Inspect this directory and summarize what exists: {target_dir}",
        runner=assistant,
        metadata={"example_type": "tool_calling", "target_directory": target_dir},
    )

    write_extra_json(
        package,
        "expected_summary.json",
        {
            "expected_tools": ["list_directory"],
            "expected_files": ["project_overview.txt", "quarterly_report.txt"],
        },
    )
    missing = assert_standard_outputs("02_tools_file_explorer")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
