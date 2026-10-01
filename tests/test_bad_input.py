#!/usr/bin/env python3
"""Bad input exits 2 and does not echo the file."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_psp.py"
FRONT = ROOT / "scripts" / "validate-skill-frontmatter.py"
TOKEN = "super-secret-token"


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCORE), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScorePspBadInput(unittest.TestCase):
    def test_good_example_scores(self):
        result = run(["--file", str(ROOT / "examples" / "good.json")])
        self.assertIn(result.returncode, (0, 1))
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_file(self):
        result = run(["--file", str(ROOT / "no-such-psp.json")])
        self.assertEqual(result.returncode, 2)
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_bad_json_hides_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "psp.json"
            path.write_text('{"signal": "' + TOKEN + '"', encoding="utf-8")
            result = run(["--file", str(path)])
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(TOKEN, result.stderr)
        self.assertNotIn(TOKEN, result.stdout)

    def test_array_rejected(self):
        result = run(["--stdin"], stdin="[]")
        self.assertEqual(result.returncode, 2)
        self.assertIn("JSON must be an object", result.stderr)

    def test_directory_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(["--file", tmp])
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a file", result.stderr)

    def test_vocabulary_string_does_not_crash(self):
        result = run(["--stdin"], stdin='{"signal":"s","pain":"p","vocabulary":"nope"}')
        self.assertIn(result.returncode, (0, 1))
        self.assertNotIn("Traceback", result.stderr)


class FrontmatterRead(unittest.TestCase):
    def test_pack_skills_still_valid(self):
        result = subprocess.run(
            [sys.executable, str(FRONT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_non_utf8_is_an_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "demo"
            skill.mkdir()
            (skill / "SKILL.md").write_bytes(b"\xff\xfe not text")
            result = subprocess.run(
                [sys.executable, str(FRONT)],
                cwd=tmp,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot read SKILL.md as UTF-8 text", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
