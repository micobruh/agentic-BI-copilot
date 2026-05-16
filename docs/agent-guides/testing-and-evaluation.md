# Testing And Evaluation

Common commands:

```bash
PYTHONPATH=src pytest tests/unit/test_sql_validator.py
PYTHONPATH=src pytest
```

The plain `pytest` command may fail to import `bi_copilot` unless the package is installed or `PYTHONPATH=src` is set.

Use focused tests for narrow behavior changes. Broaden coverage when changes touch shared workflow behavior, state contracts, SQL validation, or final answer grounding.

Evaluation data and regression cases live under:

- `tests/evaluation/`
- `tests/unit/`
