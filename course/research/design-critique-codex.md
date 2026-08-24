我的結論很直接：**我會批准「雙材質」的核心策略，但退回目前這套表現手法。**它解決了資訊分區，尚未解決品牌辨識；真正的升級不在更漂亮的深藍，而在讓「診斷影像與判讀方法」成為唯一主角。

## A. 對內部提案的批判

### 哪裡對

1. **暖白閱讀層＋中性黑影像層，是正確的認知分工。**

   現況把網格鋪滿全站，又在 header、hero、章節列反覆使用 navy–teal 漸層與光暈，所有內容都被包裝成監視器介面，見 [clinical.css](/Users/ethanstudio/Projects/knee-ultrasound-course/src/web/css/clinical.css:84)。這會讓真正的超音波、X 光與 MRI 失去視覺特權。

   IMAIOS 的啟示不是「醫學網站要黑」，而是黑色集中服務影像瀏覽、切面、標籤、pan/zoom、cross-reference 等任務；周邊資訊仍維持一般閱讀介面。[IMAIOS e-Anatomy 使用指南](https://files.imaios.com/Userguides/userguide_eanatomy_en.pdf)

2. **teal 收斂為互動色、琥珀專管標註，遠勝現在的 teal 無所不在。**

   現況 teal 同時代表品牌、選取、完成、焦點、掃描、進度、裝飾光源，語意已經失焦。將色彩改成行為契約是對的：

   - Teal：可操作、選取、播放、下一步
   - Amber：ROI、量測、影像標註
   - Red：錯誤、危險、重大陷阱

3. **訂製 pictogram 是最有潛力形成品牌資產的一項。**

   目前 Lucide 的 layers、microscope、activity、scan-line 只是「醫療類 icon」，無法教人怎麼擺探頭或辨識切面，見 [index.html](/Users/ethanstudio/Projects/knee-ultrasound-course/src/web/index.html:35)。若 pictogram 能準確表達探頭方向、病人姿勢、左右側與 longitudinal/transverse plane，它就不只是裝飾，而是課程內容本身。

4. **動效只留診斷語意，完全正確。**

   現在 hero 的掃描線、假超音波 sector、波形與 ROI 動畫在演「像醫療設備」，見 [clinical.css](/Users/ethanstudio/Projects/knee-ultrasound-course/src/web/css/clinical.css:260)。醫師不會因此更信任內容。動效應只發生在切面對照、cine loop、探頭移動與標註揭示。

### 哪裡是平庸的安全牌

- **暖白＋黑＋琥珀、serif＋mono，本身已是成熟出版／高級 medtech 的標準配方。**如果只做換色換字，會從「醫療 SaaS 模板」換成「醫學期刊模板」，仍然沒有自己的臉。
- **Noto Serif TC 不會自動產生學術權威。**Serif 若套在所有標題上，尤其是密集課程卡片，很容易變成文化出版或人文展覽；它只能用於首頁主標與章節開場。
- **「永遠中性黑」只是表面規則，不是設計概念。**IMAIOS 與 Complete Anatomy 的辨識度來自可操作的影像、標籤與獨有內容，而不是黑底。Complete Anatomy 甚至明確以高精度、可拆解的模型作為產品中心；介面是在替模型退場。[Elsevier Complete Anatomy](https://www.elsevier.com/products/complete-anatomy)
- **訂製 icon 若仍被放進圓角小方框，最後只會成為比較昂貴的 Lucide。**它必須和教學步驟、影像定位及評量直接連動。

### 執行風險

1. **最大風險是真實影像不足。**目前 hero 是 CSS 模擬的超音波畫面；這是整站最削弱專業感的元素。寧可放一張經匿名、醫師審核、有來源的真實影像，也不要精緻的假 HUD。

2. **琥珀會與「注意／警告」衝突。**必須規定琥珀只表示影像上的 finding、ROI、measurement；警告仍用紅色，且搭配圖形與文字，不能只靠色相。

3. **跨 modality 的標註規則容易失控。**超音波需要探頭與方向標記，X 光需要投照方向和 detector，MRI 需要切面、序列與 laterality。不能硬用一套 icon 文法處理三者；應共用骨架，保留 modality-specific 部件。

4. **目前其實沒有可靠地載入 Noto Sans TC。**字型堆疊先選系統 UI 與 PingFang，且 HTML 沒有 webfont 宣告，見 [tokens.css](/Users/ethanstudio/Projects/knee-ultrasound-course/src/web/css/tokens.css:48) 與 [index.html](/Users/ethanstudio/Projects/knee-ultrasound-course/src/web/index.html:12)。導入 Serif 前應先處理自託管、字重、CJK subset 與 fallback，否則不同平台會像不同品牌。

5. **兩種材質若按 section 交替，會像兩個網站拼接。**正確關係應是「病例紙承載黑色 viewer」，不是 landing 一套、課程內頁另一套。

NEJM 值得借鑑的正是這種節制：它用 serif/sans 的清楚分工、單欄摘要及圖像周圍的留白建立閱讀權威；Image Challenge 則把一次互動收斂成一張影像、一個問題、一組選項與回答分布。[NEJM 設計說明](https://www.nejm.org/doi/full/10.1056/NEJM199607043350110)、[NEJM Image Challenge](https://www.nejm.org/image-challenges)

## B. 我的強化方向：影像會診桌，而非診斷工作站

我會拿掉大部分深藍、全頁網格、光暈、玻璃效果與假儀器動畫，改成：

- 暖白病例紙佔主要閱讀面積。
- 真實影像以無陰影、近乎無圓角的黑色 viewer 嵌入紙面。
- 版面像經整理的會診紀錄：影像、投照／探頭位、finding、鑑別診斷形成一條可追蹤的判讀鏈。
- 留白與細線負責層級，不再靠大量卡片與色塊。
- 每章只選一張「代表性影像」建立記憶錨點。

建議六色：

| 角色 | 色票 |
|---|---|
| 閱讀紙面 | `#F4F0E7` |
| 主文字／深墨 | `#17211F` |
| 診斷畫布 | `#0B0D0E` |
| 紙面分隔線 | `#C9C2B6` |
| 互動 teal | `#007F7A` |
| 標註 amber | `#E29A2D` |

**刻意取消品牌 navy。**中性黑與暖紙已足夠形成對比；navy 只會把它拉回熟悉的醫療科技模板。

字體配對：

- 主標、章節開場：`Noto Serif TC 600`
- 內文、操作介面：`Noto Sans TC 400 / 500 / 700`
- 切面代碼、尺寸、序列、時間：`IBM Plex Mono 500`
- Serif 不進按鈕、導航、單元標題或長段正文。
- Mono 不用來製造「機器感」，只用在真正可比較的資料。

Pictogram 採三層結構：

1. 身體區域／姿勢輪廓  
2. 探頭、X 光束或 MRI 切面  
3. 方向點、laterality、active plane  

不要圓角容器；以一致的 1.5px 線寬、固定視角與 amber active state 直接放在內容旁。

**Hero 概念一句話：**  
「一張真實膝部影像橫跨暖白病例紙與黑色診斷畫布，探頭 pictogram 指定切面，單一琥珀標註揭示關鍵 finding——沒有假 HUD。」

## C. 最關鍵的一條建議

**把「經醫師審核的真實影像＋精準標註」當成品牌識別，其他設計全部退後。**

「設計感」不應來自更多效果，而應來自只有這門課能提供的觀看方式。只要 hero 還是 CSS 假超音波，再漂亮都像行銷頁；一旦真實影像、切面 pictogram 與判讀標註形成一致系統，專業感和辨識度會同時成立。
