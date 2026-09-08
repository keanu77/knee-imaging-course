# Browser smoke

Build the site and serve `dist` first (`make build`, then `make serve`). Run:

```sh
BASE_URL=http://127.0.0.1:8899/ node tests/browser_smoke.cjs
```

The runner uses an existing `playwright` installation. If it is outside the normal module lookup, set `PLAYWRIGHT_MODULE` to its module directory. It does not install dependencies or add runtime packages. Chrome is the default browser channel; set `PLAYWRIGHT_CHANNEL=bundled` to use Playwright's installed Chromium. `SMOKE_TIMEOUT_MS` controls timeouts; `SMOKE_ARTIFACT_DIR` optionally saves screenshots of failures.

Fourteen scenarios cover search and player restoration, deep links/history/dialog focus, keyboard video navigation focus, persistent shortcut disabling, exclusion of hidden quiz rationale from search (with a positive note-search control), a real no-JavaScript reading page, the no-JavaScript homepage reading links, visible recovery from a failed course-data request, shared-video unit identity across reload/share/saved state, and navigation at 320/390/768px. Additional checks cover mobile course entry, responsive navigation, readable search results, empty-filter recovery, normal page scrolling for notes, mobile selection focus, four approved sports units, quiz source disclosure, static content boundaries, and unique-video counting. Every scenario runs in a fresh browser context and checks uncaught page errors. Failures produce a nonzero exit code.

YouTube responses use an inert iframe fixture. These checks prove site-owned navigation, iframe parameters and controls, not actual video streaming, YouTube telemetry, subtitle availability, or absence of out-of-range frames during native playback. Source availability and playback boundaries still require separate real-source verification. Quiz rationale exclusion is a search/learning behavior, not a claim that static client-side quiz answers are secret.
