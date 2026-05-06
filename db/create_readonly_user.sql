-- db/create_readonly_user.sql
--
-- Requires psql variables:
--   readonly_user
--   readonly_password
--   database_name
--
-- Example:
--   psql -v readonly_user=bi_readonly \
--        -v readonly_password=secret \
--        -v database_name=olist_bi \
--        -f db/create_readonly_user.sql

DO $$
DECLARE
    role_name text := :'readonly_user';
    role_password text := :'readonly_password';
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles
        WHERE rolname = role_name
    ) THEN
        EXECUTE format(
            'CREATE ROLE %I LOGIN PASSWORD %L',
            role_name,
            role_password
        );
    ELSE
        EXECUTE format(
            'ALTER ROLE %I WITH LOGIN PASSWORD %L',
            role_name,
            role_password
        );
    END IF;
END
$$;

GRANT CONNECT ON DATABASE :"database_name" TO :"readonly_user";

GRANT USAGE ON SCHEMA public TO :"readonly_user";

GRANT SELECT ON ALL TABLES IN SCHEMA public TO :"readonly_user";

GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO :"readonly_user";

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO :"readonly_user";

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON SEQUENCES TO :"readonly_user";