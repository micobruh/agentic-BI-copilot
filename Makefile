include .env
export

POSTGRES_CONTAINER ?= olist_bi_postgres

wait-postgres:
	@echo "Waiting for PostgreSQL to be ready..."
	@until docker exec $(POSTGRES_CONTAINER) pg_isready -U $(POSTGRES_USER) -d $(POSTGRES_DB); do \
		sleep 1; \
	done
	@echo "PostgreSQL is ready."

reset-db:
	docker compose down -v
	docker compose up -d postgres
	$(MAKE) wait-postgres
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < db/schema.sql
	docker compose run --rm app uv run python scripts/load_postgres.py
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < db/views.sql
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < db/indexes.sql
	docker compose run --rm app uv run python scripts/create_readonly_user.py

schema:
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < db/schema.sql

views:
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < db/views.sql

indexes:
	docker exec -i $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < db/indexes.sql

load-data:
	docker compose run --rm app uv run python scripts/load_postgres.py

readonly-user:
	docker compose run --rm app uv run python scripts/create_readonly_user.py

psql:
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

admin-user-test:
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

	\dt
	\dv

	SELECT COUNT(*) FROM orders;
	SELECT COUNT(*) FROM order_items;
	SELECT COUNT(*) FROM marketing_qualified_leads;
	SELECT COUNT(*) FROM closed_deals;

	SELECT * FROM v_order_revenue LIMIT 5;
	SELECT * FROM v_lead_conversion LIMIT 5;

	\q

read-only-user-test:	
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(BI_READONLY_USER) -d $(POSTGRES_DB)

	SELECT COUNT(*) FROM orders;
	DROP TABLE orders;

	\q