# Runtime Agents And Prompts

## Agent Conventions

All runtime agents should subclass `BaseAgent` from `src/bi_copilot/agents/base.py`.

Each agent should implement:

- `build_chain()`: construct the LangChain runnable
- `build_input(state: BIState)`: extract only the fields needed by that agent
- `parse_output(output, state: BIState)`: return a partial `BIState` update dict

`BaseAgent.ainvoke()` appends an audit entry on success and returns an error update on exception. Keep this behavior in mind when changing output types or parser behavior.

Use Pydantic output parsers for internal structured outputs:

- planner output
- verifier output
- future routing/classification outputs

Use plain strings only where the downstream contract expects free text:

- SQL generation returns raw SQL
- final reporter output returns user-facing Markdown/text

## Runtime Prompt Guidelines

Runtime prompts live in `src/bi_copilot/prompts/`.

Current prompts:

- `planner.md`: planning and retrieval-target selection
- `sql_generator.md`: governed PostgreSQL SQL generation
- `verifier.md`: final verification criteria
- `reporter.md`: final business-facing answer style and grounding rules

When editing prompts:

- keep prompts task-specific
- avoid leaking repo maintenance guidance into runtime prompts
- require grounding in provided schema, metadata, query result, and validation outputs
- state output format explicitly
- for structured agents, keep prompt instructions aligned with the Pydantic model
- for SQL generation, preserve SELECT-only and single-statement constraints
- for final reporting, Markdown is the preferred user-facing format

Do not use `AGENTS.md` as a runtime prompt unless the application is deliberately designed to do so.
