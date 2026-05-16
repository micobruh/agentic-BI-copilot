---
name: prompt-engineering
description: Edit runtime prompts for the BI copilot agents. Use when changing src/bi_copilot/prompts/*.md, agent prompt inputs, structured output instructions, SQL generation behavior, reporter answer style, or verifier criteria.
---

# Prompt Engineering

Use this skill to keep runtime prompts precise, grounded, and aligned with code contracts.

## Workflow

1. Inspect the agent class that reads the prompt.
2. Identify the prompt inputs from `build_input()`.
3. For structured agents, inspect the Pydantic output model.
4. Edit only the prompt files needed for the behavioral change.
5. Keep output format instructions explicit.

## Prompt Contracts

- `planner.md` must produce fields compatible with `PlannerOutput`.
- `sql_generator.md` must return raw PostgreSQL SQL only.
- `verifier.md` must produce fields compatible with `VerifierOutput`.
- `reporter.md` should return the final business-facing answer, preferably Markdown.

## Grounding Rules

Runtime prompts should tell agents to use only provided:

- user question
- plan
- database schema
- relevant tables
- metric definitions
- SQL validation result
- query result
- verification result

Do not let prompts rely on hidden repo context, external knowledge, or `AGENTS.md`.

## SQL Prompt Rules

Preserve:

- SELECT-only
- PostgreSQL-compatible SQL
- one statement only
- no markdown fences
- no invented tables, columns, joins, metrics, filters, or business rules
- safe grain and pre-aggregation guidance

## Reporter Prompt Rules

The reporter should:

- answer directly
- stay grounded in query results
- mention important caveats
- avoid raw JSON dumps for small results
- avoid showing SQL unless requested
- avoid internal agent names

## Verifier Prompt Rules

The verifier should be strict about:

- invalid SQL validation result
- unsupported summary claims
- metric definition drift
- missing filters
- unsafe joins or fanout
- empty results interpreted as findings
