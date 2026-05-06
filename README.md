# Dataset

It is combined by Brazilian E-Commerce Public Dataset and Marketing Funnel. The provider is Olist. The schema is shown below:

![olist_schema](assets/olist_schema.png)

![marketing_funnel_schema](assets/marketing_funnel_schema.png)

# Run the app

Build the image:

```
docker compose up --build
```

Create the postgresql database:

```
docker compose up -d
uv run python scripts/load_postgres.py
```

Create read-only user:

```
docker exec -i olist_bi_postgres psql -U postgres -d olist_bi < db/create_readonly_user.sql
```