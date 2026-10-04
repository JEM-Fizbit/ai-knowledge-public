#!/usr/bin/env python3
"""Strip a markdown script to speakable plain text, then LINT what is left.

The division of labour matters. This script does only the mechanical half —
dropping an explicitly marked non-spoken header, removing markdown syntax, normalising dashes.
It deliberately does NOT convert figures, currency or initialisms into words:
"£3.8m" -> "three point eight million pounds" is a judgement call (is it
"three point eight" or "three point eight million"? is "ARR" spoken or spelled?)
and a script that guesses silently would corrupt Mode A, where the wording is
the artefact and must not change.

So instead it REPORTS everything that will mangle in speech, with line numbers,
and exits 1 under --strict. Fix a temporary copy or oral script, re-run, then render. That
gates rendering on a successful preparation result.

Usage:
    prepare_text.py IN.md [-o OUT.txt] [--strict] [--quiet]

    --strict      exit 1 if the lint finds anything.

Lint findings go to stderr so stdout stays pipeable.
"""

import argparse
import re
import sys
from pathlib import Path

# Mechanical, meaning-preserving substitutions only.
STRIP = [
    (re.compile(r"^\s{0,3}#{1,6}\s*", re.M), ""),          # heading markers
    (re.compile(r"^\s{0,3}>\s?", re.M), ""),               # blockquote markers
    (re.compile(r"^\s*[-*+]\s+", re.M), ""),               # bullet glyphs
    (re.compile(r"^\s*\d+[.)]\s+", re.M), ""),             # ordered list markers
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), ""),             # images: drop entirely
    (re.compile(r"\[([^\]]+)\]\([^)]*\)"), r"\1"),         # links: keep the text
    (re.compile(r"\*\*([^*]+)\*\*"), r"\1"),               # bold
    (re.compile(r"(?<!\w)_{2}([^_]+)_{2}(?!\w)"), r"\1"),  # bold (underscore)
    (re.compile(r"(?<!\w)\*([^*\n]+)\*(?!\w)"), r"\1"),    # italic
    (re.compile(r"(?<!\w)_([^_\n]+)_(?!\w)"), r"\1"),      # italic (underscore)
    (re.compile(r"`([^`]+)`"), r"\1"),                     # inline code
    (re.compile("[\\u2014\\u2013]"), " - "),                          # dashes a synth mangles
    (re.compile("[\u201c\u201d]"), '"'),
    (re.compile("[\u2018\u2019]"), "'"),
]

# What survives stripping but still fails in speech. Each is a judgement call
# for a human or the model, never for this script.
LINT = [
    (re.compile(r"[£$€¥]"), "currency symbol - write the amount in words"),
    (re.compile(r"%"), "percent sign - write 'percent'"),
    (re.compile(r"&"), "ampersand - write 'and'"),
    (re.compile(r"\d"), "digits - write numbers, dates and times as words"),
    (re.compile(r"(?<![A-Za-z])[A-Z]{2,6}(?![A-Za-z])"),
     "unspaced initialism - space it (A B C) or it is read as a word"),
    (re.compile(r"\|"), "table pipe - convert the table to a sentence or drop it"),
    (re.compile(r"https?://"), "bare URL - drop it or name the destination"),
]


def split_header(text: str) -> str:
    """Remove only the explicit oral-script header, never a normal divider."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "<!-- audio-brief: non-spoken header -->":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                return "\n".join(lines[i + 1:])
        raise ValueError("marked non-spoken header needs a closing ---")
    return text


def strip_markdown(text: str) -> str:
    # Fenced code blocks are never speakable; remove before anything else.
    text = re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)
    for pat, rep in STRIP:
        text = pat.sub(rep, text)
    text = re.sub(r"^\s*---\s*$", "", text, flags=re.M)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return "\n".join(l.strip() for l in text.splitlines()).strip()


def lint(text: str):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for pat, why in LINT:
            m = pat.search(line)
            if m:
                out.append((n, m.group(0).strip(), why, line.strip()[:70]))
                break  # one finding per line is enough to send it back
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    body = strip_markdown(split_header(a.infile.read_text(encoding="utf-8")))
    findings = lint(body)
    if not body or (findings and a.strict):
        print("empty text or speech lint failed; output was not written", file=sys.stderr)
        for n, hit, why, ctx in findings[:40]:
            print(f"line {n}: {hit!r}: {why}", file=sys.stderr)
        return 1

    if a.out:
        a.out.write_text(body + "\n", encoding="utf-8")
    else:
        sys.stdout.write(body + "\n")

    words = len(body.split())
    if not a.quiet:
        print(f"{words} words, ~{words / 155:.1f} min at 155 wpm", file=sys.stderr)

    findings = lint(body)
    if findings and not a.quiet:
        print(f"\n{len(findings)} line(s) will mangle in speech:", file=sys.stderr)
        for n, hit, why, ctx in findings[:40]:
            print(f"  line {n:>4}  {hit!r:<12} {why}\n            {ctx}", file=sys.stderr)
        if len(findings) > 40:
            print(f"  ... and {len(findings) - 40} more", file=sys.stderr)
    return 1 if (findings and a.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
