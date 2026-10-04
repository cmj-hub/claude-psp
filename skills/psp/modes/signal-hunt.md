# Signal hunt — which signals to watch

Lists 5-10 public signals worth tracking for one ICP segment, with source and cadence.

## Contents

- Activation
- Before you start
- Signal taxonomy
- Workflow

## Activation

`/psp:psp signal-hunt`, or:
- "What signals should we hunt for <ICP>"
- "Find signals for <segment>"
- "Signal hunt"

## Before you start

Read `brand-config.json` and `SOUL.md` from the project root. If either
is missing, stop and run the [setup](setup.md) mode instead. From them, carry:

- `icp` and `exclusion_criteria` — the segment is already locked
- `SOUL.md` vocabulary — the only source of pain language
- `SOUL.md` won't-chase boundaries — never surface those signals
- `research_cadence.signal_freshness_window_days` — default 14, never
  more than 30

## Signal taxonomy

The skill produces signal candidates across 6 categories:

| Category | Examples |
|---|---|
| **Hiring** | Specific role open ≤30 days; team size jump; first-of-kind hire (first SDR, first VP) |
| **Funding** | Round announced ≤30 days; secondary; bridge; ARR milestone |
| **Leadership** | New C-level / VP ≤30 days; departure; board change |
| **Product** | New tier / pricing change / feature launch / public roadmap ≤30 days |
| **Pivot** | Website hero rewrite; positioning shift; rebrand; new ICP language |
| **Content** | Podcast / panel / public talk on the relevant pain ≤30 days |

## Workflow

### 1. Take the ICP segment

Use `brand-config.icp.segment` unless the user names another (e.g.
"Series-B SaaS, $20-50M ARR, PLG motion"). If they're vague, ask for
precision before continuing.

### 2. Generate 5-10 candidate signals

For each candidate, output:

- **Signal type** (from the 6 categories)
- **What to look for** (specific shape — e.g. "Demand Gen Lead role posted ≤14 days")
- **Where to find it** — prefer sources switched on in
  `brand-config.signal_sources` (LinkedIn / Crunchbase / RSS / podcast
  feeds / their own blog). Public pages only; no logins, no API keys.
- **Cadence** (daily / weekly / event-driven)
- **Why this signal implies operational pain for this ICP**

### 3. Rank by hunting feasibility

Rank the 5-10 candidates by:
- **Volume**: how many target companies show this signal monthly
- **Specificity**: how directly it implies actionable pain
- **Effort**: how hard to operationalize the hunt

Volume is an estimate. Label it `est.` and say what it rests on. Do
not present a guess as a count.

### 4. Output

```markdown
# Signal hunt — <ICP segment>

| # | Signal | Where | Cadence | Pain implied | Volume (est.) |
|---|---|---|---|---|---|
| 1 | Demand Gen Lead role posted ≤14d | LinkedIn job search + RSS | Daily | Pipeline gap | ~15-30/mo |
| 2 | Series B announced ≤30d | Crunchbase + CB Insights newsletter | Weekly | 3x revenue mandate | ~5-10/mo |
| 3 | New CMO ≤60d | LinkedIn search + The Org | Weekly | 90-day GTM stack review | ~3-8/mo |
| 4 | ... | ... | ... | ... | ... |

## Recommended hunt stack
1. **Daily**: LinkedIn job posts (manual)
2. **Weekly**: Crunchbase + The Org
3. **Event-driven**: Podcast RSS for relevant shows

## Operational notes
- Capture signal date so freshness is enforced
- Tag each signal with the implied pain at capture time
- Signals older than `signal_freshness_window_days` (default 14) drop
  from the outreach queue; nothing older than 30 days stays in it
```

### 5. Hand off

Once signals are picked, hand to:
- **construct** mode ([construct.md](construct.md)) → map each signal to a felt pain
- **prospect-list** (`/prospect-list:who-to-contact`) → who shows the signal this week
- **cold-email** (`/cold-email:cold-email`) → first-line opener uses Signal verbatim

If a companion pack is not installed, name its install line
(`/plugin install <name>@gtm-operator-skills`); do not do its job here.

End with one line: `Next: /psp:psp construct` (map the top signals to
pain), or `Next: /prospect-list:who-to-contact` once the `psp` block is
published.
