// Pure playback boundaries, shared by note buttons, keyboard seeking and resume.
export function parseClock(text) {
  const parts = String(text ?? "").trim().split(":");
  if (parts.length < 2 || parts.length > 3 || !parts.every((p) => /^\d+$/.test(p))) return null;
  const n = parts.map(Number);
  if (n.at(-1) >= 60 || (n.length === 3 && n[1] >= 60)) return null;
  const result = n.reduce((acc, part) => acc * 60 + part, 0);
  return Number.isSafeInteger(result) ? result : null;
}

export function parseSegmentRanges(text) {
  const parts = String(text ?? "").split(/[、，；;,]/).map((s) => s.trim()).filter(Boolean);
  if (!parts.length) return null;
  const ranges = [];
  for (const part of parts) {
    const match = /^((?:\d{1,2}:)?\d{1,2}:\d{2})\s*[–-]\s*((?:\d{1,2}:)?\d{1,2}:\d{2})$/.exec(part);
    if (!match) return null;
    const start = parseClock(match[1]), end = parseClock(match[2]);
    if (start === null || end === null || start >= end || (ranges.length && start <= ranges.at(-1).end)) return null;
    ranges.push({ start, end });
  }
  return ranges;
}

export function playbackPolicy(item) {
  const text = String(item?.diagnostic_segment_range ?? "").trim();
  const ranges = parseSegmentRanges(text);
  const duration = parseClock(item?.duration);
  const blocked = (item?.contains_intervention === true || !!text) &&
    (!ranges || (duration !== null && ranges.some((r) => r.end > duration)));
  return { blocked, ranges: blocked ? [] : ranges, duration };
}

// End is exclusive: a seek at the intervention boundary must not play that frame.
export function allowedPosition(policy, seconds = 0) {
  if (policy.blocked || typeof seconds !== "number" || !Number.isFinite(seconds)) return null;
  const target = Math.max(0, seconds);
  if (!policy.ranges) return policy.duration === null ? target : Math.min(target, Math.max(0, policy.duration - 1));
  for (const range of policy.ranges) {
    if (target < range.start) return range.start;
    if (target < range.end) return target;
  }
  return Math.max(policy.ranges.at(-1).start, policy.ranges.at(-1).end - 1);
}

export function rangeAt(policy, seconds) {
  return policy.ranges?.find((r) => seconds >= r.start && seconds < r.end) || null;
}

export function isTrustedPlayerMessage(event, frameWindow) {
  return !!frameWindow && event.origin === "https://www.youtube-nocookie.com" && event.source === frameWindow;
}
