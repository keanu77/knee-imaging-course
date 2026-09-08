"""Shared safe presentation for local reviews and approved case exercise pages."""

from __future__ import annotations

import re
from html import escape
from urllib.parse import urlsplit

IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")
DRAFT_NOTICE = "進階判讀練習草稿，未發布；課程自訂練習，不是認證評量"
CSS = """
:root{color-scheme:light;--paper:#faf8f2;--panel:#fff;--ink:#1b2933;--muted:#52636c;--line:#c9d0ce;--accent:#17616a}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.8 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang TC",sans-serif}header,main,footer{max-width:960px;margin:auto;padding:2rem clamp(1rem,4vw,3rem)}header,footer{border-block:1px solid var(--line)}h1{font-size:clamp(1.8rem,4vw,2.6rem);line-height:1.4}h2{font-size:1.5rem;line-height:1.5}h3{font-size:1.1rem}p,li{overflow-wrap:anywhere}a{color:var(--accent);overflow-wrap:anywhere;text-underline-offset:.2em}button,textarea,input{font:inherit}button,a,textarea,input{touch-action:manipulation}button{min-height:44px;padding:.65rem 1rem;border:1px solid var(--accent);border-radius:6px;background:var(--panel);color:var(--accent);cursor:pointer}button[type=submit]{background:var(--accent);color:white}button:disabled{opacity:.6;cursor:default}:focus-visible{outline:3px solid var(--accent);outline-offset:4px}[hidden]{display:none!important}.skip{position:absolute;top:-6rem;padding:1rem;background:var(--panel);z-index:2}.skip:focus{top:0}.notice{padding:1rem;border-left:4px solid var(--accent);background:#e8efed}.muted{color:var(--muted);font-size:.95rem}nav ul{display:flex;flex-wrap:wrap;gap:.5rem 2rem;padding-left:1.25rem}nav a{display:inline-block;min-height:44px;padding:.4rem 0}.case{margin:2rem 0;padding:1.5rem;border:1px solid var(--line);border-radius:8px;background:var(--panel);scroll-margin-top:1rem}.case>h2{margin-top:0}.prompt,.answer-text{white-space:pre-line}label.answer-label{display:block;font-weight:700;margin-bottom:.6rem}textarea{display:block;width:100%;min-height:15rem;padding:1rem;border:1px solid var(--muted);border-radius:6px;background:var(--panel);color:var(--ink);resize:vertical}.actions{display:flex;flex-wrap:wrap;gap:.75rem;margin:1rem 0}.comparison{margin-top:1.5rem;padding-top:1rem;border-top:2px solid var(--accent)}fieldset{min-width:0;margin:1rem 0;padding:1rem;border:1px solid var(--line);border-radius:6px}legend{font-weight:700;padding-inline:.35rem}.choices{display:flex;flex-wrap:wrap;gap:.5rem}.choices label{display:flex;align-items:center;gap:.5rem;padding:.5rem .7rem;min-height:44px;border:1px solid var(--line);border-radius:5px;cursor:pointer}.choices input{width:1.1rem;height:1.1rem;flex-shrink:0}.reflections{background:var(--paper);padding:1rem}.print-answer{display:none}.print-action{margin-top:1rem}footer{font-size:.9rem}.status:empty{display:none}
@media(max-width:600px){header,main,footer{padding:1.25rem}.case{padding:1rem;margin:1.5rem 0}.actions button{width:100%}.choices{display:grid}.choices label{width:100%}}
@media print{body{background:white;color:black;font-size:11pt}header,main,footer{max-width:none;padding:.5rem 0}.skip,nav,button,.actions,textarea,.privacy,.choices,.status,noscript{display:none!important}.print-answer{display:block;white-space:pre-wrap;overflow-wrap:anywhere;border:1px solid #888;padding:1rem;min-height:3rem}.case{padding:.75rem;border-color:#888;break-inside:auto}.case+.case{break-before:page}.case,h2,h3,fieldset,.comparison{height:auto!important;max-height:none!important;overflow:visible!important}h2,h3,legend{break-after:avoid}a{color:black;text-decoration:underline}.notice{background:none;border-color:#555}.comparison[hidden]{display:none!important}.reflections{padding:.5rem;background:none}footer{border:0}}
"""
JS = """
(() => {
  const labels = {'0':'需重做', '1':'部分符合', '2':'能說明證據', 'NA':'待督導'};
  const syncPrint = form => {
    form.querySelector('.print-answer').textContent = form.querySelector('textarea').value || '尚未作答';
  };
  const reflect = form => {
    const list = form.querySelector('[data-reflections]');
    list.replaceChildren();
    form.querySelectorAll('fieldset').forEach(fieldset => {
      const selected = fieldset.querySelector('input:checked');
      const li = document.createElement('li');
      li.textContent = fieldset.querySelector('legend').textContent + '：' +
        (selected ? labels[selected.value] : '尚未自評');
      list.append(li);
    });
  };
  document.querySelectorAll('.case form').forEach(form => {
    const response = form.querySelector('textarea');
    const comparison = form.querySelector('.comparison');
    const status = form.querySelector('.status');
    response.addEventListener('input', () => {
      response.setCustomValidity('');
      syncPrint(form);
    });
    form.addEventListener('submit', event => {
      event.preventDefault();
      response.setCustomValidity(response.value.trim() ? '' : '請先寫下你的判讀與依據，再開啟對照。');
      if (!form.reportValidity()) return;
      comparison.hidden = false;
      form.querySelector('[type=submit]').hidden = true;
      form.querySelector('[data-reopen]').hidden = false;
      reflect(form);
      status.textContent = '已開啟對照。請逐項反思，必要時與督導討論。';
      comparison.querySelector('h3').focus();
      syncPrint(form);
    });
    form.addEventListener('change', () => reflect(form));
    form.querySelector('[data-reopen]').addEventListener('click', () => comparison.querySelector('h3').focus());
    form.querySelector('[data-reset]').addEventListener('click', () => {
      form.reset();
      response.value = '';
      response.setCustomValidity('');
      comparison.hidden = true;
      form.querySelector('[type=submit]').hidden = false;
      form.querySelector('[data-reopen]').hidden = true;
      form.querySelector('[data-reflections]').replaceChildren();
      syncPrint(form);
      status.textContent = '已清除本題作答與自評，可以重新練習。';
      response.focus();
    });
    syncPrint(form);
  });
  document.querySelector('[data-print]').addEventListener('click', () => window.print());
  window.addEventListener('beforeprint', () => document.querySelectorAll('.case form').forEach(syncPrint));
})();
"""


def esc(value: str) -> str:
    return escape(value, quote=True)


def safe_url(value: object) -> str:
    if not isinstance(value, str) or any(ord(char) <= 32 for char in value):
        raise ValueError("Source URLs must be absolute HTTP(S) URLs without whitespace")
    try:
        parsed = urlsplit(value)
        valid = (
            parsed.scheme in {"http", "https"}
            and parsed.hostname
            and not parsed.username
            and not parsed.password
            and "\\" not in value
        )
        _ = parsed.port  # Validate malformed or out-of-range ports, too.
    except ValueError as error:
        raise ValueError("Invalid source URL") from error
    if not valid:
        raise ValueError("Source URLs must use HTTP(S), without credentials")
    return value


def require_text(item: dict, key: str, where: str) -> None:
    if not isinstance(item.get(key), str) or not item[key].strip():
        raise ValueError(f"{where}.{key} must be a non-empty string")


def require_list(item: dict, key: str, where: str, *, allow_empty: bool = False) -> list:
    value = item.get(key)
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ValueError(f"{where}.{key} must be {'a' if allow_empty else 'a non-empty'} list")
    return value


def validate_content(payload: dict) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Case payload must be an object")
    require_text(payload, "title", "payload")
    seen = set()
    for index, case in enumerate(require_list(payload, "cases", "payload")):
        where = f"cases[{index}]"
        if not isinstance(case, dict):
            raise ValueError(f"{where} must be an object")
        for key in ("id", "title", "modality", "prompt"):
            require_text(case, key, where)
        if not IDENTIFIER.fullmatch(case["id"]) or case["id"] in seen:
            raise ValueError(
                f"{where}.id must be unique and use letters, digits, hyphens or underscores"
            )
        seen.add(case["id"])
        for key in ("tasks", "critical_errors"):
            values = require_list(case, key, where, allow_empty=key == "critical_errors")
            if any(not isinstance(value, str) or not value.strip() for value in values):
                raise ValueError(f"{where}.{key} requires non-empty strings")
        for key, fields in (
            ("materials", ("title", "url", "note")),
            ("model_answer", ("heading", "text")),
            ("rubric", ("criterion", "anchor")),
            ("reference_links", ("title", "url")),
        ):
            for entry in require_list(case, key, where):
                if not isinstance(entry, dict):
                    raise ValueError(f"{where}.{key} entries must be objects")
                for field in fields:
                    require_text(entry, field, f"{where}.{key}")
                if "url" in fields:
                    safe_url(entry["url"])


def source_link(item: dict) -> str:
    return f'<a href="{esc(safe_url(item["url"]))}" target="_blank" rel="noopener noreferrer">{esc(item["title"])}（新分頁）</a>'


def list_items(items: list[str]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def render_case(case: dict, index: int, unit_link: str = "") -> str:
    identifier = f"case-{case['id']}"
    materials = "".join(
        f'<li>{source_link(item)}<p class="muted">{esc(item["note"])}</p></li>'
        for item in case["materials"]
    )
    answers = "".join(
        f'<h4>{esc(item["heading"])}</h4><p class="answer-text">{esc(item["text"])}</p>'
        for item in case["model_answer"]
    )
    rubrics = []
    for number, item in enumerate(case["rubric"]):
        choices = "".join(
            f'<label><input type="radio" name="{identifier}-rubric-{number}" value="{value}">{label}</label>'
            for value, label in (
                ("0", "0 · 需重做"),
                ("1", "1 · 部分符合"),
                ("2", "2 · 能說明證據"),
                ("NA", "NA · 待督導"),
            )
        )
        rubrics.append(
            f"<fieldset><legend>{esc(item['criterion'])}</legend><p>{esc(item['anchor'])}</p>"
            f'<div class="choices">{choices}</div></fieldset>'
        )
    critical = (
        f"<h4>需要重新檢視的關鍵錯誤</h4><ul>{list_items(case['critical_errors'])}</ul>"
        if case["critical_errors"]
        else ""
    )
    references = "".join(f"<li>{source_link(item)}</li>" for item in case["reference_links"])
    return f"""
<section class="case" id="{identifier}" aria-labelledby="{identifier}-title">
<h2 id="{identifier}-title">練習 {index:02d} · {esc(case["modality"])}</h2>
<p class="prompt">{esc(case["prompt"])}</p>
{unit_link}
<h3>觀察素材</h3><p class="notice">來源網站可能直接顯示診斷或解說，因此這是開放素材練習，並非盲測。連結僅在你開啟時連線至來源網站。</p><ul>{materials}</ul>
<h3>請完成以下判讀</h3><ol>{list_items(case["tasks"])}</ol>
<form autocomplete="off">
<label class="answer-label" for="{identifier}-response">你的判讀與依據</label>
<p class="privacy muted" id="{identifier}-privacy">請勿輸入病人姓名、病歷號或其他可識別資料。作答與自評僅保留於目前頁面，不會傳送或寫入網站儲存空間；重新整理或關閉頁面後不保留。列印檔由你自行保管。</p>
<textarea id="{identifier}-response" aria-describedby="{identifier}-privacy" required autocomplete="off" spellcheck="false"></textarea>
<div class="print-answer" aria-hidden="true"></div>
<div class="actions"><button type="submit">完成作答，開啟對照</button><button type="button" data-reopen hidden>回到判讀對照</button><button type="button" data-reset>重新練習（清除本題）</button></div>
<p class="status" role="status" aria-live="polite"></p>
<div class="comparison" hidden>
<h3 tabindex="-1">判讀對照與反思：{esc(case["title"])}</h3>
{answers}{critical}
<h4>逐項自評</h4><p>請依作答內容選擇目前狀態。這些選項用於反思與督導討論，不計算臨床合格分數，也不判定通過。</p>
{"".join(rubrics)}
<div class="reflections"><h4>我的項目反思</h4><ul data-reflections aria-live="polite"></ul></div>
<h4>對照來源</h4><ul>{references}</ul>
</div></form></section>"""


def render_document(payload: dict, *, draft: bool, unit_links: dict[str, str] | None = None) -> str:
    validate_content(payload)
    unit_links = unit_links or {}
    notice = DRAFT_NOTICE if draft else "課程自訂進階判讀練習，不是認證評量"
    suffix = " · 草稿審閱" if draft else ""
    back = (
        ""
        if draft
        else '<p><a href="../?tab=home">回到課程首頁</a> · <a href="../?tab=course">瀏覽課程內容</a></p>'
    )
    navigation = "".join(
        f'<li><a href="#case-{case["id"]}">練習 {index:02d} · {esc(case["modality"])}</a></li>'
        for index, case in enumerate(payload["cases"], 1)
    )
    cases = "".join(
        render_case(case, index, unit_links.get(case["id"], ""))
        for index, case in enumerate(payload["cases"], 1)
    )
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>{esc(payload["title"])}{suffix}</title><style>{CSS}</style></head>
<body><a class="skip" href="#main">跳到練習</a>
<header>{back}<p class="notice">{notice}</p><h1>{esc(payload["title"])}</h1>
<p>先記錄觀察、判讀依據與不確定處，再開啟對照並逐項自評。外部素材可能包含答案；本頁不能用來證明臨床勝任能力。</p>
<nav aria-label="練習目錄"><ul>{navigation}</ul></nav>
<button class="print-action" type="button" data-print>列印目前作答與已開啟的對照</button></header>
<main id="main" tabindex="-1"><noscript><p class="notice">此頁需要 JavaScript 才能開啟作答後對照與自評。你仍可閱讀題目與來源；請勿在此輸入需要保存的作答。</p></noscript>{cases}</main>
<footer><p>{notice}。重新練習會清除該題目前的作答與自評。</p></footer>
<script>{JS}</script></body></html>"""
