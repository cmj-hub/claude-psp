# Changelog

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
