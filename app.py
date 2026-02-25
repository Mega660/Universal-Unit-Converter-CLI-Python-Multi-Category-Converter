#!/usr/bin/env python3
"""
Unit Converter CLI Application
──────────────────────────────
Supports 10 categories: Length, Mass, Time, Speed, Area, Volume,
Data, Energy, Pressure, and Temperature.  Includes conversion history.

Usage:
    python app.py
"""

from __future__ import annotations

import sys
from typing import Dict, List

from converter import convert, smart_format, ConversionError
from history import History, HistoryEntry
from units import ALL_CATEGORIES, LINEAR_CATEGORIES, TEMPERATURE


# ── ANSI helpers ────────────────────────────────────────────────────────

def _c(code: str, t: str) -> str:
    return f"\033[{code}m{t}\033[0m"

def bold(t: str) -> str:    return _c("1", t)
def dim(t: str) -> str:     return _c("2", t)
def green(t: str) -> str:   return _c("32", t)
def yellow(t: str) -> str:  return _c("33", t)

def cyan(t: str) -> str:    return _c("36", t)
def red(t: str) -> str:     return _c("31", t)
def magenta(t: str) -> str: return _c("35", t)


# ── Display helpers ─────────────────────────────────────────────────────

def banner() -> None:
    print(bold(cyan("\n╔══════════════════════════════════════════╗")))
    print(bold(cyan("║         Universal Unit Converter         ║")))
    print(bold(cyan("╚══════════════════════════════════════════╝")))


def show_categories() -> None:
    print(f"\n  {bold('Categories:')}")
    for i, cat in enumerate(ALL_CATEGORIES, 1):
        print(f"    {cyan(str(i)):>6s}. {cat}")
    print()


def show_units(category: str) -> None:
    if category == "Temperature":
        units = sorted(TEMPERATURE.keys())
    else:
        units = sorted(LINEAR_CATEGORIES[category].keys())
    print(f"\n  {bold(f'Units in {category}:')}")
    cols = 3
    for i in range(0, len(units), cols):
        row = units[i:i + cols]
        print("    " + "".join(f"{dim(str(i + j + 1))+'.':<5s} {u:<24s}" for j, u in enumerate(row)))
    print()
    return units


def show_history(history: History) -> None:
    entries = history.entries
    if not entries:
        print(dim("\n  No conversion history yet.\n"))
        return
    print(f"\n  {bold('Recent Conversions:')}")
    print(f"  {'─' * 70}")
    for e in entries[-15:]:
        print(
            f"  {dim(e.timestamp)}  "
            f"{smart_format(e.value)} {e.from_unit} → "
            f"{green(smart_format(e.result))} {e.to_unit}  "
            f"{dim(f'[{e.category}]')}"
        )
    print()


def prompt(text: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"  {text}{suffix}: ").strip()
    return raw or default


# ── Interactive loop ────────────────────────────────────────────────────

def pick_category() -> str | None:
    show_categories()
    raw = prompt("Select category (number or name, 'q' to quit)")
    if raw.lower() in ("q", "quit"):
        return None
    # by number
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(ALL_CATEGORIES):
            return ALL_CATEGORIES[idx]
    except ValueError:
        pass
    # by name
    for cat in ALL_CATEGORIES:
        if cat.lower() == raw.lower():
            return cat
    print(red(f"  Unknown category: '{raw}'"))
    return "__retry__"


def pick_unit(category: str, label: str) -> str | None:
    units = show_units(category)
    raw = prompt(f"{label} unit (number or name)")
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(units):
            return units[idx]
    except ValueError:
        pass
    if raw.lower() in [u.lower() for u in units]:
        return raw.lower()
    print(red(f"  Unknown unit: '{raw}'"))
    return None


def main() -> None:
    history = History()

    banner()
    print(dim("  Type 'q' to quit, 'h' for history, 'c' to clear history.\n"))

    while True:
        cat = pick_category()
        if cat is None:
            print(cyan("\n  Goodbye!\n"))
            break
        if cat == "__retry__":
            continue

        from_unit = pick_unit(cat, "From")
        if not from_unit:
            continue
        to_unit = pick_unit(cat, "To")
        if not to_unit:
            continue

        raw_value = prompt("Value to convert")

        # special commands
        if raw_value.lower() in ("q", "quit"):
            print(cyan("\n  Goodbye!\n"))
            break
        if raw_value.lower() == "h":
            show_history(history)
            continue
        if raw_value.lower() == "c":
            history.clear()
            print(green("  History cleared."))
            continue

        try:
            value = float(raw_value)
        except ValueError:
            print(red(f"  '{raw_value}' is not a valid number."))
            continue

        try:
            result = convert(value, from_unit, to_unit, cat)
        except ConversionError as e:
            print(red(f"  Error: {e}"))
            continue

        formatted = smart_format(result)
        print(
            f"\n  {bold(smart_format(value))} {from_unit}"
            f"  =  {bold(green(formatted))} {to_unit}\n"
        )

        history.add(HistoryEntry.create(cat, value, from_unit, to_unit, result))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(cyan("\n  Goodbye!\n"))
