"""Exercise real playback policy and player lifecycle, including hostile messages."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HARNESS = r"""
import assert from 'node:assert/strict';
const policyModule = await import('__POLICY__');
const {parseSegmentRanges, playbackPolicy, allowedPosition, rangeAt, isTrustedPlayerMessage} = policyModule;
for (const separator of [',', ';', '、', '，', '；']) {
  assert.deepEqual(parseSegmentRanges(`02:03–06:29${separator}06:44-14:22`), [{start:123,end:389},{start:404,end:862}]);
}
for (const invalid of ['', null, '00:00–00:00', '02:60–03:59', '00:00–02:00;01:59–03:00', '00:00–02:00;02:00–03:00', '0:00oops–2:00']) {
  assert.equal(parseSegmentRanges(invalid), null);
  const p = playbackPolicy({contains_intervention:true, diagnostic_segment_range:invalid});
  assert.equal(p.blocked, true);
  assert.equal(allowedPosition(p, 0), null);
}
const item = { vid:'abcdefghijk', name:'test', title:'test', url:'https://www.youtube.com/watch?v=abcdefghijk', i:0,
  duration:'15:00', contains_intervention:true, diagnostic_segment_range:'02:03–06:29；06:44–14:22'};
const p = playbackPolicy(item);
for (const [input, expected] of [[0,123],[-1,123],[123,123],[388.5,388.5],[389,404],[399,404],[404,404],[862,861],[999,861]]) {
  assert.equal(allowedPosition(p,input), expected);
  assert.ok(rangeAt(p, expected));
}
for (const invalid of [NaN, Infinity, '123', null]) assert.equal(allowedPosition(p,invalid), null);
assert.equal(playbackPolicy({...item,duration:'03:00'}).blocked,true);
assert.equal(allowedPosition(playbackPolicy({duration:'01:00'}),70),59);
assert.equal(allowedPosition(playbackPolicy({}),70),70);
const activeWindow = {};
assert.ok(isTrustedPlayerMessage({origin:'https://www.youtube-nocookie.com',source:activeWindow}, activeWindow));
for (const origin of ['https://youtube.attacker.com','https://www.youtube-nocookie.com.evil.test','http://www.youtube-nocookie.com','https://www.youtube.com']) {
  assert.equal(isTrustedPlayerMessage({origin,source:activeWindow},activeWindow),false);
}
assert.equal(isTrustedPlayerMessage({origin:'https://www.youtube-nocookie.com',source:{}},activeWindow),false);

// Minimal DOM models iframe replacement; assertions invoke the actual player APIs.
const events = {};
globalThis.addEventListener = (name, fn) => (events[name] ||= []).push(fn);
const saved = new Map();
globalThis.localStorage = {getItem:k=>saved.get(k) ?? null,setItem:(k,v)=>saved.set(k,v)};
globalThis.location = {origin:'https://course.test'};
globalThis.matchMedia = () => ({addEventListener(){}, matches:false});
let frame = null;
const commands = [];
const frameHost = {
  set innerHTML(value) {
    this.html = value;
    frame = value.includes('<iframe') ? {contentWindow:{postMessage:(data,origin)=>commands.push({data:JSON.parse(data),origin})}, addEventListener(){},remove(){frame=null;}} : null;
  },
  get innerHTML(){return this.html;}
};
const infoHost = {innerHTML:''};
const status = {textContent:''};
const toast = {textContent:'',classList:{add(){},remove(){}}};
let focusedSearch = null;
const courseSearch = {focus(){focusedSearch='course';}};
const playlistSearch = {focus(){focusedSearch='player';}};
globalThis.document = {querySelector:s=>({'#ytFrame':frame,'#playerFrame':frameHost,'#playerInfo':infoHost,'#playerStatus':status,'#playerFrame iframe':frame,'#ytToast':toast,'#search':courseSearch,'#playlistSearch':playlistSearch}[s] || null)};
const Player = await import('__PLAYER__');
const message = (source, origin, data) => events.message.forEach(fn=>fn({source,origin,data:JSON.stringify(data)}));
const origin='https://www.youtube-nocookie.com';
Player.play(item,{total:1});
assert.match(frameHost.innerHTML,/start=123/);
assert.match(frameHost.innerHTML,/end=389/);
assert.match(frameHost.innerHTML,/autoplay=1/);
let firstFrame = frame;
message(frame.contentWindow,origin,{event:'initialDelivery',info:{currentTime:0,playerState:-1}});
assert.equal(Player.getPosition(),123,'Startup time=0 must not overwrite selected range or pause autoplay');
assert.ok(!commands.some(c=>c.data.func==='pauseVideo'));
message({},origin,{event:'infoDelivery',info:{currentTime:300}});
message(frame.contentWindow,'https://youtube.evil.test',{event:'infoDelivery',info:{currentTime:300}});
assert.equal(Player.getPosition(),123);
message(frame.contentWindow,origin,{event:'infoDelivery',info:{currentTime:234}});
assert.equal(Player.getPosition(),234);
assert.equal(Player.seekTo(399),true);
assert.notEqual(frame,firstFrame);
assert.match(frameHost.innerHTML,/start=404/);
assert.match(frameHost.innerHTML,/end=862/);
message(firstFrame.contentWindow,origin,{event:'infoDelivery',info:{currentTime:280}});
assert.equal(Player.getPosition(),404);
message(frame.contentWindow,origin,{event:'infoDelivery',info:{currentTime:500}});
assert.equal(Player.getPosition(),500);
message(frame.contentWindow,origin,{event:'infoDelivery',info:{currentTime:900}});
assert.equal(Player.getPosition(),404);
assert.ok(commands.some(c=>c.data.func==='pauseVideo'));
assert.ok(commands.some(c=>c.data.func==='seekTo' && c.data.args[0]===404));
message(frame.contentWindow,origin,{event:'infoDelivery',info:{currentTime:555}});
Player.stop();
assert.equal(frame,null);
assert.equal(Player.getPosition(item),555);
Player.resume(item,{total:1});
assert.match(frameHost.innerHTML,/start=555/);
assert.match(frameHost.innerHTML,/autoplay=0/);
assert.match(frameHost.innerHTML,/end=862/);
const Keys = await import('__KEYS__');
let playerTab = true;
Keys.bindKeys({next(){},prev(){},nextChapter(){},prevChapter(){},isPlayerTab:()=>playerTab});
const key = (k, extra={}) => {
  const event = {key:k, preventDefault(){this.defaultPrevented=true;}, ...extra};
  events.keydown.forEach(fn=>fn(event));
  return event;
};
document.activeElement = {tagName:'BUTTON',closest:()=>true};
assert.equal(key(' ').defaultPrevented,undefined,'Space must activate focused buttons');
assert.equal(key('ArrowRight').defaultPrevented,undefined,'Arrows must remain with native controls');
document.activeElement = null;
assert.equal(key('ArrowRight',{defaultPrevented:true}).defaultPrevented,true);
key('/'); assert.equal(focusedSearch,'player');
playerTab = false; key('/'); assert.equal(focusedSearch,'course'); playerTab = true;
message({},origin,{event:'infoDelivery',info:{duration:900}});
key('9'); assert.equal(Player.getPosition(),555,'Spoofed duration must not enable numeric seek');
message(frame.contentWindow,origin,{event:'infoDelivery',info:{duration:900,currentTime:555}});
key('9'); assert.equal(Player.getPosition(),810);
Keys.setShortcutsEnabled(false);
assert.equal(saved.get('knee-imaging:single-key-shortcuts'),'false');
const beforeDisabled = Player.getPosition();
const commandsBeforeDisabled = commands.length;
focusedSearch = null;
for (const shortcut of ['n','p','t','9','j','k','l','m','f','ArrowRight','/',' ']) {
  assert.equal(key(shortcut).defaultPrevented,undefined,`${shortcut} must be inactive when disabled`);
}
assert.equal(Player.getPosition(),beforeDisabled);
assert.equal(commands.length,commandsBeforeDisabled);
assert.equal(focusedSearch,null);
// The setting remains reachable through ? even with all single-key actions off.
const originalQuery = document.querySelector;
let dialog = null;
const checkbox = {id:'singleKeyShortcuts',checked:false};
document.querySelector = s => s === '#keySheet' ? dialog : s === '#singleKeyShortcuts' ? checkbox : originalQuery(s);
document.body = {append(el){dialog=el;}};
document.createElement = tag => {
  assert.equal(tag,'dialog');
  const listeners = {};
  return {style:{},classList:{add(){},remove(){}},open:false,
    setAttribute(){},addEventListener(name,fn){listeners[name]=fn;},
    showModal(){this.open=true;},close(){this.open=false;listeners.close?.();},
    querySelector(){return {focus(){}};},listeners};
};
key('?'); assert.equal(dialog.open,true,'? must remain available when single-key shortcuts are disabled');
assert.match(dialog.innerHTML,/啟用單鍵快捷鍵/);
assert.equal(key('Escape').defaultPrevented,undefined,'Native dialog must receive Escape');
dialog.listeners.change({target:{id:'singleKeyShortcuts',checked:true}});
assert.equal(checkbox.checked,true);
dialog.close();
assert.equal(saved.get('knee-imaging:single-key-shortcuts'),'true');
key('/'); assert.equal(focusedSearch,'player');
Player.stop();
Player.play({...item,vid:'badbadbadba',diagnostic_segment_range:null},{total:1});
assert.equal(frame,null);
assert.equal(Player.seekTo(200),false);
Player.stop();
const contextA = {...item,unitId:'unit-a'};
const contextB = {...item,unitId:'unit-b'};
Player.play(contextA,{total:2,startSeconds:150});
message(frame.contentWindow,origin,{event:'infoDelivery',info:{currentTime:200}});
Player.stop();
Player.play(contextB,{total:2,startSeconds:450});
message(frame.contentWindow,origin,{event:'infoDelivery',info:{currentTime:500}});
Player.stop();
Player.resume(contextA,{total:2});
assert.match(frameHost.innerHTML,/start=200/,'Same video in unit A keeps its own position');
Player.stop();
Player.resume(contextB,{total:2});
assert.match(frameHost.innerHTML,/start=500/,'Same video in unit B keeps its own position');
Player.stop();
console.log('Playback policy, source authentication, range switch, boundary pause and persisted non-autoplay resume passed.');
"""


def main():
    script = (
        HARNESS.replace("__POLICY__", (ROOT / "src/web/js/playback-policy.js").as_uri())
        .replace("__PLAYER__", (ROOT / "src/web/js/player.js").as_uri())
        .replace("__KEYS__", (ROOT / "src/web/js/keys.js").as_uri())
    )
    result = subprocess.run(
        ["node", "--input-type=module", "--eval", script], text=True, capture_output=True
    )
    print(result.stdout, end="")
    if result.returncode:
        print(result.stderr, file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
