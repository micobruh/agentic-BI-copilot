from bi_copilot.tools.sql_query_guard import ValidationPolicy, validate_sql


SCHEMA = {
    "orders": {"order_id", "amount", "customer_id"},
    "customers": {"customer_id", "name"},
}


def test_rejects_random_word():
    result = validate_sql("oof")
    assert not result["is_valid"]
    assert "not_select_query" in result["risk_flags"]


def test_rejects_arithmetic_expression():
    result = validate_sql("6 + 7")
    assert not result["is_valid"]
    assert "not_select_query" in result["risk_flags"]


def test_accepts_select_query():
    result = validate_sql("""
        SELECT COUNT(*) 
        FROM orders 
        WHERE amount > 100
    """, schema=SCHEMA)
    assert result["is_valid"]
    assert "select_star" not in result["risk_flags"]


def test_warns_on_select_star_projection():
    result = validate_sql("SELECT orders.* FROM orders LIMIT 10", schema=SCHEMA)
    assert result["is_valid"]
    assert "select_star" in result["risk_flags"]


def test_accepts_with_select_query():
    result = validate_sql("""
        WITH order_counts AS (
            SELECT COUNT(*) AS n_orders
            FROM orders
        )
        SELECT n_orders
        FROM order_counts
        LIMIT 10
    """, schema=SCHEMA)
    assert result["is_valid"]


def test_rejects_disallowed_schema_qualified_table():
    result = validate_sql("SELECT order_id FROM private.orders", schema=SCHEMA)
    assert not result["is_valid"]
    assert "disallowed_schema" in result["risk_flags"]


def test_validates_cte_output_columns():
    result = validate_sql("""
        WITH c AS (
            SELECT order_id
            FROM orders
        )
        SELECT c.bad_column
        FROM c
    """, schema=SCHEMA)
    assert not result["is_valid"]
    assert "unknown_column" in result["risk_flags"]


def test_accepts_derived_table_alias_columns():
    result = validate_sql("""
        SELECT t.order_id
        FROM (
            SELECT order_id
            FROM orders
        ) AS t
        LIMIT 10
    """, schema=SCHEMA)
    assert result["is_valid"]


def test_nested_scope_does_not_make_outer_column_ambiguous():
    result = validate_sql("""
        SELECT order_id
        FROM orders
        WHERE EXISTS (
            SELECT 1
            FROM customers
            WHERE customers.customer_id = orders.customer_id
        )
        LIMIT 10
    """, schema=SCHEMA)
    assert result["is_valid"]
    assert "ambiguous_column" not in result["risk_flags"]


def test_nested_limit_does_not_hide_unbounded_outer_query():
    result = validate_sql("""
        SELECT order_id
        FROM (
            SELECT order_id
            FROM orders
            LIMIT 1
        ) AS t
    """, schema=SCHEMA)
    assert not result["is_valid"]
    assert "missing_limit" in result["risk_flags"]


def test_warns_on_nested_select_star_projection():
    result = validate_sql("""
        SELECT t.order_id
        FROM (
            SELECT *
            FROM orders
        ) AS t
        LIMIT 10
    """, schema=SCHEMA)
    assert result["is_valid"]
    assert "select_star" in result["risk_flags"]


def test_accepts_union_readonly_query():
    result = validate_sql("""
        SELECT order_id
        FROM orders
        UNION
        SELECT customer_id
        FROM customers
        LIMIT 10
    """, schema=SCHEMA)
    assert result["is_valid"]


def test_validates_union_cte_output_columns():
    result = validate_sql("""
        WITH ids AS (
            SELECT order_id AS id
            FROM orders
            UNION
            SELECT customer_id AS id
            FROM customers
        )
        SELECT ids.bad_column
        FROM ids
    """, schema=SCHEMA)
    assert not result["is_valid"]
    assert "unknown_column" in result["risk_flags"]


def test_returns_normalized_safe_sql_for_valid_query():
    result = validate_sql("select order_id from orders limit 10", schema=SCHEMA)
    assert result["is_valid"]
    assert result["safe_sql"] == "SELECT order_id FROM orders LIMIT 10"


def test_does_not_return_safe_sql_for_invalid_query():
    result = validate_sql("SELECT bad_column FROM orders LIMIT 10", schema=SCHEMA)
    assert not result["is_valid"]
    assert result["safe_sql"] is None


def test_rejects_row_returning_query_without_limit_by_default():
    result = validate_sql("SELECT order_id FROM orders", schema=SCHEMA)
    assert not result["is_valid"]
    assert "missing_limit" in result["risk_flags"]


def test_can_warn_instead_of_error_for_missing_limit():
    result = validate_sql(
        "SELECT order_id FROM orders",
        schema=SCHEMA,
        policy=ValidationPolicy(require_limit_for_row_queries=False),
    )
    assert result["is_valid"]
    assert "missing_limit" in result["risk_flags"]


def test_rejects_limit_above_policy_maximum():
    result = validate_sql("SELECT order_id FROM orders LIMIT 1001", schema=SCHEMA)
    assert not result["is_valid"]
    assert "limit_too_high" in result["risk_flags"]


def test_can_block_joins():
    result = validate_sql(
        """
        SELECT o.order_id
        FROM orders AS o
        JOIN customers AS c
            ON o.customer_id = c.customer_id
        LIMIT 10
        """,
        schema=SCHEMA,
        policy=ValidationPolicy(allow_joins=False),
    )
    assert not result["is_valid"]
    assert "join_not_allowed" in result["risk_flags"]


def test_can_block_ctes():
    result = validate_sql(
        """
        WITH c AS (
            SELECT order_id
            FROM orders
        )
        SELECT order_id
        FROM c
        LIMIT 10
        """,
        schema=SCHEMA,
        policy=ValidationPolicy(allow_ctes=False),
    )
    assert not result["is_valid"]
    assert "cte_not_allowed" in result["risk_flags"]


def test_can_block_subqueries():
    result = validate_sql(
        """
        SELECT t.order_id
        FROM (
            SELECT order_id
            FROM orders
        ) AS t
        LIMIT 10
        """,
        schema=SCHEMA,
        policy=ValidationPolicy(allow_subqueries=False),
    )
    assert not result["is_valid"]
    assert "subquery_not_allowed" in result["risk_flags"]


def test_can_block_set_operations():
    result = validate_sql(
        """
        SELECT order_id
        FROM orders
        UNION
        SELECT customer_id
        FROM customers
        LIMIT 10
        """,
        schema=SCHEMA,
        policy=ValidationPolicy(allow_set_operations=False),
    )
    assert not result["is_valid"]
    assert "set_operation_not_allowed" in result["risk_flags"]


def test_rejects_non_allowlisted_function():
    result = validate_sql(
        "SELECT LOWER(name) FROM customers LIMIT 10",
        schema=SCHEMA,
        policy=ValidationPolicy(allowed_functions=frozenset({"count"})),
    )
    assert not result["is_valid"]
    assert "function_not_allowlisted" in result["risk_flags"]
