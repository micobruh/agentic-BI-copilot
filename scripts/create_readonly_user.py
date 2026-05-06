import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
READONLY_USER = os.environ["BI_READONLY_USER"]
READONLY_PASSWORD = os.environ["BI_READONLY_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]


def quote_identifier(identifier: str) -> str:
    """
    Safely quote a PostgreSQL identifier such as a role or database name.
    """
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


def main() -> None:
    engine = create_engine(DATABASE_URL)

    readonly_user = quote_identifier(READONLY_USER)
    database_name = quote_identifier(POSTGRES_DB)

    with engine.begin() as conn:
        role_exists = conn.execute(
            text("SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :role_name"),
            {"role_name": READONLY_USER},
        ).scalar()

        if role_exists:
            conn.execute(
                text(
                    f"""
                    ALTER ROLE {readonly_user}
                    WITH LOGIN PASSWORD :password
                    """
                ),
                {"password": READONLY_PASSWORD},
            )
            print(f"Updated password for existing role: {READONLY_USER}")
        else:
            conn.execute(
                text(
                    f"""
                    CREATE ROLE {readonly_user}
                    LOGIN PASSWORD :password
                    """
                ),
                {"password": READONLY_PASSWORD},
            )
            print(f"Created role: {READONLY_USER}")

        conn.execute(text(f"GRANT CONNECT ON DATABASE {database_name} TO {readonly_user}"))
        conn.execute(text(f"GRANT USAGE ON SCHEMA public TO {readonly_user}"))
        conn.execute(text(f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {readonly_user}"))
        conn.execute(text(f"GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO {readonly_user}"))

        conn.execute(
            text(
                f"""
                ALTER DEFAULT PRIVILEGES IN SCHEMA public
                GRANT SELECT ON TABLES TO {readonly_user}
                """
            )
        )

        conn.execute(
            text(
                f"""
                ALTER DEFAULT PRIVILEGES IN SCHEMA public
                GRANT SELECT ON SEQUENCES TO {readonly_user}
                """
            )
        )

    print("Read-only user setup completed.")


if __name__ == "__main__":
    main()