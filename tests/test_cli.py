#!/usr/bin/env python3
"""Scorer CLI convention: --json, fix lines on exit 1, Next: line on every run."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_psp.py"


def run(*args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCORE), *args], input=stdin, capture_output=True, text=True
    )


class ScorerCli(unittest.TestCase):
    def test_json_flag_matches_format_json(self):
        a = run("--file", str(ROOT / "examples" / "good.json"), "--json")
        b = run("--file", str(ROOT / "examples" / "good.json"), "--format", "json")
        self.assertEqual(a.returncode, 0)
        self.assertEqual(json.loads(a.stdout), json.loads(b.stdout))

    def test_pass_names_next_suite_step(self):
        result = run("--file", str(ROOT / "examples" / "good.json"))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines()[-1], "Next: /evp:evp")
        data = json.loads(run("--file", str(ROOT / "examples" / "good.json"), "--json").stdout)
        self.assertEqual(data["next"], "/evp:evp")
        self.assertEqual(data["reasons"], [])

    def test_refusal_lines_say_what_to_change(self):
        result = run("--file", str(ROOT / "examples" / "bad.json"))
        self.assertEqual(result.returncode, 1)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(lines[-1], "Next: fix the lines above and run this again.")
        fixes = [line for line in lines if line.startswith("- ")]
        self.assertTrue(fixes)
        for line in fixes:
            self.assertIn(" → ", line)

    def test_json_reasons_and_fixes_are_parallel(self):
        data = json.loads(run("--file", str(ROOT / "examples" / "persona.json"), "--json").stdout)
        self.assertEqual(len(data["reasons"]), len(data["fixes"]))
        self.assertIn("persona has no pain in the buyer's language", data["reasons"])
        self.assertEqual(data["refusal"], "persona has no pain in the buyer's language")
        self.assertTrue(data["next"].startswith("fix the lines above"))

    def test_help_shows_example(self):
        result = run("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("examples/good.json", result.stdout)



class StableOutput(unittest.TestCase):
    def test_same_output_under_any_hash_seed(self):
        import os
        outs = set()
        for seed in ("1", "2", "3"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "score_psp.py"), '--file', 'examples/bad.json'],
                capture_output=True, text=True, cwd=ROOT, env=env,
            )
            outs.add(proc.stdout)
        self.assertEqual(len(outs), 1)

if __name__ == "__main__":
    unittest.main()
