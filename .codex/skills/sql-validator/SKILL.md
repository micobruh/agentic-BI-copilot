---
name: sql-validator
description: Extend and maintain the BI copilot SQL validator. Use when changing src/bi_copilot/tools/sql_query_guard.py, ValidationPolicy, sqlglot parsing, SQL safety rules, schema-reference validation, or tests for generated SQL safety.
---

# SQL Validator

Use this skill to modify SQL validation without weakening the BI copilot's safety boundary.

## Workflow

1. Inspect `src/bi_copilot/tools/sql_query_guard.py` and the relevant tests in `tests/unit/test_sql_validator.py`.
2. Preserve parser-based validation with `sqlglot`; do not replace core checks with ad hoc string matching.
3. Keep validation outputs stable unless the user explicitly wants an API change:
   - `is_valid`
   - `errors`
   - `warnings`
   - `risk_flags`
   - `referenced_tables`
   - `parsed_type`
   - `safe_sql`
4. Add or update tests for every validator behavior change.
5. Run `PYTHONPATH=src pytest tests/unit/test_sql_validator.py`.

## Rules To Preserve

- Accept only one SQL statement.
- Accept SELECT/read-only analytics only.
- Reject write, DDL, and command expressions.
- Reject unknown tables/views and columns.
- Reject cross-catalog references and disallowed schemas.
- Keep allowed schemas explicit; currently `public`.
- Flag `SELECT *`.
- Enforce `ValidationPolicy.require_limit_for_row_queries`.
- Enforce `ValidationPolicy.max_limit`.
- Validate function allowlist behavior.
- Return canonical `safe_sql` only when the query is valid.

## Schema Handling

`get_database_schema()` returns `dict[str, list[str]]`. The validator type should accept generic column collections and convert to sets internally only where membership checks need it.

Do not force the database schema back to `dict[str, set[str]]`; lists are intentional for state serialization and prompt readability.

## Test Patterns

Prefer small tests that assert:

- validity or invalidity
- important error text or risk flag
- referenced table list
- `safe_sql` is present only for valid SQL

When adding a new risk category, assert the `risk_flags` value directly so future agents notice regressions.
