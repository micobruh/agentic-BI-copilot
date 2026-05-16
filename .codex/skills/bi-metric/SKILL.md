---
name: bi-metric
description: Add, revise, or verify governed BI metrics for the copilot. Use when editing data/metadata/metric_glossary.yaml, changing metric SQL formulas, metric caveats, prompt metric rules, or tests involving revenue, GMV, order count, AOV, delivery, reviews, or funnel metrics.
---

# BI Metric

Use this skill to keep metric definitions governed, explicit, and safe across prompts, metadata, and SQL behavior.

## Workflow

1. Inspect `data/metadata/metric_glossary.yaml` before changing metric logic.
2. Check `data/metadata/table_descriptions.yaml` for grain, joins, caveats, and column meanings.
3. Update prompts only if the agent instructions need to know a new general rule.
4. Update tests or evaluation cases when metric behavior changes.
5. For SQL behavior, verify the generated logic respects table grain and avoids fanout.

## Metric Definition Checklist

Each governed metric should state:

- business name and optional abbreviation
- description
- SQL formula or recommended logic
- required tables
- default filters
- default date column when relevant
- grain
- caveats and unsafe alternatives

## Current Core Metric Rules

- Revenue uses delivered orders unless the user asks otherwise.
- Revenue uses `SUM(order_items.price)`, not `payment_value`, unless the user asks for paid amount.
- GMV includes `order_items.price + order_items.freight_value`.
- Order count after joins uses `COUNT(DISTINCT orders.order_id)`.
- AOV must be computed at order grain; do not use `AVG(order_items.price)`.
- Repeat-customer analysis should use `customer_unique_id`.
- Joining multiple one-to-many tables can inflate metrics; pre-aggregate the many side.

## Change Safety

Do not silently redefine an existing metric. If the business meaning changes, update:

- metric glossary
- affected prompt rules
- tests/evaluation examples
- any expected answer wording that mentions the metric

Prefer adding explicit caveats over relying on agent inference.
