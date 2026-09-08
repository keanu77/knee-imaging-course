#!/usr/bin/env python3
"""Render draft case exercises as an isolated, local review page (stdlib only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "build"))

from case_render import DRAFT_NOTICE, render_document, validate_content

ROOT = Path(__file__).resolve().parents[1]
NOTICE = DRAFT_NOTICE


def validate(payload: dict) -> None:
    if not isinstance(payload, dict) or payload.get("review_status") != "draft":
        raise ValueError("This review-only renderer accepts review_status='draft' exclusively")
    validate_content(payload)


def render(payload: dict) -> str:
    validate(payload)
    return render_document(payload, draft=True)


def build(input_path: Path, output_dir: Path) -> Path:
    input_path, output_dir = Path(input_path), Path(output_dir)
    resolved = output_dir.resolve()
    if any(
        resolved == ROOT / folder or ROOT / folder in resolved.parents
        for folder in ("dist", "public")
    ):
        raise ValueError("Review drafts must not be written into public website output")
    html = render(json.loads(input_path.read_text(encoding="utf-8")))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "index.html"
    target.write_text(html, encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        target = build(args.input, args.output_dir)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Case review build failed: {error}\n")
    print(target)


if __name__ == "__main__":
    main()
