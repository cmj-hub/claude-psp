---
name: psp
description: >
  Pain Signal Profile (PSP) builder for B2B operators. Translates public,
  recent, verifiable signals (job posts, funding rounds, leadership changes,
  product launches, pricing changes, hiring patterns) into the felt
  operational pain that drives buying decisions — and then into the EVP that
  speaks to it. Anchors every output on a signal that the prospect actually
  did, not a demographic guess about who they are. Foundation of the JMC
  framework; loaded by cold-email, outbound-audit, and EVP skills. Triggers
  on: "build a PSP", "pain signal profile", "what's our ICP pain", "what
  signals should we hunt", "signal to pain mapping", "buyer pain", "PSP
  worksheet", "find the signal".
allowed-tools:
  - Read
  - Write
  - Grep
  - WebFetch
---

# PSP — Pain Signal Profile Builder

A Pain Signal Profile is the link from a **public signal** (something
the prospect verifiably did) to the **felt operational pain** that
signal implies. It's the foundation underneath cold email, outbound
audits, EVPs, content strategy, and sales conversations in the JMC
framework.

## Quick reference

| Slash | What it does |
|---|---|
| `/psp` | Interactive — build a PSP from scratch with the operator |
| `/psp construct <ICP>` | Walk through PSP construction for a specific ICP segment |
| `/psp signal-hunt <ICP>` | Surface 5-10 public signals worth hunting for an ICP |
| `/psp validate <PSP>` | Stress-test a draft PSP against the framework |

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
- Just shipped a feature / product / pricing change (≤45 days)
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

## Workflow

### 1. Pick the ICP segment

Ask: "Which segment are we building a PSP for? Be specific —
'B2B SaaS' is too broad. 'Series-B SaaS companies $20-50M ARR with a
PLG motion' is workable."

### 2. Run the signal hunt

For the ICP segment, surface 5-10 public signal candidates. Use the
`psp-signal-hunt` sub-skill if available, or walk through manually
using the patterns above.

### 3. Map signal → pain for the top 3 signals

For each of the top 3 signals, ask: "If this happened, what is the
operator at that company feeling at 11am on Tuesday?"

Don't accept abstract pain ("they need better demand gen"). Force a
specific operational moment.

### 4. Anchor timing

For each pain, identify which 90-day trigger makes it acute right now.

### 5. Identify the felt-pain role

For each pain, who in the org **feels** it? Often it's a layer below
the buying authority.

### 6. Capture vocabulary

Read 5-10 sources of recipient-written content (job posts, LinkedIn
comments, their team's tweets, conference talks). Extract 8-12 phrases
they actually use about this pain.

### 7. Output

Produce a structured PSP doc:

```markdown
# PSP — <ICP segment name>

## Signal
<Top public signal worth hunting>

## Pain
<What that signal implies operationally — in their language>

## Timing
<Which 90-day trigger makes it acute>

## Role (felt-pain holder)
<The person who feels the pain at 11am Tuesday>

## Vocabulary
<8-12 phrases they use about this in private>

## Top 5 signals worth hunting (for the operations team to track)
1. <Signal>
2. <Signal>
...
```

## Sub-skills

- [`skills/psp-construct`](../skills/psp-construct) — full-workflow construction
- [`skills/psp-signal-hunt`](../skills/psp-signal-hunt) — surface signals for an ICP

## Where this skill plugs in downstream

Once you have a PSP, plug it into:

- **[claude-cold-email](https://github.com/cmj-hub/claude-cold-email)** — every cold email anchors on the PSP signal
- **[claude-evp](https://github.com/cmj-hub/claude-evp)** — your EVP must speak to the PSP pain in their vocabulary
- **JMC Cold Email & Outreach Craft course** — full sequence design
- **JMC Pain Signal Profiles course** — the deep methodology

## Free hosted version

The same job runs in a browser, no install and no key:
[Pain Signal Profile Extractor](https://jaymountconsulting.com/tools/psp-extractor)
