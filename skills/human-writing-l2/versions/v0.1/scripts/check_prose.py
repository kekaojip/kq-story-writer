#!/usr/bin/env python3
"""Human Writing L2 diagnostics for Chinese web fiction.

Read-only heuristic scanner. It never rewrites prose and never estimates
whether text is "AI" or "human".
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

SENTENCE_RE = re.compile(r"[^。！？!?\n]+[。！？!?]?")
PARA_SPLIT = re.compile(r"\n\s*\n")
PUNCT = re.compile(r"[\s，。！？!?；;：:、,.…—\-\"“”‘’（）()【】\[\]<>《》]+")

CLOSURE_HINTS = (
    "所以", "也就是说", "这意味着", "总之", "归根结底", "换句话说",
    "至少有一点可以确定", "这就是", "他终于明白", "他忽然意识到",
)

ROAD_SIGNS = (
    "值得注意的是", "需要指出的是", "从某种意义上说", "还有一层",
    "更微妙的是", "更重要的是",
)

PIVOTS = (
    re.compile(r"(?:并)?不是[^。！？\n]{0,80}而是"),
    re.compile(r"并非[^。！？\n]{0,80}而是"),
    re.compile(r"看似[^。！？\n]{0,80}(?:其实|实际|实则)"),
    re.compile(r"真正[^，。！？\n]{0,18}的(?:，)?是"),
    re.compile(r"[^，。！？\n]{1,14}不重要，(?:重要|要紧)的是"),
    re.compile(r"(?:总|一直|曾|都)?以为[^！？\n]{2,60}?(?:其实|才发现|才明白|才知道|后来才)"),
)

CONSTRAINT_TOMBSTONES = (
    "没有继续试", "没继续试", "没有再试", "并没有升级", "没有升级",
    "奖励没有增加", "奖励没增加", "期限没有变化", "期限没变",
    "问题依旧存在", "问题仍然存在", "旧问题仍在",
)


def visible_len(text: str) -> int:
    return len(PUNCT.sub("", text))


def cv(values: list[int]) -> float | None:
    if len(values) < 2:
        return None
    mean = statistics.mean(values)
    if not mean:
        return None
    return statistics.pstdev(values) / mean


def max_run(flags: list[bool]) -> int:
    best = cur = 0
    for flag in flags:
        cur = cur + 1 if flag else 0
        best = max(best, cur)
    return best


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def analyze(text: str) -> dict:
    paragraphs = [p.strip() for p in PARA_SPLIT.split(text) if p.strip() and not p.lstrip().startswith("#")]
    sentences = [m.group().strip() for m in SENTENCE_RE.finditer(text) if visible_len(m.group()) >= 2]

    sentence_lengths = [visible_len(s) for s in sentences]
    paragraph_lengths = [visible_len(p) for p in paragraphs]
    short_sentence_flags = [n <= 8 for n in sentence_lengths]
    single_sentence_flags = [len(re.findall(r"[。！？!?]", p)) <= 1 for p in paragraphs]

    findings: list[dict] = []

    for phrase in CLOSURE_HINTS:
        for m in re.finditer(re.escape(phrase), text):
            findings.append({"line": line_no(text, m.start()), "signal": "closure_hint", "sample": phrase})

    for phrase in ROAD_SIGNS:
        for m in re.finditer(re.escape(phrase), text):
            findings.append({"line": line_no(text, m.start()), "signal": "model_road_sign", "sample": phrase})

    for pattern in PIVOTS:
        for m in pattern.finditer(text):
            findings.append({"line": line_no(text, m.start()), "signal": "pivot_pattern", "sample": m.group()[:60]})

    for phrase in CONSTRAINT_TOMBSTONES:
        for m in re.finditer(re.escape(phrase), text):
            findings.append({"line": line_no(text, m.start()), "signal": "constraint_tombstone", "sample": phrase})

    metrics = {
        "paragraph_count": len(paragraphs),
        "sentence_count": len(sentences),
        "mean_sentence_chars": round(statistics.mean(sentence_lengths), 2) if sentence_lengths else 0,
        "sentence_length_cv": round(cv(sentence_lengths), 3) if cv(sentence_lengths) is not None else None,
        "paragraph_length_cv": round(cv(paragraph_lengths), 3) if cv(paragraph_lengths) is not None else None,
        "short_sentence_ratio": round(sum(short_sentence_flags) / len(short_sentence_flags), 3) if short_sentence_flags else 0,
        "max_consecutive_short_sentences": max_run(short_sentence_flags),
        "single_sentence_paragraph_ratio": round(sum(single_sentence_flags) / len(single_sentence_flags), 3) if single_sentence_flags else 0,
        "max_consecutive_single_sentence_paragraphs": max_run(single_sentence_flags),
    }

    warnings: list[str] = []
    if len(sentence_lengths) >= 20 and metrics["sentence_length_cv"] is not None and metrics["sentence_length_cv"] < 0.35:
        warnings.append("sentence_lengths_are_low_variance")
    if len(paragraph_lengths) >= 12 and metrics["paragraph_length_cv"] is not None and metrics["paragraph_length_cv"] < 0.45:
        warnings.append("paragraph_lengths_are_low_variance")
    if metrics["max_consecutive_short_sentences"] >= 5:
        warnings.append("long_short_sentence_stack")
    if metrics["max_consecutive_single_sentence_paragraphs"] >= 6:
        warnings.append("long_single_sentence_paragraph_stack")

    return {
        "metrics": metrics,
        "warnings": warnings,
        "findings": findings,
        "note": "Heuristics only. Flags require contextual review. Do not optimize prose to clear every flag.",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Read-only L2 prose diagnostics")
    ap.add_argument("file", help="UTF-8 prose file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    result = analyze(text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("Human Writing L2 diagnostic")
    for key, value in result["metrics"].items():
        print(f"{key}: {value}")
    print("warnings:")
    for item in result["warnings"] or ["none"]:
        print(f"- {item}")
    print("findings:")
    for item in result["findings"][:50]:
        print(f"- line {item['line']}: {item['signal']} :: {item['sample']}")
    print(result["note"])


if __name__ == "__main__":
    main()
