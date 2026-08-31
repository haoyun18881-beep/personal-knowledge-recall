# Codex QA integration

Codex QA diary evidence is optional. The Skill must remain useful when the diary Skill is not installed.

## Detection

Use the host's normal Skill discovery. Do not assume a fixed installation path and do not claim that a QA lookup ran unless the corresponding Skill was actually available and invoked.

## Fallback order

1. Search Obsidian first.
2. If Obsidian is insufficient and `qa_fallback` is `auto`, use `codex-qa-diary-recall` for the narrowest indexed diary or manifest evidence.
3. Read raw Session evidence only for exact wording, dates, evidence, Session/Thread IDs, or when indexed diary evidence is insufficient.
4. If the diary Skill is missing, skip it without error and state the checked scope only when it affects the answer.

`qa_fallback: off` disables the QA diary and raw Session fallback.

## Evidence roles

- Obsidian: reviewed knowledge, project state, and structured experience.
- QA diary and manifest: indexed historical leads and precise source locations.
- Raw Session: last-resort source evidence and original wording.

Retired QA memory nodes are frozen audit artifacts, not an ordinary recall layer. Current instructions and current project evidence override every historical layer.

The Skill does not require or reactivate a QA memory candidate system.

Codex QA repository: <https://github.com/haoyun18881-beep/codex-qa-memory>
