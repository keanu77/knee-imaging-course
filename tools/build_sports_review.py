#!/usr/bin/env python3
"""Build a local-only, self-contained review desk without changing approval state."""

from __future__ import annotations

import argparse
import json
import math
import re
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}\Z")
CSS = """
:root{color-scheme:light dark;--paper:#faf8f2;--panel:#f0ede4;--ink:#1a2330;--muted:#59646c;--line:#d8d2c4;--accent:#17616a;--warning:#785500}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.8 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang TC",sans-serif}
header,main,footer{max-width:1180px;margin:auto;padding:2rem clamp(1rem,4vw,3rem)}header{border-bottom:1px solid var(--line)}h1{font-size:clamp(1.8rem,4vw,3rem);line-height:1.4;margin:.6rem 0}h2{font-size:1.6rem;line-height:1.5}h3{font-size:1.15rem;line-height:1.5}p{margin:.65rem 0}a{color:var(--accent);overflow-wrap:anywhere;text-underline-offset:.2em}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:3px}.badge{display:inline-block;padding:.2rem .65rem;border:1px solid currentColor;border-radius:4px;color:var(--warning);font-weight:700}.notice{padding:1rem 1.25rem;background:var(--panel);border-left:4px solid var(--warning)}nav ul{display:flex;flex-wrap:wrap;gap:.5rem 2rem;padding-left:1.2rem}.module,.sources{margin:2.5rem 0;padding-top:1.5rem;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem 2.5rem}.field{min-width:0}li{margin:.5rem 0}ul,ol{padding-left:1.4rem}.meta{font-size:.9rem;color:var(--muted)}.video,.question{padding:1.25rem;margin:1.25rem 0;border:1px solid var(--line);border-radius:8px;background:var(--panel)}.video h3{margin-top:0}.frame{aspect-ratio:16/9;width:100%;border:0;background:#111}.range-buttons{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}button{font:inherit;background:var(--paper);color:var(--accent);border:1px solid var(--accent);border-radius:4px;padding:.5rem .8rem;cursor:pointer}button[aria-pressed=true]{background:var(--accent);color:var(--paper)}details{border-top:1px solid var(--line);margin-top:1rem;padding-top:.6rem}summary{cursor:pointer;font-weight:650}.assessment{white-space:pre-line}.pending{color:var(--warning)}.skip{position:absolute;top:-5rem;background:var(--paper);padding:1rem}.skip:focus{top:0}footer{border-top:1px solid var(--line)}
@media(max-width:760px){.grid{grid-template-columns:1fr}header,main,footer{padding:1.25rem}.video{padding:.8rem}}
@media(prefers-color-scheme:dark){:root{--paper:#10151b;--panel:#1a222b;--ink:#edf1f4;--muted:#afbac2;--line:#414b55;--accent:#8ad0d4;--warning:#efcc82}}
"""
JS = """
document.addEventListener('click', function(event) {
  const button = event.target.closest('button[data-frame]');
  if (!button) return;
  const frame = document.getElementById(button.dataset.frame);
  if (!frame) return;
  frame.src = button.dataset.src;
  button.closest('.range-buttons').querySelectorAll('button').forEach(function(item) {
    item.setAttribute('aria-pressed', item === button ? 'true' : 'false');
  });
});
"""


def esc(value: object) -> str:
    return escape(str(value if value is not None else ""), quote=True)


def safe_url(value: object) -> str | None:
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        return None
    try:
        p = urlsplit(value)
        return (
            value
            if p.scheme in {"http", "https"} and p.hostname and not p.username and not p.password
            else None
        )
    except ValueError:
        return None


def link(label: object, url: object) -> str:
    href = safe_url(url)
    return (
        f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'
        if href
        else esc(label)
    )


def seconds(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value) if math.isfinite(value) and value >= 0 and int(value) == value else None
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        if re.fullmatch(r"\d+:\d{2}(?::\d{2})?", value):
            parts = [int(x) for x in value.split(":")]
            if any(x >= 60 for x in parts[1:]):
                return None
            total = 0
            for part in parts:
                total = total * 60 + part
            return total
    return None


def video_id(video: dict) -> str | None:
    candidate = video.get("id") or video.get("video_id")
    if isinstance(candidate, str) and VIDEO_ID.fullmatch(candidate):
        return candidate
    url = safe_url(video.get("url"))
    if not url:
        return None
    parsed = urlsplit(url)
    host = parsed.hostname
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        candidate = parse_qs(parsed.query).get("v", [""])[0]
    elif host == "youtu.be":
        candidate = parsed.path.lstrip("/")
    else:
        return None
    return candidate if VIDEO_ID.fullmatch(candidate) else None


def diagnostic_ranges(video: dict) -> list[tuple[int, int]]:
    duration = seconds(video.get("duration_seconds"))
    ranges = []
    for pair in video.get("diagnostic_ranges", []):
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            continue
        start, end = seconds(pair[0]), seconds(pair[1])
        if (
            start is not None
            and end is not None
            and end > start
            and (duration is None or end <= duration)
        ):
            ranges.append((start, end))
    return ranges


def valid_segments(video: dict) -> list[tuple[dict, int, int]]:
    duration = seconds(video.get("duration_seconds"))
    boundaries = diagnostic_ranges(video)
    ranges = []
    candidates = video.get("segments") or [
        {"start": start, "end": end, "title": f"診斷範圍 {i + 1}"}
        for i, (start, end) in enumerate(boundaries)
    ]
    for segment in candidates:
        start, end = seconds(segment.get("start")), seconds(segment.get("end"))
        if (
            start is None
            or end is None
            or end <= start
            or (duration is not None and end > duration)
            or (
                "diagnostic_ranges" in video
                and not any(a <= start and end <= b for a, b in boundaries)
            )
        ):
            continue
        ranges.append((segment, start, end))
    return ranges


def clock(value: object) -> str:
    number = seconds(value)
    if number is None:
        return str(value or "")
    hours, rest = divmod(number, 3600)
    minutes, sec = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{sec:02d}" if hours else f"{minutes:02d}:{sec:02d}"


def render_video(video: dict, index: int) -> str:
    identifier = video_id(video)
    ranges = valid_segments(video)
    frame_id = f"review-video-{index}"
    parts = [f'<article class="video"><h3>{esc(video.get("title", "待補片名"))}</h3>']
    parts.append('<span class="badge">DRAFT · 待策展裁決</span>')
    meta = [video.get("presenter"), video.get("channel"), video.get("upload_date")]
    if video.get("duration_seconds") is not None:
        meta.append(f"{video['duration_seconds']} 秒")
    parts.append(f'<p class="meta">{esc(" · ".join(str(x) for x in meta if x))}</p>')
    caption = video.get("caption_kind") or video.get("english_captions_status") or "未提供字幕驗證"
    parts.append(f"<p>字幕：{esc(caption)}</p>")
    for label, fields in (
        ("來源與講者", ("source_originality", "qualification_scope")),
        ("本次查核方式與待辦", ("review_method",)),
        ("經典例外", ("classic_reason", "classic_exception_reason")),
        ("診斷範圍與限制", ("scope_note", "diagnostic_segment_range", "intervention_scan_status")),
        ("收錄用途", ("purpose",)),
    ):
        values = [str(video[field]) for field in fields if video.get(field)]
        parts.append(
            f"<p><strong>{label}：</strong>{esc('；'.join(values) if values else '待確認')}</p>"
        )
    if "diagnostic_ranges" in video:
        bounds = "、".join(f"{clock(a)}–{clock(b)}" for a, b in diagnostic_ranges(video))
        parts.append(f"<p><strong>診斷範圍草稿：</strong>{esc(bounds or '未提供有效範圍')}</p>")
    parts.append(f"<p>{link('原始影片（含課程以外內容）', video.get('url'))}")
    if video.get("qualification_evidence_url"):
        parts.append(f" · {link('講者資格證據', video['qualification_evidence_url'])}")
    if video.get("discovery_evidence_url"):
        parts.append(f" · {link('片源出處', video['discovery_evidence_url'])}")
    parts.append("</p>")
    if identifier and ranges:

        def embed(start: int, end: int) -> str:
            return (
                f"https://www.youtube-nocookie.com/embed/{identifier}?start={start}&end={end}&rel=0"
            )

        first = ranges[0]
        parts.append(
            f'<iframe class="frame" id="{frame_id}" src="{esc(embed(first[1], first[2]))}" '
            f'title="{esc(video.get("title", "教學影片"))}：診斷片段預覽" loading="lazy" '
            'referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe>'
        )
        parts.append('<div class="range-buttons" aria-label="診斷片段切換">')
        for position, (segment, start, end) in enumerate(ranges):
            label = f"{clock(segment.get('start'))}–{clock(segment.get('end'))} · {segment.get('title', '診斷片段')}"
            parts.append(
                f'<button type="button" data-frame="{frame_id}" data-src="{esc(embed(start, end))}" aria-pressed="{"true" if position == 0 else "false"}">{esc(label)}</button>'
            )
        parts.append("</div>")
    else:
        parts.append(
            '<p class="pending">尚無有效診斷時間範圍，未載入播放器。請先核對字幕與範圍。</p>'
        )
    if video.get("segments"):
        parts.append('<ol aria-label="逐段摘要">')
        allowed_ids = {id(s) for s, _, _ in ranges}
        for segment in video["segments"]:
            invalid = "（時間範圍無效，未建立播放入口）" if id(segment) not in allowed_ids else ""
            parts.append(
                f"<li><strong>{esc(clock(segment.get('start')))}–{esc(clock(segment.get('end')))} · {esc(segment.get('title'))}</strong> {invalid}<p>{esc(segment.get('summary'))}</p></li>"
            )
        parts.append("</ol>")
    parts.append("</article>")
    return "".join(parts)


def module_questions(payload: dict, module: dict) -> list:
    if module.get("questions"):
        return module["questions"]
    questions = payload.get("questions", {})
    if isinstance(questions, dict):
        entry = questions.get("units", questions).get(module.get("id"), [])
        return entry.get("questions", []) if isinstance(entry, dict) else entry
    return [q for q in questions if q.get("unit_id") == module.get("id")]


def render_questions(questions: list, references: dict | None = None) -> str:
    if not questions:
        return ""
    parts = ["<h3>知識檢核草稿</h3>"]
    for question in questions:
        parts.append(
            f'<article class="question"><p><strong>{esc(question.get("stem") or question.get("question"))}</strong></p><ol type="A">'
        )
        for option in question.get("options", []):
            parts.append(
                f"<li>{esc(option.get('text') if isinstance(option, dict) else option)}</li>"
            )
        parts.append("</ol><details><summary>檢視答案與解析</summary><ul>")
        for option in question.get("options", []):
            if isinstance(option, dict):
                state = (
                    "正確"
                    if option.get("correct") is True
                    else "錯誤"
                    if option.get("correct") is False
                    else "未標示"
                )
                parts.append(
                    f"<li><strong>{state} · {esc(option.get('text'))}</strong><p>{esc(option.get('rationale'))}</p></li>"
                )
        if question.get("answer") is not None:
            answer = question["answer"]
            options = question.get("options", [])
            if (
                isinstance(answer, int)
                and not isinstance(answer, bool)
                and 0 <= answer < len(options)
            ):
                choice = options[answer]
                label = choice.get("text") if isinstance(choice, dict) else choice
                answer = f"正確答案：{chr(65 + answer)} · {label}"
            parts.append(f"<li>{esc(answer)}</li>")
        if question.get("rationale"):
            parts.append(f"<li>{esc(question['rationale'])}</li>")
        for ref_id in question.get("reference_ids", []):
            ref = (references or {}).get(ref_id)
            parts.append(
                f"<li>出處：{link(ref.get('title', ref_id), ref.get('url'))}</li>"
                if ref
                else f"<li>出處：{esc(ref_id)}</li>"
            )
        for source in question.get("source_links", []):
            parts.append(f"<li>教學對照：{link(source.get('title'), source.get('url'))}</li>")
        parts.append("</ul></details></article>")
    return "".join(parts)


def render(payload: dict) -> str:
    title = esc(payload.get("title", "運動傷害超音波教材"))
    modules = payload.get("module_drafts", [])
    references = {
        ref["id"]: ref
        for ref in [
            *payload.get("existing_references", []),
            *payload.get("reference_candidates", []),
        ]
    }
    videos = payload.get("selected_videos", payload.get("candidates", []))
    nav = "".join(
        f'<li><a href="#module-{i}">{esc(module.get("name"))}</a></li>'
        for i, module in enumerate(modules, 1)
    )
    body = []
    for index, module in enumerate(modules, 1):
        body.append(
            f'<section class="module" id="module-{index}"><span class="badge">DRAFT · 未發布</span><h2>{index:02d} · {esc(module.get("name"))}</h2><p class="meta">{esc(module.get("id"))} · {esc(module.get("chapter"))}</p><p>{esc(module.get("summary"))}</p><div class="grid">'
        )
        for field, label in (
            ("objectives", "學習目標"),
            ("required_views", "必要影像與視圖"),
            ("key_points", "判讀重點"),
            ("pitfalls", "常見陷阱"),
        ):
            body.append(
                f'<div class="field"><h3>{label}</h3><ul>'
                + "".join(f"<li>{esc(v)}</li>" for v in module.get(field, []))
                + "</ul></div>"
            )
        body.append(
            f'</div><h3>練習與評量</h3><p class="assessment">{esc(module.get("assessment"))}</p>'
        )
        practice_ids = [
            identifier for identifier in module.get("practice_case_ids", [])
            if isinstance(identifier, str) and re.fullmatch(r"[A-Za-z0-9_-]+", identifier)
        ]
        if practice_ids:
            body.append('<p><strong>實際作答：</strong>' + " · ".join(
                f'<a href="cases/index.html#case-{esc(identifier)}">練習 {esc(identifier.rsplit("-", 1)[-1])}</a>'
                for identifier in practice_ids
            ) + '</p>')
        if module.get("content_boundary"):
            body.append(
                f'<p class="notice"><strong>內容範圍：</strong>{esc(module["content_boundary"])}</p>'
            )
        for case in module.get("source_cases", []):
            body.append(
                f'<p><strong>原始教學案例：</strong>{link(case.get("title"), case.get("url"))}</p><p class="meta">{esc(case.get("note"))}</p>'
            )
        body.append(render_questions(module_questions(payload, module), references))
        body.append("<h3>引用來源</h3><ul>")
        for ref_id in module.get("reference_ids", []):
            ref = references.get(ref_id)
            body.append(
                f'<li>{link(ref.get("title", ref_id), ref.get("url"))} <span class="meta">{esc(ref_id)}</span></li>'
                if ref
                else f'<li class="pending">{esc(ref_id)}：尚未提供來源 metadata</li>'
            )
        body.append("</ul><h3>對應影片</h3>")
        matching = [
            (i, video)
            for i, video in enumerate(videos)
            if module.get("id") in (video.get("module_ids") or [video.get("proposed_unit_id")])
        ]
        body.append(
            "".join(
                f'<p><a href="#video-{i}">{esc(video.get("title"))}</a></p>'
                for i, video in matching
            )
            or '<p class="pending">本單元尚未配對影片。</p>'
        )
        body.append("</section>")
    video_html = "".join(
        f'<div id="video-{i}">{render_video(video, i)}</div>' for i, video in enumerate(videos)
    )
    new_refs = []
    for ref in payload.get("reference_candidates", []):
        label = f"PMID {ref['pmid']}" if ref.get("pmid") else ref.get("id", "")
        new_refs.append(
            f'<li>{link(ref.get("title"), ref.get("url"))}<p class="meta">{esc(label)} · {esc(ref.get("publication_date", ref.get("year")))} · {esc(ref.get("metadata_status"))}</p><p>{esc(ref.get("evidence_type"))}</p></li>'
        )
    reference_html = (
        '<section class="sources" id="new-references"><h2>本批新增文獻與查核紀錄</h2><ol>'
        + "".join(new_refs)
        + "</ol></section>"
    )
    corrections = payload.get("proposed_corrections", [])
    if corrections:
        reference_html += '<section class="sources"><h2>既有教材修正提案</h2>'
        for correction in corrections:
            reference_html += (
                f'<article><h3>{esc(correction.get("question_id"))}</h3>'
                f'<p>原解析：{esc(correction.get("before"))}</p>'
                f'<p>修正為：{esc(correction.get("after"))}</p>'
                f'<p>{esc(correction.get("reason"))}</p>'
                f'<p>{link("查證來源", correction.get("source_url"))}</p></article>'
            )
        reference_html += '</section>'
    return f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>{title}｜策展審閱台（草稿）</title><style>{CSS}</style></head><body>
<a class="skip" href="#content">跳至審閱內容</a><header><span class="badge">DRAFT · 未發布</span><h1>{title}<br>策展審閱台</h1><p>{len(modules)} 個單元 · {len(videos)} 支影片 · {len(references)} 筆引用</p><p class="notice">本頁供集中審閱，全部內容維持草稿；產生此頁不代表核准或發布。請逐項核對醫學內容、來源與講者資格、經典影片例外和診斷範圍，再向課程策展流程提交裁決。</p><p><a href="payload.json" download>下載本次完整 JSON 副本</a> · 準備日期（UTC）：{esc(payload.get("prepared_at_utc", "未提供"))}</p><nav aria-label="單元目錄"><ul>{nav}<li><a href="#videos">影片與範圍裁決</a></li></ul></nav></header>
<main id="content">{"".join(body)}<section class="sources" id="videos"><h2>影片與範圍裁決</h2><p>片段按鈕以草稿 start/end 框定播放器；原片可能包含課程範圍以外內容。時間格式或範圍不合的條目只保留來源連結，不建立播放入口；能播放不代表已完成醫學或視聽審閱。</p>{video_html}</section>{reference_html}</main><footer><p>此工具只產生本機審閱檔，不變更 syllabus、審閱戳記或正式站。</p></footer><script>{JS}</script></body></html>"""


def build(input_path: Path, output_path: Path) -> dict:
    source, target = input_path.resolve(), output_path.resolve()
    if target.is_relative_to(ROOT / "dist"):
        raise ValueError("Review artifacts must not be written into the production dist directory")
    if target.suffix.lower() != ".html":
        raise ValueError("Output must be an HTML file")
    raw = source.read_text(encoding="utf-8")
    payload = json.loads(raw)
    if target == source or target.with_name("payload.json") == source:
        raise ValueError("Output must not overwrite the input payload")
    html = render(payload)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    target.with_name("payload.json").write_text(raw, encoding="utf-8")
    return {
        "html": str(target),
        "payload": str(target.with_name("payload.json")),
        "modules": len(payload.get("module_drafts", [])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "course/research/2026-09-08-sports-ultrasound-candidates.json",
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / ".tmp/review/sports-ultrasound/index.html"
    )
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.input, args.output), ensure_ascii=False))
    except (ValueError, OSError) as error:
        parser.exit(1, f"Review build failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
