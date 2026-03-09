from __future__ import annotations

import asyncio
import os

from _common import assert_standard_outputs, get_project_paths, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.model_client import tool_call_result
from autogen_infrastructure.orchestrators import run_agent_example
from autogen_infrastructure.tools_registry import file_explorer_tools


def _last_content(task_result: object) -> str:
    messages = getattr(task_result, "messages", [])
    if not messages:
        return ""
    return str(getattr(messages[-1], "content", ""))


async def main() -> None:
    paths = get_project_paths()
    target_dir = str(paths.data / "documents")

    reviewer = build_replay_assistant(
        name="reviewer",
        responses=[
            "Proposal: run file inventory on data/documents and summarize key files.",
        ],
        system_message="Propose one actionable next step and wait for human approval.",
    )
    proposal_result = await reviewer.run(task=f"Propose next action for: {target_dir}")
    proposal_text = _last_content(proposal_result)

    human_decision = os.getenv("HUMAN_APPROVAL", "approve").strip().lower()
    approved = human_decision in {"approve", "approved", "yes", "y", "true", "1"}

    if approved:
        executor = build_replay_assistant(
            name="executor",
            responses=[
                tool_call_result(
                    name="list_directory",
                    arguments={"path": target_dir},
                    call_id="human_approved_1",
                ),
                "Execution finished after human approval.",
            ],
            tools=file_explorer_tools(),
            system_message="Execute only approved actions.",
        )
        _, package = await run_agent_example(
            example_id="09_human_in_the_loop",
            task=f"Human approved. Execute the proposed action for: {target_dir}",
            runner=executor,
            metadata={"example_type": "human_in_the_loop", "approved": True},
        )
    else:
        reject_agent = build_replay_assistant(
            name="executor",
            responses=["Execution skipped because the human reviewer rejected the action."],
            system_message="If approval is missing, do not execute tools.",
        )
        _, package = await run_agent_example(
            example_id="09_human_in_the_loop",
            task="Human rejected the action. Confirm that execution is skipped.",
            runner=reject_agent,
            metadata={"example_type": "human_in_the_loop", "approved": False},
        )

    write_extra_json(
        package,
        "human_decisions.json",
        {
            "proposal": proposal_text,
            "raw_decision_env": human_decision,
            "approved": approved,
        },
    )

    missing = assert_standard_outputs("09_human_in_the_loop")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
