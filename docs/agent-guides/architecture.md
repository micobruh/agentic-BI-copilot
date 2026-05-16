# Architecture

## Project Purpose

This project is an MCP-enabled Agentic Business Intelligence Copilot for the Olist Brazilian E-Commerce and Marketing Funnel datasets.

The application is intended to:

- inspect governed metadata and database schema
- plan how to answer a business question
- generate safe read-only PostgreSQL SQL
- validate generated SQL before execution
- execute SQL with read-only credentials
- verify that the result actually supports the answer
- produce a concise final business-facing answer

Core themes:

- governed BI, not free-form database chatting
- metadata-grounded SQL generation
- read-only database access
- SQL safety validation
- self-verification before final reporting

## Tech Stack

- Python 3.11+
- `uv`
- LangChain / LangGraph-style agents
- Pydantic for structured state and agent outputs
- PostgreSQL for analytics
- SQLAlchemy for DB inspection and execution
- sqlglot for SQL parsing and validation
- PyYAML for metadata loading
- pytest for tests
- ruff and mypy are listed as dev dependencies
- Docker Compose for local PostgreSQL setup

## Repository Map

- `src/bi_copilot/agents/`: runtime agent classes
- `src/bi_copilot/prompts/`: runtime system prompts for each agent
- `src/bi_copilot/graph/state.py`: shared workflow state contract
- `src/bi_copilot/graph/nodes/`: LangGraph node wrappers
- `src/bi_copilot/graph/workflow.py`: intended workflow assembly
- `src/bi_copilot/tools/database.py`: database schema inspection and read-only SQL execution
- `src/bi_copilot/tools/sql_query_guard.py`: SQL validator and safety policy
- `src/bi_copilot/tools/metadata.py`: metadata YAML loaders
- `src/bi_copilot/mcp/servers/`: MCP server wrappers for tools
- `data/metadata/table_descriptions.yaml`: semantic table metadata
- `data/metadata/metric_glossary.yaml`: governed metric definitions
- `db/schema.sql`: base table DDL
- `db/views.sql`: analytics views
- `db/indexes.sql`: indexes
- `tests/unit/test_sql_validator.py`: main SQL validator test suite

## Intended Runtime Flow

1. Retrieve schema and governed metadata.
2. `PlannerAgent` determines intent, needed evidence, relevant tables, and next action.
3. `SQLAgent` generates PostgreSQL SELECT-only SQL from the question, schema, relevant tables, and metric definitions.
4. SQL validation checks safety, schema references, policy, and query shape.
5. SQL execution runs only validated read queries through read-only database credentials.
6. `ReporterAgent` drafts the final business-facing answer.
7. `VerifierAgent` checks that SQL, validation result, query result, and answer are aligned and grounded.
