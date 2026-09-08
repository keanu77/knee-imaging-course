"""Local review artifacts must expose drafts without publishing or inventing playback ranges."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from build_sports_review import ROOT, build, render


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def fixture():
    return {
        "review_status": "draft",
        "module_drafts": [
            {
                "id": f"m{i}",
                "name": f"Module {i}",
                "summary": "summary",
                "objectives": ["Objective"],
                "required_views": ["Views"],
                "key_points": ["Points"],
                "pitfalls": ["Pitfall"],
                "assessment": "Assessment",
                "reference_ids": ["R1", "R2"],
            }
            for i in range(4)
        ],
        "reference_candidates": [
            {"id": "R1", "title": "Primary paper", "url": "https://example.org/paper"}
        ],
        "existing_references": [
            {"id": "R2", "title": "Existing guideline", "url": "https://example.org/guideline"}
        ],
        "selected_videos": [
            {
                "id": "abcdefghijk",
                "url": "https://www.youtube.com/watch?v=abcdefghijk",
                "title": "Video",
                "module_ids": ["m0"],
                "duration_seconds": 180,
                "presenter": "A, MD",
                "qualification_evidence_url": "https://example.org/faculty",
                "caption_kind": "English manual",
                "classic_reason": "Anatomical reference",
                "scope_note": "Diagnostic only",
                "segments": [
                    {
                        "start": "00:10",
                        "end": "01:00",
                        "title": "First",
                        "summary": "First summary",
                    },
                    {"start": 90, "end": 120, "title": "Second", "summary": "Second summary"},
                ],
            }
        ],
    }


class SportsReviewTest(unittest.TestCase):
    def test_four_modules_original_fields_and_sources_are_visible(self):
        html = render(fixture())
        document = Document(html)
        modules = [
            attrs
            for tag, attrs in document.tags
            if tag == "section" and attrs.get("class") == "module"
        ]
        self.assertEqual(len(modules), 4)
        for value in (
            "Objective",
            "Views",
            "Points",
            "Pitfall",
            "Assessment",
            "Primary paper",
            "Existing guideline",
            "First summary",
        ):
            self.assertIn(value, html)
        self.assertIn("DRAFT · 未發布", html)
        self.assertIn("noindex, nofollow", html)
        self.assertNotIn("approve", html.lower())
        self.assertIn("payload.json", html)

    def test_bounded_iframe_and_switch_buttons(self):
        document = Document(render(fixture()))
        frames = [attrs for tag, attrs in document.tags if tag == "iframe"]
        self.assertEqual(len(frames), 1)
        self.assertEqual(
            frames[0]["src"],
            "https://www.youtube-nocookie.com/embed/abcdefghijk?start=10&end=60&rel=0",
        )
        self.assertEqual(frames[0]["loading"], "lazy")
        self.assertEqual(frames[0]["referrerpolicy"], "strict-origin-when-cross-origin")
        self.assertIn("title", frames[0])
        buttons = [attrs for tag, attrs in document.tags if tag == "button"]
        self.assertEqual(len(buttons), 2)
        self.assertIn("start=90&end=120", buttons[1]["data-src"])

    def test_bad_and_absent_ranges_do_not_create_players(self):
        for segments in (
            [],
            [{"start": "bad", "end": 40}],
            [{"start": 50, "end": 40}],
            [{"start": 0, "end": 181}],
            [{"start": -1, "end": 20}],
        ):
            payload = fixture()
            payload["selected_videos"][0]["segments"] = segments
            document = Document(render(payload))
            self.assertFalse(any(tag == "iframe" for tag, _ in document.tags))
            self.assertFalse(any(tag == "button" for tag, _ in document.tags))
        payload = fixture()
        payload["candidates"] = payload.pop("selected_videos")
        payload["candidates"][0].pop("segments")
        self.assertIn("尚無有效診斷時間範圍", render(payload))

    def test_untrusted_text_and_urls_cannot_inject_markup_or_active_links(self):
        payload = fixture()
        payload["module_drafts"][0]["name"] = '<img src=x onerror="alert(1)">'
        payload["selected_videos"][0]["title"] = "</iframe><script>alert(1)</script>"
        payload["selected_videos"][0]["qualification_evidence_url"] = "javascript:alert(1)"
        payload["reference_candidates"][0]["url"] = "data:text/html,attack"
        html = render(payload)
        document = Document(html)
        self.assertIn("&lt;img", html)
        self.assertIn("&lt;/iframe&gt;", html)
        self.assertEqual(sum(tag == "script" for tag, _ in document.tags), 1)
        self.assertFalse(any(tag == "img" for tag, _ in document.tags))
        for tag, attrs in document.tags:
            if tag == "a":
                self.assertFalse(attrs.get("href", "").startswith(("javascript:", "data:")))
                if attrs.get("href", "").startswith("https://"):
                    self.assertEqual(attrs["rel"], "noopener noreferrer")

    def test_question_answers_are_in_closed_details(self):
        payload = fixture()
        payload["module_drafts"][0]["questions"] = [
            {
                "stem": "Question",
                "options": [{"text": "Choice", "correct": True, "rationale": "Answer explanation"}],
            }
        ]
        html = render(payload)
        document = Document(html)
        details = [attrs for tag, attrs in document.tags if tag == "details"]
        self.assertTrue(details)
        self.assertTrue(all("open" not in attrs for attrs in details))
        self.assertIn("Answer explanation", html)
        self.assertGreater(html.index("Answer explanation"), html.index("<details>"))

    def test_declared_diagnostic_boundaries_are_enforced_and_review_method_is_visible(self):
        payload = fixture()
        video = payload["selected_videos"][0]
        video["diagnostic_ranges"] = [[10, 60]]
        video["review_method"] = "Metadata and captions only; audiovisual review pending"
        html = render(payload)
        document = Document(html)
        buttons = [attrs for tag, attrs in document.tags if tag == "button"]
        self.assertEqual(len(buttons), 1)
        self.assertIn("start=10&end=60", buttons[0]["data-src"])
        self.assertIn(video["review_method"], html)
        self.assertIn("00:10–01:00", html)
        video["diagnostic_ranges"] = []
        self.assertNotIn("<iframe", render(payload))
        video["diagnostic_ranges"] = [[10, 60]]
        video["segments"] = []
        self.assertIn("<iframe", render(payload))

    def test_numeric_zero_based_answer_resolves_to_labeled_option(self):
        payload = fixture()
        payload["module_drafts"][0]["questions"] = [
            {"question": "Q", "options": ["Wrong", "Right"], "answer": 1, "rationale": "Why"}
        ]
        html = render(payload)
        self.assertIn("正確答案：B · Right", html)
        self.assertGreater(html.index("正確答案：B · Right"), html.index("<details>"))

    def test_rebuild_preserves_payload_and_rejects_production_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            source = path / "input.json"
            source.write_text(json.dumps(fixture(), ensure_ascii=False))
            original = source.read_bytes()
            output = path / "review/index.html"
            first = build(source, output)
            html = output.read_bytes()
            self.assertEqual(first, build(source, output))
            self.assertEqual(html, output.read_bytes())
            self.assertEqual(original, source.read_bytes())
            self.assertEqual(original, (output.parent / "payload.json").read_bytes())
            with self.assertRaises(ValueError):
                build(source, ROOT / "dist/review/index.html")
            with self.assertRaises(ValueError):
                build(source, source)


if __name__ == "__main__":
    unittest.main()
