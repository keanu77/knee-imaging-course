#!/usr/bin/env node
// Real journal streams, separate from the YouTube fixtures in browser_smoke.cjs.
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8899/';
const out = process.env.SMOKE_ARTIFACT_DIR || '.tmp/journal-clips-browser';

(async () => {
  await fs.mkdir(out, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const report = { base, checkedAt: new Date().toISOString(), fixtures: false, streams: [], layouts: [] };
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.request.get(new URL('course.json', base).href);
    const course = await response.json();
    const unit = course.chapters.flatMap(c => c.units).find(u => u.id === 'us-saphenous-postop');
    assert(unit, 'This must be the new build');
    assert.equal(unit.journal_clips.length, 2);
    assert.equal(course.meta.journal_clip_count, 2);
    await page.goto(new URL('?tab=course#us-saphenous-postop', base).href);
    const host = page.locator('#us-saphenous-postop');
    await host.locator('.JournalClip').first().waitFor();
    assert.equal(await host.locator('.JournalClip').count(), 2);
    for (let i = 0; i < unit.journal_clips.length; i++) {
      const video = host.locator('video').nth(i);
      const before = await video.evaluate(v => ({ preload: v.preload, autoplay: v.autoplay }));
      assert.equal(before.preload, 'none');
      assert.equal(before.autoplay, false);
      await video.scrollIntoViewIfNeeded();
      await video.evaluate(v => { v.muted = true; return v.play(); });
      await page.waitForFunction(index => {
        const v = document.querySelectorAll('#us-saphenous-postop video')[index];
        return v.currentTime > 1 && v.getVideoPlaybackQuality().totalVideoFrames > 2;
      }, i, { timeout: 30000 });
      const sample = await video.evaluate(v => ({ url: v.currentSrc, duration: v.duration,
        time: v.currentTime, readyState: v.readyState, frames: v.getVideoPlaybackQuality().totalVideoFrames }));
      assert.equal(sample.url, unit.journal_clips[i].url);
      assert(Math.abs(sample.duration - unit.journal_clips[i].duration_seconds) < .2);
      report.streams.push(sample);
      await video.evaluate(v => v.pause());
      await host.locator('.JournalClip').nth(i).screenshot({ path: path.join(out, `clip-${i + 1}.png`) });
    }
    // Starting another clip must pause the first; leaving or hiding a unit must pause playback.
    const first = host.locator('video').first();
    const second = host.locator('video').nth(1);
    await first.evaluate(v => { v.currentTime = 0; return v.play(); });
    await second.evaluate(v => { v.currentTime = 0; return v.play(); });
    assert(await first.evaluate(v => v.paused));
    await host.locator('[data-toggle="unit"]').click();
    assert(await second.evaluate(v => v.paused));
    await host.locator('[data-toggle="unit"]').click();
    await second.evaluate(v => v.play());
    await page.locator('.AppHeader__brand[data-tab-link="home"]').click();
    assert(await second.evaluate(v => v.paused));
    await page.locator('[data-tab="course"]').click();
    await page.locator('#search').fill('隱神經');
    await page.waitForFunction(name => document.querySelector('#searchResults')?.textContent.includes(name), unit.name);
    await page.locator('#search').fill('');
    assert.equal(await host.locator('.QuizQuestion').count(), 3);
    for (const fieldset of await host.locator('.QuizQuestion').all()) {
      await fieldset.locator('.QuizOption').first().click();
      assert(await fieldset.locator('input').first().isChecked());
    }
    await host.locator('[data-action="submit-quiz"]').click();
    assert.match(await host.locator('.Quiz__result').innerText(), /答對 [0-3]\/3/);
    for (const width of [320, 390, 1440]) {
      await page.setViewportSize({ width, height: 950 });
      await page.goto(new URL('?tab=course#us-saphenous-postop', base).href);
      await page.locator('.JournalClip').first().waitFor();
      const dimensions = await page.evaluate(() => ({ width: innerWidth, scroll: document.documentElement.scrollWidth }));
      assert(dimensions.scroll <= dimensions.width + 1, 'No horizontal overflow');
      report.layouts.push({ type: 'interactive', ...dimensions });
      if (width === 390) await page.locator('#us-saphenous-postop').screenshot({ path: path.join(out, 'mobile-unit.png') });
      await page.goto(new URL('units/us-saphenous-postop/', base).href);
      assert.equal(await page.locator('video').count(), 2);
      assert((await page.locator('#key_points').innerText()).includes('4 × 3 × 2 mm'));
      const reading = await page.evaluate(() => ({ width: innerWidth, scroll: document.documentElement.scrollWidth }));
      assert(reading.scroll <= reading.width + 1);
      report.layouts.push({ type: 'reading', ...reading });
    }
    assert.deepEqual(errors, []);
    report.lifecycle = 'pause on another clip, unit collapse, and tab change passed';
    report.searchAndQuiz = 'passed';
    report.success = true;
    console.log('PASS real journal streams, lifecycle, search, quiz, and six responsive views');
  } catch (error) {
    report.success = false;
    report.error = error.stack;
    process.exitCode = 1;
    console.error(error);
  } finally {
    await fs.writeFile(path.join(out, 'verification.json'), JSON.stringify(report, null, 2) + '\n');
    await browser.close();
  }
})();
