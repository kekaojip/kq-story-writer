#!/usr/bin/env python3
"""Read-only Writer draft length preflight using the shared visible_chars_v1 metric."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from wordcount_core import evaluate_wordcount, measure_wordcount, target_from_outline


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    parser.add_argument("--outline", type=Path, default=None)
    parser.add_argument("--target", type=int, default=None)
    args = parser.parse_args()

    body = args.draft.read_text(encoding="utf-8")
    target = args.target
    if target is None and args.outline is not None:
        try:
            target = target_from_outline(args.outline.read_text(encoding="utf-8"))
        except Exception:
            target = None

    result = measure_wordcount(body) if target is None else evaluate_wordcount(body, target)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
