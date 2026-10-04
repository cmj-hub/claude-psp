# Status — where you are and what's next

State-aware router for PSP work. Operators don't ship outreach on
day 1 — they walk a sequence: ICP precision → primary PSP → vocabulary
mining → secondary PSPs → operationalize signal hunting → refresh.

## Activation

Runs on a bare `/psp:psp` or `/psp:psp status`, or:
- "Where do I start with PSPs"
- "What's next for my PSP work"
- "I'm new to PSPs"

## State detection

```python
state = {
    "has_brand_config":    file_exists("brand-config.json"),
    "has_soul":            file_exists("SOUL.md"),
    "has_primary_psp":     brand_config.psp_drafts.primary and brand_config.psp_drafts.primary.pain != "",
    "psp_published":      brand_config.psp and brand_config.psp.primary_pain != "",  # the block evp and the suite read
    "has_secondary_psp":   brand_config.psp_drafts.secondary is not None,
    "vocabulary_ok":       len(brand_config.psp_drafts.primary.vocabulary or []) >= 4,  # 4 to operate, 8+ target
    "signals_sourced":     any value true in brand_config.signal_sources,
    "psp_age_days":        days_since(brand_config.psp_drafts.primary.refreshed_at),  # missing → treat as stale
}
```

| State | Route to |
|---|---|
| `!has_brand_config OR !has_soul` OR no `operator`/`icp` | [setup](setup.md) mode |
| `has_config AND !has_primary_psp` | [construct](construct.md) mode (build primary PSP) |
| `has_primary_psp AND !psp_published` | Score `psp_drafts.primary`; on exit 0 and a yes, publish the `psp` block ([construct](construct.md) Step 9). Downstream packs read `psp`, not the draft. |
| `has_primary_psp AND !vocabulary_ok` | "Vocabulary list <4 phrases — let's mine more. Need help?" |
| `vocabulary_ok AND !signals_sourced` | "Pick signal sources. Run `/psp:psp signal-hunt`." |
| `signals_sourced AND psp_age_days > psp_refresh_days` (default 90) | "PSP last refreshed >90 days ago — re-run `/psp:psp setup`" |
| `signals_sourced AND psp_age_days <= psp_refresh_days` | "PSP is fresh + operational. Want to build a secondary PSP? Or push downstream into `/evp:evp` + `/cold-email:cold-email`?" |

## Welcome flow

```
> /psp:psp

Welcome. Let's figure out where you are.

[Detected: brand-config.json missing]

You're at step 1 of 6:

1. ⬜ Onboarding — capture ICP + 1 primary PSP draft (15 min)   ← YOU ARE HERE
2. ⬜ Mine 8+ vocabulary phrases from real buyer writing
3. ⬜ Pick signal sources + cadence
4. ⬜ Run first signal hunt → 5-10 candidates
5. ⬜ Build secondary PSP for the next-priority segment
6. ⬜ Plug into /evp:evp + /cold-email:cold-email downstream

Step 1 takes ~15 minutes. Ready? (y/n)
```

## Status check mode

`/psp:psp status`:

```
# PSP program status

Brand config:        ✓ brand-config.json
SOUL:                ✓ SOUL.md (3 stories)
Primary PSP:         ✓ "Series-B SaaS pipeline-gap" (refreshed 12 days ago)
Published psp:       ✓ psp block in brand-config.json (read by evp, cold-email, prospect-list)
Vocabulary:          ✓ 8 phrases mined
Signal sources:      ✓ LinkedIn + Crunchbase + 2 RSS feeds
Secondary PSP:       ⬜ Not yet built

Recommended next step:
→ Build secondary PSP for your next-priority segment, OR
→ Push primary PSP into /evp:evp (lock the EVP) + /cold-email:cold-email (ship outreach)

Next: /evp:evp
```

End the status with one `Next:` line: the first unmet row above, or
`/evp:evp` once the `psp` block is published. `/gtm:next` (hub plugin)
names the next pack across the whole suite.

## Other modes

- [setup.md](setup.md)
- [construct.md](construct.md)
- [signal-hunt.md](signal-hunt.md)
