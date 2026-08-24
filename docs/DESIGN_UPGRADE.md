# 膝部超音波課程站升級藍圖

## A.【設計／視覺】

現況基礎良好：`tokens.css` 已具設計 token、深淺色與 `prefers-reduced-motion`；`layout.css`、`clinical.css` 也已有響應式斷點、黏性側欄和清楚的臨床工作站識別。主要差距不是「缺乏風格」，而是視覺語言偏儀器儀表板，真實醫學影像、長文閱讀性與影像標註尚未成為畫面主角。

| 優先 | 建議與現況差距 | 可落地規格 | 工作量／新資產／config 影響 |
|---|---|---|---|
| A1 | **重整字體階層。** `tokens.css` 的正文為 14px，`clinical.css` 大量 eyebrow、code、badge 僅 8–9px；英文字大寫與 tracking 過密，中文長時間閱讀負擔偏高。 | 正文桌面 16px／行高 1.7、行動版 16px；單元標題 22–24px、節標題 28–32px；輔助資訊最低 12px。中文採系統字體／Noto Sans TC，數值、影像參數才使用 mono。限制文章文字欄約 68–76ch。 | **S**；新資產：否；config：**低**，新增選用 `theme.typography`，亦可先純 CSS 完成。 |
| A2 | **降低「科幻工作站」裝飾密度。** `clinical.css` 的全頁格線、掃描動畫、發光陰影及大量 `CLINICAL MODULE`／`LIVE PROTOCOL` 標籤會與真正影像爭奪注意力。 | 保留深藍＋青綠品牌識別，但移除正文區格線與常駐 glow；HeroScan、Console monitor 改為次要裝飾或只在首頁出現。課程內頁採安靜的中性底色、薄分隔線和較少容器層級。 | **S**；新資產：否；config：**無～低**，以 CSS 和 `theme.density` 開關處理。 |
| A3 | **建立醫學語意色彩，而非只靠品牌色。** 現有 teal 同時負責品牌、選取與進度，attention/danger 又分散於 Primer 與 clinical tokens。 | 固定語意：青綠＝目前位置／互動；藍＝連結／延伸資訊；綠＝已掌握；琥珀＝陷阱／不確定；紅＝安全警示；紫＝實證／研究。所有狀態同時搭配圖示與文字，避免只靠顏色。 | **S**；新資產：否；config：**低**，將 `tone` 對應集中為 semantic token。 |
| A4 | **讓真實超音波影像成為核心視覺。** 現站只有 CSS 模擬的超音波介面和 YouTube 影像，沒有可獨立觀察的教學圖。 | 首頁以經授權的「探頭位置＋正常超音波＋標註後影像」三聯圖取代純 CSS monitor；單元首屏先展示代表影像，再進入文字與影片。影像固定黑／深灰診斷畫布，不受頁面主題反相。 | **L**；新資產：**是，影像、探頭位置照片或插圖、授權與去識別資料**；config：**高**，新增 `media[]`、來源、授權、alt、caption、credit、審閱欄位。 |
| A5 | **建立一致的標註影像語法。** Radiology Assistant 以箭頭、顏色區域和「先觀察、後解說」串起系統化判讀；AMBOSS 也將 image overlay 作為核心教學工具。[Radiology Assistant](https://staging.radiologyassistant.nl/chest/chest-x-ray/basic-interpretation) [AMBOSS](https://www.amboss.com/us/features) | 採 SVG overlay 疊在原圖上：實線箭頭＝目標結構、虛線＝邊界、半透明區塊＝ROI；提供「標註開／關」及標籤列表。正常解剖、病灶、陷阱各使用固定色彩，並提供文字等價描述。 | **M**；新資產：**是，逐圖標註資料**；config：**高**，新增 normalized `overlays[]` 座標、label、category、description。 |
| A6 | **補足影像比較版型。** 現有 `.ClinicalBrief__grid` 適合文字檢核，但沒有正常／異常、靜態／動態、超音波／X-ray／MRI 的同步比較。 | 新增 2-up／3-up compare：同步縮放、拖曳、標註開關及「共同點／差異」說明；手機改為 swipe 或上下排列，避免縮成不可讀縮圖。 | **M**；新資產：**是**；config：**中～高**，新增 `comparisonSets[]` 與各面板關聯。 |
| A7 | **完成影像安全的暗色模式。** 現有深色模式完整，但尚未處理醫學影像、annotation 和列印模式。 | 不套用 `filter: invert()`；影像區固定中性黑，overlay 需通過對比檢查；記住「系統／亮／暗」三態。列印時固定白底、保留標註並輸出影像來源。 | **S**；新資產：否；config：**低**，media 可選 `preferredBackground`。 |
| A8 | **提升觸控、可讀性與動態節制。** 現有 `:focus-visible`、reduced-motion 是好基礎，但部分 8–11px 控件和 icon-only 按鈕仍不利行動裝置。 | 互動目標至少 44×44px；停止常駐 pulse／sweep；tooltip 同時支援 focus；桌面 hover 不作為唯一揭露方式；所有影像工具列提供明文標籤或可展開說明。 | **S–M**；新資產：否；config：**無**。 |

---

## B.【介面／互動】

Radiopaedia 的病例頁把病史、影像序列、quiz mode、問題與討論放在同一病例脈絡；Radiology Assistant 常先要求學員觀察，再逐步揭露判讀；Osmosis 將流程組織成 Learn → Review → Test → Reinforce；Medality 則以病例微課程、DICOM、quiz、checklist 和 gold-standard report 模擬臨床工作。[Radiopaedia 病例示例](https://radiopaedia.org/cases/pleural-lipoma?lang=us) [Osmosis Learning Loop](https://www.osmosis.org/why-osmosis/learning-loop) [Medality](https://medality.com/cme/)

| 優先 | 學習體驗 pattern | 純靜態站可行性 | 工作量／新資產／config 影響 |
|---|---|---|---|
| B1 | **「繼續學習」首頁。** 顯示上次單元、下一個核心任務、待複習題與整體完成率；取代只有章節數量的首頁入口。 | **完全可行**，以 localStorage 儲存；跨裝置同步才需要後端。 | **S**；新資產：否；config：**低**，使用既有章節順序並加 `estimated_minutes`。 |
| B2 | **單元內固定微學習流程。** 每單元依序呈現「目標 → 正常定位 → 掃描操作 → 影像判讀 → 常見陷阱 → 自我檢核」，完成當前階段後才突出下一步。 | **完全可行**。 | **M**；新資產：視單元而定；config：**中**，由扁平 unit 擴為 `activities[]` 或標準化 section。 |
| B3 | **捲動式 ultrasound stack／cine viewer。** 滾輪、拖曳、觸控 swipe、播放／暫停、速度、frame index、縮放、重設與全螢幕；預載相鄰影格。 | **完全可行**；JPEG/WebP stack、MP4/WebM cine 可純前端。完整 DICOM windowing 則屬高成本版本。 | **L**；新資產：**是，大量去識別序列**；config：**高**，新增 stack manifest、frame metadata、poster、方向與 modality。 |
| B4 | **病例 Quiz mode。** 先隱藏標註和診斷，依序回答「定位—描述—鑑別—結論」；提交後顯示正解、理由、錯誤選項解析與相關章節。 | **完全可行**，答案與作答紀錄存 localStorage。 | **M**；新資產：常需影像；config：**高**，新增 `cases[]`、`questions[]`、choices、rationale、references、difficulty。 |
| B5 | **把二元完成改為掌握度。** 現況只記錄 unit done；改為「未開始／學習中／已完成／需複習」，並分別計算影片、病例與檢核完成度。 | **完全可行**；跨裝置同步需後端。 | **M**；新資產：否；config：**中**，activity ID 必須穩定，localStorage state 需版本化與 migration。 |
| B6 | **低負擔間隔複習。** Quiz 後讓學員選「不熟／尚可／熟練」，建立今日複習佇列；錯題在 1、3、7、14 日重現。 | **可純靜態實作個人版**；無登入時無法跨裝置或供教師追蹤。 | **M**；新資產：否；config：**中**，題目需穩定 ID、concept tags、複習規則版本。 |
| B7 | **弱點導向的 High-yield mode。** AMBOSS 會依錯題凸顯薄弱知識，並提供 High-Yield mode、難度及解析。[AMBOSS](https://www.amboss.com/us/features) | **可純靜態做本機版**：依錯題標亮相關 key point、pitfall 和病例；群體比較需後端。 | **M**；新資產：否；config：**中**，題目與 `concept_ids`、內容段落必須互相連結。 |
| B8 | **提升搜尋為「醫學索引」。** 現有搜尋是 DOM substring，已有類型、核心與肌群篩選；升級為繁中／英文同義詞、解剖區域、影像模式、正常／病理、難度、證據等級篩選，結果顯示命中片段。 | **完全可行**，build 時產出精簡 search index；篩選狀態寫入 URL。 | **M**；新資產：否；config：**中**，新增 aliases、concept tags、modality、pathology、difficulty。 |
| B9 | **章節導覽升級為 task navigation。** 保留既有側欄與 IntersectionObserver，高亮到「目前單元／活動」，底部固定上一項、下一項和回到病例；手機用章節抽屜。 | **完全可行**。 | **S–M**；新資產：否；config：**低**。 |
| B10 | **課程級鍵盤導航。** 現有快捷鍵集中於 YouTube；擴充 `J/K` 前後影格、`A` 標註、`Q` 進入 quiz、`[`/`]` 前後病例、`N/P` 前後單元，並避免輸入框衝突。 | **完全可行**。 | **S**；新資產：否；config：**低**，快捷鍵文案放入 UI config。 |
| B11 | **可分享的深連結。** 現有支援 tab、play index 與 unit hash；擴充至病例、frame、annotation state、quiz 題目和搜尋 filter，播放項目改用穩定 ID 而非易變 index。 | **完全可行**。 | **S–M**；新資產：否；config：**低**，所有實體需永久 ID。 |
| B12 | **影像與 Quiz 無障礙。** Viewer 工具可全鍵盤操作；slider 提供 `aria-valuenow`；overlay 同步文字列表；作答後以 `aria-live` 宣告結果；不自動播放 cine。 | **完全可行**。 | **M**；新資產：需撰寫影像描述；config：**中**，強制 `alt`、long description、transcript。 |
| B13 | **離線學習模式。** 快取 app shell、課程 JSON、縮圖和使用者指定的病例包；顯示下載大小與版本，避免自動快取全部高容量影像。 | **可行**，Service Worker 仍是純靜態；YouTube 本身不能保證離線。 | **M**；新資產：否；config：**中**，新增 asset manifest、cache version、病例包大小。 |

---

## C.【內容豐富度】

本站已有 `objectives`、必備視圖、判讀重點、陷阱、自我評估文字、參考文獻和實證分級，但多數仍是「文字＋外部影片」。以下依「教學價值高、成本低」優先；內容新增時應延續目前的醫療審閱、來源、日期、揭露及稽核機制。

Orthobullets 將每日主題、題目、常考文獻、影片與 teaching cases 串成同一學習計畫；Medality 進一步提供病例 checklist、DICOM、解說題與 gold-standard report。[Orthobullets](https://www.orthobullets.com/anatomy/322190/general-moc-90-day-study-plan) [Medality](https://medality.com/cme/)

| 排序 | 本站應新增的內容型態 | 教學價值與交付定義 | 工作量／新資產／config 影響 |
|---|---|---|---|
| **P0-1** | **可下載的膝部超音波判讀檢核表** | 把既有 `required_views`、`key_points`、`pitfalls` 重組成一頁式「病人姿勢—探頭方向—必備視圖—動態操作—異常描述—限制」表；提供列印與 PDF。 | 價值 **5/5**；**S**；新資產：否；config：**中**，新增 checklist 分組，build 自動產生 HTML／PDF。 |
| **P0-2** | **雙語名詞表與影像徵象索引** | 收錄繁中、英文、縮寫、同義詞、定義、常見誤用、相關單元；滑過術語可看短定義，搜尋可命中雙語別名。 | 價值 **5/5**；**S–M**；新資產：否；config：**中**，新增 `glossary.json` 與 `concept_ids`。 |
| **P0-3** | **每單元 3–5 題即時知識檢核** | 不只把現有 assessment 顯示成提示文字；加入影像定位、單選、多選與排序題，每個選項均有解析與引用。 | 價值 **5/5**；**M**；新資產：部分需要影像；config：**高**，新增正式 question schema 與 audit。 |
| **P0-4** | **正常／病理／陷阱對照組** | 每個主要解剖區至少一組：正常、典型病灶、常見假象或正常變異；要求學員先列出差異，再揭露標註。 | 價值 **5/5**；**M**；新資產：**是**；config：**高**，新增 comparison set、diagnosis、teaching points、授權資料。 |
| **P0-5** | **標準病例卡** | 固定欄位：主訴、年齡範圍、掃描問題、影像、觀察提示、findings、鑑別、impression、pearls、限制與參考文獻。病例先匿名呈現，診斷延後揭露。 | 價值 **5/5**；**M**；新資產：**是**；config：**高**，新增獨立 `cases` entity，單元只引用 case ID。 |
| **P1-1** | **正常解剖標註圖譜** | 以前／內／外／後側及屈伸角度組織；同一結構提供探頭位置、B-mode、必要時 Doppler 和文字描述。 | 價值 **5/5**；**L**；新資產：**大量影像與探頭插圖**；config：**高**。 |
| **P1-2** | **可捲動 cine／序列病例庫** | 先從短 ultrasound cine 開始，不必一開始導入完整 DICOM；每個 stack 有方向、frame 數、探頭動作、關鍵 frame 和標註。 | 價值 **5/5**；**L**；新資產：**大量序列**；config：**高**。 |
| **P1-3** | **Gold-standard 描述與報告範例** | Quiz 完成後展示「合格 findings」「精簡 impression」「不應過度推論處」，訓練由看圖到臨床溝通，而非只猜診斷。 | 價值 **5/5**；**M**；新資產：否；config：**中～高**，病例增加 report、acceptable variants、red flags。 |
| **P1-4** | **Testable concepts／臨床珍珠卡** | 每單元列出 3–7 個「必會判斷」，並標示 Core／Extension、常見誤答與對應題目；可切換 High-yield mode。 | 價值 **4/5**；**S–M**；新資產：否；config：**中**，新增 `concepts[]` 並與題目、段落互連。 |
| **P1-5** | **主張層級的 evidence map** | 現有 evidence grade 多落在單元或動作類別；改為每項重要主張直接顯示證據等級、研究設計、適用族群、更新日與爭議點。 | 價值 **4/5**；**M**；新資產：否；config：**高**，新增 claim ID、citation linkage、review expiry。 |
| **P1-6** | **錯題卡與間隔複習卡** | 自動把錯題轉為「影像提示正面／答案與判讀理由背面」，也允許學員收藏陷阱或術語。 | 價值 **4/5**；**M**；新資產：沿用現有圖；config：**中**，question／concept 需可產生 flashcard。 |
| **P2-1** | **掃描流程與鑑別診斷圖** | 例如「後膝腫塊」由 compressibility、vascularity、與關節相通性導向 Baker cyst、血管病灶或其他腫塊；每節點連到病例。 | 價值 **4/5**；**M–L**；新資產：**是，流程插圖**；config：**高**，新增 decision-tree schema。 |
| **P2-2** | **正常變異與 mimics 小型圖譜** | 集中整理 anisotropy、reverberation、正常低回音區及容易誤認的血管／滑囊，並提供「如何排除」操作。 | 價值 **4/5**；**L**；新資產：**是**；config：**高**。 |
| **P2-3** | **前測／後測與能力雷達** | 依前、內、外、後側，正常解剖、操作、判讀、陷阱分面呈現掌握度；雷達只顯示個人本機結果，不宣稱正式能力認證。 | 價值 **3/5**；**M**；新資產：否；config：**中～高**，每題需 competency tags；教師／群體版需後端。 |
| **P3** | **完整 DICOM／跨模態病例包** | 提供 ultrasound、X-ray、MRI 對照及專業 viewer，最接近臨床，但授權、去識別、容量、維護和 QA 成本最高；應在內容與 quiz 模型穩定後再做。 | 價值 **5/5**；**L+**；新資產：**大量 DICOM 與授權**；config：**高**，另建 manifest、去識別稽核與版本策略。 |

建議交付順序為：先完成 **P0 的 checklist、名詞表、互動題與少量對照病例**，驗證內容模型和學習流程；再投入 **標註圖譜、cine viewer、gold-standard report 與間隔複習**；完整 DICOM 與跨裝置學習紀錄則留作後續平台化階段。
