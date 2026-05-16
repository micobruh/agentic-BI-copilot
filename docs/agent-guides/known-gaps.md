# Known Gaps

Before assuming behavior exists, inspect the relevant file. The repo is actively being built.

Current cautions:

- several files in `src/bi_copilot/graph/nodes/` may be empty or skeletal
- `src/bi_copilot/graph/workflow.py` may still need workflow assembly
- `tests/unit/test_workflow.py` may still need workflow-level coverage
- the implemented test coverage is strongest around SQL validation
- MCP server wrappers exist, but graph integration may still need implementation
- pycache files may exist in the working tree; do not treat them as source
