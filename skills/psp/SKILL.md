---
name: psp
description: "Builds and scores a Pain Signal Profile (PSP): a public, recent signal, the operational pain it implies, why it is acute now, who feels it, and the buyer's own words. Publishes the locked primary to brand-config.json for the rest of the suite. Use when the operator asks to build, score or refresh a PSP, map signals to pain, pick which signals to hunt, or check PSP status. Not for the value-proposition line (use evp), not for picking who to contact this week (use prospect-list), not for writing the email (use cold-email)."
argument-hint: "[construct | signal-hunt | validate | status | setup]"
allowed-tools: Read Write Grep WebFetch Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py:*)
license: MIT
models: ""

---

# PSP — Pain Signal Profile Builder

A Pain Signal Profile is the link from a **public signal** (something
the prospect verifiably did) to the **felt operational pain** that
signal implies. It's the foundation underneath cold email, outbound
audits, EVPs, content strategy, and sales conversations in the JMC
framework.

## Start here — every invocation

> **Scoring something pasted needs no setup.** If the operator handed you a line, post, draft, or file to score, run the scorer on it first and report the result; missing config only means some checks are skipped, so say which. Offer setup afterwards as the next step. Check whether files exist with Read or Glob, not a shell command.

1. Read `brand-config.json` and `SOUL.md` from the project root. Both
   are shared by every pack in the suite; this pack owns only
   `psp_drafts`, `psp`, `signal_sources`, `research_cadence`, and its
   own sections of [SOUL.md](../../SOUL.md).
2. Either missing, or `operator`/`icp` empty → run the `setup` mode
   first, whatever was asked (scoring a pasted PSP is the exception above). Do not draft a PSP without both files
   (see `AGENTS.md`).
3. Route by `$ARGUMENTS`. If it names a mode, go straight to it. If it
   is empty, run `status`. Otherwise match the request to a row.
4. Read the mode file with the Read tool and follow it.

| You say / argument | Mode file |
|---|---|
| (nothing), `status`, "where do I start", "PSP status" | [modes/status.md](modes/status.md) |
| `setup`, `onboarding`, "set up", "refresh my config" | [modes/setup.md](modes/setup.md) |
| `construct`, "build a PSP for…" | [modes/construct.md](modes/construct.md) |
| `signal-hunt`, "what signals should we hunt" | [modes/signal-hunt.md](modes/signal-hunt.md) |
| `validate`, "score this PSP" | no file: run the scorer (below) |

Moved in 0.6: the old sub-skills (`psp-kickoff`, `psp-onboarding`,
`psp-construct`, `psp-signal-hunt`) are these modes. Type
`/psp:psp <mode>`.

Files this pack writes in the operator's project: `brand-config.json`
and `SOUL.md` at the root (shared), and the PSP doc at `gtm/psp.md`.
Create `gtm/` if it is missing.

### Validate

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py --file gtm/psp.md   # markdown PSP doc
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py --file brand-config.json --json-path psp_drafts.primary
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py --file brand-config.json --json-path psp   # published block
```

`${CLAUDE_PLUGIN_ROOT}` is the plugin's install folder; the scorer
sits in its `scripts/`. On a host that doesn't expand the variable
(plain-skills install), use `scripts/score_psp.py` from the pack root. The scorer is stdlib Python — no network,
no key. Add `--json` for one JSON object.

Exit 0 means operational: 70+, the signal is ≤30 days old, and the
pain uses one of the buyer's vocabulary phrases. Exit 1 means fix the
flagged axes first: every reason prints as `- what is wrong → what to
change`. Show the operator every line; do not round a 69 up.

The artifact is one pain brief: the pain sentence in the buyer's words,
plus the phrase lifted from them. A passing run prints it under
`## Pain brief` with `Buyer phrase:`. A persona table (title, company,
cares-about, challenge) is refused with `persona has no pain in the
buyer's language`; a high score whose pain uses none of their phrases is
refused with `pain is not in the buyer's language`. Both exit 1.

## The core stance

A PSP is **not** an ICP, persona, or demographic. Those describe who
the buyer **is**. A PSP describes:

1. What the buyer **just did** (signal — public, recent, verifiable)
2. What that signal **implies** about their operational reality (pain)
3. **Why now** the pain is acute (timing)
4. **Who feels the pain most** within the company (role)
5. **What language** they use about it internally (vocabulary)

If you can't fill in all five, you don't have a PSP yet.

## The framework

```
Signal      →  Pain          →  Timing       →  Role          →  Vocabulary
(verifiable    (operational    (why now is    (who feels it    (their words,
 thing they    consequence)    acute)          most)            not yours)
 did)
```

### Component 1: Signal

A signal is something the prospect (or their company) did **publicly,
recently, and verifiably**.

**Good signals:**

- Just posted a job for `<role>` on LinkedIn (≤30 days)
- Just announced funding (Series A/B/C, ≤30 days)
- Just shipped a feature / product / pricing change (≤30 days)
- Just hired / promoted a relevant exec (≤30 days)
- Just changed website positioning or hero (≤14 days)
- Just appeared on a relevant podcast / conference / panel
- Just published a content piece on the topic

**Not signals:**

- "Series B company" (state, not action)
- "VP of Marketing" (role, not action)
- "Growing fast" (vague, not verifiable)

### Component 2: Pain

The pain is what the signal **implies** about the prospect's day-to-day
operational reality. It is *always* phrased as a thing the operator
feels, not a thing you sell.

**Examples (signal → pain mapping):**

| Signal | Implied pain |
|---|---|
| Posted "Senior Demand Gen Lead" role 4 days ago | Pipeline gap; existing motion not producing SQLs |
| Announced Series B last month | Pressure to 3x revenue in 18 months while keeping CAC flat |
| Shipped enterprise tier yesterday | Need new sales motion; legacy SDRs not built for $50k+ ACV |
| New CRO hired 6 weeks ago | Re-evaluating GTM stack in next 90 days |
| Pricing page now shows "Contact us" | Moving up-market; existing inbound funnel may not fit |

### Component 3: Timing — why now is acute

The same pain can exist for years; what makes it actionable now? Most
buyer movement happens in a 90-day window after one of three triggers:

- **A new exec joins** (90-day plan in motion)
- **A budget cycle opens** (Q4 planning, fiscal new year)
- **An obvious failure ships** (missed quarter, churn spike, launch flop)

Name which trigger is in play. If none, the PSP isn't time-anchored
and outreach will fall flat.

### Component 4: Role

Within the company, who feels the pain most acutely? Not who *makes
the decision* — who *feels the pain*. Often these differ.

- The CMO **feels** missed-quarter pain
- The Demand Gen Lead **feels** pipeline-gap pain
- The CRO **feels** CAC-payback pain
- The COO **feels** ops-scaling pain

Outreach lands when it reaches the person who **feels** the pain, even
if the buying decision routes elsewhere.

### Component 5: Vocabulary

What language do they use about this pain in private — Slack, internal
docs, hiring posts, AMA Qs? You need their words, not your category
words.

- Don't say "demand generation challenges" → they say "pipeline gap"
- Don't say "buyer enablement" → they say "deals stalling"
- Don't say "GTM efficiency" → they say "we're burning cash"
- Don't say "ICP fit" → they say "we keep closing wrong-fit logos"

The fastest way to find the vocabulary: read their job posts, their
LinkedIn comments, their team's public AMA responses.


## Finish every run with the next step

When a mode ends well (a PSP scores exit 0, or the `psp` block is
published), say the next step in one line: `Next: /evp:evp` to write
the line for this pain. If evp is not installed:
`/plugin install evp@gtm-operator-skills`. On exit 1, the next step is
the fix lines, then score again.

## Works with the suite

This is step 1 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`).

- **Reads:** `operator` and `icp` from `brand-config.json` if present (`/gtm:setup` fills them once for the suite).
- **Writes:** `psp_drafts`, `signal_sources`, `research_cadence`, and, once the operator locks a primary PSP, the `psp` block (`signal_anchors`, `primary_pain`, `timing_trigger`, `felt_pain_role`, `vocabulary`). Merge at the field level; never overwrite another pack's keys.
- **Before this:** `/gtm:setup` once, when `operator` or `icp` is empty. Otherwise nothing.
- **After this:** evp (`/evp:evp`) to write the line for this pain; prospect-list (`/prospect-list:who-to-contact`) to find who shows the signal this week; pricing (`/pricing:pricing`) when price is the open question.

If a companion pack is not installed, name it and its install line (`/plugin install <name>@gtm-operator-skills`); do not do its job inline.

Go deeper: the JMC Pain Signal Profiles course (methodology) and Cold Email & Outreach Craft course (sequence design).

## Free hosted version

The same job runs in a browser, no install and no key:
[Pain Signal Profile Extractor](https://jaymountconsulting.com/tools/psp-extractor)
