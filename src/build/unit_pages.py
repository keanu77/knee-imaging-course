"""Render approved course units as readable, JavaScript-independent documents."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from urllib.parse import quote, urlsplit

UNIT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")
SECTIONS = (
    ("objectives", "學習目標"),
    ("required_views", "必要影像與掃描視圖"),
    ("key_points", "判讀重點"),
    ("pitfalls", "常見陷阱"),
)
STYLE = """
* { box-sizing: border-box; }
body { margin: 0; background: var(--bgColor-default); color: var(--fgColor-default);
  font-family: var(--fontStack-sans); line-height: 1.85; }
a { color: var(--fgColor-accent); text-underline-offset: .2em; overflow-wrap: anywhere; }
a:hover { text-decoration-thickness: 2px; }
a:focus-visible { outline: 3px solid var(--fgColor-accent); outline-offset: 4px; }
.skip { position: absolute; top: -6rem; padding: .75rem; background: var(--bgColor-default); }
.skip:focus { top: .5rem; z-index: 2; }
.masthead, main, footer { max-width: 76rem; margin: auto; padding: 1.5rem clamp(1rem, 4vw, 3rem); }
.masthead { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem;
  border-bottom: 1px solid var(--borderColor-default); font-size: .95rem; }
.layout { display: grid; grid-template-columns: minmax(0, 1fr) 15rem; gap: 4rem; }
.eyebrow, .meta { color: var(--fgColor-muted); font-size: .9rem; }
h1 { font-family: var(--fontStack-display); font-weight: 600; font-size: clamp(1.9rem, 3.2vw, 2.75rem); line-height: 1.55; margin: .6rem 0 1.5rem; text-wrap: balance; }
h2 { font-size: 1.3rem; line-height: 1.6; margin: 0 0 1.25rem; }
h3 { font-size: 1.1rem; line-height: 1.6; margin: 0 0 .5rem; }
p { margin: .75rem 0; }
.intro { font-size: 1.1rem; }
section { margin: 2.5rem 0; padding-top: 1.5rem; border-top: 1px solid var(--borderColor-default); }
li { padding-left: .25rem; margin: .7rem 0; }
ul, ol { padding-left: 1.5rem; }
.toc { align-self: start; position: sticky; top: 2rem; margin-top: 2rem; font-size: .9rem; padding-left: 1.5rem; border-left: 1px solid var(--borderColor-default); }
.toc h2 { font-size: 1rem; }
.toc a { display: inline-block; padding-block: .25rem; }
.toc ol { padding-left: 1.25rem; }
.video { padding: 1.25rem; margin: 1rem 0; border: 1px solid var(--borderColor-default);
  background: var(--bgColor-muted); border-radius: .25rem; overflow-wrap: anywhere; }
#scope { padding: 1.25rem; background: var(--bgColor-accent-muted); border: 0; border-left: 3px solid var(--fgColor-accent); }
.video .segments { padding-left: 1.25rem; }
.assessment { white-space: pre-line; }
.action { display: inline-block; padding: .65rem 1rem; border: 1px solid var(--borderColor-accent-emphasis);
  border-radius: .4rem; font-weight: 650; }
footer { border-top: 1px solid var(--borderColor-default); margin-top: 2rem; }
@media (max-width: 800px) { .layout { display: flex; flex-direction: column; gap: 0; }
  .toc { position: static; order: -1; margin-top: .5rem; padding: 1rem; border: 1px solid var(--borderColor-default); }
  .toc ol { display: flex; flex-wrap: wrap; gap: .25rem 1.75rem; }
  .toc li { margin: 0; } }
@media print { .masthead, .toc, .action, .skip { display: none; } .layout { display: block; }
  body { background: white; color: black; } main { max-width: none; padding: 0; }
  .video, section { break-inside: avoid; } a { color: inherit; } }
"""


def text(value: object) -> str:
    return escape(str(value or ""), quote=True)


def safe_url(value: object) -> str | None:
    """Permit public HTTP(S) links only; malformed and active schemes remain plain text."""
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        return None
    try:
        parsed = urlsplit(value)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
        ):
            return None
        return value
    except ValueError:
        return None


def external_link(label: object, url: object) -> str:
    target = safe_url(url)
    if not target:
        return text(label)
    return f'<a href="{text(target)}" target="_blank" rel="noopener noreferrer">{text(label)}</a>'


def approved_units(course: dict) -> list[tuple[dict, dict]]:
    units = []
    seen = set()
    for chapter in course.get("chapters", []):
        for unit in chapter.get("units", []):
            if unit.get("review_status") != "approved":
                continue
            unit_id = unit.get("id", "")
            if not isinstance(unit_id, str) or not UNIT_ID.fullmatch(unit_id):
                raise ValueError(f"Invalid approved unit id: {unit_id!r}")
            if unit_id in seen:
                raise ValueError(f"Duplicate approved unit id: {unit_id}")
            seen.add(unit_id)
            units.append((chapter, unit))
    return units


def unit_url(site: str, unit: dict) -> str:
    return f"{site.rstrip('/')}/units/{quote(unit['id'], safe='')}/"


def list_section(key: str, label: str, values: list) -> str:
    return (
        f'<section id="{key}"><h2>{label}</h2><ul>'
        + "".join(f"<li>{text(value)}</li>" for value in values)
        + "</ul></section>"
    )


def render_videos(unit: dict) -> str:
    videos = []
    seen = set()
    candidates = [*(unit.get("lessons") or [unit.get("lesson")]), *(unit.get("drills") or [])]
    for video in candidates:
        if not video or video.get("review_status", "approved") != "approved":
            continue
        url = video.get("url", "")
        if url in seen:
            continue
        seen.add(url)
        parts = [
            f'<article class="video"><h3>{external_link(video.get("title") or video.get("name"), url)}</h3>'
        ]
        metadata = [video.get("channel"), video.get("presenter"), video.get("duration")]
        parts.append(f'<p class="meta">{text(" · ".join(str(x) for x in metadata if x))}</p>')
        for field in ("why", "scope_note"):
            if video.get(field):
                parts.append(f"<p>{text(video[field])}</p>")
        if video.get("diagnostic_segment_range"):
            parts.append(f"<p>課程診斷範圍：{text(video['diagnostic_segment_range'])}</p>")
        if video.get("qualification_evidence_url"):
            parts.append(
                f"<p>{external_link('講者資格來源', video['qualification_evidence_url'])}</p>"
            )
        segments = [
            segment
            for segment in video.get("segments", [])
            if segment.get("review_status", "approved") == "approved"
        ]
        if segments:
            parts.append('<ol class="segments" aria-label="影片段落摘要">')
            for segment in segments:
                clock = f"{segment.get('start', '')}–{segment.get('end', '')}"
                parts.append(
                    f"<li><strong>{text(clock)} · {text(segment.get('title'))}</strong>"
                    f"<p>{text(segment.get('summary'))}</p></li>"
                )
            parts.append("</ol>")
        parts.append("</article>")
        videos.append("".join(parts))
    return (
        '<section id="videos"><h2>教學影片與段落摘要</h2>' + "".join(videos) + "</section>"
        if videos
        else ""
    )


def render_unit(chapter: dict, unit: dict, config: dict) -> str:
    site = config["site"]
    name = site["name"]
    title = f"{unit['name']}｜{name}"
    canonical = unit_url(site["url"], unit)
    interactive = f"../../?tab=course#{quote(unit['id'], safe='')}"
    summary = unit.get("summary", "")
    description = " ".join(str(summary).split())
    robots = (
        "index, follow"
        if config.get("medical", {}).get("allowIndexing", False)
        else "noindex, nofollow"
    )
    sections = []
    navigation = []
    if unit.get("content_boundary"):
        sections.append(
            '<section id="scope"><h2>影片涵蓋範圍</h2>'
            f'<p>{text(unit["content_boundary"])}</p></section>'
        )
        navigation.append(("scope", "影片涵蓋範圍"))
    for key, label in SECTIONS:
        if unit.get(key):
            sections.append(list_section(key, label, unit[key]))
            navigation.append((key, label))
    if unit.get("assessment"):
        sections.append(
            '<section id="assessment"><h2>練習與評量</h2>'
            f'<p class="assessment">{text(unit["assessment"])}</p></section>'
        )
        navigation.append(("assessment", "練習與評量"))
    if unit.get("practice_cases"):
        links = "".join(
            f'<li><a href="../../practice/#case-{quote(case["id"], safe="")}">{text(case["title"])}</a></li>'
            for case in unit["practice_cases"]
        )
        sections.append(
            '<section id="practice"><h2>進階判讀練習</h2>'
            '<p>先寫所見、鑑別、限制及報告，再開啟對照。</p>'
            f'<ul>{links}</ul></section>'
        )
        navigation.append(("practice", "進階判讀練習"))
    videos = render_videos(unit)
    if videos:
        sections.append(videos)
        navigation.append(("videos", "教學影片"))
    references = [*(unit.get("references") or []), *(unit.get("source_cases") or [])]
    if references:
        items = []
        for ref in references:
            details = " · ".join(
                str(ref[key]) for key in ("organization", "journal", "year", "type") if ref.get(key)
            )
            items.append(
                f"<li>{external_link(ref.get('title'), ref.get('url'))}"
                + (f'<p class="meta">{text(details)}</p>' if details else "")
                + "</li>"
            )
        sections.append(
            '<section id="references"><h2>參考文獻與來源</h2><ol>'
            + "".join(items)
            + "</ol></section>"
        )
        navigation.append(("references", "參考文獻"))
    toc = "".join(f'<li><a href="#{key}">{label}</a></li>' for key, label in navigation)
    review_note = f"<p>{text(unit['review_note'])}</p>" if unit.get("review_note") else ""
    return f'''<!doctype html>
<html lang="{text(site.get("locale", "zh-Hant"))}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{text(title)}</title>
<meta name="description" content="{text(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{text(canonical)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{text(title)}">
<meta property="og:description" content="{text(description)}">
<meta property="og:url" content="{text(canonical)}">
<meta property="og:image" content="{text(site["url"].rstrip("/"))}/og.png">
<link rel="stylesheet" href="../../css/tokens.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&amp;display=swap">
<style>{STYLE}</style>
<link rel="stylesheet" href="../../css/sports-medicine.css">
</head>
<body>
<a class="skip" href="#reading">跳至單元內容</a>
<a class="HubReturn" href="https://imaging-course-hub.sportsmedicine.tw/" target="_blank" rel="noopener noreferrer" aria-label="返回運動醫學影像學習站首頁（新分頁）"><span aria-hidden="true">←</span> 學習站首頁</a>
<header class="masthead"><a href="../../">{text(name)}</a><a href="{interactive}">回到互動課程</a></header>
<main id="reading" tabindex="-1">
<div class="layout">
<div>
<p class="eyebrow">{text(chapter.get("title", ""))} · 單元閱讀</p>
<h1>{text(unit["name"])}</h1>
<p class="intro">{text(summary)}</p>
<a class="action" href="{interactive}">開啟互動課程與影片學習</a>
{"".join(sections)}
</div>
<nav class="toc" aria-label="本頁目錄"><h2>本頁內容</h2><ol>{toc}</ol></nav>
</div>
</main>
<footer>{review_note}<a href="{interactive}">回到此單元的互動課程</a></footer>
</body>
</html>
'''


def write_unit_pages(course: dict, config: dict, destination: Path) -> list[str]:
    """Write only approved units, removing stale generated pages after revocation."""
    units = approved_units(course)
    root = destination / "units"
    current_ids = {unit["id"] for _, unit in units}
    # This namespace belongs to generated reading pages; never leave a revoked page live.
    if root.exists():
        for stale in root.glob("*/index.html"):
            if stale.parent.name not in current_ids:
                stale.unlink()
    urls = []
    for chapter, unit in units:
        directory = root / unit["id"]
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(render_unit(chapter, unit, config), encoding="utf-8")
        urls.append(unit_url(config["site"]["url"], unit))
    return urls
