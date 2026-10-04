# Security

## What this pack does on your machine

- One script, `scripts/score_psp.py`: stdlib Python, run locally. It reads the PSP draft you point it at (a `.json` or `.md` file, `brand-config.json`, or stdin) and prints a score. It writes nothing.
- The skills read `brand-config.json` and `SOUL.md` from your project root.
- The skills write only to your project root: `brand-config.json` (this pack's keys, merged at the field level), this pack's sections of `SOUL.md`, and `psp-<segment-slug>.md`. They ask before changing a filled field.
- Network: no script opens a network connection. `psp`, `psp-construct` and `psp-signal-hunt` allow the agent's WebFetch to read a public page (a careers page, a press release) when you ask for one.
- `install.sh` / `install.ps1` print the repo URL and exit. They download and copy nothing.
- No telemetry. No credentials asked for or stored.
- Nothing is sent, posted or published by the pack.

## Reporting a vulnerability

Email jay@jaymountconsulting.com with "security" and the repo name in the subject, or open a private advisory under this repo's Security tab. Do not open a public issue for a vulnerability. Expect a reply within five business days.

## Supported versions

Only the latest release on `main` gets fixes.
