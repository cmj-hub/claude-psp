<p align="center">
  <img src="./assets/header.svg" alt="claude-psp — Pain Signal Profile for B2B operators" width="100%">
</p>

# claude-psp

> Replace a static ICP with a five-part buying brief an agent can score — no live data required to start.

A Pain Signal Profile is a five-part buying brief: a public signal, the operational pain it implies, why that pain is acute now, who feels it at 11am on Tuesday, and the exact phrases that person uses. It replaces a static ICP.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-psp?style=social)](https://github.com/cmj-hub/claude-psp)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-psp — terminal demo of scoring a sample PSP" width="100%">
</p>

Verified: `examples/good.json` → **100/100**. `examples/bad.json` (demographic-as-signal) → **37/100** with per-axis flags. Deterministic Python. No LLM. No paid API.

## Install

Two commands. Works in Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, Continue, Roo, and the rest of the [skills CLI](https://skills.sh) agent list.

```bash
npx skills add cmj-hub/claude-psp --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/claude-psp
/plugin install psp
```

The first line is the cross-harness install. The second is Claude Code's plugin (slash commands + reviewer agents).

npm (from GitHub — this pack is not on npmjs.com):

```bash
npm install github:cmj-hub/claude-psp
npx jmc-psp
```

`npx jmc-psp` runs the same installer as `curl` below.

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-psp/main/install.sh | bash
```

Windows: `iwr https://raw.githubusercontent.com/cmj-hub/claude-psp/main/install.ps1 -useb | iex`

## What you walk out with in 15 minutes

Artifact: `examples/good.json` vs `examples/bad.json`. Score the sample 100 vs 37, then write yours.

```bash
python3 scripts/score_psp.py --file examples/good.json
python3 scripts/score_psp.py --file examples/bad.json; echo "bad should exit non-zero" 
```

One loop. One ICP. Example data. Then do yours.

## What this pack will not do

- It will not hunt live signals on LinkedIn or Crunchbase.
- It will not pick this quarter's PSP for you.
- It will not build a multi-ICP portfolio.
- It will not refresh vocabulary from your CRM.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## Also in the pack

| Piece | Job |
|---|---|
| `psp` orchestrator | Construct / validate / route |
| `scripts/score_psp.py` | 5-axis score: signal, pain, timing, role, vocabulary |
| `psp-construct` | Walk the five components |
| `psp-signal-hunt` | After the sample — lists public signal *types*, does not scrape |

Sub-skills stay in the repo. First run is the loop above, not the operating system.

## How is a Pain Signal Profile different from an ICP?

An ICP describes who the buyer is (Series B, VP Marketing, 50 employees). A PSP describes what they just did, what that implies operationally, why it is acute now, who feels it, and the words they use. State is not a signal. A job post four days ago is.

## Do I need live data to start?

No. The pack ships a Series-B 14-SQL sample. Score it, then swap in your book. Live hunt is not the first loop.

## Does this hunt signals for me?

No. `signal-hunt` names the *kinds* of public signals worth watching. It does not log into LinkedIn or pull Crunchbase. Closed-loop hunt on your accounts is Operator Pass.

## Suite, course, Operator Pass

- Suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [Pain Signal Profiles](https://jaymountconsulting.com/learn/courses/pain-signal-profiles)
- Operator Pass: [https://jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- **[Early Value Proposition](https://github.com/cmj-hub/claude-evp)** — `claude-evp`
- **[Signal-anchored cold email](https://github.com/cmj-hub/claude-cold-email)** — `claude-cold-email`
- **[Four-pillar founder brand](https://github.com/cmj-hub/claude-founder-brand)** — `claude-founder-brand`
- **[Pricing surgery](https://github.com/cmj-hub/claude-pricing)** — `claude-pricing`
- **[Breakthrough Advertising (Schwartz)](https://github.com/cmj-hub/claude-breakthrough-advertising)** — `claude-breakthrough-advertising`
- **[Johanson / Stanley tutorial email](https://github.com/cmj-hub/claude-johanson-stanley)** — `claude-johanson-stanley`

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com). Public build: [https://jaymountconsulting.com/build](https://jaymountconsulting.com/build). Skill suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills).
