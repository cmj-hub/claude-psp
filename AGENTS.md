# AGENTS.md — Behavior rules for claude-psp

## Identity layering

| File | Job | Owner |
|---|---|---|
| `skills/psp/SKILL.md` + `skills/psp/modes/` | JMC FRAMEWORK (5-component PSP), one skill with modes | JMC (do not edit) |
| `SOUL.md` | Operator's perspective on their buyer | You |
| `brand-config.json` | ICP precision + PSP drafts + published `psp` block + signal sources | You (shared with every pack in the suite) |

## Rules

1. **Always load brand-config.json + SOUL.md first.** Missing either → run the `setup` mode (`skills/psp/modes/setup.md`).
2. **Refuse abstract pain.** Force the 11am-Tuesday operational moment. If the operator says "they need better demand gen", push back.
3. **No demographics as signals.** "VP of Marketing at Series B SaaS" is not a signal. Quote what they DID.
4. **No fabricated signals.** If a candidate signal can't be sourced publicly, don't include it.
5. **Pain language must come from the operator's vocabulary list.** Refuse to substitute category jargon.
6. **Time-anchor every PSP.** Without a 90-day trigger (new-exec / budget-cycle / obvious-failure), the PSP isn't operational.
7. **Felt-pain role ≠ buying authority.** Push the operator to name who FEELS the pain at 11am Tuesday.
8. **Stale signals get flagged.** Signals >30 days old should not be in active outreach lists.
9. **Score before you hand off.** Run `scripts/score_psp.py` on every PSP and show the operator each flag. Exit 1 (under 70, a stale signal, or a pain that uses none of the buyer's vocabulary phrases) means it isn't operational yet.
10. **Merge, never overwrite.** `brand-config.json` and `SOUL.md` are shared by every pack in the suite. Read the existing file, add or update only this pack's fields (`psp_drafts`, `psp`, `signal_sources`, `research_cadence`), and leave every other key exactly as it was. Never rewrite the file from the example, never delete another pack's keys. Show the diff and ask before changing a field that already has a value. `operator` and `icp` are shared: fill gaps only. In `SOUL.md`, touch only this pack's own `## ` sections.
11. **Publish the locked primary.** When the operator locks a primary PSP that the scorer passes, write the `psp` block: `signal_anchors` (`psp_drafts.primary.signal` first), `primary_pain`, `timing_trigger`, `felt_pain_role`, `vocabulary`. Downstream packs (evp, prospect-list, cold-email, pricing, geo, email-sequence) read `psp`, not the drafts.

## What the agent NEVER does

- Generates a PSP without brand-config.json + SOUL.md (refuses + routes to onboarding) Scoring a draft the operator pasted is the exception: score it, say which checks the missing config skipped, then offer setup.
- Invents vocabulary the operator hasn't sourced from real buyer writing
- Uses generic LinkedIn-thought-leader voice
- Substitutes the operator's category jargon back into their PSP
- Rewrites `brand-config.json` or `SOUL.md` wholesale, or drops another pack's keys or sections

## Onboarding flow

If both config files are missing on first invocation, run the `setup`
mode, `skills/psp/modes/setup.md` (~15-minute guided setup). Shared
`operator`/`icp` questions are asked once for the suite by `/gtm:setup`.

## Work files

The PSP doc goes to `gtm/psp.md` in the operator's project (create
`gtm/` if missing). `brand-config.json` and `SOUL.md` stay at the root.
