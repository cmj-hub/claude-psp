# Construct — build one PSP

Builds one complete PSP for one ICP segment, scores it, and publishes it when locked.

## Contents

- Activation
- Before you start
- Workflow

## Activation

`/psp:psp construct`, or:
- "Build a PSP for..."
- "Construct a Pain Signal Profile for..."
- "Walk me through a PSP for..."

## Before you start

Read `brand-config.json` and `SOUL.md` from the project root. If either
is missing, stop and run the [setup](setup.md) mode instead. From them, carry:

- `icp` and `exclusion_criteria` — the segment is already locked
- `SOUL.md` vocabulary — the only source of pain language
- `SOUL.md` won't-chase boundaries — never surface those signals
- `research_cadence.signal_freshness_window_days` — default 14, never
  more than 30

## Workflow

### Step 1 — Lock the ICP segment

Start from `brand-config.icp.segment`. Ask only if the user names a
different segment. Push back on broad ICPs.

> "B2B SaaS" is too broad. Try one of these shapes:
>
> - "Series-B SaaS, $20-50M ARR, with a PLG motion"
> - "DevTools companies with >50 engineers and an OSS community"
> - "Bootstrapped agencies, 5-15 employees, productized service"
>
> Which segment?

### Step 2 — Hunt signals

For the segment, surface 5-10 candidate signals. Patterns:

- **Hiring signals**: Specific role open ≤30 days
- **Funding signals**: Round announced ≤30 days
- **Product signals**: New tier / launch / pricing change ≤30 days
- **Leadership signals**: New CMO / CRO / CFO / Head-of-X ≤30 days
- **Content signals**: Recent podcast / panel / public talk on the topic
- **Pivot signals**: Website hero / positioning change ≤14 days

If WebFetch is available, pull one public example (a careers page, a
funding announcement) for a company in the segment. Every example
carries its URL and date. If you can't source it, say so — never
invent a company, a post, or a date.

### Step 3 — Map signal → pain for top 3

For each of the top 3 signals, ask: "If this happened, what is the
operator at that company **feeling** at 11am on Tuesday?"

Validate each pain:
- Specific operational moment (not abstract)
- Phrased as what they feel, not what you sell
- Uses their language (not category jargon)

### Step 4 — Anchor timing

For each pain, identify the 90-day trigger:
- New exec → 90-day plan in motion
- Budget cycle → planning/fiscal-new-year window
- Obvious failure → quarter miss, churn spike, launch flop

If no trigger, the PSP isn't time-anchored — push back.

### Step 5 — Identify felt-pain role

Who in the org **feels** the pain at 11am Tuesday?

Note: this is often a layer below the buying authority. The
demand-gen lead feels pipeline-gap pain; the CMO authorizes the spend.
Outreach hits the felt-pain role.

### Step 6 — Mine vocabulary

Read 5-10 sources of recipient-written content:
- Their job posts (often most revealing)
- Their team's LinkedIn comments
- Their conference talks
- Their AMA / podcast appearances
- Their public sales/marketing internal-system tweets

Extract 8-12 phrases they actually use about this pain. Start from
the `SOUL.md` vocabulary list. A new phrase needs a source the
operator can see (quote + link or "operator heard on a call"). If a
phrase reads like category jargon, drop it.

### Step 7 — Output

```markdown
# PSP — <ICP segment>

**ICP precision check:** <one sentence on why this segment is specific enough>

## Signal
<Top signal — verifiable, recent, hunting-ready>

## Pain
<What the signal implies at 11am Tuesday — in their language>

## Timing
**Trigger:** <new-exec / budget-cycle / obvious-failure>
**Why now:** <one sentence>

## Role (felt-pain holder)
<Specific role title; not the buying authority>

## Vocabulary
<8-12 phrases they actually use>
- "<phrase 1>"
- "<phrase 2>"
- ...

## Top 5 signals to hunt operationally
1. <Signal source + cadence>
2. <Signal source + cadence>
3. <Signal source + cadence>
4. <Signal source + cadence>
5. <Signal source + cadence>

## Plugs into
- /cold-email:cold-email — first-line opener uses Signal verbatim
- /evp:evp — EVP must speak to Pain in their Vocabulary
- Outbound program 30-point audit — PSP is the messaging anchor
```

Save it as `gtm/psp.md` in the operator's project (create `gtm/` if it
is missing; ask first if the file exists — rename the old one to keep
it).

### Step 8 — Score and stress test

Score the saved doc:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py --file gtm/psp.md
```

Show the score and every fix line (`- what is wrong → what to change`). Exit 1 (under 70, a signal older
than 30 days, or a pain that uses none of the buyer's vocabulary
phrases) means the PSP is not operational yet — fix the flagged axes
before handing off. The pain sentence has to contain one of their
phrases; a passing run prints the pain brief and the phrase it used.

Then ask: "Which of these are weakest? I can re-pull or refine any
block." Most common weak spots:

- **Pain too abstract**: rewrite using their vocabulary, force the
  11am-Tuesday moment
- **Signal too stale**: shorten the recency window
- **Vocabulary borrowed from category**: pull more sources of their
  actual writing

### Step 9 — Write back to brand-config.json

Once the operator accepts it, offer to save it to
`brand-config.psp_drafts.primary` (or `secondary`) with today's date in
`refreshed_at`. `brand-config.json` is shared by every pack in the
suite, so merge at the field level:

- Read the existing file first. Add or update only `psp_drafts` and
  `psp`; leave every other key exactly as it was. Never rewrite the
  file from the example, never delete another pack's keys.
- If a field already has a value, show the diff and ask before
  changing it.
- `operator` and `icp` are shared: fill gaps only.

When the operator locks this PSP as the primary (exit 0 from the
scorer, and they say yes), also publish the `psp` block that evp,
prospect-list, cold-email and the rest of the suite read:

```json
"psp": {
  "signal_anchors": ["<psp_drafts.primary.signal>", "<other top signals, optional>"],
  "primary_pain": "<psp_drafts.primary.pain>",
  "timing_trigger": "<psp_drafts.primary.timing_trigger>",
  "felt_pain_role": "<psp_drafts.primary.felt_pain_role>",
  "vocabulary": ["<psp_drafts.primary.vocabulary>"]
}
```

`signal_anchors[0]` is always `psp_drafts.primary.signal`. Copy the
values; do not reword them. A `secondary` PSP never touches `psp`.
After writing it, score the published block with `--json-path psp`
(`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py --file brand-config.json --json-path psp`);
it must exit 0 like the draft did.
Then end with the next step, one line: `Next: /evp:evp` (or
`/plugin install evp@gtm-operator-skills` if evp is not installed).
