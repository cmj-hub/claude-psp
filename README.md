# claude-psp

A Claude Code skill that builds **Pain Signal Profiles** — the link
from a public signal (what a prospect just did) to the felt
operational pain that drives B2B buying.

Foundation of the JMC framework. Plugs into cold email, EVP, outbound
audits, content strategy, and sales conversations.

Based on the **[Pain Signal Profiles](https://jaymountconsulting.com/learn/courses/pain-signal-profiles)**
course from The Compounding Engine.

## What it does

Translates a public signal into the operational pain that signal
implies:

```
Signal      →  Pain          →  Timing       →  Role          →  Vocabulary
(verifiable    (operational    (why now is    (who feels it    (their words,
 thing they    consequence)    acute)          most)            not yours)
 did)
```

Outputs a structured PSP doc with the 5 components, plus a recommended
signal hunt stack and the 8-12 vocabulary phrases your outreach should
use verbatim.

## Sub-skills

| Sub-skill | Job |
|---|---|
| `psp-construct` | Walk through PSP construction step-by-step for a specific ICP segment |
| `psp-signal-hunt` | Surface 5-10 public signals worth hunting + recommended sources |

## Install

### Claude Code (recommended)

```bash
/plugin marketplace add cmj-hub/claude-psp
/plugin install psp
```

### One-line install

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-psp/main/install.sh | bash
```

## Usage

```
> Build a PSP for Series-B SaaS with a PLG motion
```

Claude walks through:

1. Lock the ICP segment precision
2. Hunt 5-10 candidate signals
3. Map the top 3 signals → felt operational pain
4. Anchor timing (which 90-day trigger makes it acute)
5. Identify the felt-pain role (often a layer below buying authority)
6. Mine 8-12 vocabulary phrases the prospect actually uses
7. Output the PSP doc + recommended hunt stack

## Why this matters

A Pain Signal Profile is *not* an ICP, persona, or demographic. Those
describe who the buyer **is**. A PSP describes what they **just did**
(signal), what that **implies** (pain), why **now** it's acute
(timing), who **feels** it (role), and in **what language** they
describe it internally (vocabulary).

If you can't fill in all five, you don't have a PSP yet. Outreach
that anchors on a PSP lands; outreach that anchors on demographics
gets ignored.

## Course

This skill is the agent-form of the **Pain Signal Profiles** course.
The full course covers signal taxonomy (8 categories, 30+ specific
types), signal-source operations, pain-mapping rigor, vocabulary
mining at scale, and PSP refresh cadence.

→ [jaymountconsulting.com/learn/courses/pain-signal-profiles](https://jaymountconsulting.com/learn/courses/pain-signal-profiles)

Want it all-access? **[Operator Pass](https://jaymountconsulting.com/operator-pass)**
unlocks every course in The Compounding Engine.

## License

MIT. Built by [Jay Mount Consulting](https://jaymountconsulting.com).
See [/build](https://jaymountconsulting.com/build) for what's shipping
next.
