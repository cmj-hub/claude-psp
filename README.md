<p align="center">
  <img src="./assets/lockup.png" width="880" alt="Ideal customer profile skill for Claude Code. An ideal customer profile is who buys, drawn from a public signal and the words they use on a real day, not a costume persona.">
</p>

# Ideal customer profile skill for Claude Code

An ideal customer profile is who buys, drawn from a public signal and the words they use on a real day, not a costume persona.

> Your ICP describes a costume. A Pain Signal Profile describes Tuesday at 11am.

A Pain Signal Profile is a five-part buying brief: a public signal, the operational pain it implies, why that pain is acute now, who feels it at 11am on Tuesday, and the exact phrases that person uses. It replaces a static ICP.

You already know the costume. Series B. VP of Marketing. Fifty employees. You can write that slide in your sleep. It does not tell you who to email on Thursday.

A Demand Gen Lead job post, four days ago, does. That is a thing they did. The PSP names what that post does to the person who feels the pipeline gap at 11am, and the words they use when they talk about it.

We scored both samples in this repo. The costume scored **37**. The signal scored **100**. The Python that did that is in `scripts/score_psp.py`. No LLM. No paid API.

The build guide teaches a human. The pack teaches an agent.

<p align="center">
  <img src="./assets/demo.gif" alt="Ideal customer profile skill — signal 100, costume 37" width="100%">
</p>

## What this replaces

A static ICP deck. A $15K positioning sprint's first week. The slide that says "our buyer is a VP" and then wonders why outbound is quiet.

## Install

```text
skills add cmj-hub/claude-psp --all -g --full-depth
```

`--all` writes this pack for every host the installer knows. One host:

```text
skills add cmj-hub/claude-psp --skill '*' -g --full-depth -y -a claude-code
```

Swap `claude-code` for `cursor`, `codex`, `grok`, `github-copilot`, `windsurf`, `cline`, or `opencode`.

### Claude Code only

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install psp
```

## What you walk out with in 15 minutes

Artifact: `examples/good.json` versus `examples/bad.json`.

```bash
python3 scripts/score_psp.py --file examples/good.json
python3 scripts/score_psp.py --file examples/bad.json
```

Score the sample. Then write yours. One loop. One ICP. Example data. That is the whole first run.

## What this pack will not do

It will not hunt LinkedIn for you. It will not pick this quarter's PSP. It will not ingest your CRM.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. Those are judgement calls and live data. This pack gives you the instrument and the rubric; you bring the account.

## How is a Pain Signal Profile different from an ICP?

An ICP names who they are — stage, title, headcount. A Pain Signal Profile names what they just did, what that does to their Tuesday, why it is acute now, who feels it, and the phrases they actually use.

State is not a signal. A job post four days ago is. If you cannot fill all five parts, you do not have a PSP yet.

## Do I need live data to start?

No. The Series-B sample is in `examples/`. Score it. Then swap in a signal from your book. Live hunt is not the first loop.

## Does this hunt signals for me?

No. After the sample, `signal-hunt` names the *kinds* of public signals worth watching — job posts, funding, launches, hires. It does not log in. Closed-loop hunt on live accounts is out of scope here.

## On the site

- [Pain Signal Profiles pack](https://jaymountconsulting.com/skills/claude-psp) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack
- [Course twin](https://jaymountconsulting.com/learn/courses/pain-signal-profiles) — human build guide for this pack

## Free, no signup

- **[Pain Signal Profile Extractor](https://jaymountconsulting.com/tools/psp-extractor)** — the same job as this pack, hosted. No account, no key.
- [Pain Signal Profiles framework](https://jaymountconsulting.com/frameworks/pain-signal-profiles)
- [Pain Signal Playbook](https://jaymountconsulting.com/pain-signal-playbook)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — where your go-to-market stack is leaking, sent to your inbox.

That one does ask for an email, and it enrols you in a short follow-up on the same topic. Unsubscribe whenever.

[**The Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one free edition a week on building GTM systems that compound. No pitch in it.


## Next

[Value proposition](https://github.com/cmj-hub/claude-evp)

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
