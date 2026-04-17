#!/usr/bin/env python3
"""
ai_tell_scan.py — quick programmatic scan of a draft for AI-tell patterns.

Usage:
    python3 ai_tell_scan.py <path-to-markdown-or-text-file>

Outputs a report of patterns the humanize-prose skill flags, along with
paragraph-balance statistics and sentence-length distribution.

The scan is non-destructive: it only reads the file and prints findings.
Authorial judgment is always required before acting on any flag.
"""

from __future__ import annotations
import argparse
import pathlib
import re
import statistics
import sys


AI_TELL_PHRASES = [
    r"\bfurthermore\b",
    r"\bmoreover\b",
    r"\bthus\b",
    r"\bindeed\b",
    r"\bhence\b",
    r"\bit is important to note\b",
    r"\bin conclusion\b",
    r"\bas will be shown\b",
    r"\bas will be demonstrated\b",
    r"\bin this (paper|essay)\b",
    r"\bthe following section\b",
    r"\bby and large\b",
    r"\bin a nutshell\b",
    r"\bfirst and foremost\b",
]

WEAK_ANALYTIC_VERBS = [
    r"\billustrat(es|ed|ing)\b",
    r"\bunderscor(es|ed|ing)\b",
    r"\bdemonstrat(es|ed|ing)\b",
    r"\bhighlight(s|ed|ing)\b",
    r"\bserv(es|ed|ing) (as|to)\b",
    r"\bemphasi[sz](es|ed|ing)\b",
]


def wc(s: str) -> int:
    return len(re.findall(r"\b[\w'\-]+\b", s))


def scan(text: str) -> dict:
    # Strip a leading markdown title and a trailing "## Bibliography" block
    parts = re.split(r"\n##\s+Bibliography", text, maxsplit=1)
    body = parts[0]
    body = re.sub(r"^#\s+.*\n", "", body, count=1)
    body = body.strip()

    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    para_counts = [wc(p) for p in paras]

    em_dash = body.count("\u2014")
    en_dash = body.count("\u2013")
    semicolons = body.count(";")

    phrase_hits = {}
    for pattern in AI_TELL_PHRASES:
        hits = re.findall(pattern, body, flags=re.I)
        if hits:
            phrase_hits[pattern] = len(hits)

    verb_hits = {}
    for pattern in WEAK_ANALYTIC_VERBS:
        hits = re.findall(pattern, body, flags=re.I)
        if hits:
            verb_hits[pattern] = len(hits)

    # Causal sentence-fusion pattern: detect ", because " when the left half is a full clause
    because_fusions = re.findall(r"[.!?]\s+[^.!?]{20,}?,\s+because\s+", body, flags=re.I)

    # Neat tricolons: three comma-separated gerund or adjective phrases ending with a coordinating "and"
    tricolon_candidates = re.findall(
        r"\b\w+ing,\s+\w+ing,\s+and\s+\w+ing\b|\b\w+ly,\s+\w+ly,\s+and\s+\w+ly\b",
        body,
    )

    # Sentence lengths
    sentences = re.split(r"(?<=[\.\?\!])\s+(?=[A-Z\*\"\(])", body.replace("\n", " "))
    sent_lens = [wc(s) for s in sentences if wc(s) > 0]

    # Direct quotes (>=15 chars inside double quotes)
    direct_quotes = re.findall(r'"([^"]{15,})"', body)

    # Proper nouns per paragraph (rough: capitalized multi-word sequences not at sentence start)
    proper_noun_counts = []
    for p in paras:
        # Count capitalized words not preceded by a sentence-ending punctuation boundary
        tokens = re.findall(r"\b[A-Z][a-zāēīōū]+(?:\s+[A-Z][a-zāēīōū]+){0,2}\b", p)
        proper_noun_counts.append(len(tokens))

    return {
        "paragraph_count": len(paras),
        "paragraph_word_counts": para_counts,
        "body_word_count": sum(para_counts),
        "em_dash": em_dash,
        "en_dash": en_dash,
        "semicolons": semicolons,
        "phrase_hits": phrase_hits,
        "weak_verb_hits": verb_hits,
        "causal_because_fusions": len(because_fusions),
        "neat_tricolons": len(tricolon_candidates),
        "tricolon_examples": tricolon_candidates[:3],
        "sentence_count": len(sent_lens),
        "sentence_lengths": sent_lens,
        "direct_quotes": len(direct_quotes),
        "proper_nouns_per_paragraph": proper_noun_counts,
    }


def format_report(result: dict) -> str:
    lines = []
    lines.append("=" * 62)
    lines.append("AI-TELL SCAN REPORT")
    lines.append("=" * 62)

    lines.append(f"\nBody word count: {result['body_word_count']}")
    lines.append(f"Paragraphs: {result['paragraph_count']}")
    pc = result["paragraph_word_counts"]
    lines.append(f"Paragraph word counts: {pc}")
    if pc:
        ratio = max(pc) / max(1, min(pc))
        lines.append(f"  Max-to-min paragraph ratio: {ratio:.2f}x "
                     f"{'(flag: >2.5x is unbalanced)' if ratio > 2.5 else '(OK)'}")

    pn = result["proper_nouns_per_paragraph"]
    lines.append(f"\nProper nouns per paragraph: {pn}")
    zero_ev = [i + 1 for i, n in enumerate(pn) if n == 0]
    if zero_ev:
        lines.append(f"  Paragraphs with zero proper nouns: {zero_ev} (consider adding evidence)")

    lines.append(f"\nDirect quotations (>=15 chars in double quotes): {result['direct_quotes']}")

    lines.append("\nAI-TELL PUNCTUATION (target: all zero)")
    lines.append(f"  Em-dashes (—): {result['em_dash']}")
    lines.append(f"  En-dashes (–): {result['en_dash']}  [OK in page ranges]")
    lines.append(f"  Semicolons (;): {result['semicolons']}")

    lines.append("\nAI-TELL PHRASES")
    if result["phrase_hits"]:
        for pat, n in result["phrase_hits"].items():
            lines.append(f"  {pat}: {n}")
    else:
        lines.append("  (none)")

    lines.append("\nWEAK ANALYTIC VERBS (consider plainer substitutes)")
    if result["weak_verb_hits"]:
        for pat, n in result["weak_verb_hits"].items():
            lines.append(f"  {pat}: {n}")
    else:
        lines.append("  (none)")

    lines.append(f"\nCausal sentence-fusion ('X, because Y'): {result['causal_because_fusions']}")
    lines.append(f"Neat tricolons (three -ing or -ly phrases joined by 'and'): {result['neat_tricolons']}")
    for ex in result["tricolon_examples"]:
        lines.append(f"    - {ex}")

    sl = result["sentence_lengths"]
    if sl:
        lines.append(f"\nSentence-length distribution ({len(sl)} sentences)")
        lines.append(f"  min={min(sl)}  median={statistics.median(sl):.1f}  "
                     f"max={max(sl)}  stdev={statistics.stdev(sl) if len(sl) > 1 else 0:.1f}")
        short = sum(1 for n in sl if n <= 12)
        medium = sum(1 for n in sl if 13 <= n <= 25)
        longs = sum(1 for n in sl if n > 25)
        total = max(1, len(sl))
        lines.append(f"  short (<=12): {short} ({100*short/total:.0f}%)  "
                     f"medium (13-25): {medium} ({100*medium/total:.0f}%)  "
                     f"long (>25): {longs} ({100*longs/total:.0f}%)")
        if short < max(3, total // 6):
            lines.append("  FLAG: too few short sentences. Burstiness is low. "
                         "Consider splitting a long sentence into a short + long pair.")

    lines.append("\n" + "=" * 62)
    lines.append("READINESS SUMMARY")
    lines.append("=" * 62)

    flags = 0
    if result["em_dash"] > 0: flags += 1
    if result["semicolons"] > 0: flags += 1
    if result["phrase_hits"]: flags += 1
    if result["causal_because_fusions"] > 0: flags += 1
    if result["neat_tricolons"] > 0: flags += 1
    pc = result["paragraph_word_counts"]
    if pc and max(pc) / max(1, min(pc)) > 2.5: flags += 1
    if any(n == 0 for n in result["proper_nouns_per_paragraph"]): flags += 1

    if flags == 0:
        lines.append("All programmatic checks passed. Draft is ready to submit to the detector.")
    else:
        lines.append(f"{flags} flag category(ies) above. Address them before the next detector run.")
        lines.append("Priority order: punctuation > AI-tell phrases > paragraph balance > "
                     "evidence density > sentence-length distribution.")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a draft for AI-tell patterns.")
    parser.add_argument("path", help="Path to a markdown or plain-text draft")
    args = parser.parse_args()

    p = pathlib.Path(args.path)
    if not p.exists():
        print(f"File not found: {p}", file=sys.stderr)
        return 1

    text = p.read_text(encoding="utf-8")
    result = scan(text)
    print(format_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
