---
name: evaluation
description: Add or maintain tests and evaluation cases for the BI copilot. Use when editing tests, tests/evaluation/basic_questions.json, mocked workflow tests, regression cases for SQL generation/verification/reporting, or quality checks for no invented tables/metrics.
---

# Evaluation

Use this skill to add regression coverage without depending on live LLM variability.

## Workflow

1. Inspect the behavior under test and the current state contract.
2. Prefer deterministic unit tests for tools and state transitions.
3. Mock LLMs, agents, database calls, and tool calls for workflow tests.
4. Use live database/model tests only when explicitly needed and documented.
5. Run the narrowest useful pytest command.

## Test Targets

- SQL validator behavior: `tests/unit/test_sql_validator.py`
- Workflow behavior: `tests/unit/test_workflow.py`
- Evaluation questions: `tests/evaluation/basic_questions.json`

## Good Regression Cases

Add cases for:

- no invented tables or columns
- governed revenue logic
- `COUNT(DISTINCT orders.order_id)` after joins
- AOV at order grain
- one-to-many join fanout risks
- invalid SQL blocked before execution
- empty query result not treated as a finding
- verifier warning/fail behavior
- final answer caveats

## Command Patterns

Use:

```bash
PYTHONPATH=src pytest tests/unit/test_sql_validator.py
PYTHONPATH=src pytest tests/unit/test_workflow.py
PYTHONPATH=src pytest
```

Plain `pytest` may fail imports unless the package is installed or `PYTHONPATH=src` is set.

## Test Design

Assert outputs that are part of the contract, not incidental formatting.

For LLM-like behavior, test parsed/structured results or mocked outputs. Avoid brittle assertions on full natural-language responses unless the response contract requires exact text.
