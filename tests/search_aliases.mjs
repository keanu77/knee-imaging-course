// Pure JavaScript regression harness: course, playlist and segment search agree.
import assert from 'node:assert/strict';
import { expandTerms, buildSearchIndex, searchRecords } from '../src/web/js/search-index.js';
import { setSearchGlossary, queryTerms, normalizeQuery, segmentMatches, segmentHitCount, highlight } from '../src/web/js/segment-search.js';
// Loading the player also registers browser listeners; keep them inert in this pure-JS harness.
globalThis.addEventListener = () => {};
globalThis.matchMedia = () => ({ addEventListener() {} });
const { playlistItemMatches } = await import('../src/web/js/player.js');

const glossary = [
  { zh: '半月板', en: 'Meniscus', aliases: ['Menisci'] },
  { zh: '內側半月板', en: 'Medial meniscus', aliases: ['半月板內側', 'meniscus'] },
  { zh: '特殊字元', en: '<img src=x onerror="boom">', aliases: ['   '] },
];
setSearchGlossary(glossary);
assert.equal(normalizeQuery('  Meniscus  '), 'meniscus', 'normalization stays a string');
assert.deepEqual(queryTerms('Menisci'), expandTerms('Menisci', glossary), 'same glossary expansion as course');
const segment = { title: '半月板的長軸', summary: '辨識內側半月板', detail: ['避免各向異性'] };
const item = { name: '膝部掃描', unitId: 'stable-unit', segments: [segment], learning_tier: 'core' };
const options = { doneSet: new Set(), query: 'Menisci', onlyTodo: false, learningTier: 'all' };
const index = buildSearchIndex({ chapters: [{ code: 'US1', units: [{ id: 'stable-unit', name: '膝部', drills: [{ name: item.name, segments: [segment] }] }] }] });
assert.equal(searchRecords(index, expandTerms(options.query, glossary)).length, 1, 'course finds Chinese segment from English alias');
assert.equal(playlistItemMatches(item, options), true, 'playlist finds same alias in segment');
assert.equal(segmentMatches(segment, options.query), true, 'segment rail finds same alias');
assert.equal(segmentHitCount([segment, { title: '髕骨' }], options.query), 1, 'count reflects matching segments only');
assert.equal(segmentMatches({ title: 'Meniscus' }, '半月板'), true, 'Chinese lookup expands to English');
assert.equal(playlistItemMatches({ ...item, segments: [], name: 'Meniscus' }, { ...options, query: '半月板' }), true, 'playlist metadata expands aliases too');
assert.equal(segmentMatches(segment, 'menisc'), false, 'a partial alias is not expanded');
assert.equal(playlistItemMatches(item, { ...options, onlyTodo: true, doneSet: new Set(['stable-unit']) }), false, 'completion filter still uses the unit');
assert.equal(playlistItemMatches(item, { ...options, learningTier: 'extended' }), false, 'tier filtering remains effective');
assert.equal(highlight('Medial meniscus / 半月板 <b>&', 'meniscus'), '<mark class="Hit">Medial meniscus</mark> / <mark class="Hit">半月板</mark> &lt;b&gt;&amp;', 'overlapping aliases use longest complete match and escape surrounding markup');
assert.equal(highlight('<img src=x onerror="boom">', '特殊字元'), '<mark class="Hit">&lt;img src=x onerror=&quot;boom&quot;&gt;</mark>', 'an HTML alias is escaped inside the mark');
assert.equal(segmentMatches({ title: 'unrelated' }, '特殊字元'), false, 'blank glossary alias cannot match everything');
for (const empty of ['', '   ', null]) {
  assert.deepEqual(queryTerms(empty), [], 'empty query has no terms');
  assert.equal(segmentMatches(segment, empty), false, 'empty query never marks a segment');
  assert.equal(segmentHitCount([segment], empty), 0, 'empty query has no segment hits');
  assert.equal(highlight('<b>半月板</b>', empty), '&lt;b&gt;半月板&lt;/b&gt;', 'empty query only escapes');
  assert.equal(playlistItemMatches(item, { ...options, query: empty }), true, 'empty query keeps the unfiltered playlist');
}
setSearchGlossary([]);
assert.equal(segmentMatches(segment, 'meniscus'), false, 'glossary reset does not leave stale aliases');
console.log('✓ Cross-entry aliases, metadata, overlap, HTML escaping and empty-query regressions passed');
