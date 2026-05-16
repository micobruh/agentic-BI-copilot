# SQL Safety

`src/bi_copilot/tools/sql_query_guard.py` is the main SQL safety layer.

Preserve these principles:

- only one SQL statement
- SELECT-only
- no write or DDL statements
- no cross-catalog references
- only allowed schemas, currently `public`
- reject unknown tables/views and unknown columns
- flag `SELECT *`
- require `LIMIT` for row-returning queries by default
- enforce max `LIMIT` through `ValidationPolicy`
- validate function allowlist
- use sqlglot for parsing instead of string matching

When adding validator behavior, add focused tests in `tests/unit/test_sql_validator.py`.
