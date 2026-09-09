#!/usr/bin/env python3
"""Small deterministic wordcount core for Writer Runtime.

Ported from the main workflow's story-long-write/scripts/wordcount_core.py.
Metric: visible_chars_v1.

This Writer-side copy is read-only with respect to story semantics: it measures length only.
The main workflow remains the authority for accepting, revising, or changing chapter targets.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

METRIC = "visible_chars_v1"
_WHITE_SPACE_CODEPOINTS = frozenset(
    [*range(0x0009, 0x000E)]
    + [
        0x0020,
        0x0085,
        0x00A0,
        0x1680,
        *range(0x2000, 0x200B),
        0x2028,
        0x2029,
        0x202F,
        0x205F,
        0x3000,
    ]
)
_FRONTMATTER_KEY_RE = re.compile(r"^[A-Za-z_\u3400-\u9FFF][^:\n]{0,80}:[ \t]*(?:.*)$")
_LEADING_BLANK_RE = re.compile(r"^[\u0009\u0020\u3000]*$")
_ATX_HEADING_RE = re.compile(r"^[\u0009\u0020]{0,3}#{1,6}[\u0009\u0020]+\S")


def normalize_newlines(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def strip_recognizable_frontmatter(value: str) -> str:
    lines = value.split("\n")
    if not lines or lines[0] != "---":
        return value
    closing = next((i for i in range(1, min(len(lines), 201)) if lines[i] in {"---", "..."}), -1)
    if closing < 2 or not any(_FRONTMATTER_KEY_RE.match(line) for line in lines[1:closing]):
        return value
    return "\n".join(lines[closing + 1 :])


def visible_body(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("body must be a string")
    text = normalize_newlines(value)
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = strip_recognizable_frontmatter(text).split("\n")
    while lines and _LEADING_BLANK_RE.match(lines[0]):
        lines.pop(0)
    if lines and _ATX_HEADING_RE.match(lines[0]):
        lines.pop(0)
    return "\n".join(lines)


def count_visible_chars(value: str) -> int:
    return sum(ord(ch) not in _WHITE_SPACE_CODEPOINTS for ch in visible_body(value))


def compute_bands(target: int) -> dict[str, dict[str, int]]:
    if target <= 0:
        raise ValueError("target must be positive")
    return {
        "internal": {"min": (target * 88 + 99) // 100, "max": target * 112 // 100},
        "user": {"min": (target * 85 + 99) // 100, "max": target * 115 // 100},
    }


def evaluate(value: str, target: int | None = None) -> dict[str, Any]:
    actual = count_visible_chars(value)
    result: dict[str, Any] = {"metric": METRIC, "actual": actual}
    if target is None:
        result["status"] = "measured"
        return result
    bands = compute_bands(target)
    internal_pass = bands["internal"]["min"] <= actual <= bands["internal"]["max"]
    user_pass = bands["user"]["min"] <= actual <= bands["user"]["max"]
    status = "internal_pass" if internal_pass else ("borderline" if user_pass else ("under" if actual < bands["user"]["min"] else "over"))
    result.update(
        {
            "target": target,
            "internal_band": {**bands["internal"], "status": "pass" if internal_pass else "fail"},
            "user_band": {**bands["user"], "status": "pass" if user_pass else "fail"},
            "signed_error_pct": (actual - target) / target,
            "absolute_error_pct": abs((actual - target) / target),
            "status": status,
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure Writer draft length using visible_chars_v1")
    parser.add_argument("file", type=Path)
    parser.add_argument("--target", type=int, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    result = evaluate(text, args.target)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"metric={METRIC} actual={result['actual']} status={result['status']}")
        if args.target is not None:
            print(f"target={args.target} internal={result['internal_band']} user={result['user_band']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
