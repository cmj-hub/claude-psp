#!/usr/bin/env python3
"""
score_psp.py — Deterministic Pain Signal Profile scorer.

Scores a PSP doc 0-100 across the 5 components: signal specificity,
pain specificity, timing anchor, role precision, vocabulary specificity.

USAGE:
    python3 score_psp.py --file path/to/psp.md
    python3 score_psp.py --file brand-config.json --json-path psp_drafts.primary
    python3 score_psp.py --file brand-config.json --json-path psp   # published block
    python3 score_psp.py --stdin    # full PSP JSON on stdin
    python3 score_psp.py --file examples/good.json --json   # one JSON object

OUTPUT:
    Text by default. On exit 1 every reason prints as
    "- <what is wrong> → <what to change>", then
    "Next: fix the lines above and run this again." On exit 0 the last
    line names the next suite step (Next: /evp:evp). --json adds
    "reasons", "fixes" (parallel lists) and "next" to the JSON object.

EXIT CODES:
    0  operational: score >= 70, signal not older than 30 days, and the
       pain uses a phrase from the buyer's vocabulary (prints the pain brief)
    1  needs work: score < 70, a stale signal, a persona with no pain in the
       buyer's language, or a pain that uses none of their phrases
    2  bad input (missing file, invalid JSON, wrong shape)

NO LLM. NO network calls. Pure regex + feature engineering.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


MAX_INPUT_BYTES = 2_000_000


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def _as_text(value: object) -> str:
    return value if isinstance(value, str) else ""


def read_text(path: str) -> str:
    try:
        with open(path, "rb") as handle:
            raw = handle.read(MAX_INPUT_BYTES + 1)
    except IsADirectoryError:
        fail_input(f"not a file: {path}")
    except FileNotFoundError:
        fail_input(f"file not found: {path}")
    except OSError:
        fail_input(f"cannot read file: {path}")
    if len(raw) > MAX_INPUT_BYTES:
        fail_input(f"file is too large: {path}")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input(f"file is not UTF-8 text: {path}")


def parse_json(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")
    if not isinstance(data, dict):
        fail_input("JSON must be an object")
    return data


def read_stdin_text() -> str:
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        fail_input("input is too large")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("input is not UTF-8 text")


# Abstract / generic words that downgrade specificity scores.
ABSTRACT_WORDS = {
    "scale", "growth", "optimize", "leverage", "synergy",
    "innovate", "transform", "best-in-class", "world-class",
    "next-generation", "cutting-edge", "robust", "seamless",
    "drive", "enable", "empower", "accelerate", "streamline",
}

# Firmographics — state, NOT signals.
FIRMOGRAPHIC_PATTERNS = [
    r"\bSeries\s+[A-Z]\b",
    r"\b\d+\+?\s+employees\b",
    r"\$?\d+\s*[MK]?\s*ARR\b",
    r"\b(B2B|B2C|SaaS|PLG)\b",
]

# Strong-signal patterns (verbs of action).
SIGNAL_ACTION_PATTERNS = [
    r"\bposted\b", r"\bannounced\b", r"\bshipped\b", r"\bhired\b",
    r"\bpromoted\b", r"\blaunched\b", r"\braised\b", r"\bchanged\b",
    r"\bappeared on\b", r"\brebranded\b", r"\bpivoted\b",
]

# Time-anchor language (signals recency).
RECENCY_PATTERNS = [
    # No leading \b: a word boundary never sits between a space and "≤".
    r"(?:≤|<=?|\bwithin)\s*\d+\s*(d(ay)?s?|w(eek)?s?|months?)\b",
    r"\bin (the )?(last|past)\s+\d+\s+(days?|weeks?|months?)\b",
    r"\b\d+\s+(days?|weeks?) ago\b",
    r"\bjust\b",
    r"\brecently\b",
]

TIMING_TRIGGERS = ["new-exec", "budget-cycle", "obvious-failure"]

# Words that do not count as a buyer's phrase on their own.
FILLER = {
    "they", "need", "to", "the", "a", "an", "and", "of", "for",
    "their", "our", "your", "with", "that", "this", "from", "into",
}

# Keys of a persona table: who the buyer is, not what hurts.
PERSONA_KEYS = {
    "persona", "cares_about", "challenge", "value_we_promise",
    "anti_persona", "firmographics",
}

# AGENTS.md rule 8: signals older than this stay out of active outreach.
STALE_AFTER_DAYS = 30

# "4 days ago", "≤14d", "within 2 weeks", "in the last 3 months" — not "18 months of runway".
_AGE_UNIT = r"(d|days?|w|wks?|weeks?|mos?|months?)"
AGE_PATTERN = re.compile(
    rf"(?:(?:≤|<=|<|within|in the (?:last|past)|last|past)\s*(\d+)\s*{_AGE_UNIT}\b"
    rf"|(\d+)\s*{_AGE_UNIT}\s+ago\b)",
    re.IGNORECASE,
)
UNIT_DAYS = {"d": 1, "w": 7, "m": 30}


def signal_age_days(s: str) -> Optional[int]:
    """Oldest age or window (in days) the signal text names, if any."""
    ages = []
    for m in AGE_PATTERN.finditer(s):
        n, unit = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        ages.append(int(n) * UNIT_DAYS[unit[0].lower()])
    return max(ages) if ages else None


def normalize_trigger(t: str) -> str:
    return re.sub(r"[\s_]+", "-", t.strip().lower())


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
    operational: bool = False
    pain_brief: str = ""
    buyer_phrase: str = ""
    refusal: str = ""
    reasons: List[str] = field(default_factory=list)
    fixes: List[str] = field(default_factory=list)
    next: str = ""


def buyer_phrases(vocabulary: List[str]) -> List[str]:
    """Phrases of at least two concrete words. Single words and jargon do not count."""
    found = []
    for phrase in vocabulary:
        words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'+-]*", phrase)
        concrete = [
            word for word in words
            if word.lower() not in ABSTRACT_WORDS and word.lower() not in FILLER
        ]
        if len(words) >= 2 and len(concrete) >= 2:
            found.append(phrase.strip())
    return found


def matched_buyer_phrase(pain: str, vocabulary: List[str]) -> str:
    """The first buyer phrase the pain sentence contains, or ""."""
    haystack = pain.lower()
    for phrase in buyer_phrases(vocabulary):
        if phrase.lower() in haystack:
            return phrase
    return ""


def persona_costume(data: dict) -> bool:
    """A JSON draft shaped like a persona table (title, cares-about, challenge)."""
    keys = {str(key).lower().replace("-", "_") for key in data}
    return bool(keys & PERSONA_KEYS)


def persona_markdown(text: str) -> bool:
    """A markdown doc with a Personas section and no Vocabulary section."""
    has_persona = re.search(r"(?m)^##\s+Personas\b", text) is not None
    has_vocab = re.search(r"(?m)^##\s+Vocabulary\b", text) is not None
    return has_persona and not has_vocab


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

    age = signal_age_days(s)
    if age is not None and age > STALE_AFTER_DAYS:
        score -= 5
        notes.append(f"Signal is {age} days old — stale past {STALE_AFTER_DAYS}d, keep it out of active outreach")

    if not has_action and any(re.search(p, s, re.IGNORECASE) for p in FIRMOGRAPHIC_PATTERNS):
        notes.append("Stage / headcount / category is firmographic state, not a signal — quote what they DID")

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
    abstract_hits = [w for w in sorted(ABSTRACT_WORDS) if re.search(rf"\b{re.escape(w)}\b", p, re.IGNORECASE)]
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
        elif abstract_hits:
            notes.append(f"Uses {used} vocabulary phrase(s), but abstract ones don't count as buyer voice")
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

    t_clean = normalize_trigger(t)
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
        for word in sorted(ABSTRACT_WORDS):
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


def score_psp(psp: PSPInputs, *, persona: bool = False) -> PSPScore:
    axes = [
        score_signal(psp.signal),
        score_pain(psp.pain, psp.vocabulary),
        score_timing(psp.timing_trigger),
        score_role(psp.felt_pain_role),
        score_vocabulary(psp.vocabulary),
    ]
    total = sum(a.score for a in axes)
    max_total = sum(a.max_score for a in axes)

    operational = total >= 70
    if total >= 85:
        verdict = "Strong PSP — ready to operationalize"
    elif total >= 70:
        verdict = "Solid PSP — tighten 1-2 weak axes"
    elif total >= 50:
        verdict = "Workable but needs work — re-mine vocabulary or sharpen pain"
    else:
        verdict = "Too abstract / generic — re-do onboarding"

    age = signal_age_days(psp.signal)
    if age is not None and age > STALE_AFTER_DAYS and total >= 70:
        # Rule 8 outranks the total: a stale signal is not operational.
        operational = False
        verdict = f"Stale signal ({age}d) — re-hunt before outreach"

    phrase = matched_buyer_phrase(psp.pain, psp.vocabulary)
    refusal = ""
    if not phrase:
        refusal = (
            "persona has no pain in the buyer's language" if persona
            else "pain is not in the buyer's language"
        )

    return PSPScore(
        total=total,
        max_total=max_total,
        verdict=verdict,
        axes=axes,
        operational=operational,
        pain_brief=psp.pain.strip() if phrase else "",
        buyer_phrase=phrase,
        refusal=refusal,
    )


# ----------------------------------------------------------------------------
# Fix lines: "<what is wrong> → <what to change>"
# ----------------------------------------------------------------------------

NEXT_STEP = "/evp:evp"
RETRY = "fix the lines above and run this again."

# Notes that are praise, not problems.
GOOD_NOTE = re.compile(r"(— good$|^Timing trigger valid|^Uses \d+ vocabulary phrase)")

# Notes that name a problem without saying what to change.
NOTE_FIXES = {
    "Empty signal": "quote one thing they did publicly in the last 30 days",
    "Empty pain": "write the 11am-Tuesday moment in the buyer's words",
    "Empty timing trigger": "set it to new-exec, budget-cycle or obvious-failure",
    "Empty role": "name the role that feels the pain at 11am Tuesday",
    "Empty vocabulary list": "add 4-8 phrases the buyer wrote or said",
    "Pain doesn't use any vocabulary list phrases": "put one vocabulary phrase into the pain sentence",
}

# Notes whose text after the dash is a reason, not a change to make.
PREFIX_FIXES = (
    ("Phrases averaging <2 words", "use 2-5 word phrases lifted from their writing"),
    ("Mentions a role but no action", "name what that person or company did, and when"),
    ("Signal is ", "find a signal from the last 30 days"),
    ("Pain is too terse", "add the operational detail: what breaks, for whom, this week"),
)

REFUSAL_FIXES = {
    "persona has no pain in the buyer's language":
        "replace the persona fields with signal, pain, timing_trigger, felt_pain_role and vocabulary; "
        "write the pain with one of their phrases",
    "pain is not in the buyer's language":
        "put one of your vocabulary phrases (two or more concrete words) into the pain sentence",
}


def split_note(axis: str, note: str) -> tuple:
    if note in NOTE_FIXES:
        return f"{axis}: {note}", NOTE_FIXES[note]
    what, sep, fix = note.partition(" — ")
    for prefix, better in PREFIX_FIXES:
        if note.startswith(prefix):
            return f"{axis}: {what}", better
    if sep:
        return f"{axis}: {what}", fix
    return f"{axis}: {note}", "rewrite this part and score again"


def build_fixes(result: "PSPScore") -> None:
    """Fill reasons/fixes (parallel) and next. Additive: other fields stay as they were."""
    reasons, fixes = [], []
    passed = result.operational and not result.refusal
    if not passed:
        if result.total < 70:
            reasons.append(f"score {result.total}/{result.max_total} is under 70")
            fixes.append("work through the axis lines below, lowest axis first")
        if result.refusal:
            reasons.append(result.refusal)
            fixes.append(REFUSAL_FIXES.get(result.refusal, "rewrite the pain in the buyer's words"))
        for axis in sorted(result.axes, key=lambda a: a.score - a.max_score):
            for note in axis.notes:
                if GOOD_NOTE.search(note) or "abstract ones don't count" in note:
                    continue
                what, fix = split_note(axis.name, note)
                reasons.append(what)
                fixes.append(fix)
        if not reasons:
            reasons.append(result.verdict)
            fixes.append("re-hunt a fresh signal and score again")
    result.reasons, result.fixes = reasons, fixes
    result.next = NEXT_STEP if passed else RETRY


# ----------------------------------------------------------------------------
# Input loading
# ----------------------------------------------------------------------------

def from_dict(d: dict) -> PSPInputs:
    """Reads a draft (`psp_drafts.primary`) or the published `psp` block.

    The published block names the pain `primary_pain` and carries a list of
    `signal_anchors`; the first anchor is the locked primary signal.
    """
    if not isinstance(d, dict):
        fail_input("JSON must be an object")
    vocabulary = d.get("vocabulary", []) or []
    if not isinstance(vocabulary, list):
        vocabulary = []
    signal = _as_text(d.get("signal", ""))
    if not signal:
        anchors = d.get("signal_anchors", [])
        if isinstance(anchors, list) and anchors:
            signal = _as_text(anchors[0])
    return PSPInputs(
        signal=signal,
        pain=_as_text(d.get("pain", "") or d.get("primary_pain", "")),
        timing_trigger=_as_text(d.get("timing_trigger", "") or d.get("timing", "")),
        felt_pain_role=_as_text(d.get("felt_pain_role", "") or d.get("role", "")),
        vocabulary=[item for item in vocabulary if isinstance(item, str)],
    )


def load_json_leaf(path: str, json_path: Optional[str]) -> dict:
    data = parse_json(read_text(path))
    if json_path:
        for key in json_path.split("."):
            data = data.get(key, {}) if isinstance(data, dict) else {}
    if not isinstance(data, dict):
        fail_input("JSON must be an object")
    return data


def load_from_json_file(path: str, json_path: Optional[str]) -> PSPInputs:
    return from_dict(load_json_leaf(path, json_path))


def parse_md(text: str) -> PSPInputs:
    """Very simple MD parser. Looks for ## headings matching the 5 components."""
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
            # psp-construct writes "**Trigger:** new-exec" + "**Why now:** ..."
            m = re.search(r"trigger:?\**:?\s*(.+)", body_clean, re.IGNORECASE)
            out.timing_trigger = m.group(1).strip() if m else body_clean
        elif "role" in head_l or "felt-pain" in head_l:
            out.felt_pain_role = body_clean
        elif "vocabulary" in head_l:
            # Extract bullet items
            out.vocabulary = re.findall(r"^[-*]\s+\"?(.+?)\"?$", body_clean, flags=re.MULTILINE)
    return out


def load_from_md_file(path: str) -> PSPInputs:
    return parse_md(read_text(path))


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
    if s.refusal:
        lines.extend(["", f"Refusal: {s.refusal}"])
    elif s.pain_brief and s.operational:
        lines.extend([
            "",
            "## Pain brief",
            s.pain_brief,
            "",
            f"Buyer phrase: {s.buyer_phrase}",
        ])
    if s.reasons:
        lines.extend(["", "## What to fix"])
        lines.extend(f"- {what} → {fix}" for what, fix in zip(s.reasons, s.fixes))
    lines.extend(["", f"Next: {s.next}"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score a Pain Signal Profile 0-100. Exit 0 operational, 1 needs work, 2 bad input.",
        epilog="example: python3 scripts/score_psp.py --file examples/good.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file", default=None, help="Path to PSP file (md or json)")
    parser.add_argument("--json-path", default=None, help="Dotted path in JSON to PSP block (e.g. psp_drafts.primary)")
    parser.add_argument("--stdin", action="store_true", help="Read PSP JSON from stdin")
    parser.add_argument("--json", dest="format", action="store_const", const="json",
                        help="Print one JSON object (same as --format json)")
    parser.add_argument("--format", dest="format", default="text", choices=["text", "json"],
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    persona = False
    if args.stdin:
        leaf = parse_json(read_stdin_text())
        persona = persona_costume(leaf)
        psp = from_dict(leaf)
    elif args.file:
        if args.file.endswith(".json"):
            leaf = load_json_leaf(args.file, args.json_path)
            persona = persona_costume(leaf)
            psp = from_dict(leaf)
        else:
            text = read_text(args.file)
            persona = persona_markdown(text)
            psp = parse_md(text)
    else:
        print("Need --file or --stdin.", file=sys.stderr)
        return 2

    result = score_psp(psp, persona=persona)
    build_fixes(result)
    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(format_text(result))
    if result.refusal or not result.operational:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
