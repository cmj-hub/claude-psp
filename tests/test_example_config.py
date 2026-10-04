"""brand-config.example.json: the published `psp` block matches the locked draft."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "brand-config.example.json").read_text())

PSP_KEYS = {"signal_anchors", "primary_pain", "timing_trigger", "felt_pain_role", "vocabulary"}


class PublishedPSP(unittest.TestCase):
    def test_shape(self):
        self.assertEqual(set(CONFIG["psp"]), PSP_KEYS)
        self.assertIsInstance(CONFIG["psp"]["signal_anchors"], list)
        self.assertIsInstance(CONFIG["psp"]["vocabulary"], list)

    def test_matches_primary_draft(self):
        psp, draft = CONFIG["psp"], CONFIG["psp_drafts"]["primary"]
        self.assertEqual(psp["signal_anchors"][0], draft["signal"])
        self.assertEqual(psp["primary_pain"], draft["pain"])
        self.assertEqual(psp["timing_trigger"], draft["timing_trigger"])
        self.assertEqual(psp["felt_pain_role"], draft["felt_pain_role"])
        self.assertEqual(psp["vocabulary"], draft["vocabulary"])


if __name__ == "__main__":
    unittest.main()
