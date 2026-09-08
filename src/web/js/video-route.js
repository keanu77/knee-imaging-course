// A video can teach different material in different units; keep both identities.
const VIDEO_ID = /^[\w-]{11}$/;
const UNIT_ID = /^[A-Za-z0-9][A-Za-z0-9_-]*$/;

export function playHash(item, time) {
  const params = new URLSearchParams({ play: item.vid });
  if (item.unitId) params.set("unit", item.unitId);
  if (Number.isSafeInteger(time) && time >= 0) params.set("t", String(time));
  return params.toString();
}

export function parsePlayHash(hash) {
  const params = new URLSearchParams(String(hash || "").replace(/^#/, ""));
  const vid = params.get("play"), unitId = params.get("unit"), rawTime = params.get("t");
  if (!VIDEO_ID.test(vid || "") || (unitId !== null && !UNIT_ID.test(unitId))) return null;
  if ([...params.keys()].some(key => !["play", "unit", "t"].includes(key) || params.getAll(key).length !== 1)) return null;
  const time = rawTime === null ? undefined : /^\d+$/.test(rawTime) ? Number(rawTime) : NaN;
  if (time !== undefined && (!Number.isSafeInteger(time) || time < 0)) return null;
  return { vid, unitId, time };
}

export function playlistIndex(items, reference) {
  // Preserve both earlier storage formats: array index, then YouTube ID.
  if (Number.isInteger(reference)) return reference >= 0 && items[reference] ? reference : -1;
  const vid = typeof reference === "string" ? reference : reference?.vid;
  const unitId = typeof reference === "object" ? reference?.unitId : null;
  return items.findIndex(item => item.vid === vid && (!unitId || item.unitId === unitId));
}
