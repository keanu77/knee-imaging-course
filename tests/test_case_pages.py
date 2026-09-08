"""Approved exercise pages must not leak drafts or link to unapproved units."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "build"))

from case_pages import REVIEW_FIELDS, approved_cases, write_case_pages


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def fixture():
    return {
        "title": "進階判讀練習",
        "review_status": "approved",
        "cases": [
            {
                "id": "advanced-case-01",
                "unit_id": "us-advanced",
                "title": "對照標題",
                "review_status": "approved",
                "modality": "US",
                "prompt": "記錄所見與限制。",
                "tasks": ["提供觀察依據。"],
                "materials": [
                    {"title": "素材", "url": "https://example.org/material", "note": "開放素材"}
                ],
                "model_answer": [{"heading": "對照", "text": "說明判讀依據"}],
                "rubric": [{"criterion": "依據", "anchor": "指出可觀察的特徵。"}],
                "critical_errors": [],
                "reference_links": [{"title": "來源", "url": "https://example.org/paper"}],
                "reviewed_by": "Reviewer",
                "reviewer_role": "課程策展人",
                "review_note": "策展審閱",
                "reviewed_at": "2026-09-08T00:00:00Z",
                "reviewed_commit": "a" * 40,
            }
        ],
    }


COURSE = {"chapters": [{"units": [{"id": "us-advanced", "review_status": "approved"}]}]}


class CasePagesTest(unittest.TestCase):
    def test_approved_exercises_have_stable_ids_and_course_links(self):
        payload = fixture()
        before = copy.deepcopy(payload)
        with tempfile.TemporaryDirectory() as directory:
            outputs = write_case_pages(payload, COURSE, Path(directory))
            self.assertEqual(outputs, [Path(directory) / "practice" / "index.html"])
            html = outputs[0].read_text(encoding="utf-8")
        document = Document(html)
        self.assertIn("不是認證評量", html)
        self.assertIn("並非盲測", html)
        self.assertNotIn("草稿", html)
        self.assertNotIn("未發布", html)
        self.assertIn("sans-serif", html)
        self.assertIn("不計算臨床合格分數", html)
        self.assertTrue(
            any(attrs.get("id") == "case-advanced-case-01" for _, attrs in document.tags)
        )
        links = [attrs["href"] for tag, attrs in document.tags if tag == "a"]
        self.assertIn("../?tab=home", links)
        self.assertIn("../?tab=course#us-advanced", links)
        self.assertIn("../units/us-advanced/", links)
        self.assertTrue(
            any(
                attrs.get("class") == "comparison" and "hidden" in attrs
                for _, attrs in document.tags
            )
        )
        self.assertFalse(any("src" in attrs for _, attrs in document.tags))
        self.assertEqual(payload, before)

    def test_top_level_draft_is_rejected_without_writing(self):
        payload = fixture()
        payload["review_status"] = "draft"
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                write_case_pages(payload, COURSE, Path(directory))
            self.assertFalse((Path(directory) / "practice").exists())

    def test_draft_case_is_not_in_html_links_or_embedded_answers(self):
        payload = fixture()
        # Drafts need not yet contain every field, and must not be rendered at all.
        payload["cases"].append(
            {
                "id": "draft-case",
                "review_status": "draft",
                "title": "SECRET_DRAFT",
                "model_answer": "SECRET_ANSWER",
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            [path] = write_case_pages(payload, COURSE, Path(directory))
            html = path.read_text(encoding="utf-8")
            self.assertNotIn("SECRET_", html)
            self.assertNotIn("draft-case", html)
            payload["cases"][0]["review_status"] = "draft"
            self.assertEqual(write_case_pages(payload, COURSE, Path(directory)), [])
            self.assertFalse(path.exists(), "Withdrawing all cases removes stale output")

    def test_missing_or_unapproved_unit_fails_before_output(self):
        for unit_id, status in (("unrelated", "approved"), ("us-advanced", "draft")):
            course = {"chapters": [{"units": [{"id": unit_id, "review_status": status}]}]}
            with (
                self.subTest(unit_id=unit_id, status=status),
                tempfile.TemporaryDirectory() as directory,
            ):
                with self.assertRaises(ValueError):
                    write_case_pages(fixture(), course, Path(directory))
                self.assertFalse((Path(directory) / "practice").exists())

    def test_duplicate_case_ids_and_missing_review_stamps_are_rejected(self):
        for status in ("approved", "draft"):
            payload = fixture()
            duplicate = copy.deepcopy(payload["cases"][0])
            duplicate["review_status"] = status
            payload["cases"].append(duplicate)
            with self.subTest(status=status), self.assertRaises(ValueError):
                approved_cases(payload, COURSE)
        for field in REVIEW_FIELDS:
            payload = fixture()
            payload["cases"][0].pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                approved_cases(payload, COURSE)

    def test_published_page_retains_shared_escaping_and_url_validation(self):
        payload = fixture()
        payload["cases"][0]["prompt"] = '<img src="x" onerror="attack()">'
        with tempfile.TemporaryDirectory() as directory:
            [path] = write_case_pages(payload, COURSE, Path(directory))
            html = path.read_text(encoding="utf-8")
            self.assertIn("&lt;img", html)
            self.assertFalse(any(tag == "img" for tag, _ in Document(html).tags))
        payload["cases"][0]["materials"][0]["url"] = "javascript:attack()"
        with self.assertRaises(ValueError):
            approved_cases(payload, COURSE)


if __name__ == "__main__":
    unittest.main()
