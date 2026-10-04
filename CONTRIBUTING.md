# Contributing

Thanks for opening this repo. A few notes on how this project works
before you contribute.

## What kinds of contributions land

- **Bug reports** — open an issue with a reproducible case. The
  scripts in `scripts/` are deterministic, so bugs there are usually
  one-line fixes.
- **New modes** (`skills/psp/modes/<mode>.md`) that extend the existing framework. Discuss in
  an issue first if it's a substantial addition.
- **Calibration improvements** to the scoring scripts — if you can
  show a case where the script scores wrong, that's gold.
- **Cross-runtime fixes** (Cursor, Codex, Copilot and the other hosts
  in the README's Install section).
- **Translation** of the framework reference docs.

## What doesn't land

- Renaming the JMC framework concepts (Signal → Pain → EVP → Ask, the
  5 Schwartz tiers, the 4 content pillars) — these are course-anchored.
- Adding LLM calls inside the skills. The whole point is that the
  skills are deterministic.
- Adding paid-API dependencies to scripts. Scripts must work zero-dep.
- Renaming `claude-*` → `<other-runtime>-*`. We ship per-runtime ports
  as separate plugins instead.

## Development setup

```bash
git clone https://github.com/cmj-hub/<this-repo>.git
cd <this-repo>
# Test the install locally
./install.sh   # or install.ps1 on Windows
```

For Python scripts:

```bash
# All scripts are zero-dep Python 3.8+ — just run them
python3 scripts/<script>.py --help
```

## Pull-request checklist

- [ ] Skill names follow the spec (lowercase, hyphens, ≤64 chars,
      directory matches `name:` in frontmatter)
- [ ] The pack keeps one SKILL.md (`skills/psp/SKILL.md`); new jobs are mode files
- [ ] If you touch a script, smoke-test it and paste output in the PR
- [ ] If you add a new mode, list it in the README "What's in the
      pack" table, the routing table and `argument-hint` in
      `skills/psp/SKILL.md`, and add a trigger eval under `evals/`
- [ ] `python3 -m unittest discover -s tests` and
      `bash scripts/smoke-test.sh` pass
- [ ] CHANGELOG.md updated
- [ ] No new dependencies (any of: pip packages, npm packages, API
      keys, paid services)

## Reporting calibration issues with scoring scripts

If `scripts/score_psp.py` scores something obviously wrong:

1. Paste the input that produced the wrong score
2. State your expected score + actual score
3. Note which axis is mis-calibrated

The lexicons (`ABSTRACT_WORDS`, `SIGNAL_ACTION_PATTERNS`,
`RECENCY_PATTERNS`, `FIRMOGRAPHIC_PATTERNS`) sit at the top of the
script. Calibration fixes go there, with a test in `tests/` that pins
the case — keep the deterministic path stable. `examples/good.json`
must keep scoring 100 and `examples/bad.json` 37; the README quotes
both numbers.

## License

By contributing, you agree your contributions ship under the MIT
license already on this repo.

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
Part of the JMC public-build spine — see [/build](https://jaymountconsulting.com/build).
