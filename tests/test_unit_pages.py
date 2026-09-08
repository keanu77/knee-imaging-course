"""Static reading pages preserve teaching content without leaking draft units or quiz answers."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "build"))

import seo
from unit_pages import write_unit_pages

CONFIG = {
    "site": {"url": "https://course.example", "name": "影像 & 學習", "locale": "zh-Hant"},
    "medical": {"allowIndexing": True},
}
UNIT = {
    "id": "us-1",
    "review_status": "approved",
    "name": '肌腱 <影像> "閱讀"',
    "summary": 'Original summary & <script>alert("unsafe")</script>',
    "objectives": ["objective unchanged"],
    "required_views": ["views unchanged"],
    "key_points": ["points unchanged"],
    "pitfalls": ["pitfalls unchanged"],
    "assessment": "original assessment unchanged",
    "content_boundary": "Video does not demonstrate every pathology <boundary>",
    "source_cases": [{"title": "Original society case", "url": "https://source.example/case"}],
    "questions": [{"answer": "SECRET_QUIZ_ANSWER", "rationale": "SECRET_RATIONALE"}],
    "references": [
        {
            "title": "Clinical source & evidence",
            "url": "https://source.example/paper?a=1&b=2",
            "year": 2023,
        }
    ],
    "drills": [
        {
            "title": "Video source",
            "url": "https://www.youtube.com/watch?v=abcdefghijk",
            "presenter": "Author, MD",
            "channel": "Society",
            "scope_note": "Original diagnostic boundary",
            "diagnostic_segment_range": "00:10–02:00",
            "qualification_evidence_url": "https://source.example/faculty",
            "segments": [
                {
                    "start": "00:10",
                    "end": "00:40",
                    "title": "Segment title",
                    "summary": "Original segment summary",
                }
            ],
        }
    ],
}


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class UnitPagesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        self.course = {"chapters": [{"title": "Ultrasound", "units": [copy.deepcopy(UNIT)]}]}

    def generate(self, config=None):
        self.urls = write_unit_pages(self.course, config or CONFIG, self.path)
        self.html = (self.path / "units/us-1/index.html").read_text()
        return Document(self.html)

    def test_preserves_content_sources_and_static_semantics_without_quiz_payload(self):
        document = self.generate()
        for field in ("objectives", "required_views", "key_points", "pitfalls"):
            self.assertIn(UNIT[field][0], self.html)
        for value in (
            UNIT["assessment"],
            "Original diagnostic boundary",
            "Original segment summary",
            "00:10–02:00",
            "Video does not demonstrate every pathology &lt;boundary&gt;",
            "https://source.example/case",
        ):
            self.assertIn(value, self.html)
        self.assertIn("https://source.example/paper?a=1&amp;b=2", self.html)
        self.assertIn("https://source.example/faculty", self.html)
        self.assertNotIn("SECRET_QUIZ_ANSWER", self.html)
        self.assertNotIn("SECRET_RATIONALE", self.html)
        self.assertEqual(sum(tag == "h1" for tag, _ in document.tags), 1)
        self.assertFalse(any(tag == "script" for tag, _ in document.tags))
        self.assertIn(
            ("link", {"rel": "canonical", "href": "https://course.example/units/us-1/"}),
            document.tags,
        )
        self.assertEqual(self.urls, ["https://course.example/units/us-1/"])

    def test_drafts_missing_status_and_revoked_pages_are_excluded(self):
        units = self.course["chapters"][0]["units"]
        for status in ("draft", None):
            unit = copy.deepcopy(UNIT)
            unit.update(id="draft" if status else "missing", review_status=status)
            units.append(unit)
        self.generate()
        self.assertFalse((self.path / "units/draft/index.html").exists())
        self.assertFalse((self.path / "units/missing/index.html").exists())
        units[0]["review_status"] = "draft"
        self.assertEqual(write_unit_pages(self.course, CONFIG, self.path), [])
        self.assertFalse((self.path / "units/us-1/index.html").exists())

    def test_escaping_link_schemes_and_external_target_protection(self):
        unit = self.course["chapters"][0]["units"][0]
        unit["references"].append({"title": "Unsafe source", "url": "javascript:alert(1)"})
        unit["drills"].append({"title": "Unsafe video", "url": "data:text/html,unsafe"})
        document = self.generate()
        self.assertIn("&lt;script&gt;", self.html)
        self.assertIn("&lt;影像&gt;", self.html)
        self.assertNotIn("javascript:", self.html)
        self.assertNotIn("data:text/html", self.html)
        for tag, attrs in document.tags:
            if tag == "a" and attrs.get("href", "").startswith("https:"):
                self.assertEqual(attrs["target"], "_blank")
                self.assertEqual(set(attrs["rel"].split()), {"noopener", "noreferrer"})

    def test_relative_navigation_styles_and_noindex(self):
        config = copy.deepcopy(CONFIG)
        config["medical"]["allowIndexing"] = False
        document = self.generate(config)
        self.assertIn(("meta", {"name": "robots", "content": "noindex, nofollow"}), document.tags)
        self.assertIn(
            ("link", {"rel": "stylesheet", "href": "../../css/tokens.css"}), document.tags
        )
        links = [attrs["href"] for tag, attrs in document.tags if tag == "a"]
        self.assertIn("../../?tab=course#us-1", links)
        self.assertIn("../../", links)

    def test_invalid_and_duplicate_ids_fail_before_writing(self):
        self.course["chapters"][0]["units"][0]["id"] = "../escape"
        with self.assertRaises(ValueError):
            write_unit_pages(self.course, CONFIG, self.path)
        self.course["chapters"][0]["units"] = [UNIT, UNIT]
        with self.assertRaises(ValueError):
            write_unit_pages(self.course, CONFIG, self.path)

    def test_sitemap_contains_only_generated_units_without_fake_modification_date(self):
        self.generate()
        with (
            patch.object(seo, "PUB", self.path),
            patch.object(seo, "SITE", CONFIG["site"]["url"]),
            patch.object(seo, "ALLOW_INDEXING", True),
        ):
            seo.write_sitemap(self.urls)
        sitemap = (self.path / "sitemap.xml").read_text()
        tree = ElementTree.fromstring(sitemap)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [node.text for node in tree.findall("s:url/s:loc", ns)]
        self.assertEqual(
            locations, ["https://course.example/", "https://course.example/units/us-1/"]
        )
        self.assertNotIn("lastmod", sitemap)
        with patch.object(seo, "PUB", self.path), patch.object(seo, "ALLOW_INDEXING", False):
            seo.write_sitemap(self.urls)
        self.assertEqual(len(ElementTree.fromstring((self.path / "sitemap.xml").read_text())), 0)


if __name__ == "__main__":
    unittest.main()
