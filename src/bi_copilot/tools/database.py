# src/bi_copilot/tools/database.py

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

READONLY_DATABASE_URL = os.environ["BI_READONLY_DATABASE_URL"]

engine = create_engine(READONLY_DATABASE_URL)


def run_readonly_sql(sql: str) -> list[dict]:
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return [dict(row._mapping) for row in result]