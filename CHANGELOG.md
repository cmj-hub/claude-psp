# Changelog

## [0.4.0] — 2026-10-04

Suite pass. PSP is step 1 of the GTM operator suite.

### Added
- Locking a primary PSP publishes a `psp` block to `brand-config.json` (`signal_anchors`, `primary_pain`, `timing_trigger`, `felt_pain_role`, `vocabulary`) for evp, prospect-list, cold-email and the rest of the suite. `psp-construct` Step 9 and `psp-onboarding` Step 6 write it; `psp-kickoff` routes there when the draft exists but `psp` does not.
- `brand-config.example.json` carries a `psp` block consistent with `psp_drafts.primary`; `tests/test_example_config.py` pins the match.
- "Works with the suite" section in `psp`: what it reads, writes, and hands off to.

### Changed
- `brand-config.json` and `SOUL.md` merge at the field level. The pack reads the existing file, writes only its own keys, fills `operator` and `icp` gaps only, and asks before changing a filled field. The "overwrite" offer in onboarding is gone. AGENTS.md rules 10-11.
- Skill descriptions say when to use each skill and what each is not for. Every SKILL.md carries `models: ""`.
- Scorer calls use `${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py`, pre-approved in `allowed-tools`.
- README install lines use `npx skills add` and `/plugin install psp@gtm-operator-skills`.
- `plugin.json`: author URL, repository, keywords.

## [0.3.1] — 2026-10-04

### Fixed
- The Claude Code plugin now loads the main `psp` skill. It lives in `psp/`, outside the default `skills/` scan, so `/psp` was missing and only the four sub-skills loaded. `plugin.json` now lists `"skills": ["./psp/"]`; CI checks every listed path has a `SKILL.md`.
- `psp` routes on every call: reads `brand-config.json` + `SOUL.md`, sends missing config to `psp-onboarding`, bare `/psp` to `psp-kickoff`. `/psp validate` now runs the scorer instead of naming a step that didn't exist.
- Freshness windows agree with AGENTS.md rule 8: no signal older than 30 days in active outreach (was 45 for product, 60 for leadership in places).
- `psp-kickoff` read a `refreshed_at` field the example config didn't have. Added.

### Added
- `score_psp.py` flags stale signals (>30 days, in days / weeks / months). A stale signal exits 1 whatever the total; JSON output gains `operational`.
- `score_psp.py` accepts `new exec`, `Budget_Cycle` and similar spellings of the three triggers, reads `**Trigger:** …` from the doc `psp-construct` writes, and calls out firmographic signals ("Series B", "50 employees").
- `psp-construct` and `psp-signal-hunt` load config first, honour SOUL.md won't-chase boundaries, cite a URL and date for any pulled example, and label volume as an estimate. `psp-construct` saves and scores its output.
- `tests/test_scoring.py` pins the README numbers (good 100, bad 37) and the rules above. CI now runs `tests/`.

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
