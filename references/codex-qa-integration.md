# Codex QA integration

Codex QA is optional. The Skill must remain useful when neither QA Skill is installed.

## Detection

Use the host's normal Skill discovery. Do not assume a fixed installation path and do not claim that a QA lookup ran unless the corresponding Skill was actually available and invoked.

## Fallback order

1. Search Obsidian first.
2. If Obsidian is insufficient and `qa_fallback` is `auto`, use `codex-qa-memory` when available.
3. Use `codex-qa-diary-recall` only for exact wording, dates, evidence, Session/Thread IDs, or when memory evidence is insufficient.
4. If a QA Skill is missing, skip it without error and state the checked scope only when it affects the answer.

`qa_fallback: off` disables both QA fallbacks.

## Evidence roles

- Obsidian: reviewed knowledge, project state, and structured experience.
- QA memory: compact historical leads and remembered preferences or decisions.
- QA diary: precise source evidence and original wording.

A QA `candidate` is never a durable fact. Current instructions and current project evidence override every historical layer.

Codex QA repository: <https://github.com/haoyun18881-beep/codex-qa-memory>
