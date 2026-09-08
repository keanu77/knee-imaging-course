本地檔案計算：9 章、18 單元；38 個 `drills` 影片項目 + 1 個 `source_cases` = 39 個 video-like URL，37 個唯一 URL；60 題，60 題全為 `single`；18 個單元都有文字型 `assessment`。
嚴重度統計：P0 2、P1 3、P2 2。

- **P0｜`course/data/syllabus.json:623`, `course/data/syllabus.json:1705`, `course/data/syllabus.json:1834`, `course/data/questions.json:6`**
  - **問題：** syllabus 要求「給影像／病例」判讀，但指定檔案內未見可實際開啟的本地影像病例、序列、DICOM、標註答案或盲測流程；待驗證是否由未審路徑注入。
  - **精確證據：** `assessment` 寫「給六張去識別化影像」、「案例組」、「給一組正常膝蓋 MRI」，但 `questions.json` 題目 schema 只有 `id/type/stem/options/reference_ids/difficulty`，沒有 `case_id`、`image_series`、`viewer_config`、`answer_key`、`blind_mode`。
  - **具體補強：** 新增病例練習 schema：`case_id`, `modality`, `deidentified_assets[]`, `views_or_sequences[]`, `clinical_prompt`, `tasks[]`, `hidden_diagnosis`, `answer_key`, `rubric_id`, `difficulty`, `unlock_policy`, `source_license`, `review_status`。

- **P0｜`src/web/js/app.js:425`, `src/web/js/app.js:432`, `src/web/js/app.js:513`, `course/data/questions.json:20`**
  - **問題：** 目前評量主體是認知選擇題，不足以證明進階專業判讀能力。
  - **精確證據：** 實際計算 60/60 題都是 `type: "single"`；前端 `answerIsCorrect()` 只比對正確選項 index，`gradeQuiz()` 只輸出 `答對 x/y`，沒有影像標註、量測、結構化報告、鑑別診斷排序或信心水準。
  - **具體補強：** 每個進階單元至少加 3 類可評分任務：影像標註、量測填答、結構化報告。MRI 單元需含多平面追蹤與序列選擇；超音波單元需含正交影像、動態片段、Doppler/壓力條件與限制語句。

- **P1｜`src/web/js/app.js:380`, `src/web/js/app.js:391`, `src/web/js/render.js:559`, `src/web/js/render.js:715`**
  - **問題：** `已完成` 可由使用者自行點擊，能力證據與完成進度混在一起。
  - **精確證據：** `toggleDone()` 直接 `setMastery(... "done")`；首頁進度只用 `doneSet` 算 `done / total`；這不是臨床認證冒充，但會讓「看完／自標完成」看起來像能力完成。
  - **具體補強：** 分離狀態：`content_completed`、`knowledge_quiz_passed`、`case_interpretation_passed`、`supervisor_reviewed`。UI 文案避免把任何一項寫成「合格醫師」、「credentialing」或量表認證。

- **P1｜`course/data/syllabus.json:1753`, `src/web/js/app.js:504`, `src/web/js/app.js:508`, `src/web/js/app.js:526`**
  - **問題：** syllabus 有整合考核與督導回饋，但前端沒有保存或評分督導項目。
  - **精確證據：** `assessment` 要「限定時間內完成四區掃描、提交最低影像集與結構化報告、合格督導逐項回饋」；實作只保存 `{ answered, correctAt }`，答對後恢復 `learning/done`，沒有 assessor、影像集、報告、時間限制或回饋紀錄。
  - **具體補強：** 新增 rubric：`coverage`, `image_quality`, `orthogonal_confirmation`, `measurement_accuracy`, `artifact_control`, `report_consistency`, `safety_escalation`, `uncertainty_language`；每項 0–2 分，任何安全升級錯誤或重大漏掃即不通過。

- **P1｜`course/data/syllabus.json:1123`, `course/data/syllabus.json:1127`, `course/data/questions.json:1703`, `src/web/js/render.js:485`**
  - **問題：** 外部公開病例／影片來源不能等同可重複盲測病例。
  - **精確證據：** `source_cases` 明寫「僅連結原頁，未複製病例影像」；題目 `source_links` 會由前端渲染成「題目來源」，可能在作答前暴露線索。外部 URL 是否可開啟因禁網路，待驗證。
  - **具體補強：** 建立本地去識別病例包，作答前隱藏來源、診斷與影片標題；作答後才揭露來源與解析。盲測模式要隨機化病例順序，並記錄首次作答。

- **P2｜`course/data/questions.json:8`, `course/data/questions.json:1656`, `course/data/questions.json:1988`, `src/web/js/render.js:481`**
  - **問題：** 難度 taxonomy 不一致，削弱進階能力追蹤。
  - **精確證據：** 文件寫 `difficulty（core|advanced）`，實際資料使用 `extension`；前端只是原樣顯示 difficulty，沒有能力層級統計。
  - **具體補強：** 統一為 `core / advanced / expert` 或明確定義 `extension`；進度需分開報告「核心知識」、「進階病例判讀」、「督導實作」。

- **P2｜`src/web/js/render.js:692`, `src/web/js/render.js:697`, `course/data/syllabus.json:503`, `course/data/syllabus.json:505`**
  - **問題：** 影片項目數被當成學習主軸資訊，但影片可播放或公開觀看不是能力證據。
  - **精確證據：** 首頁以 `drills.length` 顯示「影片項目」；影片條目有 `embed_status`、`playback_status`，這只能證明教材可觀看，不能證明醫師合格、量表認證或進階判讀通過。
  - **具體補強：** 報表分成「教材 URL 可用性」與「可評分病例數」。能力頁只顯示病例通過率、rubric 分項、盲測首次通過率與督導簽核，不用影片觀看數代表能力。
