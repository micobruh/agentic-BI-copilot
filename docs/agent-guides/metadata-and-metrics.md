# Metadata And Metrics

Semantic metadata lives in YAML files under `data/metadata/`.

Use:

- `load_table_descriptions()` for table semantics, grains, joins, and caveats
- `load_metric_glossary()` for governed metric definitions

Important governed metric behavior:

- revenue should use delivered orders unless the user asks otherwise
- revenue should come from `order_items.price`, not `payment_value`, unless the user asks for paid amount
- order counts after joins should use `COUNT(DISTINCT orders.order_id)`
- average order value should be computed at order grain, not with `AVG(order_items.price)`
- joins across one-to-many tables can inflate metrics; pre-aggregate when needed
