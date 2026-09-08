# 發布與驗證

2026-09-09 實查：本專案由 Cloudflare Pages 的 GitHub integration 發布。

- GitHub：`keanu77/knee-imaging-course`，repository ID `1318617772`。
- Cloudflare Pages：`knee-ultrasound-course`，production branch `main`。
- 平台 build command：`python3 src/build/build.py`；root 為 repository 根目錄，output 為 `dist`。
- 正式網址：https://knee-imaging.sportsmedicine.tw/
- Cloudflare source config 仍顯示更名前的 `knee-ultrasound-course`，repository ID 與目前 GitHub 相同；勿另建專案或重設網域。

使用者本次 `ship` 已授權提交與推送前輪完成的 UI、運動傷害與進階教材。兩份教材批准分別見 `course/research/2026-09-08-sports-ultrasound-approval.json` 與 `2026-09-08-advanced-approval.json`；受審原稿不可改寫。

## 推送前

```bash
make check
make verify
PLAYWRIGHT_MODULE=/path/to/playwright BASE_URL=http://127.0.0.1:8899/ node tests/browser_smoke.cjs
```

GitHub Actions 執行 `uv sync --locked` 與 `make check`。本專案為 Python 標準庫建置及原生 JavaScript，語法檢查採 `make jscheck`，沒有 TypeScript 編譯步驟。

本機 uv cache 受限時可使用 `UV_CACHE_DIR=/tmp/knee-ship-uv-cache make check PY=.venv/bin/python`。不要放寬內容審閱、診斷範圍或測試閘門。

## 推送後

1. 確認 GitHub main 的 SHA 與本機 HEAD 相同，並查看 quality workflow。
2. `wrangler pages deployment list --project-name knee-ultrasound-course --environment production --json` 確認新 SHA 的正式部署成功。
3. 比對正式站與本機 `dist/course.json`、主要 JS/CSS、`practice/index.html` 及單元閱讀頁的內容 SHA-256；HTTP 200 不足以證明新版本上線。
4. 驗證正式站課程導覽與練習入口、作答後解析、手機版面。

不使用 `make deploy`／Direct Upload。保留既有 indexing 設定與策展紀錄；課程收錄不等於臨床能力認證。
