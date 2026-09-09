#!/usr/bin/env python3
"""Read-only Writer draft length preflight using the shared visible_chars_v1 metric.

Resolution order:
1. explicit --target
2. task-level explicit range / target
3. outline canonical 字数目标 + 字数口径
4. target_unresolved (never silently treated as a passed target check)
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from wordcount_core import count_visible_chars, evaluate_wordcount, target_from_outline


_RANGE_PATTERNS = [
    re.compile(
        r"(?:字数范围|目标字数|字数目标|目标长度|approximate\s+length|target(?:_chars|\s+length)?)"
        r"[^0-9\n]{0,40}([1-9]\d{2,6})\s*(?:-|–|—|~|～|至|到)\s*([1-9]\d{2,6})",
        re.IGNORECASE,
    ),
]
_SINGLE_PATTERNS = [
    re.compile(
        r"(?:字数目标|目标字数|目标长度|target_chars|target\s+length)"
        r"\s*[:：=]?\s*([1-9]\d{2,6})\s*(?:字|字符|中文字符)?",
        re.IGNORECASE,
    ),
]


def _read_optional(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _task_spec(text: str | None) -> dict[str, Any] | None:
    if not text:
        return None
    for pattern in _RANGE_PATTERNS:
        match = pattern.search(text)
        if match:
            low, high = int(match.group(1)), int(match.group(2))
            if low > high:
                low, high = high, low
            return {"kind": "range", "min": low, "max": high, "source": "task"}
    for pattern in _SINGLE_PATTERNS:
        match = pattern.search(text)
        if match:
            return {"kind": "target", "target": int(match.group(1)), "source": "task"}
    return None


def _outline_target(text: str | None) -> int | None:
    if not text:
        return None
    try:
        return target_from_outline(text)
    except Exception:
        return None


def _range_result(body: str, spec: dict[str, Any], outline_target: int | None) -> dict[str, Any]:
    actual = count_visible_chars(body)
    low, high = int(spec["min"]), int(spec["max"])
    status = "within_user_band" if low <= actual <= high else ("under" if actual < low else "over")
    result: dict[str, Any] = {
        "schema": "story-wordcount-task-range/v1",
        "metric": "visible_chars_v1",
        "source": spec["source"],
        "target_range": {"min": low, "max": high},
        "actual": actual,
        "status": status,
        "invalid_reason": None,
    }
    if outline_target is not None:
        result["outline_target"] = outline_target
        if not (low <= outline_target <= high):
            result["status"] = "target_conflict"
            result["invalid_reason"] = "OUTLINE_TARGET_OUTSIDE_TASK_RANGE"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    parser.add_argument("--task", type=Path, default=None)
    parser.add_argument("--outline", type=Path, default=None)
    parser.add_argument("--target", type=int, default=None)
    args = parser.parse_args()

    body = args.draft.read_text(encoding="utf-8")
    task_text = _read_optional(args.task)
    outline_text = _read_optional(args.outline)
    task_spec = _task_spec(task_text)
    outline_target = _outline_target(outline_text)

    if args.target is not None:
        result = evaluate_wordcount(body, args.target)
        result["source"] = "explicit_arg"
        if outline_target is not None and outline_target != args.target:
            result["status"] = "target_conflict"
            result["invalid_reason"] = "EXPLICIT_TARGET_DIFFERS_FROM_OUTLINE_TARGET"
            result["outline_target"] = outline_target
    elif task_spec and task_spec["kind"] == "range":
        result = _range_result(body, task_spec, outline_target)
    elif task_spec and task_spec["kind"] == "target":
        target = int(task_spec["target"])
        result = evaluate_wordcount(body, target)
        result["source"] = "task"
        if outline_target is not None and outline_target != target:
            result["status"] = "target_conflict"
            result["invalid_reason"] = "TASK_TARGET_DIFFERS_FROM_OUTLINE_TARGET"
            result["outline_target"] = outline_target
    elif outline_target is not None:
        result = evaluate_wordcount(body, outline_target)
        result["source"] = "outline"
    else:
        result = {
            "schema": "story-wordcount-target-resolution/v2",
            "metric": "visible_chars_v1",
            "source": None,
            "target": None,
            "actual": count_visible_chars(body),
            "status": "target_unresolved",
            "invalid_reason": "NO_PARSEABLE_TARGET_IN_ARG_TASK_OR_OUTLINE",
        }

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
