# 進階內容 multi-LLM audit：Pass 2 對抗驗證

日期：2026-09-08。角色：獨立唯讀驗證，不核准教材，不修改正式資料。此報告判斷的是本輪受稽核版本，主流程仍在建立新的進階草稿，不能將草稿數量併入已輸出課程。

已完整讀取四份原始報告（共 252 行）：`/tmp/knee-advanced-audit/out-codex.md`（37 行）、`out-grok.md`（116 行）、`out-agy.md`（51 行）、`out-qwen.md`（48 行）。逐項對照 syllabus、questions、glossary、相关 segments、config、build 的輸出選擇、app 的進度與評分、render 的來源和通知、filters、playback-policy、player、CSS。下列 confidence 是「所拆分缺陷成立」的信心；**低於 0.70 不列必修缺陷**。建議有價值不等於現有實作有錯；P0 也不直接沿用外部模型標籤。

## 自行重算的基準

| 項目 | 實際數量與計算口徑 |
|---|---|
| 章／單元 | 9 章、18 單元；所設定章節的 unit 均 approved |
| 影片 | 38 個 drill 項目、36 支不同影片；core 8 項、extension 30 項 |
| 模態 | XR 7 支、US 13 支、MRI 16 支；US 有 15 個項目，因 Onishi、Kira 各在兩單元使用 |
| 片段／問題 | generated `segment_count=354`；60 題全部 single；difficulty core 48、extension 12、advanced 0 |
| 單元 level | foundation 9、intermediate 6、advanced **3**：`ch6-u1`、`ch7-u1`、`us-sport-hamstring-calf`；MRI 的 4 個單元均 foundation |
| 其他 | reference catalog 31；glossary 120；source_cases 1 個 AMSSM 網頁連結，不是新增影片 |
| 輸出一致性 | `dist/course.json` metadata 與上列單元／影片／題目計算一致；原資料中的工作流程字串 draft 不能當作未輸出單元數 |

因此 Codex 的「39 video-like URL、37 unique URL」是把病例網頁混入的 URL 統計，不能拿來報影片數；Grok 影片與題數正確，但「唯一 advanced 單元」錯誤。影片完整長度亦不等於可採用的診斷片段時數。

查核快照 SHA-256：

```text
syllabus.json  1e1eba9229a07157a6a0cf46443bae18b54a8dc7aa9088e2ce539490ee00cf7b
questions.json 19e8413405a33f87fc18f741068c35787ca154865e8577d94a22982f221c7583
segments.json  5d0da967e7e5e4792a6f63c0b2ed6dc4be76ea3aac43b8cf69f5226cae878a19
glossary.json  bf27679cfcf46813a129b609eab994ffb111518f385757574cb758d73878f8ef
course.config.json ce8181806c8acc4a53621b0089cdeb08f0c0bea3ce384d146a9b2a52e39d4dc2
dist/course.json   35ef6b1f65ff5d98b7df1a34fbaebb91da2a06ddf9e94eb1b6549154bb3de3df
```

## Codex：7 項逐一裁決

| ID | 拆分後結論 | Confidence／裁決 | 實際證據與修正方向 |
|---|---|---|---|
| C1 | assessment 要求病例實作，但網站沒有交付可操作影像病例包／盲測流程 | 0.99；接受，P0 降 P1 | `ch11-u1`、`mr3-u1`、`mr3-u2` 的 assessment 明寫給病例；正式資料與前端無 DICOM／序列病例 schema、標註／量測／報告提交。這是進階學習交付缺口，並非已發生病人傷害。未解鎖的新草稿不算已解決。|
| C2 | 60 題單選不足以證明專業判讀能力 | 1.00；接受，P0 降 P1 | `app.js:425–455` 按 option.correct 算分；沒有影像表現或評分規準。新增開放式 reasoning／報告有用，但不能聲稱自評就是通過能力測驗。|
| C3 | 自標完成與掌握程度混淆 | 0.94；接受 P1 | `toggleDone` 可直接切為 done；aria-label 寫「掌握度」；首頁只計 doneSet。改為自記學習進度，另呈現答題／病例實作紀錄；不必建立假的專科證照。|
| C4 | 督導考核只在文字，沒有提交／回饋紀錄 | 0.99；接受 P1 | `ch7-u1.assessment` 要最低影像集與督導回饋；前端只存 answered/correctAt。不把線下作業說成線上已實作。若不提供上傳，需清楚標為督導下的離線練習。|
| C5a | 外部公開病例不等於未知答案盲測 | 0.99；接受 P1 | `source_cases` 明載未複製影像；觀看原頁會看到答案。需要病例授權、去識別與獨立答案處理才可稱盲測。|
| C5b | source_links 在作答前直接洩漏來源 | 0.05；剔除 | `render.js:485` 生成 DOM，但 `clinical.css:739–740` 預設 display:none，僅 `.Quiz__form.is-graded` 顯示，`app.js:434` 提交後才加 class。CSS 先隱藏符合此普通自學測驗；DOM 可被開發工具檢視則表示它不是高風險考試系統，不能當成一般 UI 洩漏缺陷。|
| C6 | difficulty 文件與資料不一致 | 1.00；接受 P2 | `questions._doc` 定義 core/advanced，實際新增題為 extension；`render.js:481` 原樣顯示英文。可明確定義 extension 或統一層級，不必強制增加 expert 標籤。|
| C7a | 影片數被冒充醫師能力證明 | 0.10；剔除 | UI 寫「個影片項目」「支精選影片」「學習進度」，頁面／assessment 已有 credentialing 限制；不存在此直接等同。|
| C7b | 新能力路徑應另報可實作病例與回饋 | 0.92；接受為 C1/C2 的改進方向 | 避免重複記缺陷；36 支與 38 項已分開，沒有影片數灌水的證據。|

## Grok：8 項與其補強建議

| ID | 拆分後結論 | Confidence／裁決 | 實際證據與修正方向 |
|---|---|---|---|
| G1 | root/ramp/移位碎片已有影片，但缺乏對應進階任務 | 0.99；接受，P0 降 P1 | 實讀 `DoyfsqfuLAw` 06:01–10:18、`hDwxyjJIdHk` 08:10–12:40：有 root、ramp、flap、bucket-handle 與術後。`ch11-u1` 目標只概括形態，4 題不測逐平面 root/ramp/碎片定位。不可說現有影片沒有這些內容。|
| G1b | 必須把 extrusion ≥3 mm 當成完成標準 | 0.35；剔除該強制數值建議 | 既有影片使用 3 mm，但進階應記錄毫米、部位、平面與連帶所見，避免以單一門檻替代診斷。最新 [SSR 2026 共識](https://pubmed.ncbi.nlm.nih.gov/42283751/) 支持描述式報告與標準量測。|
| G2 | ACL 當下缺伴隨損傷清單；PLC 以可選解剖延伸為主 | 0.98；接受，P0 降 P1 | `ch11-u1` 沒有串起 root/ramp/PLC；`mr3-u1` 4 支皆 extension、foundation/anatomy。LaPrade `3tQZa_6rEW0` 已有多韌帶損傷，Agten `P3Qoj2nyw78` 已講 ACL/PCL 伴隨，屬教學組織不足。|
| G2b | core-only 是否隱藏 extension | 1.00；確認原報待驗證項 | `filters.js:91–106` 按 learningTier 隱藏 drill，零符合影片的整個單元也隱藏；故 MR3-u1 在 core-only 不見。適合建立進階必學路徑，無須把所有延伸一律改 core。|
| G3 | 軟骨修復術後教學缺口 | 0.99；接受 P1 | `mr3-u2` 影片是原生軟骨形態＋ACL graft；required_views、題目未涉及 OATS/ACI/MACI/microfracture 術後。|
| G3b | 「軟骨與術後」章名必然虛假，必須改名 | 0.50；剔除強制改名 | 該名稱亦可表示軟骨病理與其他術後並列，已有正文界定；新增具體範圍更清楚，但不足以判定標題欺瞞。|
| G4 | SIF 缺陽性對照、獨立任務與命名更新 | 0.97；接受 P1 | `mr3-u2` 已有骨折帶、T1、流體序列與骨髓鑑別的目標／required_views，不是「完全無視圖」。Kijowski 11:35–12:37 是未見骨折線的案例；無 SIFK glossary 或專題知識題。|
| G4b | SIF/root/extrusion 關聯毫無資料 | 0.25；剔除 | 現有 Kijowski 筆記已提 extrusion，且 [2023 root/ramp review](https://pubmed.ncbi.nlm.nih.gov/37384542/) 與 [2023 SIF review](https://pubmed.ncbi.nlm.nih.gov/37782395/) 可支持關聯；應補明確引用，不應說未知。|
| G4c | 「沒有骨折線就不得報 SIFK」 | 0.02；剔除，有害的過度絕對化 | 應仔細尋找低訊號帶並整合分布與病史，不能將未辨識骨折線當充分排除。原出版社 [SIF 影像討論](https://www.thieme-connect.de/products/ejournals/html/10.1055/a-2344-5337) 明述初期 fracture line 可能不可辨識。也不能反過來把所有水腫命名 SIF。|
| G5a | 腓總神經病變／真正彈響 cine 不足 | 0.98；接受 P1 | `ch4-u1` 神經是解剖追蹤，唯一片是旁半月板囊腫；snapping content_boundary 明寫病例 cine 未附。|
| G5b | 全站動態 US 都沒有，dynamic 單元必須全部降級 | 0.15；剔除外推 | Pedret 有動態正常與腱膜傷害；Kira 09:52–12:08 有 LCL 連續性／內翻示範。缺的是病理彈響循環與條件完備的應力訓練，正常動態與病理 cine 不能混為一談。型別代表主題，不等於聲稱每項已示範；保留範圍说明並補 cine。|
| G6a | 進階 MRI 在 core-only 路徑不足 | 0.99；接受 P1，與 G2 合併 | 8 個 core 項目；PLC、ACL 術後均 extension。不同程度可以有不同必學集合，不能用只看 foundation 影片作為高階完成依據。|
| G6b | 全課唯一 advanced 單元是 calf | 0.00；剔除 | 自算 advanced 3 個，包含 ch6-u1、ch7-u1。MRI level 不適切則成立。|
| G7 | 半月板術後沒有專屬對照／正向作業 | 0.96；接受 P1（原 P2） | `mr3-u2` 已有術後半月板 required_views、資料比對和限制；Dong 11:24–12:40 有術後教學。缺成組再撕裂與預期變化的應用，不能說僅有一句免責。|
| G8 | 沒有 advanced 題、glossary 缺 ramp/SIF | 1.00；接受 P2 | 數據吻合；補標籤不能取代更高認知任務，與 C6、G1、G4 合併實作。|

Grok 六個建議模組的優先方向大致合理；只有實際完成來源、內容與作業後才能改成「已涵蓋」。兩平面／連續切面是判讀策略，不能將所有病理或術後情境壓成無例外的必要充分診斷條件。

## AGY：6 項逐一拆分

| ID | 拆分後結論 | Confidence／裁決 | 實際證據與修正方向 |
|---|---|---|---|
| A1a | 相同 hash 證明偽冒批准 | 0.00；剔除 | `2026-09-08-sports-ultrasound-approval.json` 明確綁整個 4 單元 proposal，非單支影片內容 hash。實際重新 SHA-256 得 `f15403…6a41`，與所有引用一致；批准語句「可以收錄」、語義、基底 commit 與限制都有記錄。|
| A1b | 每片 intervention_timestamp_note 混入其他講者 | 1.00；接受 P2 | 6 個項目都寫 Rao/Pedret 的同一段通用說明；Onishi、Kira 個別欄位不精確。各片 scope_note 與時間範圍則有分開。應改成各自時間註記，不能據此推斷所有來源審查虛假。|
| A1c | recording date/disclosure 未完全查得，因此批准不實 | 0.05；剔除 | 原始錄製日期為 null 附 date_note，沒有虛填；`audit_medical.py:405–417` 明允許未知但需註記。disclosure 如實記未知，三支 2020 有經典例外理由，已具體策展批准；這不是第三方醫療背書。|
| A2 | Matt Waldrop 資格 URL 只指影片本身 | 0.98；接受 P2（原 P1） | `HD4KGcpu7C8` 確為自身 URL，缺獨立機構資格佐證；但 AMSSM 官方具名來源不是零證據，`curation_status=provisional` 亦有說明。不應宣稱已證實假醫師，補機構頁即可。|
| A3 | snapping 單元沒有病理彈響 cine | 1.00；接受 P1 | 只有 Kira 一片，boundary 明確；與 G5a 合併。|
| A4a | ESSR unlisted 就是不可公开合法觀看／不合格 | 0.05；剔除 | 本地 playback_status 寫官方 e-learning 直接連結、公開 playback 與 embed 確認；unlisted 是不列搜尋，不是 private。任何第三方影片都會有失效可能，不能僅因 unlisted 推定較不永續。|
| A4b | ESSR 精確原錄製日尚未核實 | 1.00；接受 P2 已知保留事項 | 兩片 date_note 與 pending-date-verification 正確揭露 2021 年與 cutoff 邊界不明；應持續查證／保留標註，不能擅寫 2023 錄製或宣稱違反批准。|
| A5a | Pedret 未設定 31:12 後邊界，播放邏輯失效 | 0.00；剔除 | `diagnostic_segment_range=09:44–31:12`；`playback-policy.js:25–32` 正是讀該欄。`player.js:226–232` iframe 有 end、206–214 邊界外暫停；不是按 intervention_start 截斷。start/end 也不是隔離原平台或逐影格保障，既有範圍聲明有講清楚。|
| A5b | 介入通知文字把第一個時間後全部描述為操作示範 | 0.96；接受 P2（驗證時另定位） | `render.js:59–61` 固定寫「自…起包含注射／介入操作示範」；Rao 19:00 與 Pedret 09:20 其實是討論／內視鏡例子，不全是注射示範，而且後面可能再有診斷段。應用個別 scope_note 中性的「原片含處置相關內容」；不需改播放演算法。|
| A6a | 空 drills 單元 approved 即交付違規 | 0.10；剔除 | US1 config quota 本來就是 2 單元／0 影片；orientation、foundation 有文字與文獻，審閱批准不以有影片為必要條件。US4 分開 pathology 理論與 reporting survey，同樣不是缺資料錯誤。|
| A6b | 應明確顯示文字／掃描清單學習形式 | 0.75；接受 P2 UX 建議 | 有助說清影片項目为0的學習方式；不能稱內容虛假，亦不要求灌入無關影片。|

## Qwen：8 項逐一裁決

| ID | 結論 | Confidence／裁決 | 真實題幹、所有選項與解析核對 |
|---|---|---|---|
| Q1 `ch11-u1-q4` | 已處理影像與症狀／治療邊界，沒有被指稱的誤導 | 0.05；剔除 P0 | 正解標準命名與臨床脈絡；錯選「直接歸因疼痛」明確駁回。報告自己也承認處理正確，再加免責不是修錯。|
| Q2 `us-sport-collateral-q1` | 屍體閾值被直接套入活體 | 0.15；剔除 P1 | 正解只是記錄方向、角度、位置和對側條件，沒有任何數值閾值。單元 key_points、pitfalls 與 assessment 三處已明確禁止屍體 cutoff 泛化。可追加單題提示，但無證據支持現有過度承諾。|
| Q3 `us-sport-extensor-q3` | 沒寫個人預後限制 | 0.00；剔除 | 錯誤選項 B 的 rationale 已寫「群體風險關聯不能精確預測個人的疼痛時間」。Qwen 只讀正解解析漏掉另選項；其建議「證明非相關性」又比原文「不等於」更絕對，不能採用。|
| Q4 `ch8-u1-q1` | Ottawa rule 被誤作骨折確診 | 0.05；剔除 | 題幹問是否照 X 光，正解不宣告骨折；rule 任一陽性應進行 X 光的用途清楚。不能把正確照影像決策改成「陽性仍可不照」式模糊建議。|
| Q5 `ch10-u1-q2` | Magic angle 沒有限定序列 | 0.00；剔除 | 題幹與正解都寫短 TE；錯選 C 要長 TE／多平面驗證。Qwen 的 T1/T2* 分法易漏 PD 等短 TE 序列，且 fat suppression 不消除 magic angle；不採用。|
| Q6 `mr3-u1-q2` | TT-TG 沒註明切點限制 | 0.00；剔除 | 正解解析已寫序列／族群影響，C 寫單一值不是診斷，D 寫報告記載方法。另有不同的真錯誤見 N1。|
| Q7a `ch9-u1-q3` | CT 是唯一合理途徑的說法需要上下文 | 0.65；不列必修缺陷 | 現有選項中 CT 追查是合理答案，沒提供 MRI 選項不代表否定 MRI；可在進階升級模組補情境，不強制改掉答案。|
| Q7b | 因腎功能／對比劑禁忌改用 MRI 的建議 | 0.02；剔除 | 隱匿骨折 CT 常不需 IV contrast；[ACR](https://acsearch.acr.org/docs/69419/Narrative/) 相應情境列 MRI without contrast Usually Appropriate、CT without contrast May Be Appropriate。不得新增不相干的對比劑限制。|
| Q8 `ch5-u1-q2` | 沒有動脈瘤壓迫風險警示 | 0.00；剔除 | 選項 C 解析全文是「壓力會改變外觀，且對動脈瘤加壓有風險」；報告漏掉後半。毋須另加未在原題證據中證實的破裂敘述。|

## 獨立發現與處置優先

**N1，P1，confidence 0.99：TT-TG 錯誤選項解析方向反了。** `mr3-u1-q2` 選項 B「CT 與 MRI 的 20 mm 切點通用」是錯選沒問題，但 rationale 寫「會系統性高估異常比例」。同題與單元已指出 MRI 通常較 CT 低；把較高的 CT threshold 套至 MRI，方向應是可能低估／漏判，不是高估。 [CT/MRI 成對研究](https://pubmed.ncbi.nlm.nih.gov/25575535/) 證實 MRI 系統性較低；不宜聲稱所有族群固定差。最小修正為「兩種模態量測與切點不可直接互換，應採用與影像方法及族群相符的判準」。此次僅指出，未改動原批准題組。

真正優先項為病例應用與回饋（C1–C4）、root/ramp/伴隨傷搜尋（G1/G2）、術後軟骨與半月板、SIF 對照、周邊神經與病理動態（G3–G7），加上 N1。它們支持「目前不足以證明獨立專科能力」，但不能支持「所有現有內容只有入門」或以某固定影片數保證頂尖水準。

metadata 的 A1b/A2/A4b/A5b、層級 C6/G8 是具體次優先事項；不要為通過 audit 而虛填來源日期、宣告所有影片醫學內容已背書，或悄悄改舊批准內容。進階草稿此時有 7 個 module_drafts，仍為 draft，作業與題目由主流程編輯中，**未在此报告宣告其已符合所有缺口或已獲批准**。

本次沒有重跑 build 或瀏覽器測試，因未修程式；完成的是 JSON 自行統計、摘要 hash 核對、flagged code/data 閱讀與針對性原始來源查核。此報告不是醫療背書或發佈簽核。
