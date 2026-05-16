# Deletion Candidates

No direct contradictions were found in the original `AGENTS.md`.

The following guidance was omitted or condensed because it was redundant, vague, or already covered by standard coding-agent behavior.

## Redundant

- "Guidance for Codex and other coding agents working on this repository." The root file itself already establishes this.
- "When reading files, prefer `rg`, `rg --files`, and short `sed` ranges." This is useful as agent behavior, but not project-specific.
- "Run `git status --short`" was kept in root, but the longer six-step session checklist was condensed.
- Repeated warnings that project-local skills are not runtime prompts were consolidated in one file.

## Too Vague

- "Follow the existing style." Kept only as concrete conventions in the linked guides.
- "Prefer small, focused functions." Generally good advice, but too broad to justify root placement.
- "Avoid unrelated refactors." Important operationally, but standard for coding agents; the root keeps only the user-change preservation rule.

## Overly Obvious

- "Use type annotations." Standard for this Python codebase and visible in source.
- "Use Pydantic models for structured agent outputs." Kept only where it affects runtime agent contracts.
- "Keep prompts in Markdown files rather than hardcoding long prompt text." Kept only in prompt-specific guidance.

## Time-Sensitive

- Phrases like "currently a stub," "empty," and "as of this guide" were softened in linked docs because those claims can become stale quickly.
