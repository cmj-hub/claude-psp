# Changelog

## [0.3.0] — 2026-09-08

Public magnet pass. Instrument stays public. First loop is 15 minutes.

### Added
- Definition-first README (GEO paragraph, 15-minute artifact, FAQ H2s, current Pass price).
- Cross-agent installer: `npx skills add cmj-hub/claude-psp --all -g --full-depth` (Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, and the rest of the skills CLI list). Fallback copies into well-known `*/skills` dirs.
- `package.json` (`jmc-psp`) so `npm install github:cmj-hub/claude-psp` and `npx jmc-psp` work. Not published to npmjs.com.
- `examples/` golden good/bad pair for the first loop.

### Changed
- Removed pricing copy from the public pack; CTAs point at the free hosted tools.
- `plugin.json` description is the definition, homepage is /skills.

## [0.2.1] — 2026-05-24

Marketplace-submission compliance pass. No functional changes.

### Fixed
- `plugin.json` `author` field now an object `{ "name": "..." }` per Claude Code plugin manifest schema. `claude plugin validate` now passes.

## [0.2.0] — 2026-05-23

Polish pass matching claude-cold-email v0.2.

### Added
- 3-tier config: `brand-config.example.json` + `SOUL.md` + `AGENTS.md`
- 2 new sub-skills: `psp-onboarding` (15-min setup) + `psp-kickoff` (state-aware router)
- Deterministic script: `scripts/score_psp.py` — scores any PSP 0-100 across 5 axes; catches abstract jargon, demographic-as-signal, missing recency, C-level-vs-felt-pain
- README rewrite with cost-replacement positioning + mermaid diagram

### Verified
- score_psp.py: strong PSP → 100/100; abstract PSP → 32/100 with per-axis flags

## [0.1.0] — 2026-05-23

Initial release.
