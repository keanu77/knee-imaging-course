"""Validate journal-hosted diagnostic clips separately from YouTube lectures."""

from __future__ import annotations

import math
import re
from urllib.parse import urlsplit

MEDIA_HOSTS = {"cdn.ncbi.nlm.nih.gov", "www.e-jyms.org"}


def media_url(value: object) -> bool:
    if not isinstance(value, str) or any(c.isspace() or ord(c) < 32 for c in value):
        return False
    try:
        url = urlsplit(value)
        return (
            url.scheme == "https"
            and url.hostname in MEDIA_HOSTS
            and not url.username
            and not url.password
            and url.port is None
            and url.path.endswith(".mp4")
            and not url.query
            and not url.fragment
        )
    except ValueError:
        return False


def approved_clips(unit: dict, references: dict) -> list[dict]:
    """Fail closed on malformed approved clips; drafts never enter public output."""
    result, seen = [], set()
    for clip in unit.get("journal_clips", []):
        if clip.get("review_status") != "approved":
            continue
        label = f"{unit.get('id')}/{clip.get('id')}"
        ident = clip.get("id", "")
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9-]+", ident) or ident in seen:
            raise ValueError(f"{label}: invalid or duplicate journal clip id")
        seen.add(ident)
        if not media_url(clip.get("url")):
            raise ValueError(f"{label}: invalid journal media URL")
        for field in (
            "title",
            "authors",
            "journal",
            "published_at",
            "source_url",
            "case_context",
            "scope_note",
            "caption_note",
            "license",
            "last_verified_at",
            "verification_note",
            "review_note",
            "reviewed_payload_sha256",
        ):
            if not isinstance(clip.get(field), str) or not clip[field].strip():
                raise ValueError(f"{label}: missing {field}")
        source = urlsplit(clip["source_url"])
        if source.scheme != "https" or not source.hostname or source.username or source.password:
            raise ValueError(f"{label}: invalid article URL")
        if clip.get("contains_intervention") is not False:
            raise ValueError(f"{label}: journal clips must be diagnostic-only in their entirety")
        duration = clip.get("duration_seconds")
        if (
            isinstance(duration, bool)
            or not isinstance(duration, (int, float))
            or not math.isfinite(duration)
            or duration <= 0
        ):
            raise ValueError(f"{label}: invalid duration")
        if clip.get("reference_id") not in references:
            raise ValueError(f"{label}: unknown reference")
        observations = clip.get("observations")
        if not isinstance(observations, list) or not observations or any(
            not isinstance(x, str) or not x.strip() for x in observations
        ):
            raise ValueError(f"{label}: missing observation notes")
        result.append(clip)
    return result
