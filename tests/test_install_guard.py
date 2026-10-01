#!/usr/bin/env python3
"""Fallback installer refuses a symlink or a non-kebab name before deleting."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAFE_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"


def stage(dest: Path) -> None:
    shutil.copy2(ROOT / "install.sh", dest / "install.sh")
    for name in ("psp", "skills", "agents"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, dest / name, symlinks=False)


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
        text = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("LC_ALL=C", text)
        self.assertIn("the pack contains a symlink", text)

    def test_clean_copy_lands_under_temp_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "pack"
            home = Path(tmp) / "home"
            pack.mkdir()
            home.mkdir()
            stage(pack)
            result = invoke(pack, home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".claude" / "skills" / "psp" / "SKILL.md").is_file())
            self.assertTrue(
                (home / ".claude" / "skills" / "psp-construct" / "SKILL.md").is_file()
            )

    def test_symlink_refuses_before_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "pack"
            home = Path(tmp) / "home"
            pack.mkdir()
            home.mkdir()
            stage(pack)
            outside = Path(tmp) / "outside"
            outside.mkdir()
            (pack / "skills" / "psp-evil").symlink_to(outside)
            keep = home / ".claude" / "skills" / "psp" / "KEEP"
            keep.parent.mkdir(parents=True)
            keep.write_text("keep", encoding="utf-8")
            result = invoke(pack, home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr)
            self.assertEqual(keep.read_text(encoding="utf-8"), "keep")

    def test_uppercase_refuses_before_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "pack"
            home = Path(tmp) / "home"
            pack.mkdir()
            home.mkdir()
            stage(pack)
            bad = pack / "skills" / "BadName"
            bad.mkdir()
            (bad / "SKILL.md").write_text("nope", encoding="utf-8")
            keep = home / ".claude" / "skills" / "BadName" / "KEEP"
            keep.parent.mkdir(parents=True)
            keep.write_text("keep", encoding="utf-8")
            result = invoke(pack, home)
            self.assertNotEqual(result.returncode, 0, result.stderr)
            self.assertIn("lowercase", result.stderr)
            self.assertEqual(keep.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
