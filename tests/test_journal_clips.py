"""Journal supplements cannot bypass curation, source, or diagnostic boundaries."""

from __future__ import annotations

import copy
import importlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/build"))

approved_clips = importlib.import_module("journal_clips").approved_clips
media_url = importlib.import_module("journal_clips").media_url
render_journal_clips = importlib.import_module("unit_pages").render_journal_clips


class JournalClipsTest(unittest.TestCase):
    def setUp(self):
        package = json.loads(
            (ROOT / "course/research/2026-09-12-saphenous-candidate.json").read_text()
        )
        self.unit = package["unit"]
        self.references = package["reference_catalog"]
        self.clip = self.unit["journal_clips"][0]
        self.clip.update(
            review_status="approved", review_note="curation", reviewed_payload_sha256="a" * 64
        )

    def test_drafts_do_not_leak_into_public_payload_or_static_page(self):
        draft = self.unit["journal_clips"][1]
        draft["title"] = "PRIVATE_DRAFT_MARKER"
        result = approved_clips(self.unit, self.references)
        self.assertEqual([c["id"] for c in result], [self.clip["id"]])
        self.assertNotIn("PRIVATE_DRAFT_MARKER", render_journal_clips(self.unit))

    def test_approved_source_must_be_known_https_media(self):
        for url in [
            "javascript:alert(1)",
            "https://cdn.ncbi.nlm.nih.gov.evil.test/clip.mp4",
            "https://user@cdn.ncbi.nlm.nih.gov/clip.mp4",
            "https://www.e-jyms.org/clip.mp4?x=1",
            "https://www.e-jyms.org:8443/clip.mp4",
            "http://www.e-jyms.org/clip.mp4",
        ]:
            with self.subTest(url=url):
                self.assertFalse(media_url(url))
                self.clip["url"] = url
                with self.assertRaisesRegex(ValueError, "media URL"):
                    approved_clips(self.unit, self.references)

    def test_intervention_and_missing_provenance_fail_closed(self):
        original = copy.deepcopy(self.clip)
        for key, value in [
            ("contains_intervention", True),
            ("duration_seconds", float("nan")),
            ("duration_seconds", True),
            ("reference_id", "unknown"),
            ("license", ""),
            ("reviewed_payload_sha256", ""),
            ("observations", "Not an array"),
            ("observations", [""]),
        ]:
            with self.subTest(key=key):
                self.clip.clear()
                self.clip.update(original)
                self.clip[key] = value
                with self.assertRaises(ValueError):
                    approved_clips(self.unit, self.references)

    def test_reading_page_preserves_context_notes_and_native_controls(self):
        self.clip["title"] = '<script>alert("x")</script>'
        html = render_journal_clips(self.unit)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn('controls playsinline preload="none"', html)
        self.assertNotIn("autoplay", html)
        for field in ("case_context", "scope_note", "caption_note", "license"):
            self.assertIn(self.clip[field], html)

    def test_duplicate_ids_are_rejected(self):
        self.unit["journal_clips"].append(copy.deepcopy(self.clip))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            approved_clips(self.unit, self.references)


if __name__ == "__main__":
    unittest.main()
