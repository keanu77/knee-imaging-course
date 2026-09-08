# 多模型稽核 Pass 2：逐項對抗驗證

日期：2026-09-08。範圍：knee-image-course 公開網站前端、建置與課程資料。此文件核對外部模型的每一項 finding；不是醫學內容簽核，也不是修復完成證明。

## 基準與方法

- 受審基準：公開 `9b68659`，副本 `/tmp/knee-multi-audit/public`。本地基準 `75cfd6c`。已實際執行 `git diff 9b68659 75cfd6c`，唯一差異為 `src/build/checklist.py` 兩行署名／審閱措辭，不影響本次前端 finding。
- 四份原始輸出已保存在 `docs/audits/2026-09-08-model-reports/`：`codex.md`、`grok.md`、`agy.md`、`qwen.md`。AGY 採實際有分析內容的 embedded 重試報告；不得以空結果的 `out-agy.md` 充數。
- 下列檔案行號一律指公開基準；已讀被標示區段與相關呼叫端，而非僅依報告重述。當前工作樹正同步修復，因此不以目前 diff 否定公開基準缺陷，也不以「程式已改」替代瀏覽器驗收。
- confidence 表示「限定後的缺陷宣稱成立」信心，不是嚴重度；小於 0.70 的原宣稱剔除。把可重現錯誤、潛在資料條件、產品改善建議分開，不把模型的 P0 原封沿用。
- 主 agent 已實測的四項保留為確認缺陷：390px 分頁按鈕無法點選；播放→課程→影片後 iframe 空白；初訪單元深連結停首頁；帶診斷範圍影片的 iframe 未帶範圍。這些實測由主 agent 提供，本文件作者不宣稱另行重跑。

## 數字與資料複算

直接解析公開 `course/data/syllabus.json`、`segments.json`、`questions.json`、`glossary.json`：

| 指標 | 複算結果 | 結論 |
| --- | --- | --- |
| 章節／單元 | 9／14 | 與 README 相符 |
| 影片出現次數／URL 去重 | 32／32 | 現資料無共用 URL |
| 核心／延伸 | 8／24 | 與 README 相符 |
| 單元審閱狀態 | 14 個 approved；全部有 reviewed_by | 不能宣稱混入草稿；此欄位代表記錄存在，不是重新簽核 |
| 筆記 | 32 份影片記錄、332 段；32 份均 approved | 全部以 url 或 video_url 可與教材 URL 配對 |
| 測驗／名詞 | 48 題／120 條 | 與 README 相符 |
| 無影片單元 | ch0-u1、ch1-u1、ch6-u1，共 3 個 | 前者為導讀；不能一律當缺陷 |
| 含介入影片 | 6 支 | 其中 1 支診斷範圍不連續，必須保留多區段模型 |

六支範圍依序為 `0:00-2:29`、`02:03–21:45`、`02:33–19:08、19:20–35:54`、`00:00-25:20`、`02:29–15:36`、`12:53–34:13`。單用 `intervention_start_timestamp` 當所有影片的終點會錯刪合法後段。

## Codex：15 項全核對

| ID／原嚴重度 | 裁決／confidence | 已確認根因與限制 | 驗收方式 |
| --- | --- | --- | --- |
| C01 P1 跳轉連結 | 採用 P1／1.00 | index.html:35 指 #main；tokens.css:215 只有裁切樣式，沒有 focus 顯示。app.js:666-669 將非課程分頁的 #main 隱藏。 | 首頁、課程、播放器各以 Tab 聚焦跳轉連結，須可見並將焦點帶到當前可見主內容。 |
| C02 P1 巢狀控制 | 採用 P1／1.00 | render.js:547-550，button 包含 tabindex=0、role=checkbox 的掌握度控制。 | DOM 不含 button 內互動控制；鍵盤可各自展開／改掌握度，彼此不誤觸。 |
| C03 P1 展開語意 | 採用 P1／1.00 | render.js:593、app.js:838-839,1016-1017 只改 class；肌群宣告初始 expanded=false 後未同步。章節／單元未宣告狀態。 | 初始、點擊、全展開、搜尋、深連結、複習入口皆同步 aria-expanded 與 aria-controls；讀屏不讀收合內容。 |
| C04 P1 快捷鍵 | 採用 P1／1.00 | keys.js:119 僅排除 input/textarea/select/contenteditable；空白與方向鍵攔截按鈕、分隔條，且未檢查 defaultPrevented。全域單字元快捷鍵無關閉／重設入口。 | 播放頁按鈕空白正常啟動，分隔條箭頭只調宽；可停用字元快捷鍵，停用後不攔截 N/P/T 等字元。 |
| C05 P1 快捷鍵視窗 | 採用 P1／1.00 | keys.js:90-111 是 div+role=dialog，無焦點移入／限制／還原，關閉鈕只有 aria-hidden SVG。 | 開啟後焦點進視窗、Tab 不出界、背景不可操作、Escape/關閉還原焦點且關閉鈕有名稱。 |
| C06 P1 導覽焦點 | 採用 P1／0.99 | setTab 隱藏來源；playAt→play 重建 playerInfo、renderPlaylist 重建 playlist（app.js:735-742、player.js:250,286），無焦點接續。 | 鍵盤換片、播放清單切片、切分頁及返回單元後焦點留在有意義的位置，繼續 Tab 不回頁首。 |
| C07 P1 換片鈕名稱 | 採用 P1／1.00 | player.css:459-463 在 ≤900px display:none 隱藏文字；player.js:306-307 無 aria-label。 | 900px、390px 的可及性樹仍有「上一部影片／下一部影片」。 |
| C08 P1 手機署名 | 採用；390px 阻斷列 P0／1.00 | clinical.css:1632-1634 的隱藏規則被 2056-2058 同 specificity 的 inline-flex 覆寫；767px grid 與113px偏移假設不足。主 agent 已實測按不到 tab。 | 320/390/767/900px 無交疊；三分頁文字可讀且可點；固定頂列不遮深連結目標。 |
| C09 P2 狀態僅視覺 | 採用 P2／0.99 | filters.js:47-49、app.js:944-947,1053-1058、player.js:237 只改特定 active/playing class，計數无 live region。不是所有控制都缺：核心切換原已有 aria-pressed。 | 類型／分面／待完成鈕有同步 pressed，播放項目有 current，結果數變化可被宣讀；不破壞既有核心鈕。 |
| C10 P1 深連結 | 採用；主流程列 P0／1.00 | app.js:1227-1260 先選預設 home，hash 單元處理只展開隱藏節點、不切 course。 | 清 storage 開 #ch8-u1 直接顯示正確單元；#XR1 同理；前後頁恢復。 |
| C11 P2 標題語意 | 採用 P2／1.00 | render.js:555,596 章節與單元皆 span，子內容卻 h3/h4。 | 標題導覽含章節 h2、單元 h3，內部標題層級一致且不引入巢狀互動。 |
| C12 P2 重繪首頁 | 採用 P2／0.99 | 首次開單元時 markLearning→setMastery→renderLanding 與 rememberUnit→renderLanding 各重建一次；未量測速度。 | 隱藏首頁時不重建 landingBody；返回首頁顯示最新進度；不得聲稱未量測的毫秒改善。 |
| C13 P2 拖曳排版 | 採用 P2／0.95 | pointermove→apply 寫 style→fitFrame 讀 layout 再寫；這是同步讀寫風險，尚無卡頓量測。 | 每 animation frame 最多一次套用；pointercancel 結束拖曳；performance trace 才能支持效能數值。 |
| C14 P2 JS 正文 | 採用 P2／0.99 | index.html:254-258 是載入提示，app.js fetch 後渲染正文；seo.py 僅 metadata/schema 等，未生成教材正文。不是所有爬蟲都不執行 JS。 | 關 JS／直接 HTTP 讀 HTML 能取得主要教材、語意連結與審閱範圍；JS 增強不重複正文。 |
| C15 P2 lastmod | 採用 P2／1.00 | seo.py:260 使用 date.today 而非內容修訂時間。 | 無內容修改的不同日建置不改 lastmod；無可信日期可省略。 |

## Grok：14 項與 2 項待驗證全核對

| ID／原嚴重度 | 裁決／confidence | 已確認根因與限制 | 驗收方式 |
| --- | --- | --- | --- |
| G01 P0 先考後看片 | 降級 P1／0.95 | render.js:561-576 的 quiz 在 drills 前；lessonBox 在 quiz 前但本資料影片放 drills。是流程選擇，不是阻斷或必然無法學習。 | 預設順序為重點／影片／知識檢核，提供直接檢核入口；不強迫等待看完影片。 |
| G02 P0 續讀 | 降級 P1／0.98 | renderHome:633-635 last||first 不看 done；會返回已完成單元。不是「14單元卡住」：仍可自行選章。 | 已完成上次單元時建議下一未完成；待複習／學習中有入口；全完成切為複習，不錯稱尚未開始。 |
| G03 P0 雙軌搜尋 | 採用 P1／1.00 | app.js:1037-1042 只更新 query，頂欄輸入不切分頁；filters.js 用 Unit.textContent，不含仅播放器渲染的332段；只展開 chapter。player.js:199-210 才搜筆記。 | 首頁／課程／播放器搜尋一致；以只在筆記出現的詞找得到命中摘要與時間碼；點击到正確片段；中英同義詞一致。 |
| G04 P0 上線文案 | 部分採用 P1／1.00；硬編碼永久顯示子宣稱剔除／0.05 | config:404 ctaLede 確實保留草稿/noindex 與 allowIndexing=true、14 approved 矛盾。index:223 的初值會由 app.js:251 courseReviewLabel 覆寫，不是正常載入後永久顯示審阅中。 | 首頁及課程狀態取同一資料，使用策展審閱措辭；移除誤導初值；含草稿 fixture 不顯示全數通過。 |
| G05 P1 超音波主軸偏重 | 採用 P1／0.94 | index:113-115,213-219 掃描工作站，config 步驟先探頭，render:185-199 共用 SCAN KEYS。是跨影像定位問題，不能推論學員一定走錯。 | 首頁清楚 XR→US→MRI，三類入口與檢核標籤適合其影像，仍保持超音波特色。 |
| G06 P1 無首頁分頁 | 採用 P1／0.93 | index:47-58 只有課程/影片；品牌仍能回首頁且有 aria-label，因此「回不去」誇大，真正問題為入口難發現。 | 手機與桌機皆有明確首頁入口及選取狀態，鍵盤可到。 |
| G07 P1 立場卡空白 | 採用 P1／1.00 | render:660 只讀 CFG.stance.verdicts，而 config:343 為空；syllabus 三則 summary 存在卻沒渲染。三則內容偏超音波為教材範圍建議。 | 三卡皆顯示原核准 summary；另加 XR/MRI 內容須走新內容審閱，不擅改既有醫學意義。 |
| G08 P1 掌握度斷裂 | 部分採用 P1／0.99 | 學習中/待複習未計入完成數屬真，但完成率仅算 done 不算錯誤；滿分不自動完成可保留手動自評。播放器 review→toggleDone 對 hidden #main 捲動為真 bug。 | 保留準確完成數，另清楚顯示四態；播放器待複習動作切課程並聚焦檢核；不把答對等同臨床能力。 |
| G09 P1 open 只寫不讀 | 採用 P1／1.00 | app:1063-1066 保存 bool；1246-1248 只判 null 決定首章，未還原 true/false。 | 全展開後重整仍展開；全收合保持收合；首次有合理初始狀態。 |
| G10 P1 代碼衝突 | 採用 P1／1.00 | render:554 从 ch8-u1 生成 CH8/U1，而 syllabus 章代碼 XR1。 | 對外章代碼與卡片一致；id/hash 保持向後相容。 |
| G11 P1 篩選空殼/三單元無片 | 部分採用 P1／0.99 | kind/core 只隱藏 drill，不淘汰不匹配 unit；三單元 drills=[] 已複算。ch0導讀純閱讀合理；其他兩單元影片增補是教材工作，不是資料損毀。 | 核心／類型篩選不留無匹配影片空殼；正常閱讀單元明標「閱讀」；增片先完成來源及範圍核對。 |
| G12 P1 搜尋品質 | 部分採用 P1／0.98 | glossary includes(q) 擴展短字過廣；DOM textContent 包含隱藏 rationale；播放查詢无同義詞。搜尋命中解析不等於把解析直接顯示或洩露安全機密。 | 精確別名／合理前綴擴展；只存在 rationale 的詞不命中單元；已作答解析保持可讀；跨入口詞彙相同。 |
| G13 P2 視覺噪音 | 採用 P2／0.91 | approved徽章逐卡重複，介面有多處全大寫英文；app:569-624 分類直接 anatomy 等。是密度與語言一致性建議。 | 移除不必要裝飾與代碼、介面中文化；保留可查核的審閱狀態，不把所有信任資料刪掉。 |
| G14 P2 完成粒度 | 採用 P2 改善建議／0.90 | player:200 onlyTodo 以單元 doneSet 過濾該單元全部片。並非一次把全課32片都隱藏，也不必強制追蹤每片。 | 明示「隱藏已完成單元的影片」或提供逐片看過狀態，觀看紀錄與單元掌握度分開。 |
| G15 待驗證 窄屏擠壓 | 採用並合併 C08／1.00 | 主 agent 390px 實測補上模型缺的 render 證據。 | 同 C08。 |
| G16 待驗證 首屏閃切 | 降為 P2 首屏狀態一致性／0.90 | index 的 course selected 與默认 home 存在原始標記／init切換落差；肉眼「閃」受網速/繪製時機影響尚未量測。 | 慢網路影片記錄或截圖確認首屏不短暫顯示錯誤 tab/重複 h1；不得聲稱已量得 CLS。 |

## AGY：10 項全核對

| ID／原嚴重度 | 裁決／confidence | 已確認根因與限制 | 驗收方式 |
| --- | --- | --- | --- |
| A01 P0 範圍缺強制控制 | 採用 P0／1.00 | player:141-147 无 end、預設甚至无診斷 start；seekTo 與 keys 快轉不套範圍。文案承諾已框限超過實作。跨來源 YouTube 原生控制不能被本站完整隔離，不能承諾零影格越界。 | 6片全驗 start/end；不連續範圍可各自選；筆記/鍵盤/深連結/恢復位置共用政策；失效資料不載入；來源說明準確表達限制。 |
| A02 P0 自動播放 | 降級 P1／1.00 | app:1241-1244 註解說不自動，實際 play→autoplay=1。瀏覽器可能封鎖聲音，因此「必定立即有聲」不成立。 | 重整／重新進站／回播放器為 autoplay=0；使用者明確點播放可 autoplay=1；播放位置保存。 |
| A03 P1 URL 索引覆寫 | 降級 P2 潛在資料風險／0.99 | app:1184 Map URL→單一index；支援共用影片時後者覆寫。公開資料32个URL均唯一，現況錯跳宣稱剔除。 | fixture 同影片放兩單元，點各自卡片都保持單元脈絡；保存與分享也不能只靠影片 id 判單元。 |
| A04 P1 hashchange | 採用 P1，合併 C10／1.00 | app:1264-1271 只處理 play，與初載單元 hash 行為不一致。 | 單元/章節 hashchange、popstate、上一頁/下一頁同一解析流程且有可見目標。 |
| A05 P1 播放器 review | 採用 P1，合併 G08／1.00 | toggleDone review 分支展開與 scrollIntoView 但 #main hidden，未切分頁。 | 待複習單元在播放器按完成，顯示課程且焦點落檢核。 |
| A06 P1 URL格式失去筆記 | 降級 P2 潛在資料風險／0.99 | build:96-108,377 用原始URL；支援多種YouTube寫法却无 canonical key。現資料 32 份段落均正確配對，不能聲稱現在丟筆記。 | 短/長URL及時間參數 fixture 配對同影片；遇同 id 不同審閱內容不可默默覆寫。 |
| A07 P2 隱藏寬度歸零 | 採用 P2／0.99 | initResizer在初始player隱藏時執行；clamp上限0，使 initial 样式成260。只初始化 style，未立即覆寫localStorage，故「永久存檔重置」需降為這次畫面尺寸錯誤。 | 先儲存寬度如420，從首頁啟動後進播放器仍420（視可用寬度合理夾限）；無0寬計算。 |
| A08 P2 lastUnit失效 | 剔除／0.02 | 雖未在load處過濾，但renderHome:633-635已以units.find解析 lastUnit，找不到退回first；按鈕用resume.unit.id而非儲存壞值，主張不成立。 | 可保留 stale id→第一單元回歸例；不為誤報加重複狀態清理。 |
| A09 P2 建置URL不阻斷 | 部分採用 P2／0.99 | build:556-566 只印URL警告，確實不加problems。但audit.py:705-718會報缺/壞URL、Makefile:70 check包含audit，不能推論整套CI無閘門。 | build單獨也對缺/壞URL非零退出；保留現有audit。依實際部署命令判斷是否有繞過check，勿臆稱已有缺陷片上線。 |
| A10 P2 origin寬鬆 | 採用 P2／1.00 | keys:34 includes(youtube) 且無event.source匹配；可接受外部視窗的偽造播放器狀態。攻擊需取得window reference並可發message；未證明任意網域可直接接管網站、XSS或讀資料。 | 同時精確origin、current iframe contentWindow、事件型別與值範圍；惡意包含youtube的來源、錯iframe、非finite值不改狀態。 |

## Qwen：7 項與 2 項待驗證全核對

| ID／原嚴重度 | 裁決／confidence | 已確認根因與限制 | 驗收方式 |
| --- | --- | --- | --- |
| Q01 P0 數量／草稿衝突 | 剔除／0.01 | 報告自己列14/32一致，只猜若有draft才錯；實際14全approved且具名。不能把待查條件當P0。 | 保留資料統計與審閱閘門；不為模型猜測改正確數字。 |
| Q02 P0 核心數量 | 剔除／0.01 | 複算8core+24extension正確，config定義tier標籤不必同時設定數量上限。 | 建置衍生統計即可。 |
| Q03 P1 中英混用 | 降級 P2，合併 G13／0.96 | hands-on training、credentialing及裝飾英文確存在。可以中文化，但credentialing不可草率翻為「執業認證」而改變機構授權概念。 | 統一「實機操作訓練」「機構資格審核／授權」等適合現有語境文字；必要專業縮寫保留。 |
| Q04 P1 狀態標示 | 永久錯誤顯示宣稱剔除／0.05；初始文案改善合併G04 | app:251已動態呼叫courseReviewLabel覆寫index初值。另「醫療審閱通過」不是合理修法：本課記錄明訂策展審閱不背書第三方臨床內容。 | 動態與初始皆使用準確策展措辭，與G04一起處理。 |
| Q05 P1 收錄規則技術化 | 降級 P2／0.97 | config:379把yt-dlp/oEmbed工程細節放學員須知。是閱讀負荷建議，不是醫療缺陷。 | 對外說來源／資格／字幕／可播放狀態已查核；工具與稽核紀錄保留於維護文件。 |
| Q06 P2 導覽僅代碼 | 剔除／0.01 | app renderNav:325-338以code找chapter，並輸出ch.title；報告未查到呼叫鏈。真正代碼衝突在G10，不是此條。 | 無需補不存在的標題映射。 |
| Q07 P2 required views | 採用 P2／1.00 | config:356學員步驟確留required views；與同頁「必備視圖」不一致。 | 使用「必備視圖清單」等現有一致用詞，不改醫學內容。 |
| Q08 待驗證 cutoff過時 | 剔除／0.00 | cutoff不是內容截至日。audit_medical:505判content_date < cutoff需經典例外；brief明示2021-08-01之後近期影片。教材有2026-03-06日期。 | 保留近期門檻及經典例外；不得把網站標成僅更新至2021。 |
| Q09 待驗證具名簽核 | 缺少記錄宣稱剔除／0.01 | 14個單元皆approved及reviewed_by，字段齐全。README「醫師簽核」仍可精確改成「具名策展審閱」，但不是Qwen所猜的未簽核。 | 數據驗證保留；文案與review_note的策展責任一致。 |

## 主 agent 實測補充的獨立根因

**H01 P0：切回播放器空白（confidence 1.00）。** 公開 app.js `setTab` 離開player呼叫stop，player.js stop移除iframe並清currentItem；回player只refreshPlaylist/fitFrame，未play或resume。不是YouTube偶發網路故障。驗收：播放A至已知時間→課程→影片，iframe恢復A及位置；不自動有聲播放；重整同樣可恢復；切B不套A的位置。

## 當前修復中的補充風險與驗收界線

下列讀於修復途中，主 agent 後續改動可能已處理；不能當成最終版本結論。

1. `playback-policy.js` 已建多區段解析與origin+source精確判定，方向符合A01/A10。自動監聽只能依YouTube遙測回覆執行，仍不可保證原生拖動、網路延遲或原站播放零越界；對外文案必須保留這個限制。
2. `app.js` 新的setTab/goToUnit有聚焦，但讀取時playAt仍會重建換片按鈕與playlist卻不還原焦點。C06須以鍵盤換片獨立驗收，不能只驗切分頁。
3. `keys.js` 已避免Space/箭頭攔截原生控制，並改用dialog；仍需確認全域單字母快捷鍵是否有停用/重設途徑。C04兩部分不能以其中一項完成代表全部。
4. 新搜尋索引以教材資料取代DOM包含解析，有助G03/G12；需確認課程搜尋、播放清單、段落高亮都用一致別名。搜尋結果自身包含影片/段落/單元三種記錄，結果數不得直接叫「影片數」。
5. 新增運動傷害超音波候選屬本輪使用者另加需求，應獨立核對來源、字幕、可嵌入、講者、診斷範圍與內容審閱；不能以本份UI稽核代替教材驗收，也不能把候選檔寫入成功當作已新增可學習內容。

## 整合優先序與完成證據

- **P0**：手機導覽可點、播放器返回與位置、初訪/歷史深連結、診斷播放範圍與正確限制說明。
- **P1**：鍵盤/焦點/標題與控制語意主要障礙、搜尋命中並跳段、續讀與複習、學習順序、三影像主軸、空立場卡、審閱文案、展開狀態、篩選空殼與章代碼。
- **P2**：非阻斷狀態可及性、語言與密度、重繪/拖曳效能、無JS正文與lastmod、未來共用影片/URL格式健全性、建置單獨閘門、訊息驗證。

完成證據須同時包括適合的資料／函式測試與真實瀏覽器流程。建置、離線稽核、語法檢查與既有測試全綠只能證明它們覆蓋的範圍，不能自行證明上列UI情境、教材新增或正式站發布完成。本報告不宣稱Core Web Vitals、對比度、WCAG全站合規或影片來源可用性已量測通過。
