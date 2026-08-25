#!/usr/bin/env python3
"""Initialize a non-destructive scientific-figure run directory."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def parse_subplots(value: str) -> list[str]:
    items = [item.strip() for item in value.split(",") if item.strip()]
    if not items:
        raise argparse.ArgumentTypeError("at least one subplot ID is required")
    if len(set(items)) != len(items):
        raise argparse.ArgumentTypeError("subplot IDs must be unique")
    for item in items:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,31}", item):
            raise argparse.ArgumentTypeError(
                f"invalid subplot ID {item!r}; use letters, digits, hyphens, or underscores"
            )
    return items


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def write_new_json(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a traceable run directory for an editable scientific figure."
    )
    parser.add_argument("run_dir", type=Path, help="new or empty run directory")
    parser.add_argument("--name", required=True, help="stable figure name")
    parser.add_argument(
        "--mode",
        choices=("new", "reconstruction", "revision"),
        default="new",
    )
    parser.add_argument("--width-mm", required=True, type=positive_float)
    parser.add_argument("--height-mm", required=True, type=positive_float)
    parser.add_argument("--subplots", default="A", type=parse_subplots)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_dir = args.run_dir.expanduser().resolve()

    if run_dir.exists() and any(run_dir.iterdir()):
        print(f"error: run directory is not empty: {run_dir}", file=sys.stderr)
        return 2

    directories = (
        "input",
        "planning",
        "assets/imagegen",
        "assets/source-derived",
        "build",
        "qa",
        "final",
    )
    for relative in directories:
        (run_dir / relative).mkdir(parents=True, exist_ok=True)

    figure_spec = {
        "schema_version": 1,
        "figure": {
            "name": args.name,
            "mode": args.mode,
            "width_mm": args.width_mm,
            "height_mm": args.height_mm,
            "final_formats": ["pptx", "pdf"],
        },
        "sources": {"manuscript": [], "caption": [], "figures": []},
        "visual_system": {
            "sans_font": None,
            "math_font": None,
            "minimum_text_pt": None,
            "palette": {},
            "line_weights_pt": {},
        },
        "subplots": [
            {
                "id": subplot,
                "purpose": "",
                "reading_order": index + 1,
                "status": "planned",
                "frozen": False,
            }
            for index, subplot in enumerate(args.subplots)
        ],
        "constraints": [],
        "uncertainties": [],
    }
    layout_blueprint = {
        "schema_version": 1,
        "coordinate_system": "millimetres from slide top-left",
        "slide": {"width_mm": args.width_mm, "height_mm": args.height_mm},
        "objects": [
            {
                "id": f"subplot-{subplot}",
                "type": "subplot",
                "subplot": subplot,
                "bounds_mm": {"x": None, "y": None, "w": None, "h": None},
                "aspect_locked": False,
                "status": "planned",
            }
            for subplot in args.subplots
        ],
    }
    asset_manifest = {"schema_version": 1, "assets": []}

    write_new_json(run_dir / "planning/figure-spec.json", figure_spec)
    write_new_json(run_dir / "planning/layout-blueprint.json", layout_blueprint)
    write_new_json(run_dir / "assets/asset-manifest.json", asset_manifest)

    template = Path(__file__).resolve().parent.parent / "assets/templates/qa-report.md"
    if template.exists():
        shutil.copyfile(template, run_dir / "qa/qa-report.md")

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
