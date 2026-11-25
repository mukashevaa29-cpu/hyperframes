# Visual review brief

You are reviewing reference videos from a Russian YouTube channel ("The Last Rule", flat 2D vector
animation, "N rules to survive X" format, 13-28 min each). We are building a style bible so a new
English-language channel can produce videos with the same craft (we copy technique, not their
characters, stories or text). Be concrete and measurable; vague adjectives are useless.

Root: /tmp/claude-0/-home-user-hyperframes/2e98b923-55d9-5c59-87c3-4747827667cd/scratchpad/ref

For each video `NN_<id>` assigned to you, under `analysis/NN_<id>/`:

- `summary.json`: video-level metrics computed from EVERY frame at 30 fps (cuts/min, shot length
  percentiles, pop-ins/min = UI elements/labels appearing, caption changes/min, camera moves per
  shot, transitions, luma/contrast/saturation, vignette = centre-minus-edge luma, palette, loudness).
- `shots.json`: one entry per shot (start s, dur, into = transition type, camera = static/push-in/
  pull-out/pan/tilt/shake, zoom = cumulative scale over the shot, light_events = darken/brighten/flash
  with timestamps, popin_t = timestamps of pop-ins).
- `sheets/t_XX.jpg`: contact sheets, one frame every 3 s, 6x8 tiles, timestamp in yellow top-left.
  LOOK AT EVERY ONE.
- `sheets/cuts_XX.jpg`: each row = one cut, 5 frames before + 3 after (shot number on the left).
  Look at all of them.
- `shots/NNNN.jpg`: first frame of each shot at 960x540; open specific ones when you need detail
  (shadows, line weight, textures, typography). Open at least 10 per video.
- `../transcripts/NN_<id>.json` (if present): Russian narration with word timings.
- Original video `../videos/NN_<id>.mkv` if you must grab an exact frame:
  `ffmpeg -ss <sec> -i <file> -frames:v 1 -vf scale=960:-1 <out>.jpg` (write outputs into
  `analysis/NN_<id>/review/`, nowhere else).

Write `analysis/NN_<id>/review.md` per video with these sections, each with specifics
(timestamps, hex colours, pixel/percent sizes, durations):

1. Structure: cold open (what happens in first 30-60 s, hook mechanics), chapter/rule cards
   (look, duration, animation), progress indicators, ending / CTA.
2. Characters: proportions (head:body), outline or no outline, line weight, shading (flat / cel /
   none), face design (eyes, mouth), how they animate (blink, arm swing, walk, mouth flaps?), how
   many per scene, silhouettes.
3. Backgrounds & locations: list every distinct location with timestamp; depth layers; level of
   detail; texture/grain; perspective (side view? 3/4?).
4. Light & shadow: day/night ratio, light sources (lamps, torches, screens, moon), how light is drawn
   (radial gradients, cones, glow), shadows (drop shadows? none? silhouettes?), vignette, darkening
   used for tension, colour temperature shifts.
5. Contrast & colour: palette families per mood, accent colours and what they mean (red = danger?
   green = safe? yellow = keyword?), saturation.
6. Camera: how push-ins/pull-outs are used (speed, when), pans, shake (when, intensity), any parallax.
   Use shots.json numbers.
7. Transitions & cuts: cut rhythm vs narration (cut on sentence end?), any special transitions,
   what the first frames of a new shot look like (fade-in from dark? elements build in?).
8. Overlays, text & effects: caption style (font look, weight, case, size as % of frame height,
   position, highlight colours, words per caption, karaoke?), labels/stickers/stamps (shapes,
   colours, tilt, pop animation), icons, arrows, X marks, timers/clocks, phone UIs, particles,
   rain/snow, glows, flicker, grain, screen shake on impacts.
9. Pacing: how often something new appears; relation to words.
10. Top 10 reusable techniques from this video (most distinctive first).

Finally, in your reply to me, give a cross-video synthesis for your group (what is constant, what
varies) in <= 400 words. Do not paste the per-video files into the reply.
