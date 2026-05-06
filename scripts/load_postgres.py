from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/olist_bi",
)

RAW_DATA_DIR = Path("data/raw")


CSV_TABLE_MAP = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "product_category_translation",
    "olist_marketing_qualified_leads_dataset.csv": "marketing_qualified_leads",
    "olist_closed_deals_dataset.csv": "closed_deals",
}


def load_csv_to_postgres(engine, csv_path: Path, table_name: str) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing file: {csv_path}")

    print(f"Loading {csv_path} -> {table_name}")

    df = pd.read_csv(csv_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=10_000,
        method="multi",
    )

    print(f"Loaded {len(df):,} rows into {table_name}")


def main() -> None:
    engine = create_engine(DATABASE_URL)

    for relative_path, table_name in CSV_TABLE_MAP.items():
        csv_path = RAW_DATA_DIR / relative_path
        load_csv_to_postgres(engine, csv_path, table_name)

    print("All CSV files loaded successfully.")


if __name__ == "__main__":
    main()