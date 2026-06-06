# AGENTS.md

Development-time guidance for coding agents working on the MCP-enabled Agentic BI Copilot for the Olist e-commerce and marketing funnel datasets.

This file is not a runtime prompt for the BI copilot. Runtime agent behavior lives in `src/bi_copilot/prompts/*.md`.

## Essentials

- Package manager: `uv`.
- Python version: 3.11+.
- Before editing, run `git status --short` and preserve unrelated user changes.
- Use `PYTHONPATH=src pytest` or `PYTHONPATH=src pytest tests/unit/test_sql_validator.py`; plain `pytest` may not import `bi_copilot`.
- Never commit `.env`, raw Kaggle datasets, credentials, generated artifacts, or `__pycache__` files.
- Before changing SQL generation, metrics, metadata, prompts, or workflow routing, read the relevant guide under `docs/agent-guides/`; business metric semantics and table grain are project-specific and cannot be inferred safely from code alone.

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

## Optional External Skills

The project-local skills in `.codex/skills/` remain the default source of task guidance. The broader Antigravity/Awesome Skills catalog includes a few useful fallbacks for work that is not fully covered locally:

- `antigravity-skill-orchestrator`: use sparingly for complex, multi-domain tasks when the right skill mix is unclear.
- `langgraph`: useful for deeper workflow graph, state, branching, checkpointing, or human-in-the-loop changes.
- `mcp-builder` or `mcp-tool-developer`: useful when adding or redesigning MCP servers/tools and their agent-facing contracts.
- `tool-design`: useful when debugging MCP tool misuse, ambiguous tool descriptions, or tool-selection failures.
- `agent-evaluation` or `advanced-evaluation`: useful for LLM-agent benchmark design, rubrics, judge prompts, and reliability metrics beyond the local evaluation skill.
- `ai-agent-development` or `ai-agents-architect`: useful for larger agent architecture changes, multi-agent planning, memory, and orchestration.
- `llm-ops`: useful for production-quality LLM cost, prompt, eval, and observability decisions.
- `api-security-best-practices` or `privacy-by-design`: useful for API/MCP hardening, credential handling, and user-data protections.
- `sql-pro`, `postgresql`, or `postgres-best-practices`: useful for general SQL and Postgres tuning, but defer to local SQL safety and metric semantics first.

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
