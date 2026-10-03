#!/usr/bin/env python3
"""Installers point at the repo and do not download or copy into $HOME."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAFE_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
REPO = "https://github.com/cmj-hub/claude-psp"


def invoke(pack: Path, home: Path):
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["PATH"] = SAFE_PATH
    return subprocess.run(
        ["bash", str(pack / "install.sh")],
        cwd=pack,
        env=env,
        capture_output=True,
        text=True,
    )


class InstallGuard(unittest.TestCase):
    def test_scripts_copy_matches_root(self):
        self.assertEqual(
            (ROOT / "install.sh").read_bytes(),
            (ROOT / "scripts" / "install.sh").read_bytes(),
        )
        self.assertEqual(
            (ROOT / "install.ps1").read_bytes(),
            (ROOT / "scripts" / "install.ps1").read_bytes(),
        )

    def test_installers_have_no_npx_or_home_copy(self):
        forbidden = ("npx", "curl", "wget")
        for rel in ("install.sh", "scripts/install.sh", "install.ps1", "scripts/install.ps1"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            lower = text.lower()
            for token in forbidden:
                self.assertNotIn(token, lower, rel)
            self.assertNotIn("$HOME/", text, rel)
            self.assertNotIn("$HOME\\", text, rel)
            self.assertNotIn("$env:USERPROFILE", text, rel)
            self.assertIn(REPO, text)

    def test_pointer_does_not_write_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "pack"
            home = Path(tmp) / "home"
            pack.mkdir()
            home.mkdir()
            shutil.copy2(ROOT / "install.sh", pack / "install.sh")
            result = invoke(pack, home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(REPO, result.stdout)
            self.assertFalse((home / ".claude").exists())
            self.assertEqual(list(home.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
