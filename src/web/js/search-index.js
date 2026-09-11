// Search approved course material directly, independently of collapsed DOM and quiz answers.
export function expandTerms(query, glossary = []) {
  const q = String(query || "").trim().toLowerCase();
  if (!q) return [];
  const terms = new Set([q]);
  for (const entry of glossary) {
    const aliases = [entry.zh, entry.en, ...(entry.aliases || [])].filter(Boolean);
    if (aliases.some(value => value.toLowerCase() === q)) {
      aliases.forEach(value => terms.add(value.toLowerCase()));
    }
  }
  return [...terms];
}
const words = value => Array.isArray(value) ? value.map(words).join(" ") :
  value && typeof value === "object" ? Object.values(value).map(words).join(" ") : String(value || "");
export function buildSearchIndex(course) {
  return course.chapters.flatMap(ch => ch.units.flatMap(u => {
    const base = { unitId: u.id, unitName: u.name, chapter: ch.code };
    const unit = { ...base, kind: "unit", title: u.name,
      text: words([u.summary, u.objectives, u.required_views, u.key_points, u.pitfalls, u.assessment, u.tight, u.weak,
        (u.journal_clips || []).filter(c => c.review_status === "approved").map(c => [c.title, c.case_context, c.observations])]) };
    const videos = [...(u.lessons || (u.lesson ? [u.lesson] : [])), ...(u.drills || [])];
    return [unit, ...videos.flatMap(v => {
      const videoId = /(?:v=|youtu\.be\/)([\w-]{11})/.exec(v.url || "")?.[1];
      const common = { ...base, videoId, videoKind: v.kind || "lesson", tier: v.learning_tier || "core", videoTitle: v.name || v.title };
      return [{ ...common, kind: "video", title: v.name || v.title, text: words([v.title, v.presenter, v.channel, v.target, v.why]) },
        ...(v.segments || []).map(seg => ({ ...common, kind: "segment", title: seg.title, start: seg.start,
          text: words([seg.summary, seg.detail]) }))];
    })];
  })).map(record => ({ ...record, haystack: `${record.title} ${record.text}`.toLowerCase() }));
}
export function searchRecords(index, terms, { filter = "all", learningTier = "all" } = {}) {
  if (!terms.length) return [];
  return index.filter(r => {
    if (r.kind !== "unit" && ((filter !== "all" && r.videoKind !== filter) || (learningTier !== "all" && r.tier !== learningTier))) return false;
    if (r.kind === "unit" && (filter !== "all" || learningTier !== "all")) return false;
    return terms.some(term => r.haystack.includes(term));
  }).map(r => ({ ...r, match: terms.find(term => r.haystack.includes(term)),
    score: terms.some(term => r.title.toLowerCase().includes(term)) ? 2 : 1 }))
    .sort((a,b) => b.score - a.score || (a.kind === "segment" ? -1 : 1) - (b.kind === "segment" ? -1 : 1));
}
export function excerpt(text, term, length = 150) {
  const raw = String(text || "");
  const at = raw.toLowerCase().indexOf(term);
  const start = Math.max(0, at - 45);
  return `${start ? "…" : ""}${raw.slice(start, start + length)}${raw.length > start + length ? "…" : ""}`;
}
