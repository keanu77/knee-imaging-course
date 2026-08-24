# GitHub 與未授權發布 handoff

## 本次 GitHub 範圍

1. 建立 private repo `keanu77/knee-ultrasound-course`，預設分支 `main`。
2. 以 `feat/knee-course-v1` 提交完整課程內容並推送。
3. 建立 draft PR，確認 GitHub Actions 的 `make check` 通過。
4. PR 明載醫療狀態為 `draft`、`allowIndexing=false`，以及 OG 與真實瀏覽器 QA 待 MacBook Air 執行。

本次不 merge；`main` 不因 draft PR 自動取得課程內容。

## Cloudflare 設定僅供未來記錄

- GitHub repo：`keanu77/knee-ultrasound-course`
- 預定 Pages 專案名：`knee-ultrasound-course`
- 預定 production branch：`main`
- root directory：repo 根目錄
- build command：`uv run python src/build/build.py`
- build output：`dist`
- 正式網域：`https://knee-imaging.sportsmedicine.tw`
- Cloudflare zone：`sportsmedicine.tw`

這些值只是 frozen brief。此次不建立 Cloudflare Pages、不連接 GitHub、不建立 preview、不修改 DNS、不加入 custom domain，也不執行 production smoke。

## 本次 gate 與 Air 端 handoff

Codex 本機必須通過：

```bash
make build
make check
make verify
```

`make og` 不在 Codex sandbox 執行。MacBook Air 端需在 sandbox 外產生 `og.png`，確認尺寸 1200×630、文字未截斷且對比可讀；並以真實瀏覽器完成 320／390／desktop 的水平溢位、鍵盤、console、network、YouTube fallback 及 44px 觸控目標檢查。

在任何未來 preview 或 production 發布前，仍須確認 HTML robots meta 與 `_headers` 的 `X-Robots-Tag` 均為 `noindex`，且 AI crawler 封鎖存在。醫療審閱未完成前不得把 `allowIndexing` 改為 `true`。
