先讀稽核範圍與課程材料，只做唯讀涵蓋度與學習順序分析。接著讀課程設定與大綱，並核對影片、題目與逐段筆記的實際內容深度。開始核對單元、影片、題目數量，並用關鍵詞搜實際教材深度，不把影片標題當充分證據。接著讀進階單元本文、題目與逐段筆記，核對缺口是深度不足還是完全沒有。# 膝關節影像課程：進階涵蓋度與學習順序稽核

材料盤點（`course/data/syllabus.json`、`course/course.config.json`、`course/data/questions.json`、`course/data/segments.json`）：9 章、18 單元、drill 槽位 38、不重複影片 36、知識檢核 60 題（`difficulty: core` 48、`extension` 12、`advanced` 0）。`learning_tier: core` 僅 8 支。觀看公開影片或通過本課題目，不構成合格醫師、credentialing 或量表認證。

缺口狀態（不以影片標題為充分證據）：

| 主題 | 狀態 |
| --- | --- |
| 半月板 root／ghost／extrusion | **已有、深度不足**：core 片末段有病例，單元目標只列命名 |
| ramp | **已有、深度不足**：兩片逐段筆記有詞，單元目標／必備視圖／題目／名詞表皆無 |
| 移位碎片（bucket-handle／flap） | **已有、深度不足**：目標列 bucket-handle 名稱；flap 搜尋未寫進必備視圖與檢核 |
| 半月板術後 | **已有、深度不足**：`mr3-u2` 文字＋Dong 片末段；無專屬 drill、無正向考題 |
| PLC | **已有、深度不足**：解剖＋一則完全損傷病例，全標 extension，單元類型為 anatomy |
| ACL 伴隨損傷 | **已有、深度不足**：病例與筆記出現，ACL 教學當下不要求搜尋清單 |
| 軟骨術後（修復／移植） | **完全沒有** |
| SIFK | **有詞無模組** |
| 神經 US | **已有解剖路徑、無神經病變模組**（隱神經僅選掃筆記） |
| 動態 US | **單元殼有、可觀看動態 cine 不足**（彈響單元自承未附） |

---

## P0

### P0-1 半月板 root／ramp／移位未從影片筆記升成可考核搜尋路徑

- **檔案:行號**：`course/data/syllabus.json:1995-2025`；`course/data/questions.json:1241-1366`；`course/data/segments.json:2833-2866`、`2982-3024`；`course/data/glossary.json`（無 `ramp` 條目）
- **問題**：進階徵象被塞進 MR2 單一 `level: "foundation"` 單元，與撕裂門檻、ACL bone bruise、Englund 證據邊界並列。學習者若只完成單元文字與四題 core 檢核，可以「過關」而不會做後根雙平面追蹤、ramp 或移位碎片定位。
- **精確證據**：`ch11-u1` 目標把 root tear 寫成型態命名之一，未列 ramp、未要求 ghost sign、未要求 extrusion ≥3 mm、未要求 displaced fragment 位置。`key_points`／`required_views` 停在「訊號是否延伸至關節面」。四題分別考撕裂門檻、pivot-shift 挫傷、Englund、報告態度；root tear 只出現在錯誤選項（`ch11-u1-q2`）。相對地，core 片 `DoyfsqfuLAw` 06:01–10:18 已示範完全後根 radial tear（extrusion、shiny corner、ghost sign）、horizontal flap 落入 meniscotibial recess、ACL 背景下 ramp；extension 片 `hDwxyjJIdHk` 另有 ramp≈急性 ACL 12%、Wrisberg rip、縮小半月板須鑑別術後。單元 `assessment` 要三組病例，實際 MCQ 未對應。
- **具體補強**：在 MR2 撕裂門檻之後、MR3 之前拆出獨立進階單元（見模組 1）。把 Ahlawat／Dong 既有段落寫進 `objectives`／`required_views`／`key_points`；新增 `difficulty: advanced` 題，題幹限該單元已寫內容。`glossary` 補 ramp。Core 標籤改到含搜尋路徑的片，或取消「只看核心必看」對此單元的可跳過性。

### P0-2 ACL 診斷當下沒有伴隨損傷必修清單；PLC 被放在可跳過的解剖延伸

- **檔案:行號**：`course/data/syllabus.json:1885`、`2003-2016`、`2035-2046`、`2159-2254`；`course/course.config.json:131-132,282-305`；`course/data/questions.json:1276-1300,1379-1406`；`course/data/segments.json:3283-3289,3356-3363`
- **問題**：學習順序把 ACL 放在 MR1／MR2，把 PLC 放在 MR3 且四支影片全 `learning_tier: "extension"`、單元 `type: "anatomy"`、`level: "foundation"`。進階判讀需要的「看見 ACL 就強制搜尋 ramp／root／PLC／ALL」沒有出現在 ACL 教學點。MR1 core 片 `scope_note` 寫後外側角由「同單元其他影片補」，實際專責內容在後一章且非 core。
- **精確證據**：`ch11-u1` ACL 目標只有纖維中斷、走向、pivot-shift bone bruise、Segond；`key_points` 無伴隨清單。`mr3-u1` 目標是逐段追蹤 LCL／FCL、股二頭肌、膕肌與次要韌帶，題目考追蹤方法與 TT–TG，不考 ACL／PCL 共存。Agten PLC 解剖 09:12–10:12 寫 PLC 常伴隨 ACL 或 PCL、未治可能造成 ACL graft failure；LaPrade 病例 03:48–05:21 同時有 ACL 完全中斷、PCL 近乎完全斷裂與 PLC 三大結構撕脫。這兩支皆 extension、2015／2019 classic exception。全課 core 影片僅 8 支，MR3-u1 為 0。UI「只看核心必看」是否真的隱藏 extension：**待驗證**（未讀前端；config 有 `coreOnlyLabel`）。
- **具體補強**：在 ACL 單元當下插入伴隨損傷檢核（模組 2），完成前不得進入「ACL 已評估」。將 Agten 解剖＋LaPrade 病例改為 MR3 core，單元改 pathology／case，目標明寫交叉韌帶共存與 graft 失敗風險（模組 3）。禁止用看過 PLC 片代替這份搜尋產出。

---

## P1

### P1-1 章名「軟骨與術後」中的軟骨術後完全沒有

- **檔案:行號**：`course/course.config.json:292-305`；`course/data/syllabus.json:2156,2321-2353,2373-2387`
- **問題**：MR3 標題與 `mr3-u2` 名稱含術後，術後實際只教 ACL graft 成熟／撕裂徵象與半月板修補限制。軟骨修復、OATS／ACI／MACI／microfracture 的預期訊號、填塞整合與失敗徵象在單元目標、必備視圖、drill、題目中均不存在。
- **精確證據**：`mr3-u2` 三支片為軟骨形態分級（Kijowski，core）、ACL graft 訊號、ACL graft 完整性（皆 extension）。`objectives` 第四條術後只提 ACL graft 與半月板修補對照。Kijowski `scope_note`：定量 mapping 不在範圍；未提修復術後。題目 `mr3-u2-q1`–`q4` 為深度分級、外傷／退化形態、graft 第一年高訊號、影像與臨床失敗相關性有限。
- **具體補強**：若維持章名，必須新增軟骨修復術後模組（模組 5 的新建部分）。若無合格片源，單元與章名應改為「ACL／半月板術後」，並在單元正文標「軟骨修復術後未涵蓋」，避免標題造成已教完的假象。

### P1-2 SIFK 只有警示用語，沒有鑑別模組

- **檔案:行號**：`course/data/syllabus.json:2023,2330-2348`；`course/data/segments.json:3970-3987`；`course/data/glossary.json`（無 SIFK／SONK／subchondral insufficiency fracture）；`course/data/questions.json`（無對應題）
- **問題**：骨髓水腫鑑別被寫進陷阱與目標，但沒有必備視圖、陽性病例、名詞表或考題。唯一影片段落還是陰性例子。
- **精確證據**：`ch11-u1` pitfalls：「漏掉應力性骨折、軟骨下不全骨折」。`mr3-u2` 要求依骨折線與軟骨下位置鑑別挫傷／應力骨折／不全骨折，`key_points` 描述「近乎平行軟骨下骨板的低訊號帶與廣泛周邊水腫」。Kijowski 11:35–12:37：大量 BME 時找 fracture line 以區分退化性水腫與 subchondral insufficiency fracture，**本例未見到骨折線**。無 SIFK 專名、無與 SONK 舊名關係、無與 root tear／extrusion 的教學連結（該片只口頭說不全骨折常見於軟骨流失合併 extrusion）。
- **具體補強**：獨立短模組（模組 4），必備視圖寫清找平行軟骨下低訊號帶的平面與序列；至少一則陽性對照（現有片為陰性，需另策展或在單元文字用既有描述做「找不到骨折線就不能報 SIFK」的產出）。補 glossary 與 advanced 題。SIFK 與 root／extrusion 的關聯標 **待驗證**（材料僅有講者一句，單元未寫入）。

### P1-3 神經／動態超音波：路徑與單元類型在，病理與可觀看動態不在

- **檔案:行號**：`course/data/syllabus.json:1292-1324,1369-1393,1475-1507,1175-1226,1507`；`course/data/segments.json:4256-4262`（Onishi 片隱神經選掃）
- **問題**：進階 US 需要神經病變判讀與可重現的動態 cine。現況是腓總神經／脛神經當解剖地標，彈響與應力單元承認影片沒有該動態。
- **精確證據**：`ch4-u1` 目標含腓總神經連續追蹤，陷阱是過度壓迫或單截面；drill 是半月板旁囊腫病例，不是腓總神經病變。`ch5-u1` `type: "dynamic"`，重點是 Baker cyst 頸部與 DVT 邊界。`us-sport-snapping` `content_boundary`：「本批沒有收錄該病例彈響 cine；Kira 也明說 ITB 病例的動態影片未附」。`us-sport-collateral` 要保存外翻／內翻循環，Onishi 片 `scope_note`：「跳過動態半月板延伸推論」；Kira 片同樣未附動態。隱神經在 Onishi 逐段筆記為選掃且「本例正常」，無單元目標。
- **具體補強**：模組 6。在 `ch4-u1` 之後加腓總神經病變病例（腫脹、束狀結構喪失、繞腓骨頸卡壓）。動態單元必須有可嵌入、有字幕的完整屈伸／應力循環，否則把 `type: "dynamic"` 降回 anatomy／pathology，並在目標刪除「已示範動態」的暗示。隱神經維持選掃，但要有異常對照才算進階。

### P1-4 「核心必看」把進階 MRI 編成可跳過延伸

- **檔案:行號**：`course/course.config.json:169-178,131-132,282-305`；`course/data/syllabus.json:1998,2161-2162,2197-2310,2389-2444`
- **問題**：學習順序用 core／extension 暗示進階可選。PLC、髕股量測、ACL 術後兩集全是 extension；唯一 MRI 進階章的損傷單元被標 anatomy＋foundation。
- **精確證據**：全課 8 支 core：XR 各 1、ESSR 膝 Part 1／Part 2、Dixon 入門、Ultimate Guide、ISMRM 半月板 essentials、Kijowski 軟骨。MR3-u1 四支、ACL 術後兩支、半月板分型（含 ramp 系統講解）皆 extension。`us-sport-hamstring-calf` 是唯一 `level: "advanced"` 單元，仍配 extension 題。
- **具體補強**：重新標 tier：伴隨損傷、PLC 損傷、SIFK、術後判讀改 core。`level` 與 `type` 對齊實際認知層級。Core-only 路徑的實際隱藏行為 **待驗證**。

---

## P2

### P2-1 半月板術後只有限制聲明，沒有專屬教材與正向檢核

- **檔案:行號**：`course/data/syllabus.json:2332-2353`；`course/data/segments.json:3018-3024`；`course/data/questions.json:1605-1624`
- **問題**：修補後表面相通訊號的限制已寫，但沒有修補 vs 部分半月板切除 vs 再撕裂的對照 drill。
- **精確證據**：`mr3-u2` pitfalls／assessment 提到修補後線狀訊號須對照術前與臨床。Dong 11:24–12:40：術後形態扭曲、可需 MR arthrography。`mr3-u2-q4` 正確項是「術後 MRI 與臨床失敗相關性有限」；「修補處持續表面相通訊號即代表失敗」是錯誤選項，不是要學員產出修補後判讀步驟。
- **具體補強**：模組 5 先把 Dong 末段與 `mr3-u2` 文字收成「半月板術後」必修產出（對照舊影像、fluid signal 連續兩切面、移位碎片、手術紀錄）。軟骨修復術後仍屬完全新建，不可混充。

### P2-2 檢核全無 advanced 題，名詞表不收 ramp／SIFK

- **檔案:行號**：`course/data/questions.json:22-1988`（60 題；無 `"difficulty": "advanced"`）；`course/data/syllabus.json:1554`；`course/data/glossary.json:1751-1791`（有 meniscal-root-tear、ghost-sign、extrusion，無 ramp、無 SIFK）
- **問題**：題目難度標籤與進階單元聲明不一致，無法用檢核證明進階搜尋能力。通過測驗仍只證明 core／extension 文字點。
- **精確證據**：MRI 三單元 12 題全 core。運動 US 12 題全 extension。唯一 `level: "advanced"` 的 `us-sport-hamstring-calf` 亦然。
- **具體補強**：每新增進階模組至少 3 題 `advanced`，選項 rationale 只能引用該模組已寫內容。名詞表與單元用詞對齊。

---

## 六個優先補強模組與學習產出

材料來源僅限既有單元文字、逐段筆記與引用；軟骨修復術後在材料中不存在，標為新建。完成線上模組仍不等於獨立判讀資格。

**1. 半月板後根／ramp／移位碎片（MR2 之後、MR3 之前）**
來源：`DoyfsqfuLAw` 06:01–10:18、`hDwxyjJIdHk` 08:10–11:23、`ch11-u1` 撕裂門檻。
產出：雙平面追蹤內外側 posterior root；報 ghost sign、冠狀面垂直線、extrusion 量測與位置；在 ACL 陽性時檢查內側後角 meniscocapsular 積液（ramp）與外側後角 Wrisberg rip；描述 displaced fragment 所在 recess／notch，並列 double PCL、fragment-in-the-notch。

**2. ACL 急性傷伴隨損傷檢核（插入 `ch11-u1` ACL 段，先於 MR3）**
來源：pivot-shift bone bruise 文字、Ahlawat 末例、Dong ramp／外側敏感度下降、LaPrade 共存十字韌帶。
產出：固定清單——ACL 直接徵象 → bone bruise 機轉 → 內側 ramp → 內外側 root → 外側半月板（含矢狀不易見的小 radial／bucket-handle）→ PLC 三主結構 → Segond／ALL 區。清單未完成不得寫「其餘結構未評估卻暗示全膝陰性」。

**3. PLC 損傷（`mr3-u1` 升 core，改 pathology）**
來源：Agten 搜尋路徑、LaPrade 完全損傷、Agten 09:12 伴隨 ACL／PCL 與 graft failure。
產出：兩平面確認 FCL、膕肌腱、股二頭肌；次要韌帶未顯示不報撕裂；記錄對側／內側骨挫傷機轉；強制回答是否共存交叉韌帶損傷。解剖片與損傷片成對，不可只看解剖。

**4. SIFK 與骨髓水腫鑑別（從 `mr3-u2` 抽出）**
來源：`mr3-u2` key_points 三項鑑別、Kijowski 11:35 段（現為陰性）。
產出：對廣泛 BME 必須搜尋平行軟骨下骨板的低訊號帶；能區分無骨折線的挫傷、負荷相關應力骨折線、不全骨折；沒有骨折線就不得報 SIFK。陽性病例片 **待策展**。

**5. 術後 MRI：半月板（既有升級）＋軟骨修復（完全新建）**
半月板來源：`mr3-u2` 限制文字、Dong 11:24–12:40。產出：對照術前 MRI 與 operative report；修補後持續表面訊號 ≠ 失敗；再撕裂需連續切面 fluid 或移位碎片。
軟骨修復：材料無內容，須新建預期訊號與失敗徵象；在補上之前章名不得暗示已教。

**6. 周邊神經與動態超音波**
來源：`ch4-u1` 腓總神經路徑、Onishi 隱神經選掃（正常例）、`us-sport-snapping`／`us-sport-collateral` 的動態要求與「未附 cine」自承。
產出：腓總神經繞腓骨頸全段形態＋正交異常切面；動態單元須有可觀看、有地標的完整循環，並記錄症狀是否同步。無 cine 則撤回 dynamic 類型。隱神經異常對照沒有之前，不宣稱已涵蓋神經進階。
