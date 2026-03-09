from __future__ import annotations

import asyncio

from autogen_agentchat.teams import RoundRobinGroupChat

from _common import assert_standard_outputs, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.orchestrators import run_agent_example


async def main() -> None:
    planner = build_replay_assistant(
        name="planner_agent",
        responses=[
            "Handoff: I propose scanning documents first, then extracting risks and actions.",
        ],
        system_message="You are a planner agent. Produce compact plans.",
    )
    analyst = build_replay_assistant(
        name="analyst_agent",
        responses=[
            "Execution result: risks = onboarding delay; actions = automate onboarding and segment tracking.",
        ],
        system_message="You are an analyst agent. Convert plans into outcomes.",
    )
    team = RoundRobinGroupChat([planner, analyst], max_turns=2)

    _, package = await run_agent_example(
        example_id="04_multi_agent_handoff",
        task="Perform a simple planner-to-analyst handoff for the sample documents.",
        runner=team,
        metadata={"example_type": "multi_agent_handoff", "max_turns": 2},
    )

    write_extra_json(
        package,
        "handoff_structure.json",
        {
            "participants": ["planner_agent", "analyst_agent"],
            "handoff_pattern": "plan_then_execute",
        },
    )
    missing = assert_standard_outputs("04_multi_agent_handoff")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
