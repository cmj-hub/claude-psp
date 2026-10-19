# ICP — an ideal customer profile built from pain signals

Answers "who buys, how do I spot them, what shows they are ready now, and who do I skip" with a profile whose readiness test is a public pain signal, not a demographic. Use it when the operator asks for an ICP, an ideal customer profile, a buyer profile, or "who should we sell to".

## Contents

- Inputs
- Rules for the finished doc
- Output
- Score

## Inputs

Seller facts: what they sell, price, customers and their results, integrations, and who they lose to. An example account with dated public signals, if given. `brand-config.json` and `SOUL.md` when they exist; when the operator pasted the facts in the request, work from those and offer `setup` afterward. Do not ask questions when the facts are enough to draft; list the gaps instead.

## Rules for the finished doc

1. **Every row says where it came from.** A `Basis` column on each table: `seller fact`, `account fact` (with its date), or `inference`. An inference says what it rests on.
2. **Method rules are not facts.** Do not print recency windows ("30 days", "14 days"), trigger lists or scoring thresholds as if the seller said them. Give each signal its date and age, and let the operator choose the cut-off.
3. **Timing comes from evidence.** Name why now in the account's terms (a contract award, a hire, a stated 12-day close). Do not list trigger categories that have no evidence.
4. **No pronouns for named people** unless the source gives them. Use the name, the role, or they.
5. **No tool residue.** No config file names, scorer mentions, or notes about what was or was not run. The reader is the seller's team.
6. **Their words, marked.** Buyer phrases appear in quotation marks only when the source has those exact words, with where they came from.
7. **Unknowns once.** Collect gaps in one `Open questions` list at the end instead of writing **Unknown** in every row.
8. **No invented numbers.** Thresholds, deal sizes, buying-committee sizes and cycle lengths only when the facts give them.

## Output

```markdown
# <Seller>: ideal customer profile

<One sentence: who buys and the pain signal that says they are ready.>

## Who buys
| Dimension | Profile | Basis |
(company type, size, systems, process shape, who feels the pain, who signs)

## The pain signal
Signal → pain → why now → who feels it, for the segment, in the buyer's words.
Felt-pain role and buying role named separately.

## Signals that show they are ready now
| Signal | Where it shows up | What it implies | Basis |
(three to six, most telling first)

## Who to skip
| Exclude | Why | Basis |
(including the seller's stated loss pattern, and existing customers)

## Applied to <example account>
| Criterion | Evidence (dated) | Fit |
Then the pain brief: one sentence in the account's own words, with the phrase it uses and its source.
Verdict in one line: fit, partial fit, or no fit, and the one thing to confirm first.

## Open questions
- <gap the seller should answer, one line each>
```

Keep it to what a seller's team would act on: about 500 to 900 words, no preamble.

## Score

Save the account's pain signal (what it did and the date, the pain in its words, timing, role, vocabulary) as `gtm/psp.md` in the construct format and run (a dated signal ages against `--today`, default today):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_psp.py --file gtm/psp.md
```

On a markdown doc the scorer also refuses mentions of config files or the scorer, and a guessed he/she pronoun. Fix every line, score again, then show the profile. End with `Next: /evp:evp` only when working in the operator's project.
