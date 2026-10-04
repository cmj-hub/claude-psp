# Setup — first-run PSP config

Walks the operator through ~15 minutes of setup that makes every
downstream PSP 10x more useful than generic framework prose.

## Contents

- Activation
- Why this exists
- Workflow
- References

## Activation

Runs first whenever `brand-config.json` or `SOUL.md` is missing from
the project root, or `operator`/`icp` is empty.

Also reached through `/psp:psp setup` (`onboarding` works too), or by
asking: "Set up PSP brand config", "PSP onboarding", "Configure PSP".

## Why this exists

A generic PSP that says "Series-B SaaS feels pipeline pressure" is
worse than no PSP — it produces outreach that everyone else is also
producing. The 5-component PSP framework only generates real
differentiation when paired with:

- **Your ICP precision** (segment, exclusion, motion)
- **Your buyer's actual vocabulary** (sourced from real writing, not
  invented)
- **Your stories** (signal-to-pain mappings you've seen succeed or
  fail before)
- **Your won't-chase boundaries**

## Workflow

### Step 0 — Detect prior state

Check for existing `brand-config.json` + `SOUL.md`. Other packs in the
suite may have written them already. Read both, show what is filled,
and ask only for the gaps. If both already hold this pack's fields, ask:
"Refresh, or skip?"

### Step 1 — Shared basics (once for the whole suite)

`operator` (name, company, title, calendar_url) and `icp` (segment,
role_targets, exclusion_criteria; stage, size_range, geos optional) are
shared by every pack. If they are filled, skip this step.

If they are missing, say: "Run `/gtm:setup` once for the whole suite."
If the gtm plugin is not installed (`/plugin install
gtm@gtm-operator-skills`), ask only those shared questions inline, in
one short batch, and fill gaps only. Push back on a broad segment:

```
"B2B SaaS" is too broad. Give me stage / size / motion / region,
e.g. "Series-B SaaS, $20-50M ARR, PLG motion, US/EU".
```

Then ask the one PSP-specific ICP question, if `icp.motion` is empty:
"PLG, sales-led, or hybrid?" Save it to `brand-config.icp.motion`.

If the ICP is fuzzy, that's a finding — outreach against a fuzzy ICP
will be fuzzy. Use placeholders for now and flag them for refresh after
100 sends.

### Step 2 — Primary PSP draft

```
Now your primary PSP. Five components:

1. SIGNAL — what's a public, recent, verifiable thing your buyer does
   that implies the pain? (job post, funding round, leadership change,
   product launch, pricing change)
2. PAIN — what's the felt operational reality at 11am Tuesday when
   that signal is present? In their language, not yours.
3. TIMING TRIGGER — which 90-day window makes the pain acute now:
   new-exec / budget-cycle / obvious-failure?
4. FELT-PAIN ROLE — who at the buyer feels it most? (Often a layer
   below the buying authority.)
5. VOCABULARY — 4-8 phrases the buyer uses in private about this. If
   you don't know yet, that's step 3.
```

Save to `brand-config.psp_drafts.primary`, with today's date
(`YYYY-MM-DD`) in `refreshed_at`.

### Step 3 — Vocabulary mining

```
If you don't have 4-8 buyer phrases yet, let's mine them.

Point me at any of these sources for the buyer segment:
- 3-5 of their public LinkedIn posts
- 1-2 podcast appearances
- 2-3 of their hiring job posts (job posts reveal pain language verbatim)
- 1-2 conference talks / panel appearances
- Their public AMA responses

I'll extract candidate phrases — you confirm which ones land.
```

Only phrases the operator confirms go in the list. Never fill the list
with phrases you made up; three real phrases beat eight invented ones.

If WebFetch is available, the skill can pull + extract directly. If
not, instruct the operator to paste content and run extraction.

### Step 4 — Signal sources (operations)

```
Where will you hunt these signals? (Mark all that apply.)

1. LinkedIn job search (daily — manual)
2. Crunchbase / news pages (weekly)
3. RSS feeds for specific publications
4. Podcast feeds for relevant shows
5. Manual research only

How often refresh:
- PSP refresh cadence (default: 90 days)
- Vocabulary refresh (default: 30 days)
- Signal freshness window (default: 14 days — older signals drop)
```

Save to `brand-config.signal_sources` + `brand-config.research_cadence`.

### Step 5 — Stories (SOUL.md)

```
Tell me 3-5 stories that anchor your PSP — times you saw a signal-to-pain
mapping work or fail.

Each story: 1-2 sentences, anonymized but specific. These become
calibration points for the construct mode.

Also:
- Your won't-chase boundaries (topics / segments you refuse)
- The 11am-Tuesday operational moment of your buyer (paint it specific)
```

Save to `SOUL.md`. `## Who I am` and the shared voice sections come
from `/gtm:setup`; do not ask for them again if they are filled.

### Step 6 — Write the files

Both files live at the operator's project root and are shared by
every pack in the suite. Merge at the field level:

- Read the existing file first. Add or update only the fields this
  pack owns (`psp_drafts`, `psp`, `signal_sources`,
  `research_cadence`); leave every other key exactly as it was. Never
  rewrite the file from `brand-config.example.json` (it is the shape,
  not a template to copy), never delete another pack's keys.
- Show the diff and ask before changing a field that already has a
  value.
- `operator` and `icp` are shared: fill gaps only.
- `SOUL.md`: append or update only this pack's own `## ` sections (the
  ones in the pack's [SOUL.md](../../../SOUL.md) template); never rewrite
  another pack's section.

Then score the primary draft:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py --file brand-config.json --json-path psp_drafts.primary
```

If it exits 0 and the operator locks it as the primary, publish the
`psp` block the rest of the suite reads, with the values copied from
`psp_drafts.primary` (do not reword them):

```json
"psp": {
  "signal_anchors": ["<psp_drafts.primary.signal>"],
  "primary_pain": "<psp_drafts.primary.pain>",
  "timing_trigger": "<psp_drafts.primary.timing_trigger>",
  "felt_pain_role": "<psp_drafts.primary.felt_pain_role>",
  "vocabulary": ["<psp_drafts.primary.vocabulary>"]
}
```

If it exits 1, leave `psp` unwritten (or as it was) and run the
[construct](construct.md) mode to fix the flagged lines first.

Show preview:

```
✓ brand-config.json — ICP + 1 PSP draft + signal sources + cadence
✓ SOUL.md — 3 stories + vocabulary + 11am-Tuesday moment

Try a quick test:
> Construct a PSP for <segment>

The output will now use:
- Your ICP precision (not generic "B2B SaaS")
- Your vocabulary (not category jargon)
- Your stories as calibration

Next: /evp:evp — lock the line that speaks to this PSP
(`/plugin install evp@gtm-operator-skills` if it is not installed).
Then `/cold-email:cold-email` to ship outreach.
```

### Step 7 — Refresh cadence

```
PSPs decay. Re-run onboarding when:
- ICP shifts (new segment / segment cull)
- Buyer vocabulary evolves
- Quarterly minimum (90 days)

Re-run: `/psp:psp setup`
```

## References

- `brand-config.example.json` (pack root) — the shape of the shared file
- [SOUL.md](../../../SOUL.md) — voice template
- `AGENTS.md` (pack root) — behavior rules
- Other modes:
  - [status.md](status.md) — adaptive router that uses these files
  - [construct.md](construct.md) — uses brand + SOUL for actual PSP build
  - [signal-hunt.md](signal-hunt.md) — runs against your signal sources
