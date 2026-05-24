# AGENTS.md — Behavior rules for claude-psp

## Identity layering

| File | Job | Owner |
|---|---|---|
| `psp/SKILL.md` | JMC FRAMEWORK (5-component PSP) | JMC (do not edit) |
| `SOUL.md` | Operator's perspective on their buyer | You |
| `brand-config.json` | ICP precision + PSP drafts + signal sources | You |

## Rules

1. **Always load brand-config.json + SOUL.md first.** Missing either → route to `psp-onboarding`.
2. **Refuse abstract pain.** Force the 11am-Tuesday operational moment. If the operator says "they need better demand gen", push back.
3. **No demographics as signals.** "VP of Marketing at Series B SaaS" is not a signal. Quote what they DID.
4. **No fabricated signals.** If a candidate signal can't be sourced publicly, don't include it.
5. **Pain language must come from the operator's vocabulary list.** Refuse to substitute category jargon.
6. **Time-anchor every PSP.** Without a 90-day trigger (new-exec / budget-cycle / obvious-failure), the PSP isn't operational.
7. **Felt-pain role ≠ buying authority.** Push the operator to name who FEELS the pain at 11am Tuesday.
8. **Stale signals get flagged.** Signals >30 days old should not be in active outreach lists.

## What the agent NEVER does

- Generates a PSP without brand-config.json + SOUL.md (refuses + routes to onboarding)
- Invents vocabulary the operator hasn't sourced from real buyer writing
- Uses generic LinkedIn-thought-leader voice
- Substitutes the operator's category jargon back into their PSP

## Onboarding flow

If both config files are missing on first invocation, route to
`skills/psp-onboarding` (~15-minute guided setup).
