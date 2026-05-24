# SOUL.md — Operator voice template (for PSP work)

This file is the **operator's perspective on their buyer**. The PSP
skill loads this to anchor pain mapping in the operator's actual
understanding — not a generic "what would a VP Demand Gen feel?"
guess.

Copy this template to `SOUL.md` in your project root and fill it in.

---

## Who I am (the operator)

<One sentence about you. E.g. "I've sold to Series-B SaaS Demand Gen
leaders for 6 years and built two outbound programs to $5M+ ARR.">

## My buyer at 11am on Tuesday

<2-3 sentences painting the SPECIFIC operational moment your buyer is
in when the pain you solve is at peak. Not "they want better demand
gen" — "they're staring at last week's pipeline report knowing they
missed their target and have a board call Thursday.">

## Buyer vocabulary I've heard verbatim

<8-12 phrases your buyer has actually said to you — in calls, in
emails, in private. Not category jargon. Real strings:>

- "<phrase 1>"
- "<phrase 2>"
- ...

## Stories that anchor my PSP

<3-5 specific stories — anonymized but specific — where a signal-to-pain
mapping was right or wrong. These calibrate the PSP construct skill.>

- The Series-B SaaS that posted a Demand Gen Lead role 3 days before
  the CRO got fired
- The bootstrapped agency where the "Senior SDR" hire was a signal
  the founder was about to spend $200K/yr trying to scale outbound
  the wrong way

## What signals I will NOT chase

<Boundaries. E.g. "I will not target prospects in financial distress
without strong indication they have budget. I will not surface
political signals or anything that requires guessing about personal
life.">

---

## How the PSP skill uses this

When the PSP construct sub-skill maps signal → pain, it loads SOUL.md
+ brand-config.json together and:

1. Uses YOUR vocabulary list as the language anchor (refuses to
   substitute category jargon)
2. References your stories as calibration points ("this signal-pain
   mapping is closer to story A than story B")
3. Respects your won't-chase boundaries
4. Frames pain in the 11am-Tuesday moment you defined

The JMC framework (Signal → Pain → Timing → Role → Vocabulary) is
enforced regardless. SOUL.md ensures the output reflects how YOU read
the buyer, not a generic LinkedIn-influencer take.
