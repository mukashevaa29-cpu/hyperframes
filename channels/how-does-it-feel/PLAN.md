# How does it feel? — production notes

Owner's brief (2026-11-26): remake the owner's 4 Russian shorts in English, better than the originals, every video opens with
"How does it feel?", no sponsor inserts, rendered with `npx hyperframes`. Voice: placeholder **Brian** (free key) until the
owner buys an ElevenLabs plan and picks a voice — then re-run `kit/tts.py` + build + mix + render (word timings drive every cut).

## Layout

- `STYLE.md` — the house style (measured from the 4 references, frame by frame).
- `reference/v1..v4/` — forensic reports + Russian transcripts of the originals (v1 Hiroshima, v2 electric chair, v3 brazen bull, v4 stake).
- `kit/lib.py` — shared builder (neon helpers, mascot rig, scene/camera, captions, FX canvas, grain, HTML template).
- `kit/tts.py` — ElevenLabs VO with word timestamps. `kit/mix.py` — VO + music + SFX at -14 LUFS. `kit/sfx/` — sound library.
- `episodes/NN-slug/` — `script.txt`, `build.py` (scenes), `sfx.py` (cue list), `audio/`, `project/` (HyperFrames project).

## Pipeline per episode

1. `python3 kit/tts.py episodes/NN [voice_id name]`
2. `python3 episodes/NN/build.py` → `episodes/NN/project/index.html` + `timing.json`
3. `python3 kit/mix.py episodes/NN` → `project/assets/mix.mp3`
4. `cd episodes/NN/project && npx hyperframes lint && npx hyperframes check --json`
5. `npx hyperframes render --output <scratchpad>/NN.mp4`, then QC every 5th frame on contact sheets.

## Gotchas learned on the pilot

- GSAP `svgOrigin` is in global SVG coords: rotate rigged joints with `attr:{transform:"rotate(a)"}` on a group whose parent holds the translate.
- Never GSAP-transform an element that already has a `transform` attribute: wrap it.
- SVG filters vanish on zero-height bboxes (horizontal lines): pad with a transparent rect (`N()` does this).
- `fromTo` later in the timeline needs `immediateRender:false`, or its from-state shows from frame 0.
- Captions at `top:300px` and gauges above y≈1250 keep the YouTube Shorts safe zone clean.

## Status

- [ ] 01 brazen bull - [ ] 02 hiroshima - [ ] 03 electric chair - [ ] 04 stake
