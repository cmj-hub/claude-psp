#!/usr/bin/env python3
"""
score_psp.py — Deterministic Pain Signal Profile scorer.

Scores a PSP doc 0-100 across the 5 components: signal specificity,
pain specificity, timing anchor, role precision, vocabulary specificity.

USAGE:
    python3 score_psp.py --file path/to/psp.md
    python3 score_psp.py --file brand-config.json --json-path psp_drafts.primary
    python3 score_psp.py --stdin    # full PSP JSON on stdin

NO LLM. NO network calls. Pure regex + feature engineering.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


# Abstract / generic words that downgrade specificity scores.
ABSTRACT_WORDS = {
    "scale", "growth", "optimize", "leverage", "synergy",
    "innovate", "transform", "best-in-class", "world-class",
    "next-generation", "cutting-edge", "robust", "seamless",
    "drive", "enable", "empower", "accelerate", "streamline",
}

# Demographics — NOT signals.
DEMOGRAPHIC_INDICATORS = [
    r"\bSeries\s+[A-Z]\b",   # state, not action
    r"\b\d+\s+employees\b",  # state
    r"\b(B2B|B2C|SaaS|PLG)\b only without verb",
]

# Strong-signal patterns (verbs of action).
SIGNAL_ACTION_PATTERNS = [
    r"\bposted\b", r"\bannounced\b", r"\bshipped\b", r"\bhired\b",
    r"\bpromoted\b", r"\blaunched\b", r"\braised\b", r"\bchanged\b",
    r"\bappeared on\b", r"\brebranded\b", r"\bpivoted\b",
]

# Time-anchor language (signals recency).
RECENCY_PATTERNS = [
    r"\b≤\s*\d+\s*(d(ay)?s?|w(eek)?s?|months?)\b",
    r"\bin (the )?(last|past)\s+\d+\s+(days?|weeks?|months?)\b",
    r"\b\d+\s+(days?|weeks?) ago\b",
    r"\bjust\b",
    r"\brecently\b",
]

TIMING_TRIGGERS = ["new-exec", "budget-cycle", "obvious-failure"]


@dataclass
class PSPInputs:
    signal: str = ""
    pain: str = ""
    timing_trigger: str = ""
    felt_pain_role: str = ""
    vocabulary: List[str] = field(default_factory=list)


@dataclass
class AxisScore:
    name: str
    score: int
    max_score: int
    notes: List[str] = field(default_factory=list)


@dataclass
class PSPScore:
    total: int
    max_total: int
    verdict: str
    axes: List[AxisScore]


# ----------------------------------------------------------------------------
# Per-axis scoring
# ----------------------------------------------------------------------------

def score_signal(s: str) -> AxisScore:
    """25 points. Verifiable action + recency + specificity."""
    score = 25
    notes = []
    if not s.strip():
        return AxisScore("signal", 0, 25, ["Empty signal"])

    has_action = any(re.search(p, s, re.IGNORECASE) for p in SIGNAL_ACTION_PATTERNS)
    has_recency = any(re.search(p, s, re.IGNORECASE) for p in RECENCY_PATTERNS)

    if not has_action:
        score -= 10
        notes.append("No action verb — signal should describe what they DID")
    if not has_recency:
        score -= 8
        notes.append("No recency anchor — add ≤14d / ≤30d / 'just' / 'recently'")

    # Penalize demographics-only signals
    if not has_action and re.search(r"\b(VP|CEO|CRO|CFO|Director)\b", s):
        score -= 5
        notes.append("Mentions a role but no action — that's a demographic, not a signal")

    return AxisScore("signal", max(0, score), 25, notes)


def score_pain(p: str, vocabulary: List[str]) -> AxisScore:
    """25 points. Specific operational moment + uses vocabulary + no abstract jargon."""
    score = 25
    notes = []
    if not p.strip():
        return AxisScore("pain", 0, 25, ["Empty pain"])

    # Count abstract / generic words
    abstract_hits = [w for w in ABSTRACT_WORDS if re.search(rf"\b{re.escape(w)}\b", p, re.IGNORECASE)]
    if abstract_hits:
        deduction = min(15, len(abstract_hits) * 5)
        score -= deduction
        notes.append(f"Abstract words found: {', '.join(abstract_hits)} — use buyer vocabulary")

    # Reward use of vocabulary
    if vocabulary:
        used = sum(1 for v in vocabulary if v.lower() in p.lower())
        if used == 0:
            score -= 8
            notes.append("Pain doesn't use any vocabulary list phrases")
        else:
            notes.append(f"Uses {used} vocabulary phrase(s) — good")

    # Length: pain should be 1-2 sentences, not 5
    word_count = len(p.split())
    if word_count > 40:
        score -= 3
        notes.append(f"Pain is {word_count} words — try to compress to 1 specific sentence")
    if word_count < 5:
        score -= 5
        notes.append("Pain is too terse — needs operational detail")

    return AxisScore("pain", max(0, score), 25, notes)


def score_timing(t: str) -> AxisScore:
    """15 points. Must be one of the 3 triggers."""
    score = 15
    notes = []
    if not t.strip():
        return AxisScore("timing", 0, 15, ["Empty timing trigger"])

    t_clean = t.lower().strip()
    if t_clean in TIMING_TRIGGERS:
        notes.append(f"Timing trigger valid: {t_clean}")
    elif any(trig in t_clean for trig in TIMING_TRIGGERS):
        score -= 3
        notes.append(f"Includes a trigger keyword but not a clean match — normalize to one of: {TIMING_TRIGGERS}")
    else:
        score -= 10
        notes.append(f"Not a recognized trigger — must be one of: {TIMING_TRIGGERS}")

    return AxisScore("timing", max(0, score), 15, notes)


def score_role(r: str) -> AxisScore:
    """15 points. Specific role title + check for felt-pain-vs-buying-authority distinction."""
    score = 15
    notes = []
    if not r.strip():
        return AxisScore("felt-pain-role", 0, 15, ["Empty role"])

    # Penalize C-level only (often buying authority, not felt-pain)
    if re.match(r"^(CEO|CFO|CRO|COO|CMO|Founder)\s*$", r.strip(), re.IGNORECASE):
        score -= 5
        notes.append(f"'{r}' is often the buying authority — name who FEELS the pain at 11am Tuesday (often a layer below)")

    # Reward specific titles
    if re.search(r"\b(VP|Head of|Director|Lead|Manager)\s+(of\s+)?\w+", r, re.IGNORECASE):
        notes.append("Specific title — good")

    return AxisScore("felt-pain-role", max(0, score), 15, notes)


def score_vocabulary(v: List[str]) -> AxisScore:
    """20 points. ≥4 phrases, no generic jargon, average length not too short."""
    score = 20
    notes = []
    if not v:
        return AxisScore("vocabulary", 0, 20, ["Empty vocabulary list"])

    if len(v) < 4:
        score -= 10
        notes.append(f"Only {len(v)} phrase(s) — target 4-8 minimum")

    # Penalize abstract phrases
    abstract_hits = []
    for phrase in v:
        for word in ABSTRACT_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", phrase, re.IGNORECASE):
                abstract_hits.append(phrase)
                break
    if abstract_hits:
        score -= min(8, len(abstract_hits) * 3)
        notes.append(f"Abstract phrases: {abstract_hits} — mine real buyer writing instead")

    # Average word count — too short = single-word phrases (less specific)
    avg = sum(len(p.split()) for p in v) / max(1, len(v))
    if avg < 2:
        score -= 5
        notes.append("Phrases averaging <2 words each — too terse to be voice fingerprints")

    return AxisScore("vocabulary", max(0, score), 20, notes)


def score_psp(psp: PSPInputs) -> PSPScore:
    axes = [
        score_signal(psp.signal),
        score_pain(psp.pain, psp.vocabulary),
        score_timing(psp.timing_trigger),
        score_role(psp.felt_pain_role),
        score_vocabulary(psp.vocabulary),
    ]
    total = sum(a.score for a in axes)
    max_total = sum(a.max_score for a in axes)

    if total >= 85:
        verdict = "Strong PSP — ready to operationalize"
    elif total >= 70:
        verdict = "Solid PSP — tighten 1-2 weak axes"
    elif total >= 50:
        verdict = "Workable but needs work — re-mine vocabulary or sharpen pain"
    else:
        verdict = "Too abstract / generic — re-do onboarding"

    return PSPScore(total=total, max_total=max_total, verdict=verdict, axes=axes)


# ----------------------------------------------------------------------------
# Input loading
# ----------------------------------------------------------------------------

def from_dict(d: dict) -> PSPInputs:
    return PSPInputs(
        signal=d.get("signal", ""),
        pain=d.get("pain", ""),
        timing_trigger=d.get("timing_trigger", "") or d.get("timing", ""),
        felt_pain_role=d.get("felt_pain_role", "") or d.get("role", ""),
        vocabulary=d.get("vocabulary", []) or [],
    )


def load_from_json_file(path: str, json_path: Optional[str]) -> PSPInputs:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if json_path:
        for key in json_path.split("."):
            data = data.get(key, {}) if isinstance(data, dict) else {}
    return from_dict(data)


def load_from_md_file(path: str) -> PSPInputs:
    """Very simple MD parser. Looks for ## headings matching the 5 components."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    blocks = re.split(r"^##\s+", text, flags=re.MULTILINE)
    out = PSPInputs()
    for block in blocks:
        head, _, body = block.partition("\n")
        head_l = head.strip().lower()
        body_clean = body.strip().split("\n##")[0].strip()
        if "signal" in head_l and not out.signal:
            out.signal = body_clean
        elif "pain" in head_l and not out.pain:
            out.pain = body_clean
        elif "timing" in head_l:
            out.timing_trigger = body_clean
        elif "role" in head_l or "felt-pain" in head_l:
            out.felt_pain_role = body_clean
        elif "vocabulary" in head_l:
            # Extract bullet items
            out.vocabulary = re.findall(r"^[-*]\s+\"?(.+?)\"?$", body_clean, flags=re.MULTILINE)
    return out


def format_text(s: PSPScore) -> str:
    lines = [
        f"# PSP Score",
        f"",
        f"Score: {s.total}/{s.max_total} — {s.verdict}",
        f"",
        f"## Per-axis",
    ]
    for axis in s.axes:
        lines.append(f"  {axis.name.ljust(20)} {axis.score}/{axis.max_score}")
        for note in axis.notes:
            lines.append(f"    • {note}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", default=None, help="Path to PSP file (md or json)")
    parser.add_argument("--json-path", default=None, help="Dotted path in JSON to PSP block (e.g. psp_drafts.primary)")
    parser.add_argument("--stdin", action="store_true", help="Read PSP JSON from stdin")
    parser.add_argument("--format", default="text", choices=["text", "json"])
    args = parser.parse_args()

    if args.stdin:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as err:
            print(f"Bad JSON on stdin: {err}", file=sys.stderr)
            return 2
        psp = from_dict(data)
    elif args.file:
        if args.file.endswith(".json"):
            psp = load_from_json_file(args.file, args.json_path)
        else:
            psp = load_from_md_file(args.file)
    else:
        print("Need --file or --stdin.", file=sys.stderr)
        return 2

    result = score_psp(psp)
    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(format_text(result))
    return 0 if result.total >= 70 else 1


if __name__ == "__main__":
    sys.exit(main())
