# AGENTS.md

Development-time guidance for coding agents working on the MCP-enabled Agentic BI Copilot for the Olist e-commerce and marketing funnel datasets.

This file is not a runtime prompt for the BI copilot. Runtime agent behavior lives in `src/bi_copilot/prompts/*.md`.

## Essentials

- Package manager: `uv`.
- Python version: 3.11+.
- Before editing, run `git status --short` and preserve unrelated user changes.
- Use `PYTHONPATH=src pytest` or `PYTHONPATH=src pytest tests/unit/test_sql_validator.py`; plain `pytest` may not import `bi_copilot`.
- Never commit `.env`, raw Kaggle datasets, credentials, generated artifacts, or `__pycache__` files.

## Guides

- [Architecture](docs/agent-guides/architecture.md)
- [Runtime Agents And Prompts](docs/agent-guides/runtime-agents-and-prompts.md)
- [Workflow State And Graph](docs/agent-guides/workflow-state-and-graph.md)
- [SQL Safety](docs/agent-guides/sql-safety.md)
- [Metadata And Metrics](docs/agent-guides/metadata-and-metrics.md)
- [Database Setup](docs/agent-guides/database-setup.md)
- [Testing And Evaluation](docs/agent-guides/testing-and-evaluation.md)
- [Project-Local Skills](docs/agent-guides/project-local-skills.md)
- [Known Gaps](docs/agent-guides/known-gaps.md)
- [Deletion Candidates](docs/agent-guides/deletion-candidates.md)

## Suggested Docs Structure

```text
docs/
  agent-guides/
    architecture.md
    runtime-agents-and-prompts.md
    workflow-state-and-graph.md
    sql-safety.md
    metadata-and-metrics.md
    database-setup.md
    testing-and-evaluation.md
    project-local-skills.md
    known-gaps.md
    deletion-candidates.md
```
