---
name: metadata-retrieval
description: Implement or modify schema and metadata retrieval for the BI copilot. Use when working on get_database_schema, metadata_retriever nodes, table_descriptions.yaml, metric_glossary.yaml loading, database_schema/relevant_tables/metric_definitions state flow, or prompt context assembly.
---

# Metadata Retrieval

Use this skill to populate the BI workflow with stable schema and governed metadata.

## Workflow

1. Inspect `BIState` before changing metadata flow.
2. Load physical schema with `get_database_schema()`.
3. Load semantic table metadata with `load_table_descriptions()`.
4. Load governed metrics with `load_metric_glossary()`.
5. Keep physical schema, table descriptions, and metric definitions distinct in state or context.
6. Add tests for shape and routing behavior when retrieval nodes are implemented.

## State Meanings

- `database_schema`: all known public tables/views mapped to ordered column lists.
- `relevant_tables`: subset selected by the planner for the question.
- `metric_definitions`: governed metric glossary content.
- `retrieved_context`: extra context retrieved for planning/generation/reporting.

Do not overwrite `relevant_tables` with all available tables.

## Schema Behavior

`get_database_schema()` should:

- inspect public tables and views
- return `dict[str, list[str]]`
- sort table/view names for deterministic prompts
- preserve database inspector column order

Do not return sets from `get_database_schema()`; lists serialize better and preserve order.

## Metadata Assembly

For SQL generation, prefer passing:

- full `database_schema`, or a clearly filtered subset plus table names
- `relevant_tables`
- relevant table descriptions and caveats
- relevant metric definitions

For planning, pass available table names from `database_schema`, not prior `relevant_tables`.

## Common Risks

- mixing metric definitions into table schema
- losing grain/caveat information before SQL generation
- duplicating table metadata in multiple places
- making metadata retrieval depend on live LLM calls
