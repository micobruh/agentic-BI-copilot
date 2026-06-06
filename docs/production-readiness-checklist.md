# Production Readiness Checklist

Checklist of gaps to fill before this Agentic BI Copilot is ready for company production use.

## Runtime Stability

- [ ] Fix the verifier graph node so it imports `VerifierAgent` from the correct module.
- [ ] Fix the SQL executor node so it calls the actual read-only SQL function.
- [ ] Update settings so normal database and application environment variables do not break startup.
- [ ] Make the LangGraph workflow import, compile, and run end to end.
- [ ] Add workflow behavior for validation failure, retry exhaustion, execution failure, verifier failure, unanswerable questions, and clarification requests.
- [ ] Replace placeholder app code that references undefined objects.

## Application Interface

- [ ] Implement a production FastAPI service for asking BI questions.
- [ ] Define request and response schemas for user question, session ID, answer, generated SQL, validation status, caveats, trace ID, and errors.
- [ ] Add health and readiness endpoints.
- [ ] Add conversation/session handling.
- [ ] Add consistent error responses for model, validation, database, and workflow failures.
- [ ] Build or complete the analyst-facing frontend.

## Authentication And Authorization

- [ ] Add user authentication.
- [ ] Add role-based access control for data, SQL visibility, raw result visibility, traces, and administrative actions.
- [ ] Add tenant or workspace scoping if the system will serve multiple teams or companies.
- [ ] Ensure database access stays read-only for the BI agent.
- [ ] Add policy checks before returning sensitive query results or traces.

## Data Governance And Semantic Layer

- [ ] Convert governed metric YAML from prompt context into enforceable runtime behavior.
- [ ] Add deterministic metric validation or a metric compiler for approved formulas.
- [ ] Define allowed dimensions, filters, joins, and grains per metric.
- [ ] Add fanout protection for one-to-many and many-to-many joins.
- [ ] Add tests proving revenue, GMV, order count, AOV, delivery, reviews, and funnel metrics follow governed definitions.
- [ ] Add handling for ambiguous metric names, date ranges, and business definitions.

## Evaluation And Testing

- [ ] Add workflow-level unit tests with mocked LLMs and mocked database/tool calls.
- [ ] Expand evaluation cases beyond `tests/evaluation/basic_questions.json`.
- [ ] Test table selection, metric selection, SQL correctness, answer grounding, refusal behavior, ambiguity handling, and unsafe SQL attempts.
- [ ] Add regression tests for common BI questions and known failure modes.
- [ ] Add LLM evaluation or judge-based scoring for answer quality.
- [ ] Track evaluation results over time, preferably with LangSmith or an equivalent system.

## Observability And Auditability

- [ ] Add structured application logs.
- [ ] Add LangSmith tracing or equivalent workflow tracing.
- [ ] Capture prompt versions, model names, generated SQL, validation outputs, retry counts, and final answers.
- [ ] Track latency, token usage, model cost, database query time, and error rates.
- [ ] Persist audit traces with a trace ID.
- [ ] Redact secrets and sensitive data from logs and traces.

## Security Hardening

- [ ] Add SQL execution timeouts and database statement timeouts.
- [ ] Enforce row limits and result-size caps.
- [ ] Add stricter SQL execution policies for risky functions, schemas, and expensive query shapes.
- [ ] Add secret management for production credentials.
- [ ] Validate environment configuration at startup without exposing secrets.
- [ ] Add dependency scanning and container security checks.
- [ ] Define PII and sensitive-data handling rules.

## MCP Integration

- [ ] Complete MCP servers for glossary, SQL validation, charting, audit, and database tools.
- [ ] Implement the MCP client and registry strategy.
- [ ] Decide which tools the graph should call directly versus through MCP.
- [ ] Add tests proving agent/tool selection uses the intended MCP contracts.
- [ ] Add tool-level authentication, authorization, validation, and audit logging.

## Human-In-The-Loop Behavior

- [ ] Ask clarifying questions when the metric, date range, grain, segment, or business definition is ambiguous.
- [ ] Add approval gates for expensive, broad, or high-risk queries.
- [ ] Add user feedback capture for answer correctness and usefulness.
- [ ] Add a mechanism to revise an answer after verification warnings or user feedback.

## Deployment And Operations

- [ ] Separate API and frontend deployment targets.
- [ ] Remove development bind mounts from production containers.
- [ ] Add container health checks.
- [ ] Add database migration/versioning strategy.
- [ ] Add CI checks for tests, linting, type checking, and security scanning.
- [ ] Add environment-specific configuration for local, staging, and production.
- [ ] Add rollout and rollback procedures.

## Persistence And Memory

- [ ] Replace local SQLite checkpointing with production-grade durable state storage.
- [ ] Persist conversation history with retention and cleanup rules.
- [ ] Add TTL policies for traces, query results, and intermediate state.
- [ ] Define what memory is allowed to influence future answers.

## BI User Experience

- [ ] Show final answer, caveats, and confidence/verification status.
- [ ] Provide optional SQL preview for authorized users.
- [ ] Show result tables with safe row limits.
- [ ] Add chart generation for trend, ranking, and comparison questions.
- [ ] Add downloadable results where permitted.
- [ ] Add a concise "why this answer" trace summary.
- [ ] Add question history and follow-up question support.

## Business Problem Refinement

- [ ] Position the project as a governed BI copilot, not a generic natural-language-to-SQL chatbot.
- [ ] Frame the business value around trusted self-service analytics and reducing ad-hoc analyst backlog.
- [ ] Make metric trust the core differentiator: revenue, GMV, AOV, order count, review score, delivery performance, and funnel conversion should follow approved definitions.
- [ ] Show how the architecture can generalize beyond the Olist dataset to ecommerce, marketplace, sales, marketing, customer success, and operations analytics.
- [ ] Add a clear "company value" statement to the README and project demo.
- [ ] Explain why governance, auditability, and answer verification matter more than raw SQL generation in enterprise BI.
- [ ] Emphasize that the system is designed for business users who need reliable answers without waiting for a data analyst.

## Company-Appealing Features

- [ ] Add a metric governance dashboard that shows approved metric definitions, formulas, caveats, and example SQL.
- [ ] Add an answer trust panel that shows validation result, verifier result, caveats, used tables, used metrics, and trace ID.
- [ ] Add role-aware answer behavior, such as hiding SQL or raw rows from unauthorized users.
- [ ] Add a benchmark or evaluation report that shows pass/fail results across common BI questions.
- [ ] Add LangSmith or equivalent trace screenshots to demonstrate workflow observability.
- [ ] Add clarification flow for ambiguous questions such as "sales last month" or "best customers".
- [ ] Add business templates for common analysis workflows: revenue trend, seller performance, delivery SLA, review score, and lead conversion.
- [ ] Add chart and dashboard generation for trend, ranking, comparison, and funnel questions.
- [ ] Add analyst handoff mode that produces reviewed SQL, assumptions, caveats, and next-step suggestions when the agent is uncertain.
- [ ] Add insight-to-action behavior, such as generating a stakeholder summary or recommended follow-up analysis after a finding.

## RAG Document Set

- [ ] Use `docs/rag_sources/bi_metric_governance_handbook.pdf` for approved metric definitions, default filters, caveats, and clarification rules.
- [ ] Use `docs/rag_sources/ecommerce_operations_sla_policy.pdf` for delivery SLA thresholds, regional escalation rules, and logistics follow-up guidance.
- [ ] Use `docs/rag_sources/seller_performance_playbook.pdf` for seller tiering, seller underperformance rules, and account-manager review recommendations.
- [ ] Use `docs/rag_sources/marketing_funnel_qualification_guide.pdf` for MQL, closed-deal, conversion-rate, lead-origin, SDR, and SR interpretation rules.
- [ ] Use `docs/rag_sources/data_access_and_bi_usage_policy.pdf` for role-aware SQL visibility, raw-row access, exports, and audit requirements.
- [ ] Use `docs/rag_sources/executive_kpi_review_and_incident_playbook.pdf` for monthly business review summaries and incident follow-up recommendations.
- [ ] Keep the matching Markdown files as editable source material for regenerating PDFs.
- [ ] Label these files as synthetic internal demo documents in the README and portfolio materials.

## RAG Implementation Approach

- [ ] Implement RAG as a document evidence path alongside the SQL evidence path, not as a replacement for database querying.
- [ ] Use LangChain for the first implementation because the project already uses LangChain/LangGraph agents and can add retrievers as graph nodes with less architectural churn.
- [ ] Consider LlamaIndex only if the project later becomes document-heavy, needs advanced document indexing, or needs richer document-node abstractions.
- [ ] Use Chroma as the local portfolio vector store because it is simple, persistent, and easy to run without extra infrastructure.
- [ ] Use pgvector as the production-leaning option because the project already depends on PostgreSQL and can keep structured data, embeddings, and metadata in one operational stack.
- [ ] Avoid adding a separate vector service such as Qdrant or Weaviate until scale, multi-tenant retrieval, or advanced filtering justifies the extra infrastructure.
- [ ] Chunk documents by heading-aware sections so each retrieved chunk contains a policy name, section title, and complete rule context.
- [ ] Store metadata for each chunk: document title, document type, business domain, metric names, policy category, source path, and synthetic-document flag.
- [ ] Use metadata filters from the planner when possible, such as `metric_governance`, `delivery_sla`, `seller_performance`, `marketing_funnel`, `data_access`, or `executive_review`.
- [ ] Retrieve a small number of high-signal chunks, then pass only cited context into the reporter and verifier.
- [ ] Require the final answer to separate numeric claims from SQL results and policy claims from retrieved documents.
- [ ] Add verifier checks that policy recommendations are supported by retrieved document chunks and numeric claims are supported by query results.

## RAG Use Cases

- [ ] SLA-aware analytics: answer which customer states or sellers breached delivery thresholds using SQL metrics plus the operations SLA policy.
- [ ] Seller performance review: identify sellers for account-manager review using seller revenue, delivery, and review metrics plus the seller playbook.
- [ ] Marketing funnel diagnosis: compare lead origins against conversion benchmarks using funnel SQL metrics plus the qualification guide.
- [ ] Governed metric explanation: explain why revenue excludes freight and when GMV or paid amount should be used instead.
- [ ] Executive KPI summary: generate a business review using calculated KPIs plus the executive review template.
- [ ] Role-aware response behavior: hide SQL or raw rows according to the data access policy.
- [ ] Incident follow-up: recommend next analysis when revenue, delivery, review, or funnel metrics cross playbook thresholds.

## Portfolio And CV Positioning

- [ ] Describe the project as a production-minded governed analytics agent.
- [ ] Highlight the full agentic workflow: planner, metadata retrieval, SQL generator, SQL validator, SQL executor, reporter, verifier, and audit trace.
- [ ] Show a short demo path where a business question becomes validated SQL, executed results, a verified answer, and a trace.
- [ ] Include screenshots or a GIF for the app, SQL validation output, final answer, and observability trace.
- [ ] Include a small architecture diagram showing data, semantic metadata, graph nodes, tools, and user-facing API/frontend.
- [ ] Add a "What this demonstrates" section covering LangGraph, LangChain, SQL safety, semantic governance, evaluation, observability, and production thinking.
- [ ] Add a "Known limitations and next steps" section to show engineering judgment.

## Implementation Guidelines

- [ ] Start with one reliable end-to-end use case before expanding features. Recommended first case: "What was total revenue in 2018?"
- [ ] Keep public interfaces simple: one `POST /ask` endpoint, one workflow entrypoint, and one response object with answer, SQL, validation, verification, caveats, and trace ID.
- [ ] Treat the metric glossary as a semantic contract, not just prompt text. Add deterministic checks that generated SQL follows required tables, formulas, default filters, and caveats.
- [ ] Add mocked workflow tests before relying on real LLM calls. Mock planner, SQL generation, database execution, reporter, and verifier outputs.
- [ ] Build the evaluation harness as a normal test command so it can run in CI without manual notebooks.
- [ ] Keep SQL validation deterministic and separate from LLM judgment. The LLM verifier can add semantic critique, but it should not replace hard safety checks.
- [ ] Add observability early by attaching one trace ID to the whole request and propagating it through graph state, logs, API responses, and audit entries.
- [ ] Implement clarification as a first-class route in the workflow instead of forcing the SQL generator to guess.
- [ ] Design access control around business roles and result sensitivity before adding broad data access features.
- [ ] Keep charts downstream of validated query results. Do not let chart generation execute new SQL independently.
- [ ] For portfolio polish, prefer a small number of polished, reliable business scenarios over many partially working features.

## Suggested Build Order

- [ ] Phase 1: Fix graph import/runtime issues and make one end-to-end BI question work.
- [ ] Phase 2: Add FastAPI `/ask`, response schemas, and a simple frontend or demo script.
- [ ] Phase 3: Add deterministic metric governance checks for the core metrics.
- [ ] Phase 4: Add mocked workflow tests and evaluation cases for common BI questions.
- [ ] Phase 5: Add answer trust panel, SQL preview, caveats, and audit trace display.
- [ ] Phase 6: Add LangSmith tracing, latency/token/cost tracking, and evaluation reporting.
- [ ] Phase 7: Add role-aware behavior, clarification flow, analyst handoff, and chart generation.
