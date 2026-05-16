CREATE OR REPLACE VIEW v_order_revenue AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    DATE_TRUNC('month', o.order_purchase_timestamp)::date AS purchase_month,
    SUM(oi.price) AS product_revenue,
    SUM(oi.freight_value) AS freight_value,
    SUM(oi.price + oi.freight_value) AS gmv,
    COUNT(*) AS item_count
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp;

CREATE OR REPLACE VIEW v_order_delivery AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    CASE
        WHEN o.order_status = 'delivered'
         AND o.order_delivered_customer_date IS NOT NULL
        THEN EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400.0
        ELSE NULL
    END AS delivery_days,
    CASE
        WHEN o.order_status = 'delivered'
         AND o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1
        WHEN o.order_status = 'delivered'
         AND o.order_delivered_customer_date IS NOT NULL
        THEN 0
        ELSE NULL
    END AS is_late_delivery
FROM orders o;

CREATE OR REPLACE VIEW v_product_category_sales AS
SELECT
    COALESCE(pct.product_category_name_english, p.product_category_name) AS product_category,
    DATE_TRUNC('month', o.order_purchase_timestamp)::date AS purchase_month,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(oi.price) AS product_revenue,
    SUM(oi.freight_value) AS freight_value,
    SUM(oi.price + oi.freight_value) AS gmv
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation pct
    ON p.product_category_name = pct.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY
    COALESCE(pct.product_category_name_english, p.product_category_name),
    DATE_TRUNC('month', o.order_purchase_timestamp)::date;

CREATE OR REPLACE VIEW v_product_category_sales AS
SELECT
    COALESCE(pct.product_category_name_english, p.product_category_name) AS product_category,
    DATE_TRUNC('month', o.order_purchase_timestamp)::date AS purchase_month,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(oi.price) AS product_revenue,
    SUM(oi.freight_value) AS freight_value,
    SUM(oi.price + oi.freight_value) AS gmv
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation pct
    ON p.product_category_name = pct.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY
    COALESCE(pct.product_category_name_english, p.product_category_name),
    DATE_TRUNC('month', o.order_purchase_timestamp)::date;

CREATE OR REPLACE VIEW v_seller_performance AS
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(oi.price) AS product_revenue,
    SUM(oi.freight_value) AS freight_value,
    SUM(oi.price + oi.freight_value) AS gmv,
    AVG(r.review_score) AS average_review_score
FROM sellers s
JOIN order_items oi
    ON s.seller_id = oi.seller_id
JOIN orders o
    ON oi.order_id = o.order_id
LEFT JOIN order_reviews r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state;

CREATE OR REPLACE VIEW v_lead_conversion AS
SELECT
    mql.mql_id,
    mql.first_contact_date,
    DATE_TRUNC('month', mql.first_contact_date)::date AS first_contact_month,
    mql.origin,
    mql.landing_page_id,
    cd.seller_id,
    cd.sdr_id,
    cd.sr_id,
    cd.won_date,
    cd.business_segment,
    cd.lead_type,
    cd.business_type,
    cd.declared_monthly_revenue,
    CASE
        WHEN cd.mql_id IS NOT NULL THEN 1
        ELSE 0
    END AS is_closed,
    CASE
        WHEN cd.won_date IS NOT NULL
        THEN EXTRACT(EPOCH FROM (cd.won_date - mql.first_contact_date::timestamp)) / 86400.0
        ELSE NULL
    END AS time_to_close_days
FROM marketing_qualified_leads mql
LEFT JOIN closed_deals cd
    ON mql.mql_id = cd.mql_id;

CREATE OR REPLACE VIEW v_lead_to_seller_performance AS
SELECT
    lc.mql_id,
    lc.first_contact_date,
    lc.first_contact_month,
    lc.origin,
    lc.landing_page_id,
    lc.seller_id,
    lc.sdr_id,
    lc.sr_id,
    lc.won_date,
    lc.business_segment,
    lc.lead_type,
    lc.business_type,
    lc.declared_monthly_revenue,
    lc.is_closed,
    lc.time_to_close_days,
    sp.order_count,
    sp.product_revenue,
    sp.freight_value,
    sp.gmv,
    sp.average_review_score
FROM v_lead_conversion lc
LEFT JOIN v_seller_performance sp
    ON lc.seller_id = sp.seller_id;                