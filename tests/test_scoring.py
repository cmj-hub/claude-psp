#!/usr/bin/env python3
"""Scores the README quotes stay true, and the AGENTS.md rules the scorer enforces hold."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_psp.py"

GOOD = json.loads((ROOT / "examples" / "good.json").read_text(encoding="utf-8"))


def score(args, stdin=None):
    result = subprocess.run(
        [sys.executable, str(SCORE), *args, "--format", "json"],
        input=stdin,
        capture_output=True,
        text=True,
    )
    return result.returncode, json.loads(result.stdout)


def score_dict(d):
    return score(["--stdin"], stdin=json.dumps(d))


def axis(result, name):
    return next(a for a in result["axes"] if a["name"] == name)


class ReadmeNumbers(unittest.TestCase):
    """README, assets/spec.json and demo.gif quote these two numbers."""

    def test_good_scores_100(self):
        code, result = score(["--file", str(ROOT / "examples" / "good.json")])
        self.assertEqual(result["total"], 100)
        self.assertEqual(code, 0)

    def test_bad_scores_37(self):
        code, result = score(["--file", str(ROOT / "examples" / "bad.json")])
        self.assertEqual(result["total"], 37)
        self.assertEqual(code, 1)

    def test_example_config_primary_is_operational(self):
        code, _ = score([
            "--file", str(ROOT / "brand-config.example.json"),
            "--json-path", "psp_drafts.primary",
        ])
        self.assertEqual(code, 0)

    def test_example_config_published_block_scores(self):
        """The `psp` block uses primary_pain and signal_anchors; it scores like the draft."""
        _, draft = score([
            "--file", str(ROOT / "brand-config.example.json"),
            "--json-path", "psp_drafts.primary",
        ])
        code, result = score([
            "--file", str(ROOT / "brand-config.example.json"),
            "--json-path", "psp",
        ])
        self.assertEqual(result["axes"], draft["axes"])
        self.assertGreaterEqual(result["total"], 70)
        self.assertEqual(result["buyer_phrase"], "pipeline gap")
        self.assertEqual(result["refusal"], "")
        self.assertEqual(code, 0)

    def test_published_block_from_stdin(self):
        config = json.loads((ROOT / "brand-config.example.json").read_text(encoding="utf-8"))
        code, result = score_dict(config["psp"])
        self.assertTrue(result["operational"], result)
        self.assertEqual(result["pain_brief"], config["psp"]["primary_pain"])
        self.assertEqual(code, 0)


class StaleSignals(unittest.TestCase):
    """AGENTS.md rule 8: signals >30 days old stay out of active outreach."""

    def test_stale_signal_is_not_operational(self):
        code, result = score_dict({**GOOD, "signal": "Posted Demand Gen Lead role 45 days ago"})
        self.assertEqual(code, 1)
        self.assertFalse(result["operational"])
        self.assertIn("Stale", result["verdict"])

    def test_weeks_and_months_count(self):
        for text in ("Posted Demand Gen Lead role 6 weeks ago", "Announced Series B 2 months ago"):
            code, _ = score_dict({**GOOD, "signal": text})
            self.assertEqual(code, 1, text)

    def test_runway_is_not_an_age(self):
        code, _ = score_dict({**GOOD, "signal": "Raised Series B 5 days ago with 18 months of runway"})
        self.assertEqual(code, 0)

    def test_fresh_window_is_fine(self):
        code, _ = score_dict({**GOOD, "signal": "Posted Demand Gen Lead role ≤14 days"})
        self.assertEqual(code, 0)


class TimingTrigger(unittest.TestCase):
    def test_spelling_variants_normalize(self):
        for text in ("new exec", "New_Exec", "Budget Cycle", "obvious-failure"):
            _, result = score_dict({**GOOD, "timing_trigger": text})
            self.assertEqual(axis(result, "timing")["score"], 15, text)


class Firmographics(unittest.TestCase):
    def test_firmographic_signal_is_called_out(self):
        _, result = score_dict({**GOOD, "signal": "Series B SaaS company with 50 employees"})
        notes = " ".join(axis(result, "signal")["notes"])
        self.assertIn("firmographic", notes)


class MarkdownTemplate(unittest.TestCase):
    """The doc psp-construct writes scores without hand-editing."""

    def test_construct_output_parses(self):
        doc = """# PSP — Series-B SaaS

## Signal
Posted Senior Demand Gen Lead role on LinkedIn 4 days ago

## Pain
Pipeline gap; demand-gen motion isn't producing enough SQLs

## Timing
**Trigger:** new-exec
**Why now:** new CRO started three weeks ago

## Role (felt-pain holder)
VP Demand Gen

## Vocabulary
- "pipeline gap"
- "SDR ramp"
- "demand-gen motion isn't producing"
- "we keep closing wrong-fit logos"

## Top 5 signals to hunt operationally
1. LinkedIn job search, daily
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "psp.md"
            path.write_text(doc, encoding="utf-8")
            code, result = score(["--file", str(path)])
        self.assertEqual(result["total"], 100, result)
        self.assertEqual(code, 0)



class RecencyWindow(unittest.TestCase):
    def test_window_symbols_count_as_recent(self):
        for window in ("≤14 days", "<=14 days", "within 14 days"):
            with self.subTest(window=window):
                draft = dict(GOOD, signal=f"Posted a Demand Gen Lead role {window}")
                _code, result = score_dict(draft)
                self.assertEqual(axis(result, "signal")["score"], 25, axis(result, "signal")["notes"])

if __name__ == "__main__":
    unittest.main()
