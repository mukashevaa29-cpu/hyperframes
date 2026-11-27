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

- Built and checked: 01 brazen bull, 02 hiroshima, 03 electric chair, 04 stake (placeholder voice: Brian).
- Next: the owner picks the channel voice, then re-voice, rebuild, remix and re-render all four.

## Batch 2 (owner picked 2026-11-27): not only executions — any "How does it feel?"

05 space without a suit · 06 dinosaur asteroid · 07 Everest death zone · 08 Titanic · 09 Chernobyl.
Same pipeline: Jax (w1ovTGXs1yF9qRmr8AO9), `kit/tts.py` → `kit/tighten.py` → `build.py` → `kit/music.py` (music.json) → `kit/mix.py` → render → agent QC.
Every script opens "How does it feel? When…" and ends "And then... comes darkness." (shared `ep.ending`).
Facts kept conservative (LeBlanc 1966 vacuum accident; Chicxulub 10 km / 20 km/s; death zone 8,000 m, 1/3 oxygen;
Titanic −2 °C, ~1,500 dead, 2:20 AM; Chernobyl 1:23 AM, 28 ARS deaths within months).
