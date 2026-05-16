---
name: database-setup
description: Modify database DDL, views, indexes, loading scripts, Docker database setup, or read-only user configuration. Use when editing db/schema.sql, db/views.sql, db/indexes.sql, scripts/load_postgres.py, scripts/create_readonly_user.py, docker-compose.yml, or Makefile database targets.
---

# Database Setup

Use this skill for changes that affect the physical PostgreSQL database or local setup.

## Workflow

1. Inspect the relevant DB file before editing:
   - `db/schema.sql`
   - `db/views.sql`
   - `db/indexes.sql`
   - `scripts/load_postgres.py`
   - `scripts/create_readonly_user.py`
   - `Makefile`
2. Check whether semantic metadata must also change.
3. Check whether SQL validator tests or schema expectations must change.
4. Run database setup commands only when needed and when local dependencies/data are available.

## Setup Commands

Common Make targets:

```bash
make reset-db
make schema
make views
make indexes
make load-data
make readonly-user
```

`make reset-db` is destructive for the local Docker database volume. Do not run it unless the user requested or the task clearly requires a rebuild.

## Schema Change Checklist

When changing tables or views, consider updating:

- `data/metadata/table_descriptions.yaml`
- `data/metadata/metric_glossary.yaml`
- SQL generator prompt rules
- SQL validator tests
- evaluation questions
- README schema/setup notes

## Read-Only Safety

The BI agent should execute through read-only credentials.

Preserve:

- read access to required tables/views
- blocked write/DDL access for read-only users
- `BI_READONLY_DATABASE_URL` usage in runtime database tools

## Data Rules

- Do not commit `.env`.
- Do not commit raw Kaggle datasets.
- Keep `.env.example` as the shareable template.
- Be careful with generated artifacts and local database outputs.
