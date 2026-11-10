"""Exercise the documented command with only the installed skill available."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "psp"


class PortableSkill(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="psp artifact ")
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name).resolve()
        self.assertNotIn(ROOT, self.project.parents)
        self.installed = self.project / "installed skill"
        # No pack-root scripts, templates, or symlink targets are supplied.
        shutil.copytree(SKILL, self.installed, symlinks=True)

    def documented_command(self):
        text = (self.installed / "SKILL.md").read_text(encoding="utf-8")
        commands = re.findall(r"^python3 .+--file brand-config\.json --json-path psp_drafts\.primary$",
                              text, re.MULTILINE)
        self.assertEqual(len(commands), 1, "SKILL.md must document the draft scorer command")
        return commands[0]

    def run_examples(self, skill_root, plugin_root=None):
        env = os.environ.copy()
        env.pop("CLAUDE_PLUGIN_ROOT", None)
        env.pop("PYTHONPATH", None)
        if plugin_root is not None:
            env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
        for name, code, total in (("good", 0, 100), ("bad", 1, 37), ("persona", 1, None)):
            with self.subTest(example=name):
                example = json.loads((ROOT / "examples" / f"{name}.json").read_text())
                (self.project / "brand-config.json").write_text(
                    json.dumps({"psp_drafts": {"primary": example}}), encoding="utf-8")
                result = subprocess.run(
                    # Claude Code substitutes ${CLAUDE_SKILL_DIR} in skill text before the command runs.
                    ["bash", "-c", self.documented_command().replace("${CLAUDE_SKILL_DIR}", str(skill_root))],
                    cwd=self.project,
                    env=env, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                if total is not None:
                    self.assertIn(f"Score: {total}/100", result.stdout)
                else:
                    self.assertIn("persona has no pain in the buyer's language", result.stdout)

    def test_plain_install_scores_examples_with_documented_command(self):
        self.run_examples(self.installed)

    def test_plugin_install_scores_examples_with_documented_command(self):
        self.run_examples(ROOT / "skills" / "psp", plugin_root=ROOT)

    def test_all_relative_markdown_links_stay_inside_artifact(self):
        for doc in self.installed.rglob("*.md"):
            text = doc.read_text(encoding="utf-8")
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
            links += re.findall(r"^\s*\[[^\]]+\]:\s*(\S+)", text, re.MULTILINE)
            for link in links:
                target = urlsplit(link.strip("<>"))
                if target.scheme or target.netloc or not target.path:
                    continue
                with self.subTest(doc=str(doc.relative_to(self.installed)), link=link):
                    path = (doc.parent / unquote(target.path)).resolve()
                    self.assertTrue(path.is_relative_to(self.installed), str(path))
                    self.assertTrue(path.exists(), str(path))

    def test_mode_files_carry_no_unfilled_variables(self):
        # Mode files are read as plain text, so a ${...} variable there is never filled in.
        for doc in (self.installed / "modes").glob("*.md"):
            with self.subTest(doc=doc.name):
                self.assertNotIn("${", doc.read_text(encoding="utf-8"))

    def test_runtime_assets_are_real_files_in_artifact(self):
        for name in ("SOUL.md", "brand-config.example.json", "AGENTS.md", "scripts/score_psp.py"):
            with self.subTest(asset=name):
                path = self.installed / name
                self.assertTrue(path.is_file(), f"Missing installed asset: {name}")
                self.assertTrue(path.resolve().is_relative_to(self.installed))
        config = self.installed / "brand-config.example.json"
        if config.is_file():
            self.assertIn("psp_drafts", json.loads(config.read_text()))


if __name__ == "__main__":
    unittest.main()
