"""Publish only approved case exercises linked to approved course units."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from case_render import IDENTIFIER, render_document, require_text, validate_content
from unit_pages import approved_units

REVIEW_FIELDS = ("reviewed_by", "reviewer_role", "review_note", "reviewed_at", "reviewed_commit")


def approved_cases(cases_payload: dict, course: dict) -> list[dict]:
    """Validate the publication boundary without mutating the reviewed payload."""
    if not isinstance(cases_payload, dict) or cases_payload.get("review_status") != "approved":
        raise ValueError("Published cases require top-level review_status='approved'")
    require_text(cases_payload, "title", "cases_payload")
    entries = cases_payload.get("cases")
    if not isinstance(entries, list):
        raise ValueError("cases_payload.cases must be a list")
    units = {unit["id"] for _, unit in approved_units(course)}
    selected = []
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Case entries must be objects")
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            raise ValueError("Case IDs must use letters, digits, underscores and hyphens")
        if identifier in seen:
            raise ValueError(f"Duplicate case id: {identifier}")
        seen.add(identifier)
        if entry.get("review_status") != "approved":
            continue
        for field in REVIEW_FIELDS:
            require_text(entry, field, f"case {identifier}")
        unit_id = entry.get("unit_id")
        if not isinstance(unit_id, str) or unit_id not in units:
            raise ValueError(f"Approved case {identifier} references a missing or unapproved unit")
        selected.append(entry)
    if selected:
        validate_content({"title": cases_payload["title"], "cases": selected})
    return selected


def write_case_pages(cases_payload: dict, course: dict, outdir: Path) -> list[Path]:
    """Write practice/index.html after validating every publication dependency.

    Draft entries never appear in HTML. Empty approved sets remove this generator's
    prior output, so a repeated build cannot leave withdrawn exercises published.
    """
    selected = approved_cases(cases_payload, course)
    target = Path(outdir) / "practice" / "index.html"
    if not selected:
        target.unlink(missing_ok=True)
        return []
    unit_links = {
        case["id"]: (
            '<p class="unit-link">'
            f'<a href="../?tab=course#{quote(case["unit_id"], safe="")}">返回相關課程單元</a>'
            f' · <a href="../units/{quote(case["unit_id"], safe="")}/">閱讀單元講義</a></p>'
        )
        for case in selected
    }
    html = render_document(
        {"title": cases_payload["title"], "cases": selected}, draft=False, unit_links=unit_links
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    return [target]
