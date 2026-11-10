#!/usr/bin/env python3
"""Compatibility entry point for the scorer bundled with the PSP skill."""

from pathlib import Path
import runpy


if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).resolve().parents[1] / "skills" / "psp" / "scripts" / "score_psp.py"),
        run_name="__main__",
    )
