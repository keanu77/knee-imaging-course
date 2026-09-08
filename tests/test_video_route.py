"""Video links keep unit identity while accepting previous public link formats."""

import subprocess
from pathlib import Path

module = (Path(__file__).resolve().parents[1] / "src/web/js/video-route.js").as_uri()
script = r"""
import assert from 'node:assert/strict';
const {playHash,parsePlayHash,playlistIndex} = await import(MODULE);
const items=[{vid:'abcdefghijk',unitId:'unit-a'},{vid:'abcdefghijk',unitId:'unit-b'}];
assert.equal(playlistIndex(items,parsePlayHash('#'+playHash(items[1],300))),1);
assert.equal(parsePlayHash('#'+playHash(items[1],300)).time,300);
assert.equal(playlistIndex(items,parsePlayHash('#play=abcdefghijk&t=300')),0);
assert.equal(playlistIndex(items,1),1);
assert.equal(playlistIndex(items,'abcdefghijk'),0);
assert.equal(playlistIndex(items,{vid:'abcdefghijk',unitId:'unit-b'}),1);
assert.equal(playlistIndex(items,{vid:'abcdefghijk',unitId:'removed'}),-1);
for(const ref of [-1,2,1.5,null,{},'deleted']) assert.equal(playlistIndex(items,ref),-1);
for(const hash of ['#play=abcdefghijk&t=-1','#play=abcdefghijk&t=Infinity','#play=abcdefghijk&t=9007199254740992','#play=abcdefghijk&t=1&t=2','#play=abcdefghijk&unit=unit-a&unit=unit-b','#play=abcdefghijk&unit=%3Cscript%3E','#play=too-short','#play=abcdefghijk&unknown=1']) assert.equal(parsePlayHash(hash),null,hash);
console.log('Video route context, legacy migration, stale IDs and invalid parameters passed.');
""".replace("MODULE", repr(module))

raise SystemExit(subprocess.run(["node", "--input-type=module", "--eval", script]).returncode)
