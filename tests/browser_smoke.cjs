#!/usr/bin/env node
/* Browser regressions against an already-built, running site.
 * YouTube is replaced with an inert iframe fixture: this tests site-owned
 * controls and iframe URLs, NOT actual YouTube streaming or telemetry.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const baseURL = process.env.BASE_URL || 'http://127.0.0.1:8899/';
const artifactDir = process.env.SMOKE_ARTIFACT_DIR;
const timeout = Number(process.env.SMOKE_TIMEOUT_MS || 15000);
const videoId = url => /(?:v=|youtu\.be\/)([\w-]{11})/.exec(url)?.[1];
const address = relative => new URL(relative, baseURL).href;

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.PLAYWRIGHT_CHANNEL === 'bundled' ? {} : { channel: process.env.PLAYWRIGHT_CHANNEL || 'chrome' }),
  });
  const failures = [];
  let course;
  try {
    const sourceContext = await browser.newContext();
    const response = await sourceContext.request.get(address('course.json'));
    assert.equal(response.status(), 200, 'Build and serve the site before running browser smoke');
    course = await response.json();
    await sourceContext.close();
    const units = course.chapters.flatMap(chapter => chapter.units);
    const videos = units.flatMap(unit => [...(unit.lessons || (unit.lesson ? [unit.lesson] : [])), ...(unit.drills || [])]);
    assert(videos.length >= 2, 'Need at least two curated videos for navigation regressions');

    async function run(name, options, test) {
      const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, ...options });
      context.setDefaultTimeout(timeout);
      context.setDefaultNavigationTimeout(timeout);
      await context.route('https://www.youtube-nocookie.com/**', route => route.fulfill({
        contentType: 'text/html',
        body: '<!doctype html><title>Inert YouTube fixture: site controls only</title>',
      }));
      // Fonts and counters are unrelated external dependencies of these tests.
      await context.route('https://fonts.googleapis.com/**', route => route.fulfill({ contentType: 'text/css', body: '' }));
      await context.route('**/api/hits', route => route.fulfill({ contentType: 'application/json', body: '{"hits":0}' }));
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      try {
        await test(page, context);
        assert.deepEqual(errors, [], 'No uncaught page errors');
        console.log(`PASS ${name}`);
      } catch (error) {
        failures.push({ name, message: error.stack || String(error) });
        console.error(`FAIL ${name}: ${error.message}`);
        if (artifactDir) {
          await fs.mkdir(artifactDir, { recursive: true });
          await page.screenshot({ path: path.join(artifactDir, `${name}.png`), fullPage: true }).catch(() => {});
        }
      } finally {
        await context.close();
      }
    }

    async function ready(page, relative = '') {
      await page.goto(address(relative));
      await page.locator('#tabCourseCount').filter({ hasText: String(course.meta.units) }).waitFor({ state: 'attached' });
      await page.waitForFunction(() => !!document.body.dataset.tab);
    }
    async function tabIs(page, expected) {
      await page.waitForFunction(value => document.body.dataset.tab === value, expected);
    }

    await run('home-search-resume', {}, async page => {
      await ready(page);
      await tabIs(page, 'home');
      await page.locator('[data-tab="course"]').click();
      await page.locator('#ch8-u1 [data-toggle="unit"]').click();
      assert.equal(await page.locator('#ch8-u1 [data-toggle="unit"]').getAttribute('aria-expanded'), 'true');
      await page.locator('#search').fill('meniscus');
      await page.locator('[data-search-time]').first().waitFor();
      await page.locator('[data-search-time]').first().click();
      await page.locator('#ytFrame').waitFor();
      await tabIs(page, 'player');
      const before = new URL(await page.locator('#ytFrame').getAttribute('src'));
      await page.locator('[data-tab="course"]').click();
      await page.locator('[data-tab="player"]').click();
      await page.locator('#ytFrame').waitFor();
      const after = new URL(await page.locator('#ytFrame').getAttribute('src'));
      assert.equal(after.pathname, before.pathname, 'Returning restores the same video');
      assert.equal(after.searchParams.get('start'), before.searchParams.get('start'), 'Returning restores the requested segment position');
      assert.equal(after.searchParams.get('autoplay'), '0', 'Returning does not autoplay');
    });

    await run('deep-link-history-dialog', {}, async page => {
      await ready(page, '?tab=home#ch8-u1');
      await page.locator('#ch8-u1 .Unit__body').waitFor();
      await tabIs(page, 'course');
      await page.locator('.AppHeader__brand').click();
      await tabIs(page, 'home');
      await page.goBack();
      await tabIs(page, 'course');
      await page.locator('#ch8-u1 [data-toggle="unit"]').focus();
      const opener = await page.evaluate(() => document.activeElement.outerHTML);
      await page.keyboard.press('?');
      await page.waitForFunction(() => document.querySelector('#keySheet')?.open);
      assert(await page.locator('#keySheet').evaluate(el => el.contains(document.activeElement)), 'Dialog receives focus');
      await page.keyboard.press('Escape');
      await page.waitForFunction(() => !document.querySelector('#keySheet')?.open);
      assert.equal(await page.evaluate(() => document.activeElement.outerHTML), opener, 'Dialog restores opener focus');
    });

    await run('keyboard-video-focus', {}, async page => {
      await ready(page, `?tab=player#play=${videoId(videos[0].url)}`);
      await page.locator('#ytFrame').waitFor();
      const firstSrc = await page.locator('#ytFrame').getAttribute('src');
      await page.locator('[data-step="1"]').focus();
      await page.keyboard.press('Enter');
      await page.waitForFunction(src => document.querySelector('#ytFrame')?.getAttribute('src') !== src, firstSrc);
      assert.equal(await page.evaluate(() => document.activeElement.dataset.step), '1', 'Next-video control keeps focus after rendering');
      await page.locator('[data-step="-1"]').focus();
      await page.keyboard.press('Enter');
      assert.equal(await page.evaluate(() => document.activeElement.dataset.step), '-1', 'Previous-video control keeps focus');
      const secondItem = page.locator('.PlaylistItem').nth(1);
      await secondItem.focus();
      await page.keyboard.press('Enter');
      assert(await page.evaluate(() => document.activeElement.matches('.PlaylistItem.is-playing')), 'Keyboard playlist selection keeps focus on current item');
    });

    await run('single-key-shortcuts-disabled', {}, async page => {
      await ready(page, `?tab=player#play=${videoId(videos[0].url)}`);
      await page.locator('#ytFrame').waitFor();
      await page.locator('#view-player').focus();
      await page.keyboard.press('?');
      await page.locator('#singleKeyShortcuts').uncheck();
      await page.keyboard.press('Escape');
      assert.equal(await page.evaluate(() => localStorage.getItem('knee-imaging:single-key-shortcuts')), 'false');
      // Record preventDefault after the application's listener: disabled shortcuts
      // must not consume the keys or modify course navigation/theme/player state.
      await page.evaluate(() => {
        window.smokePreventedKeys = [];
        addEventListener('keydown', event => { if (event.defaultPrevented) window.smokePreventedKeys.push(event.key); });
      });
      const before = await page.evaluate(() => ({ tab: document.body.dataset.tab, theme: document.documentElement.dataset.theme, src: document.querySelector('#ytFrame').src }));
      for (const key of ['n', 'p', 't', '9', 'j', 'k', 'l', 'm', 'f', '/', 'ArrowRight']) await page.keyboard.press(key);
      assert.deepEqual(await page.evaluate(() => window.smokePreventedKeys), []);
      assert.deepEqual(await page.evaluate(() => ({ tab: document.body.dataset.tab, theme: document.documentElement.dataset.theme, src: document.querySelector('#ytFrame').src })), before);
      await page.reload();
      await page.locator('#ytFrame').waitFor();
      await page.locator('#view-player').focus();
      await page.keyboard.press('?');
      assert.equal(await page.locator('#singleKeyShortcuts').isChecked(), false, 'Preference survives reload and help remains accessible');
      await page.locator('#singleKeyShortcuts').check();
      await page.keyboard.press('Escape');
      const theme = await page.locator('html').getAttribute('data-theme');
      await page.keyboard.press('t');
      assert.notEqual(await page.locator('html').getAttribute('data-theme'), theme, 'Re-enabling restores shortcuts');
    });

    await run('search-excludes-answer-rationale', {}, async (page, context) => {
      const payload = structuredClone(course);
      const unit = payload.chapters.flatMap(chapter => chapter.units).find(item => item.questions?.some(question => question.options?.length));
      assert(unit, 'Need a real quiz to verify hidden rationale is excluded');
      const sentinel = 'KNEESMOKERationaleOnly928471';
      unit.questions[0].options[0].rationale = sentinel;
      const segment = payload.chapters.flatMap(chapter => chapter.units).flatMap(item => item.drills || []).flatMap(item => item.segments || [])[0];
      assert(segment, 'Need a segment for a positive search control');
      const positive = 'KNEESMOKEVisibleNote918362';
      segment.summary += ` ${positive}`;
      let fixtureServed = false;
      await context.route(url => url.pathname.endsWith('/course.json'), route => {
        fixtureServed = true;
        return route.fulfill({ contentType: 'application/json', body: JSON.stringify(payload) });
      });
      await ready(page, '?tab=course');
      assert(fixtureServed, 'Course fixture was actually served');
      await page.locator('.QuizOption__rationale').filter({ hasText: sentinel }).waitFor({ state: 'attached' });
      await page.locator('#search').fill(positive);
      await page.locator('#searchResults [data-search-time]').first().waitFor();
      assert((await page.locator('#searchResults').innerText()).includes(positive), 'Approved note content is searchable');
      await page.locator('#search').fill(sentinel);
      await page.waitForFunction(query => {
        const results = document.querySelector('#searchResults');
        return results?.querySelector('h2')?.textContent.includes(query) && results.querySelector('[role="status"]')?.textContent.startsWith('0 項結果');
      }, sentinel);
      assert.equal(await page.locator('#searchResults .SearchResult').count(), 0, 'Answer rationale never becomes a search result');
      assert.equal(await page.locator('.QuizOption__rationale').filter({ hasText: sentinel }).isVisible(), false, 'Search does not reveal ungraded rationale');
    });

    await run('no-js-unit-reading', { javaScriptEnabled: false }, async page => {
      const unit = units.find(item => item.id === 'ch4-u1');
      assert(unit, 'Expected target reading unit');
      const response = await page.goto(address('units/ch4-u1/'));
      assert.equal(response.status(), 200);
      assert.equal(await page.locator('h1').count(), 1);
      assert((await page.locator('h1').innerText()).includes(unit.name));
      assert((await page.locator('body').innerText()).includes(unit.key_points[0]), 'Main teaching content exists with JS disabled');
      assert.equal(await page.locator('script').count(), 0);
      assert.equal(await page.locator('iframe').count(), 0, 'Reading page does not start external players');
      assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'), `${course.config.site.url.replace(/\/$/, '')}/units/ch4-u1/`);
      const entry = page.locator('a.action[href="../../?tab=course#ch4-u1"]');
      await entry.waitFor();
      assert(await entry.isVisible(), 'Interactive course entry remains available');
    });

    await run('no-js-home-reading-links', { javaScriptEnabled: false }, async page => {
      await page.goto(address(''));
      const links = page.locator('noscript a[href^="/units/"]');
      assert.equal(await links.count(), units.filter(unit => unit.review_status === 'approved').length);
      await links.first().click();
      await page.locator('#reading h1').waitFor();
    });

    await run('data-failure-recovery', {}, async (page, context) => {
      await context.route(url => url.pathname.endsWith('/course.json'), route => route.fulfill({ status: 503, body: 'Unavailable' }));
      await page.goto(address(''));
      await page.getByRole('alert').waitFor();
      assert(await page.getByRole('button', { name: '重新載入', exact: true }).isVisible());
    });

    await run('shared-video-unit-context', {}, async (page, context) => {
      const payload = structuredClone(course);
      const unitList = payload.chapters.flatMap(chapter => chapter.units);
      const source = unitList.find(unit => unit.drills?.length);
      const target = unitList.find(unit => unit.id !== source.id && unit.drills?.length);
      const duplicate = { ...structuredClone(source.drills[0]), name: 'Shared video context regression' };
      target.drills.push(duplicate);
      payload.meta.drill_units++;
      await context.route(url => url.pathname.endsWith('/course.json'), route => route.fulfill({ contentType: 'application/json', body: JSON.stringify(payload) }));
      await ready(page, '?tab=player');
      await page.locator('.PlaylistItem').filter({ hasText: duplicate.name }).click();
      const reference = new URLSearchParams(new URL(page.url()).hash.slice(1));
      assert.equal(reference.get('play'), videoId(duplicate.url));
      assert.equal(reference.get('unit'), target.id, 'Share URL preserves unit context');
      assert.equal(await page.locator('.PlaylistItem[aria-current="true"]').count(), 1);
      assert((await page.locator('.PlaylistItem[aria-current="true"]').innerText()).includes(duplicate.name));
      const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('knee-ultrasound-course:playing')));
      assert.deepEqual(saved, { vid: videoId(duplicate.url), unitId: target.id });
      await page.goto(address('?tab=player'));
      await page.locator('#ytFrame').waitFor();
      assert((await page.locator('.PlaylistItem.is-playing').innerText()).includes(duplicate.name), 'Saved identity restores the second unit');
      await page.evaluate(() => localStorage.clear());
      await page.goto(address(`?tab=player#${reference}`));
      await page.locator('#ytFrame').waitFor();
      assert((await page.locator('.PlaylistItem.is-playing').innerText()).includes(duplicate.name), 'Shared link restores the second unit without saved state');
    });

    await run('mobile-reading-and-filter-recovery', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }, async page => {
      await ready(page, '?tab=course');
      assert.equal(await page.locator('#courseNav').getAttribute('open'), null);
      assert((await page.locator('#chapters').boundingBox()).y < 700, 'First chapter is reachable in the initial mobile viewport');
      await page.locator('.CourseNav__toggle').click();
      assert(await page.locator('#nav').isVisible());
      await page.locator('.CourseNav__toggle').click();
      await page.locator('#search').fill('meniscus');
      await page.locator('.SearchResult__title').first().waitFor();
      const blocks = await page.locator('.SearchResult').first().evaluate(el => {
        const title = el.querySelector('.SearchResult__title').getBoundingClientRect();
        const snippet = el.querySelector('.SearchResult__snippet').getBoundingClientRect();
        return snippet.y >= title.bottom;
      });
      assert(blocks, 'Search title and excerpt occupy separate lines');
      await page.locator('#search').fill('noMatchingKneeTerm91842');
      await page.locator('#filterBlank').waitFor();
      await page.locator('#filterBlank [data-clear-filters]').click();
      assert.equal(await page.locator('#search').inputValue(), '');
      assert.equal(await page.locator('#filterBlank').count(), 0);
      await page.locator('[data-tab="player"]').click();
      await page.locator('.PlaylistItem').first().click();
      await page.locator('#ytFrame').waitFor();
      await page.waitForFunction(() => { const r = document.querySelector('#playerFrame').getBoundingClientRect(); return r.y >= 180 && r.bottom <= innerHeight; });
      const frame = await page.locator('#playerFrame').boundingBox();
      assert(frame.y >= 180 && frame.y + frame.height <= 844, 'Selecting a video reveals the whole frame below mobile navigation');
      assert(await page.locator('#playerInfo').evaluate(el => el.scrollHeight <= el.clientHeight + 1), 'Mobile notes use normal page scrolling');
      await page.locator('[data-player-jump="playerList"]').click();
      assert(await page.locator('#playlistSearch').isVisible());
      const source = await page.locator('#ytFrame').getAttribute('src');
      await page.locator('#playlistSearch').fill('noMatchingVideo91842');
      await page.locator('[data-reset-playlist]').click();
      assert.equal(await page.locator('#playlistSearch').inputValue(), '');
      assert((await page.locator('.PlaylistItem').count()) > 0);
      assert.equal(await page.locator('#ytFrame').getAttribute('src'), source, 'Filter recovery does not restart the video');
      await page.locator('[data-player-jump="playerFrame"]').click();
      await page.waitForFunction(() => document.querySelector('#playerFrame').getBoundingClientRect().y >= 180);
      assert((await page.locator('#playerFrame').boundingBox()).y >= 180);
      await page.setViewportSize({ width: 1440, height: 900 });
      await page.locator('[data-tab="course"]').click();
      assert(await page.locator('#nav').isVisible(), 'Desktop navigation reopens after resizing');
    });

    await run('approved-sports-content-and-quiz', {}, async page => {
      const sportUnits = units.filter(unit => unit.id.startsWith('us-sport-'));
      assert.equal(sportUnits.length, 4);
      for (const unit of sportUnits) {
        await ready(page, `?tab=course#${unit.id}`);
        const host = page.locator(`#${unit.id}`);
        assert((await host.locator('.ClinicalBrief__boundary').innerText()).includes(unit.content_boundary));
        assert.equal(await host.locator('.QuizQuestion').count(), 3);
      }
      await ready(page, '?tab=course#us-sport-extensor');
      const host = page.locator('#us-sport-extensor');
      const form = host.locator('.Quiz__form');
      const questionSources = host.locator('.QuizQuestion__sources');
      assert.equal(await questionSources.isVisible(), false);
      for (const fieldset of await form.locator('fieldset').all()) {
        await fieldset.locator('.QuizOption').first().click();
        assert(await fieldset.locator('input').first().isChecked());
      }
      await form.locator('[type="submit"]').click();
      assert(await questionSources.isVisible(), 'Grading reveals the original case source');
      assert((await questionSources.locator('a').getAttribute('href')).startsWith('https://www.amssm.org/'));
      await page.goto(address('units/us-sport-snapping/'));
      assert((await page.locator('#scope').innerText()).includes('彈響 cine'));
      const uniqueVideos = new Map(videos.map(video => [videoId(video.url), video]));
      for (const clip of units.flatMap(unit => unit.journal_clips || [])) uniqueVideos.set(clip.url, clip);
      assert.equal(course.meta.video_unique, uniqueVideos.size);
      assert(course.meta.duration_unique_seconds < course.meta.duration_seconds, 'Shared video durations are not counted twice on the homepage');
    });

    for (const width of [320, 390, 768]) {
      await run(`mobile-navigation-${width}`, { viewport: { width, height: 844 }, isMobile: true, hasTouch: true }, async page => {
        await ready(page);
        await page.locator('[data-tab="course"]').click();
        await tabIs(page, 'course');
        await page.locator('[data-tab="player"]').click();
        await tabIs(page, 'player');
        await page.locator('.AppHeader__brand').click();
        await tabIs(page, 'home');
        assert(await page.locator('[data-tab="course"] .TabNav__label').isVisible(), 'Mobile tabs keep their text labels');
        const dimensions = await page.evaluate(() => ({ viewport: innerWidth, scroll: document.documentElement.scrollWidth }));
        assert(dimensions.scroll <= dimensions.viewport + 1, `No horizontal overflow at ${width}px: ${JSON.stringify(dimensions)}`);
      });
    }
  } finally {
    await browser.close();
  }
  if (failures.length) {
    failures.forEach(failure => console.error(`\n${failure.name}\n${failure.message}`));
    process.exitCode = 1;
  } else console.log('All 14 browser regression scenarios passed. YouTube streaming was not tested.');
})().catch(error => { console.error(error); process.exitCode = 1; });
