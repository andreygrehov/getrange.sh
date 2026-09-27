#!/usr/bin/env python3
"""Checks the site says what the benchmarks measured and keeps its design.

Run: python3 check.py   (exits non-zero and lists every problem it finds)
"""
import re
import sys
from pathlib import Path

here = Path(__file__).parent
page = (here / "index.html").read_text(encoding="utf-8")
css = (here / "style.css").read_text(encoding="utf-8")
problems = []

for want in [
    "Use a remote environment before downloading it.",
    "range shell", "range build", "range publish", "range run",  # the whole surface
    "go1.23-arm64.range", "go1.23-amd64.range",  # the public demos, one per arch
    "9.03 s", "6.47 s", "2.80 s",  # every lane of the race
    "613 MB", "2.38 GB",  # the storage claim
    "7.59 s", "101 MB",  # eStargz with prioritized files, same host
    "1172.0 s", "100.1 s",  # the churn comparison against re-baking
    "Time to shell",  # the laptop benchmark pane
    'href="#install"',  # the page must be actionable
]:
    if want not in page:
        problems.append(f"page is missing {want!r}")

# The race must stay honest: a claimed speedup has to match the times shown.
for mult, secs in [("1.4", 6.47), ("3.2", 2.80)]:
    expected = 9.03 / secs
    if abs(float(mult) - expected) / expected > 0.02:
        problems.append(f"lane claims {mult}x but 9.03/{secs:.2f} = {expected:.1f}x")
    if mult + "x" not in page:
        problems.append(f"race is missing the {mult}x lane")

# Design tells the site is deliberately kept free of.
for banned in ["border-radius", "text-transform:uppercase", "linear-gradient", "backdrop-filter"]:
    if banned in page or banned in css:
        problems.append(f"site reintroduced {banned!r}")

# Shadows are allowed, but only the hard offset kind: x/y offset, then 0 blur.
for shadow in re.findall(r"box-shadow:([^;}\"]+)", page + css):
    if not re.match(r"^\s*-?\d+px\s+-?\d+px\s+0\s", shadow):
        problems.append(f"box-shadow {shadow!r} is blurred; the design uses hard offsets only")

for p in problems:
    print(p)
print("ok" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
