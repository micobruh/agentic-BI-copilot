-- db/schema.sql

DROP TABLE IF EXISTS order_payments CASCADE;
DROP TABLE IF EXISTS order_reviews CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS sellers CASCADE;
DROP TABLE IF EXISTS geolocation CASCADE;
DROP TABLE IF EXISTS product_category_translation CASCADE;
DROP TABLE IF EXISTS marketing_qualified_leads CASCADE;
DROP TABLE IF EXISTS closed_deals CASCADE;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix INTEGER,
    customer_city TEXT,
    customer_state TEXT
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT REFERENCES customers(customer_id),
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE order_items (
    order_id TEXT REFERENCES orders(order_id),
    order_item_id INTEGER,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TIMESTAMP,
    price NUMERIC(12, 2),
    freight_value NUMERIC(12, 2),
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE order_payments (
    order_id TEXT REFERENCES orders(order_id),
    payment_sequential INTEGER,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value NUMERIC(12, 2),
    PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE order_reviews (
    review_id TEXT,
    order_id TEXT REFERENCES orders(order_id),
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_category_name TEXT,
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm INTEGER,
    product_height_cm INTEGER,
    product_width_cm INTEGER
);

CREATE TABLE sellers (
    seller_id TEXT PRIMARY KEY,
    seller_zip_code_prefix INTEGER,
    seller_city TEXT,
    seller_state TEXT
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INTEGER,
    geolocation_lat NUMERIC,
    geolocation_lng NUMERIC,
    geolocation_city TEXT,
    geolocation_state TEXT
);

CREATE TABLE product_category_translation (
    product_category_name TEXT PRIMARY KEY,
    product_category_name_english TEXT
);

CREATE TABLE marketing_qualified_leads (
    mql_id TEXT PRIMARY KEY,
    first_contact_date DATE,
    landing_page_id TEXT,
    origin TEXT
);

CREATE TABLE closed_deals (
    mql_id TEXT PRIMARY KEY,
    seller_id TEXT,
    sdr_id TEXT,
    sr_id TEXT,
    won_date TIMESTAMP,
    business_segment TEXT,
    lead_type TEXT,
    lead_behaviour_profile TEXT,
    has_company BOOLEAN,
    has_gtin BOOLEAN,
    average_stock TEXT,
    business_type TEXT,
    declared_product_catalog_size NUMERIC,
    declared_monthly_revenue NUMERIC
);