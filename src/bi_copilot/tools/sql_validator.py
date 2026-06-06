from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Collection

import sqlglot
from sqlglot import expressions as exp
from sqlglot.errors import ParseError


FORBIDDEN_EXPRESSIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Alter,
    exp.Create,
    exp.Command,
)

Schema = dict[str, Collection[str]]
ALLOWED_SCHEMAS = {"public"}
DEFAULT_FUNCTION_ALLOWLIST = frozenset(
    {
        "avg",
        "coalesce",
        "count",
        "date_trunc",
        "exists",
        "extract",
        "lower",
        "max",
        "min",
        "nullif",
        "round",
        "sum",
        "timestamp_trunc",
        "upper",
    }
)


@dataclass(frozen=True)
class ValidationPolicy:
    allow_joins: bool = True
    allow_ctes: bool = True
    allow_subqueries: bool = True
    allow_set_operations: bool = True
    allowed_functions: frozenset[str] | None = field(
        default_factory=lambda: DEFAULT_FUNCTION_ALLOWLIST
    )
    require_limit_for_row_queries: bool = True
    max_limit: int | None = 1000


@dataclass(frozen=True)
class Source:
    name: str
    columns: set[str] | None


def is_select_star_projection(projection: exp.Expression) -> bool:
    expression = projection.this if isinstance(projection, exp.Alias) else projection
    return isinstance(expression, exp.Star) or (
        isinstance(expression, exp.Column) and isinstance(expression.this, exp.Star)
    )


def nearest_select(expression: exp.Expression) -> exp.Select | None:
    current = expression if isinstance(expression, exp.Select) else expression.parent

    while current is not None:
        if isinstance(current, exp.Select):
            return current
        current = current.parent

    return None


def columns_for_select(select: exp.Select) -> list[exp.Column]:
    return [
        column
        for column in select.find_all(exp.Column)
        if nearest_select(column) is select
    ]


def parent_selects(select: exp.Select) -> list[exp.Select]:
    parents: list[exp.Select] = []
    current = select.parent

    while current is not None:
        if isinstance(current, exp.Select):
            parents.append(current)
        current = current.parent

    return parents


def has_aggregation(select: exp.Select) -> bool:
    aggregate_expressions = (exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max)
    return any(
        nearest_select(expression) is select
        for aggregate_expression in aggregate_expressions
        for expression in select.find_all(aggregate_expression)
    )


def normalize_policy(policy: ValidationPolicy | dict[str, Any] | None) -> ValidationPolicy:
    if policy is None:
        return ValidationPolicy()
    if isinstance(policy, ValidationPolicy):
        return policy

    policy_values = dict(policy)
    allowed_functions = policy_values.get("allowed_functions")
    if allowed_functions is not None:
        policy_values["allowed_functions"] = frozenset(
            function.lower() for function in allowed_functions
        )

    return ValidationPolicy(**policy_values)


def function_name(function: exp.Func) -> str:
    if isinstance(function, exp.Anonymous):
        return function.name.lower()
    return function.sql_name().lower()


def limit_value(query: exp.Expression) -> int | None:
    limit = query.args.get("limit")
    if limit is None:
        return None

    expression = limit.args.get("expression")
    if not isinstance(expression, exp.Literal) or expression.is_string:
        return None

    try:
        return int(expression.this)
    except ValueError:
        return None


def infer_projection_columns(
    select: exp.Select,
    sources: dict[str, Source],
) -> set[str] | None:
    columns: set[str] = set()

    for projection in select.expressions:
        if is_select_star_projection(projection):
            expression = projection.this if isinstance(projection, exp.Alias) else projection

            if isinstance(expression, exp.Column) and expression.table:
                source = sources.get(expression.table)
                if source is None or source.columns is None:
                    return None
                columns.update(source.columns)
                continue

            if any(source.columns is None for source in sources.values()):
                return None

            for source in sources.values():
                columns.update(source.columns or set())
            continue

        output_name = projection.output_name
        if output_name:
            columns.add(output_name)

    return columns


def first_select(query: exp.Expression) -> exp.Select | None:
    if isinstance(query, exp.Select):
        return query
    if isinstance(query, exp.SetOperation):
        return first_select(query.this)
    return None


def infer_query_columns(
    query: exp.Expression,
    schema: Schema,
    cte_outputs: dict[str, set[str] | None],
    errors: list[str],
    risk_flags: list[str],
    referenced_tables: set[str],
) -> set[str] | None:
    select = first_select(query)
    if select is None:
        return None

    sources = collect_select_sources(
        select,
        schema,
        cte_outputs,
        errors,
        risk_flags,
        referenced_tables,
    )
    return infer_projection_columns(select, sources)


def collect_select_sources(
    select: exp.Select,
    schema: Schema,
    cte_outputs: dict[str, set[str] | None],
    errors: list[str],
    risk_flags: list[str],
    referenced_tables: set[str],
) -> dict[str, Source]:
    sources: dict[str, Source] = {}

    def add_source(source_expression: exp.Expression | None) -> None:
        if source_expression is None:
            return

        if isinstance(source_expression, exp.Table):
            table_name = source_expression.name
            referenced_tables.add(table_name)

            if source_expression.catalog:
                errors.append(
                    f"Cross-catalog table reference is not allowed: {source_expression}"
                )
                risk_flags.append("disallowed_schema")
                return

            if source_expression.db and source_expression.db not in ALLOWED_SCHEMAS:
                errors.append(
                    f"Table reference uses disallowed schema: {source_expression}"
                )
                risk_flags.append("disallowed_schema")
                return

            alias = source_expression.alias_or_name
            if table_name in cte_outputs:
                sources[alias] = Source(table_name, cte_outputs[table_name])
                return

            if table_name not in schema:
                errors.append(f"Unknown table or view: {table_name}")
                risk_flags.append("unknown_table")
                return

            sources[alias] = Source(
                table_name,
                set(schema[table_name]),
            )
            return

        if isinstance(source_expression, exp.Subquery):
            alias = source_expression.alias
            if not alias:
                errors.append("Derived tables must use an alias.")
                risk_flags.append("missing_derived_table_alias")
                return

            subquery_select = first_select(source_expression.this)
            if subquery_select is None:
                sources[alias] = Source(alias, None)
                return

            subquery_sources = collect_select_sources(
                subquery_select,
                schema,
                cte_outputs,
                errors,
                risk_flags,
                referenced_tables,
            )
            columns = (
                infer_projection_columns(subquery_select, subquery_sources)
            )
            sources[alias] = Source(alias, columns)

    from_clause = select.args.get("from_")
    if from_clause is not None:
        add_source(from_clause.this)

    for join in select.args.get("joins") or []:
        add_source(join.this)

    return sources


def build_cte_outputs(
    tree: exp.Expression,
    schema: Schema,
    errors: list[str],
    risk_flags: list[str],
    referenced_tables: set[str],
) -> dict[str, set[str] | None]:
    cte_outputs: dict[str, set[str] | None] = {}

    for cte in tree.find_all(exp.CTE):
        if not cte.alias:
            continue

        cte_outputs[cte.alias] = infer_query_columns(
            cte.this,
            schema,
            cte_outputs,
            errors,
            risk_flags,
            referenced_tables,
        )

    return cte_outputs


def parse_single_select(sql: str) -> tuple[exp.Expression | None, list[str], list[str]]:
    errors: list[str] = []
    risk_flags: list[str] = []

    if not sql.strip():
        return None, ["SQL query is empty."], ["empty_sql"]

    try:
        statements = sqlglot.parse(sql, dialect="postgres")
    except ParseError as exc:
        return None, [f"SQL syntax error: {exc}"], ["syntax_error"]

    if len(statements) != 1:
        return None, ["Only one SQL statement is allowed."], ["multiple_statements"]

    tree = statements[0]

    if not isinstance(tree, (exp.Select, exp.SetOperation)):
        errors.append(
            "Only read-only SELECT queries are allowed. "
            f"Parsed statement type: {type(tree).__name__}."
        )
        risk_flags.append("not_select_query")

    for forbidden_expression in FORBIDDEN_EXPRESSIONS:
        if tree.find(forbidden_expression) is not None:
            errors.append(
                f"Forbidden SQL operation detected: {forbidden_expression.__name__}."
            )
            risk_flags.append("forbidden_operation")

    if errors:
        return None, errors, risk_flags

    return tree, [], []


def validate_policy(
    tree: exp.Expression,
    policy: ValidationPolicy,
) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    risk_flags: list[str] = []

    if not policy.allow_set_operations and isinstance(tree, exp.SetOperation):
        errors.append("Set operations are not allowed by the current SQL policy.")
        risk_flags.append("set_operation_not_allowed")

    if not policy.allow_ctes and tree.find(exp.CTE) is not None:
        errors.append("CTEs are not allowed by the current SQL policy.")
        risk_flags.append("cte_not_allowed")

    if not policy.allow_subqueries and tree.find(exp.Subquery) is not None:
        errors.append("Subqueries are not allowed by the current SQL policy.")
        risk_flags.append("subquery_not_allowed")

    if not policy.allow_joins:
        has_join = any(select.args.get("joins") for select in tree.find_all(exp.Select))
        if has_join:
            errors.append("JOINs are not allowed by the current SQL policy.")
            risk_flags.append("join_not_allowed")

    if policy.allowed_functions is not None:
        allowed_functions = {function.lower() for function in policy.allowed_functions}
        for function in tree.find_all(exp.Func):
            name = function_name(function)
            if name not in allowed_functions:
                errors.append(f"SQL function is not allowlisted: {name}")
                risk_flags.append("function_not_allowlisted")

    return errors, warnings, risk_flags


def validate_schema_references(
    tree: exp.Expression,
    schema: Schema,
) -> tuple[list[str], list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    risk_flags: list[str] = []
    referenced_tables: set[str] = set()

    cte_outputs = build_cte_outputs(tree, schema, errors, risk_flags, referenced_tables)
    selects = list(tree.find_all(exp.Select))
    sources_by_select: dict[int, dict[str, Source]] = {}

    for select in selects:
        sources = collect_select_sources(
            select,
            schema,
            cte_outputs,
            errors,
            risk_flags,
            referenced_tables,
        )
        sources_by_select[id(select)] = sources

        for column in columns_for_select(select):
            if isinstance(column.this, exp.Star):
                continue

            column_name = column.name
            table_alias = column.table

            if table_alias:
                source = sources.get(table_alias)
                if source is None:
                    for parent_select in parent_selects(select):
                        parent_sources = sources_by_select.get(id(parent_select), {})
                        source = parent_sources.get(table_alias)
                        if source is not None:
                            break

                if source is None:
                    errors.append(f"Unknown table alias: {table_alias}.{column_name}")
                    risk_flags.append("unknown_alias")
                    continue

                if source.columns is None:
                    warnings.append(
                        f"Could not validate column '{table_alias}.{column_name}' "
                        "because its source output columns could not be inferred."
                    )
                    risk_flags.append("derived_column_unverified")
                    continue

                if column_name not in source.columns:
                    errors.append(
                        f"Unknown column: {table_alias}.{column_name} "
                        f"(resolved to {source.name}.{column_name})"
                    )
                    risk_flags.append("unknown_column")
                continue

            candidate_sources = [
                alias
                for alias, source in sources.items()
                if source.columns and column_name in source.columns
            ]

            if len(candidate_sources) == 0:
                if any(source.columns is None for source in sources.values()):
                    warnings.append(
                        f"Could not validate unqualified column '{column_name}' "
                        "because at least one source output could not be inferred."
                    )
                    risk_flags.append("derived_column_unverified")
                else:
                    errors.append(f"Unknown unqualified column: {column_name}")
                    risk_flags.append("unknown_column")
            elif len(candidate_sources) > 1:
                errors.append(
                    f"Ambiguous unqualified column: {column_name}. "
                    f"Could belong to: {sorted(candidate_sources)}. "
                    f"Use table aliases."
                )
                risk_flags.append("ambiguous_column")
            elif len({source.name for source in sources.values()}) > 1:
                warnings.append(
                    f"Unqualified column '{column_name}' resolved to "
                    f"{candidate_sources[0]}. Consider using table aliases."
                )
                risk_flags.append("unqualified_column")

        for projection in filter(is_select_star_projection, select.expressions):
            warnings.append("SELECT * detected. Prefer explicit columns.")
            risk_flags.append("select_star")

    return errors, warnings, sorted(referenced_tables), risk_flags


def validate_query_shape(
    tree: exp.Expression,
    policy: ValidationPolicy,
) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    risk_flags: list[str] = []

    outer_select = tree if isinstance(tree, exp.Select) else tree.find(exp.Select)
    if outer_select is None:
        return errors, warnings, risk_flags

    limit_owner = tree if isinstance(tree, exp.SetOperation) else outer_select
    has_limit = limit_owner.args.get("limit") is not None
    current_limit_value = limit_value(limit_owner)
    has_group = outer_select.args.get("group") is not None
    is_row_returning_query = not has_group and not has_aggregation(outer_select)

    if policy.require_limit_for_row_queries and is_row_returning_query and not has_limit:
        errors.append("Row-returning query must include an outer LIMIT.")
        risk_flags.append("missing_limit")
    elif not has_limit and is_row_returning_query:
        warnings.append("Query has no LIMIT and may return many rows.")
        risk_flags.append("missing_limit")

    if (
        policy.max_limit is not None
        and current_limit_value is not None
        and current_limit_value > policy.max_limit
    ):
        errors.append(
            f"Query LIMIT {current_limit_value} exceeds maximum allowed "
            f"LIMIT {policy.max_limit}."
        )
        risk_flags.append("limit_too_high")

    return errors, warnings, risk_flags


def validate_sql(
    sql: str,
    schema: Schema | None = None,
    policy: ValidationPolicy | dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = normalize_policy(policy)
    tree, errors, risk_flags = parse_single_select(sql)
    if tree is None:
        return {
            "is_valid": False,
            "errors": errors,
            "warnings": [],
            "risk_flags": risk_flags,
            "referenced_tables": [],
            "safe_sql": None,
        }

    if schema is None:
        from .database import get_database_schema

        schema = get_database_schema()

    schema_errors, schema_warnings, referenced_tables, schema_risk_flags = (
        validate_schema_references(tree, schema)
    )

    policy_errors, policy_warnings, policy_risk_flags = validate_policy(tree, policy)
    shape_errors, shape_warnings, shape_risk_flags = validate_query_shape(tree, policy)

    all_errors = schema_errors + policy_errors + shape_errors
    all_warnings = schema_warnings + policy_warnings + shape_warnings
    all_risk_flags = sorted(
        set(risk_flags + schema_risk_flags + policy_risk_flags + shape_risk_flags)
    )
    is_valid = len(all_errors) == 0

    return {
        "is_valid": is_valid,
        "errors": all_errors,
        "warnings": all_warnings,
        "risk_flags": all_risk_flags,
        "referenced_tables": referenced_tables,
        "parsed_type": type(tree).__name__,
        "safe_sql": tree.sql(dialect="postgres") if is_valid else None,
    }
