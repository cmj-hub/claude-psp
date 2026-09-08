<p align="center">
  <img src="./assets/header.svg" alt="claude-psp — Pain Signal Profile for B2B operators" width="100%">
</p>

# claude-psp

> A static ICP describes a costume. A Pain Signal Profile describes Tuesday at 11am.

A Pain Signal Profile is a five-part buying brief: a public signal, the operational pain it implies, why that pain is acute now, who feels it at 11am on Tuesday, and the exact phrases that person uses. It replaces a static ICP.

"Series B SaaS, fifty employees" is a state.
A Demand Gen Lead job post, four days ago, is a signal.

We scored both on the sample in this repo.
The costume got **37**.
The signal got **100**.

The Python that did that ships with the pack. No LLM. No paid API.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-psp?style=social)](https://github.com/cmj-hub/claude-psp)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-psp — terminal demo of scoring a sample PSP" width="100%">
</p>

## Install

Two commands. Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, and the rest of the [skills CLI](https://skills.sh) list.

```bash
npx skills add cmj-hub/claude-psp --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install psp
```

Also: `npm install github:cmj-hub/claude-psp` then `npx jmc-psp`. Or `curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-psp/main/install.sh | bash`.

## What you walk out with in 15 minutes

Artifact: `examples/good.json` vs `examples/bad.json`.

```bash
python3 scripts/score_psp.py --file examples/good.json
python3 scripts/score_psp.py --file examples/bad.json
```

Score the sample. Then write yours.

One loop. One ICP. Example data. That is the whole first run.

## What this pack will not do

It will not hunt LinkedIn for you.
It will not pick this quarter's PSP.
It will not ingest your CRM.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## How is a Pain Signal Profile different from an ICP?

An ICP names who they are.
A PSP names what they just did, what that does to their Tuesday, why it is acute now, who feels it, and the words they actually use.

State is not a signal. A job post four days ago is.

## Do I need live data to start?

No. The Series-B sample is in `examples/`. Score it. Then swap in your book.

## Does this hunt signals for me?

No. After the sample, `signal-hunt` names the *kinds* of public signals worth watching. It does not log in. Closed-loop hunt on your accounts is Operator Pass.

## Suite, course, Operator Pass

- Suite: [gtm-operator-skills](https://github.com/cmj-hub/gtm-operator-skills) · [jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [Pain Signal Profiles](https://jaymountconsulting.com/learn/courses/pain-signal-profiles)
- Operator Pass: [jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- [claude-evp](https://github.com/cmj-hub/claude-evp) — 22-word line per Schwartz tier
- [claude-cold-email](https://github.com/cmj-hub/claude-cold-email) — signal, pain, EVP, binary ask
- [claude-founder-brand](https://github.com/cmj-hub/claude-founder-brand) — Pillar / Proof / Process / Person
- [claude-pricing](https://github.com/cmj-hub/claude-pricing) — three-tier contrast + pocket-price leaks

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
