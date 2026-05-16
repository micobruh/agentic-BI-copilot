---
name: workflow-node
description: Implement or modify LangGraph-style workflow nodes and routing for the BI copilot. Use when editing src/bi_copilot/graph/nodes/*, src/bi_copilot/graph/workflow.py, BIState transitions, node wrappers around agents/tools, or workflow-level tests.
---

# Workflow Node

Use this skill to wire runtime behavior without duplicating agent logic.

## Workflow

1. Inspect `src/bi_copilot/graph/state.py` first.
2. Reuse existing agent classes from `src/bi_copilot/agents/` whenever possible.
3. Keep graph nodes thin: extract state, call an agent/tool, return partial state updates.
4. Put durable behavior in agents or tools, not in graph wrapper glue.
5. Add workflow tests with mocked LLM/tool calls before relying on live database or model behavior.

## Intended Flow

1. Metadata retrieval populates `database_schema`, `metric_definitions`, and useful table context.
2. Planner returns `intent`, `plan`, `retrieval_targets`, and `relevant_tables`.
3. SQL generator writes `generated_sql`.
4. SQL validator writes `sql_validation_result`.
5. SQL executor writes `query_result` only if validation passes.
6. Reporter writes `analysis_summary` and `final_answer`.
7. Verifier writes `verification_result`.

## State Rules

- `database_schema` is all available schema context.
- `relevant_tables` is planner output, not planner input.
- `metric_definitions` is governed business metadata, not physical schema.
- Append to `errors` and `audit_trace`; do not discard existing entries.
- Return partial state dicts compatible with `BIState`.

## Routing Guidance

- Stop or ask clarification when planner says the question is not safely answerable.
- Do not execute SQL if validation result is invalid.
- Surface validation errors in `errors` and final answer path.
- Keep runtime prompts in `src/bi_copilot/prompts/`; do not hardcode long prompts in nodes.

## Verification

For workflow changes, prefer:

```bash
PYTHONPATH=src pytest
```

If no workflow tests exist for the touched path, add focused tests with fake agents/tools rather than calling live LLMs.
