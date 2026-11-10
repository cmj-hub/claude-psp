"""Freeze dated fixtures and preserve the scorer's existing freshness rule."""

import unittest
from unittest.mock import patch

import test_scoring


class FrozenFixture(unittest.TestCase):
    def test_clean_doc_is_independent_of_host_date(self):
        real_score = test_scoring.score
        for host_today in ("2026-11-10", "2040-01-01"):
            with self.subTest(host_today=host_today):
                def score_on_host(args, stdin=None):
                    if "--today" not in args:
                        args = [*args, "--today", host_today]
                    return real_score(args, stdin=stdin)

                with patch.object(test_scoring, "score", side_effect=score_on_host):
                    code, result = test_scoring.score_doc(test_scoring.DOC)
                self.assertEqual(code, 0, result)
                self.assertTrue(result["operational"], result)


class FrozenDateCases(unittest.TestCase):
    def score_event(self, event_date):
        doc = test_scoring.DOC.replace("2026-10-02", event_date)
        # Keep the CLI override explicit; these cases never read the host clock.
        return test_scoring.score(
            ["--stdin", "--today", "2026-11-10"],
            stdin=test_scoring.json.dumps({
                **test_scoring.GOOD,
                "signal": doc.split("## Signal\n", 1)[1].split("\n\n", 1)[0],
            }),
        )

    def test_fresh_at_thirty_days(self):
        code, result = self.score_event("2026-10-11")
        self.assertEqual(code, 0, result)
        self.assertTrue(result["operational"], result)

    def test_stale_at_thirty_one_days(self):
        code, result = self.score_event("2026-10-10")
        self.assertEqual(code, 1, result)
        self.assertFalse(result["operational"], result)
        self.assertIn("Stale signal (31d)", result["verdict"])

    def test_future_date_preserves_current_behavior(self):
        # The existing rule only rejects ages >30; do not add a new policy here.
        code, result = self.score_event("2026-11-11")
        self.assertEqual(code, 0, result)
        self.assertTrue(result["operational"], result)


if __name__ == "__main__":
    unittest.main()
