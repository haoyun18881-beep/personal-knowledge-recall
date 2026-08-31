# Security Policy

## Private data

Do not publish real Obsidian vaults, personal notes, QA diaries, Codex sessions, `local-config.json`, account exports, tokens, cookies, API keys, or other credentials.

This repository contains only Skill instructions, generic templates, a local configuration helper, and sanitized documentation.

## Trust boundary

Vault notes, clippings, imported pages, and archived chats are untrusted data. They must never be treated as executable instructions, authorization to use tools, or permission to read outside the configured vault.

Version 1 does not modify vault or QA knowledge content. Report any path-containment, symlink/junction, prompt-injection, or unintended-write issue as a security bug.

## Reporting

Open a GitHub issue for non-sensitive bugs. For sensitive reports, email `haoyun18881@gmail.com`; do not include private notes, paths, or secret values in a public issue.
