"""Build must attach canonical-ID notes and reject ambiguous or broken video sources."""

from __future__ import annotations

import copy
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "build"))

video_id = importlib.import_module("build").video_id


class VideoIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline_tmp = tempfile.TemporaryDirectory()
        cls.baseline_dist = Path(cls.baseline_tmp.name) / "dist"
        result = cls.build(ROOT / "course", cls.baseline_dist)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        cls.baseline = json.loads((cls.baseline_dist / "course.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls.baseline_tmp.cleanup()

    @staticmethod
    def build(course, dist):
        return subprocess.run(
            [sys.executable, str(ROOT / "src" / "build" / "build.py")],
            env={**os.environ, "COURSE": str(course), "DIST": str(dist)},
            text=True,
            capture_output=True,
            check=False,
        )

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.course = Path(self.tmp.name) / "course"
        self.dist = Path(self.tmp.name) / "dist"
        shutil.copytree(ROOT / "course", self.course)

    def read_segments(self):
        path = self.course / "data" / "segments.json"
        return path, json.loads(path.read_text())

    def first_drill(self):
        cfg = json.loads((self.course / "course.config.json").read_text())
        for chapter in cfg["chapters"]:
            path = self.course / "data" / f"{chapter['source']}.json"
            blob = json.loads(path.read_text())
            for node in blob.get("chapters", [blob]):
                for unit in node.get("units", []):
                    if unit.get("drills"):
                        return path, blob, unit["drills"][0]
        raise AssertionError("fixture has no drill")

    def assert_failed_without_writing(self, expected):
        self.dist.mkdir()
        sentinel = self.dist / "course.json"
        sentinel.write_text("previous known-good output")
        result = self.build(self.course, self.dist)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(expected, result.stdout + result.stderr)
        self.assertEqual(sentinel.read_text(), "previous known-good output")
        self.assertFalse((self.dist / "index.html").exists())
        return result

    def assert_unit_status_blocked(self, status):
        cfg = json.loads((self.course / "course.config.json").read_text())
        chapter = cfg["chapters"][0]
        path = self.course / "data" / f"{chapter['source']}.json"
        blob = json.loads(path.read_text())
        node = next(n for n in blob.get("chapters", [blob]) if n["chapter"] == chapter["code"])
        unit = node["units"][0]
        if status is None:
            unit.pop("review_status", None)
        else:
            unit["review_status"] = status
        path.write_text(json.dumps(blob))
        result = self.assert_failed_without_writing("配置章節含未核准單元")
        self.assertIn(unit["id"], result.stderr)
        self.assertIn(status or "缺少狀態", result.stderr)

    def test_draft_unit_fails_before_output(self):
        self.assert_unit_status_blocked("draft")

    def test_medical_review_unit_fails_before_output(self):
        self.assert_unit_status_blocked("medical-review")

    def test_missing_unit_review_status_fails_before_output(self):
        self.assert_unit_status_blocked(None)

    def test_research_drafts_do_not_enter_the_configured_course(self):
        research = self.course / "research"
        research.mkdir(exist_ok=True)
        (research / "unapproved-unit.json").write_text(
            json.dumps(
                {
                    "review_status": "draft",
                    "id": "research-only-unit",
                    "name": "Unpublished research",
                }
            )
        )
        result = self.build(self.course, self.dist)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads((self.dist / "course.json").read_text()), self.baseline)

    def test_canonical_urls_and_rejected_impostors(self):
        vid = "abcdefgh_12"
        for url in [
            f"https://www.youtube.com/watch?v={vid}",
            f"https://youtube.com/watch?t=62&v={vid}&feature=share",
            f"https://youtu.be/{vid}?t=62&si=token",
            f"https://www.youtube.com/watch?v={vid}#t=1m2s",
        ]:
            with self.subTest(url=url):
                self.assertEqual(video_id(url), vid)
        for bad in [
            None,
            123,
            "",
            f"http://youtu.be/{vid}",
            f"https://youtu.be/{vid}EXTRA",
            f"https://youtu.be/{vid}/extra",
            f"https://evil.test/?v={vid}",
            f"https://youtube.com.evil.test/watch?v={vid}",
            f"https://user@youtube.com/watch?v={vid}",
            f"https://youtube.com/watch?v={vid}&v=XXXXXXXXXXX",
            f"https://youtube.com/watch?v={vid}&v=",
            f"https://youtube.com/watch?v={vid}&raw=has space",
        ]:
            with self.subTest(url=bad):
                self.assertIsNone(video_id(bad))

    def test_short_time_urls_and_identical_duplicates_preserve_all_published_notes(self):
        path, blob = self.read_segments()
        for entry in blob["videos"]:
            url = entry.get("url") or entry.get("video_url")
            entry["url"] = f"https://youtu.be/{video_id(url)}?t=90&si=share"
        blob["videos"].append(copy.deepcopy(blob["videos"][0]))
        path.write_text(json.dumps(blob))
        result = self.build(self.course, self.dist)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads((self.dist / "course.json").read_text()), self.baseline)

    def test_conflicting_notes_for_same_id_fail_before_output(self):
        path, blob = self.read_segments()
        duplicate = copy.deepcopy(
            next(e for e in blob["videos"] if e["review_status"] == "approved")
        )
        duplicate["url"] = (
            f"https://youtu.be/{video_id(duplicate.get('url') or duplicate.get('video_url'))}?t=99"
        )
        duplicate["segments"][0]["summary"] = "Conflicting alternative source content"
        blob["videos"].append(duplicate)
        path.write_text(json.dumps(blob))
        self.assert_failed_without_writing("已審閱筆記衝突")

    def test_invalid_approved_note_url_fails_before_output(self):
        path, blob = self.read_segments()
        entry = next(e for e in blob["videos"] if e["review_status"] == "approved")
        entry["url"] = "https://evil.test/?v=abcdefgh_12"
        path.write_text(json.dumps(blob))
        self.assert_failed_without_writing("筆記的影片 URL 無效")

    def test_missing_video_url_fails_before_output(self):
        path, blob, drill = self.first_drill()
        drill.pop("url")
        path.write_text(json.dumps(blob))
        self.assert_failed_without_writing("缺影片連結")

    def test_malformed_video_url_fails_before_output(self):
        path, blob, drill = self.first_drill()
        drill["url"] = "https://youtu.be/abcdefgh_12EXTRA"
        path.write_text(json.dumps(blob))
        self.assert_failed_without_writing("URL 格式不正確")

    def test_draft_notes_do_not_override_approved_source(self):
        path, blob = self.read_segments()
        duplicate = copy.deepcopy(blob["videos"][0])
        duplicate["url"] = (
            f"https://youtu.be/{video_id(duplicate.get('url') or duplicate.get('video_url'))}?t=10"
        )
        duplicate["review_status"] = "draft"
        duplicate["segments"][0]["summary"] = "Unapproved draft must remain absent"
        blob["videos"].append(duplicate)
        path.write_text(json.dumps(blob))
        result = self.build(self.course, self.dist)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        actual = json.loads((self.dist / "course.json").read_text())
        expected = copy.deepcopy(self.baseline)
        expected["meta"]["segment_videos_held"] += 1
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
