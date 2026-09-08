"""Review-only case exercises must remain drafts, isolated, and accessible."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from build_case_review import NOTICE, ROOT, build, render


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def fixture():
    return {
        "title": "判讀練習審閱",
        "review_status": "draft",
        "cases": [
            {
                "id": "review-1",
                "title": "對照標題",
                "modality": "US",
                "prompt": "請依提供的素材記錄觀察。",
                "tasks": ["請說明觀察依據。"],
                "materials": [
                    {
                        "title": "原始素材",
                        "url": "https://example.org/material?a=1&b=2",
                        "note": "來源說明",
                    }
                ],
                "model_answer": [{"heading": "觀察", "text": "教學對照文字"}],
                "rubric": [{"criterion": "描述依據", "anchor": "將觀察與判讀連結。"}],
                "critical_errors": ["忽略不確定性"],
                "reference_links": [{"title": "教學來源", "url": "https://example.org/reference"}],
            }
        ],
    }


class CaseReviewTest(unittest.TestCase):
    def test_review_state_and_required_fields_fail_closed(self):
        for status in ("approved", "pending", None):
            payload = fixture()
            payload["review_status"] = status
            with self.subTest(status=status), self.assertRaises(ValueError):
                render(payload)
        for key in (
            "id",
            "title",
            "modality",
            "prompt",
            "materials",
            "tasks",
            "model_answer",
            "rubric",
            "critical_errors",
            "reference_links",
        ):
            payload = fixture()
            del payload["cases"][0][key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                render(payload)
        for payload in (None, [], {}, {"review_status": "draft", "title": "x", "cases": []}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                render(payload)

    def test_duplicate_or_unsafe_ids_are_rejected(self):
        payload = fixture()
        payload["cases"].append(copy.deepcopy(payload["cases"][0]))
        with self.assertRaises(ValueError):
            render(payload)
        for identifier in ('" onclick="attack', "space id", "<tag>"):
            payload = fixture()
            payload["cases"][0]["id"] = identifier
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                render(payload)

    def test_unsafe_urls_are_rejected_before_output(self):
        for url in (
            "javascript:alert(1)",
            "data:text/html,x",
            "//example.org/x",
            "https://user:pass@example.org",
            "https://example.org/\nattack",
            "https://example.org:bad/",
            "https://example.org:999999/",
            "https://example.org\\@evil.org",
            "https://[broken",
        ):
            for field in ("materials", "reference_links"):
                payload = fixture()
                payload["cases"][0][field][0]["url"] = url
                with self.subTest(url=url, field=field), self.assertRaises(ValueError):
                    render(payload)

    def test_text_is_escaped_without_automatic_external_requests(self):
        payload = fixture()
        attack = (
            '</textarea><img src="https://evil.org/" onerror="alert(1)"><script>attack()</script>'
        )
        payload["title"] = attack
        case = payload["cases"][0]
        case["prompt"] = attack
        case["materials"][0]["title"] = attack
        case["rubric"][0]["anchor"] = attack
        html = render(payload)
        document = Document(html)
        self.assertIn("&lt;/textarea&gt;", html)
        self.assertEqual(sum(tag == "script" for tag, _ in document.tags), 1)
        self.assertFalse(
            any(tag in ("img", "iframe", "link", "video", "audio") for tag, _ in document.tags)
        )
        self.assertFalse(any("src" in attrs for _, attrs in document.tags))
        for tag, attrs in document.tags:
            self.assertFalse(any(key.startswith("on") for key in attrs))
            if tag == "a" and attrs["href"].startswith("https:"):
                self.assertEqual(attrs["rel"], "noopener noreferrer")
                self.assertEqual(attrs["target"], "_blank")
        self.assertIn("default-src 'none'", html)
        self.assertIn("form-action 'none'", html)
        self.assertNotIn("localStorage", html)
        self.assertNotIn("fetch(", html)

    def test_answer_is_initially_hidden_and_input_has_accessible_contract(self):
        html = render(fixture())
        document = Document(html)
        self.assertIn(NOTICE, html)
        self.assertIn("並非盲測", html)
        self.assertIn("noindex, nofollow", html)
        comparison = [attrs for tag, attrs in document.tags if attrs.get("class") == "comparison"]
        self.assertIn("hidden", comparison[0])
        textarea = next(attrs for tag, attrs in document.tags if tag == "textarea")
        self.assertIn("required", textarea)
        self.assertIn("aria-describedby", textarea)
        self.assertTrue(
            any(
                tag == "label" and attrs.get("for") == textarea["id"]
                for tag, attrs in document.tags
            )
        )
        radios = [attrs for tag, attrs in document.tags if tag == "input"]
        self.assertEqual([radio["value"] for radio in radios], ["0", "1", "2", "NA"])
        self.assertEqual(len({radio["name"] for radio in radios}), 1)
        self.assertIn("response.value.trim()", html)
        self.assertIn("form.reportValidity()", html)
        self.assertIn("不計算臨床合格分數", html)
        self.assertLess(html.index("請依提供的素材"), html.index("教學對照文字"))
        self.assertIn("@media print", html)
        self.assertIn("white-space:pre-wrap", html)
        self.assertIn("beforeprint", html)

    def test_empty_critical_errors_allowed_but_invalid_nested_fields_rejected(self):
        payload = fixture()
        payload["cases"][0]["critical_errors"] = []
        self.assertIn("練習 01", render(payload))
        for field, child in (
            ("materials", "note"),
            ("model_answer", "text"),
            ("rubric", "anchor"),
            ("reference_links", "title"),
        ):
            payload = fixture()
            payload["cases"][0][field][0][child] = " "
            with self.subTest(field=field), self.assertRaises(ValueError):
                render(payload)

    def test_build_writes_only_review_html_and_rejects_public_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.json"
            source.write_text(json.dumps(fixture(), ensure_ascii=False), encoding="utf-8")
            target = build(source, root / "review")
            self.assertEqual(target.name, "index.html")
            self.assertIn(NOTICE, target.read_text(encoding="utf-8"))
            self.assertEqual([p.name for p in target.parent.iterdir()], ["index.html"])
            for folder in ("dist", "public"):
                with self.subTest(folder=folder), self.assertRaises(ValueError):
                    build(source, ROOT / folder / "case-review")
            payload = fixture()
            payload["review_status"] = "approved"
            source.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                build(source, root / "rejected")
            self.assertFalse((root / "rejected").exists())


if __name__ == "__main__":
    unittest.main()
