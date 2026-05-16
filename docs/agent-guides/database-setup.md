# Database Setup

`db/schema.sql` defines the base database schema.

`src/bi_copilot/tools/database.py` contains:

- `run_readonly_sql(sql: str) -> list[dict]`
- `get_database_schema() -> dict[str, list[str]]`

Current schema behavior:

- returns both tables and views from the public schema
- sorts table/view names alphabetically
- preserves database inspector column order
- returns `dict[str, list[str]]`, not sets

This is intentional:

- sorted table/view names make prompts and tests deterministic
- original column order keeps schema context closer to the DDL and inspector output
- lists serialize cleanly in Pydantic state and prompts

The SQL validator accepts schema columns as a generic collection and converts to sets internally where membership checks are needed.

## Make Targets

Only run Docker/database commands when they are needed for the task. They may require a populated `.env`, local Docker, and raw dataset files.

```bash
make reset-db
make schema
make views
make indexes
make load-data
make readonly-user
```

The project expects environment variables from `.env`. Important variables include database credentials and `BI_READONLY_DATABASE_URL`.

Never commit `.env` or raw Kaggle datasets. `.env.example` is the committed template.
