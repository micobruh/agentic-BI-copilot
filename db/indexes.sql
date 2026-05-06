-- db/indexes.sql

CREATE INDEX IF NOT EXISTS idx_orders_customer_id
ON orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_purchase_timestamp
ON orders(order_purchase_timestamp);

CREATE INDEX IF NOT EXISTS idx_orders_status
ON orders(order_status);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id
ON order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product_id
ON order_items(product_id);

CREATE INDEX IF NOT EXISTS idx_order_items_seller_id
ON order_items(seller_id);

CREATE INDEX IF NOT EXISTS idx_order_payments_order_id
ON order_payments(order_id);

CREATE INDEX IF NOT EXISTS idx_order_reviews_order_id
ON order_reviews(order_id);

CREATE INDEX IF NOT EXISTS idx_products_category
ON products(product_category_name);

CREATE INDEX IF NOT EXISTS idx_customers_unique_id
ON customers(customer_unique_id);

CREATE INDEX IF NOT EXISTS idx_customers_state
ON customers(customer_state);

CREATE INDEX IF NOT EXISTS idx_sellers_state
ON sellers(seller_state);

CREATE INDEX IF NOT EXISTS idx_geolocation_zip
ON geolocation(geolocation_zip_code_prefix);

CREATE INDEX IF NOT EXISTS idx_mql_first_contact_date
ON marketing_qualified_leads(first_contact_date);

CREATE INDEX IF NOT EXISTS idx_mql_origin
ON marketing_qualified_leads(origin);

CREATE INDEX IF NOT EXISTS idx_closed_deals_seller_id
ON closed_deals(seller_id);

CREATE INDEX IF NOT EXISTS idx_closed_deals_won_date
ON closed_deals(won_date);

CREATE INDEX IF NOT EXISTS idx_closed_deals_sdr_id
ON closed_deals(sdr_id);

CREATE INDEX IF NOT EXISTS idx_closed_deals_sr_id
ON closed_deals(sr_id);