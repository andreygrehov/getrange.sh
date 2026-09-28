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
    "range shell", "range run", "python:3.12", "--mount hf://",  # the whole pitch
    "gemma-3-270m-it-Q4_K_M.gguf", "moonshotai/Kimi-K2-Instruct",  # the two demos
    "18.27 s", "15.46 s", "6.73 s", "4.25 s",  # every lane of the chat race
    "2.8 s", "15.8 s", "9.5 MB", "1.03 TB",  # README and bench figures
    "Rayleigh scattering",  # the answer the demo shows
    'href="#install"', 'href="#about"', "me.png",  # actionable, and says who made it
]:
    if want not in page:
        problems.append(f"page is missing {want!r}")

# The race must stay honest: each speedup has to match the times shown.
docker = 18.27
for mult, secs in [("1.2", 15.46), ("2.7", 6.73), ("4.3", 4.25)]:
    expected = docker / secs
    if abs(float(mult) - expected) / expected > 0.05:
        problems.append(f"lane claims {mult}x but {docker}/{secs:.2f} = {expected:.2f}x")
    if mult + "x" not in page:
        problems.append(f"race is missing the {mult}x lane")

# The old demo and old panes are gone for good.
for gone in ["perf.log", "churn.log", "install.sh"]:
    if gone in page:
        problems.append(f"page still mentions {gone!r}")

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
