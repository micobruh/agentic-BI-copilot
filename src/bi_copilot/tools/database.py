# src/bi_copilot/tools/database.py
from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()

READONLY_DATABASE_URL = os.environ["BI_READONLY_DATABASE_URL"]

engine = create_engine(READONLY_DATABASE_URL)


def run_readonly_sql(sql: str) -> list[dict]:
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return [dict(row._mapping) for row in result]
    

def get_database_schema() -> dict[str, list[str]]:
    inspector = inspect(engine)

    schema: dict[str, list[str]] = {}

    for object_name in (
        *inspector.get_table_names(schema="public"),
        *inspector.get_view_names(schema="public"),
    ):
        columns = inspector.get_columns(object_name, schema="public")
        schema[object_name] = [col["name"] for col in columns]

    return dict(sorted(schema.items()))
