I could not create report.md: the file write was blocked because subagents must return findings as text. The full report is below for you to save as `/tmp/claude-0/-home-user-hyperframes/dc37cee6-8f3e-5ef7-b6ea-f227cc435783/scratchpad/ref/v1/report.md`. I read all 45 sheets in order (every frame from 0 to 1332) and measured with python: flash decay, caption bounding boxes and timing, ring radii, pupil growth, glow profiles and colours.

## Summary of the main style findings

- **Cut list is wrong.** `metrics.json` misses 5 real cuts: 418, 554, 815, 855, 922. 574 is not a cut (heat stripes appear in the same scene), 934 and 1081 are white flashes inside a shot, and 1120 is a jump reframe. That gives 14 shots: mean 3.2 s, median 2.45 s, range 1.0–7.4 s, 2.9 cuts per 10 s. All cuts are hard cuts, 1–6 frames before a new sentence starts.
- **Look:** flat 2D neon-on-black, no grain.
  - Every scene uses a pure black top (`#000`) and a red glow rising from the bottom centre (`#CC1D0B` → `#8F150C` → black at about 55% height).
  - Hero objects are outlined with a three-layer neon line: white core about 5 px, red `#FF4A4E` band about 7 px, then a glow about 20 px wide.
  - Each idea is one medical-style diagram: mushroom cloud, blast rings, eye, skin layers, kimono torso, ear, window. A recurring X-ray skeleton man stands in for "you".
  - Blue is used only for "foreign" things: the river, the glass, the ad.
  - The final act switches to a grey brick wall where the man becomes a shadow, then a pocket watch stopped at 8:15, then black.
- **Motion:** the camera is locked in 12 of 14 shots and never shakes.
  - Each shot has one action that lands 0–7 frames before the stressed word: staggered ring pop-ins, pupil burn, blister pops then burst, shockwave sweep, eardrum rupture, glass crack then shatter, disintegration into embers.
  - Idle motion is embers, wind streaks and jittering particles.
  - Big moments are marked by 5 cream-white flashes (`#FDF3E8`) that fade exponentially over 7–30 frames, not by shake.
  - Camera moves only at the end: a slow push of about 0.3% per frame, a fast push and tilt down to the watch, a 0.9 s fade to black, then 0.9 s of black.
- **Captions:**
  - Roboto Condensed Bold, all caps, about 40 px at 576 px wide (6.9% of width), centred at 13% of frame height.
  - White `#F5F5F5` with a 2 px dark outline, plus one red `#FF4040` payload word in 64% of captions.
  - 1–3 words each (1.9 on average), on screen about 0.97 s, back to back with no gaps.
  - Each pops in at 110% scale and settles to 100% in 3 frames, about 2 frames before the word is spoken. There is no exit animation.
- **Hook:** 2 white frames, then a 1.3 s scene of a giant skeleton disintegrating as the city explodes, then a flash cut to the mushroom cloud with the title question in 2-word chunks.
- **Sponsor (f639–773):** a small "SN" logo coin pops onto the torso and stretches into a full-width rounded card (y 39–61%) playing a 3D clip. The story scene stays live behind it. The caption freezes on "НА ТЕЛЕ." (on the body) for 5.5 s, and the card closes by reversing the opening.
- **Weak spots:** long static holds, the frozen caption during the ad, an all-white first frame (bad for a thumbnail), and a countdown too fast to read as seconds.

---

# FULL REPORT (report.md)

# Forensic style breakdown: "How does it feel to be in Hiroshima…" (v1)

Source: 576x1024, 30 fps, 1333 frames (44.43 s). I reviewed all 45 contact sheets in order (every frame from 0 to 1332) plus all cut pairs. I checked about 30 frames at full resolution and measured with python: flash decay, caption bounding boxes, ring radii, pupil growth, neon line profiles and sampled hex values.

**Cut list correction.** `metrics.json` reports 10 cuts: 41, 177, 246, 276, 476, 574, 777, 934, 1020, 1081. The real scene changes are 41, 177, 246, 276, **418**, 476, **554**, 777, **815**, **855**, **922**, 1020 and **1120** (jump reframe). The cuts in bold were missed by the detector.

- 574 is not a cut: heat stripes appear inside the same scene.
- 934 and 1081 are white flashes inside a shot.

## 1. Second-by-second shot log

(fN = frame. Caption text is quoted exactly; **bold** = red accent word, everything else white.)

**SHOT 1, f0–40 (1.37 s): cold open, giant X-ray man in front of an exploding city**

- **s000**
  - f0–1: full cream-white frame (`#FDF3E8`).
  - f2–15: exponential fade from white. Luma goes 245 → 60 (about ×0.88 per frame).
  - The fade reveals a giant X-ray man, taller than the city:
    - black blocky silhouette with white bone line art and an egg-shaped head;
    - Hiroshima skyline in front of him: black block buildings with salmon outlines, orange window grids, and the A-Bomb Dome on the left;
    - an orange-yellow radial fireball behind him (core `#FF9B4F`, mid `#E8501E`).
  - f2–6: his arms snap up to outstretched in about 4 frames (ease-out).
  - f17: a blurred smoke column rises top-left.
  - f18–23: shockwave. Buildings shear about 15–25° to the right, white wind dashes fly right, and his left hand starts to crumble into embers (f20).
  - f24–29: his whole body disintegrates left to right into orange particles drifting right.
  - No caption. The transcript marks `[music]` from f16.
- **s001 (f30–40):** the ember cloud drifts and fades. Static camera.
- **f41 transition:** hard cut plus a white flash at 70% opacity. Luma decays 163 → 42 by f56.

**SHOT 2, f41–176 (4.53 s): neon mushroom cloud (the title question)**

- The cloud:
  - cap made of overlapping circles in dark rust (`#801F0C`) with thin cream inner lines (1.5 px);
  - a peach core ellipse (`#FF9B4F`);
  - two glowing condensation-ring ellipses;
  - the whole silhouette traced in red neon.
- Foreground: tilted ruined buildings, the dome, and a glowing ground line at y≈73%.
- Bottom 25%: red floor glow.
- Idle motion only: embers drift, white wind dashes slide right at 3–5 px per frame. The camera is locked (measured zoom −0.01).
- Captions (word start in brackets):
  - f44 "**КАКОВО** ЭТО" (Каково f44) — "What's it like"
  - f73 "ОКАЗАТЬСЯ В" (f74) — "to find yourself in"
  - f95 "**ХИРОСИМЕ** В МОМЕНТ" (f93) — "Hiroshima at the moment"
  - f129 "ВЗРЫВА АТОМНОЙ" (f127) — "of the atomic explosion"
  - f155 "**БОМБЫ?**" (f157) — "bomb?"
- **f177 transition:** hard cut, 1 frame before "Ты" (you) at f178.

**SHOT 3, f177–245 (2.3 s): blast-radius map**

- Black background with a blue neon river (`#5A78FF`) running diagonally from lower-left to upper-right.
- A red epicentre dot, then three neon rings expand in turn:
  - each starts 5–6 frames after the last (f179, f185, f190) and grows with ease-out over about 7 frames;
  - the outer ring settles at a 254 px radius (88% of frame width across) at f196.
- Labels pop in: "500 М", "1 КМ", "2 КМ" (white, about 14 px) and a red "ЭПИЦЕНТР" (epicentre).
- f196: a white "ТЫ" (you) marker pops onto the river at 500 m.
- Captions:
  - f178 "ТЫ В **500**" — "You're at 500"
  - f198 "МЕТРАХ ОТ" — "metres from"
  - f217 "**ЭПИЦЕНТРА.**" — "the epicentre"
- **f246 transition:** hard cut into a white flash.

**SHOT 4, f246–275 (1.0 s): "FLASH!"**

- The frame starts 90% cream-white and decays roughly linearly over about 28 frames.
- Revealed: the X-ray man, centred, palms up, bones glowing white with a lavender halo. As the flash fades he turns black with a pink-red glow on a dark background.
- f247 "**ВСПЫШКА!**" ("Flash!", spoken at f248). The caption's dark outline is visible against the light background.
- **f276 transition:** hard cut, 5 frames before "Свет" (light).

**SHOT 5, f276–417 (4.73 s): the eye's retina burns out**

- A flat almond eye, 70% of frame width, centred vertically:
  - sclera `#ECE6E5`, thick neon-red rim;
  - 12 white eyelash ticks;
  - iris `#D32620` with radial lines.
- f285: small red "v" veins appear.
- f290–345: a peach-to-cream pupil disc grows until it replaces the iris (S-curve). Measured pupil area: 129 px → 614 → 2872 → 7264 → 9971 px.
- Captions:
  - f277 "СВЕТ ТАКОЙ ЯРКИЙ," — "The light is so bright,"
  - f311 "ЧТО **СЕТЧАТКА**" (5 frames ahead of the word) — "that the retina"
  - f335 "**ВЫГОРАЕТ.**" — "burns out"
  - f363 "ТЫ НЕ УСПЕВАЕШЬ" — "You don't even have time"
  - f387 "ДАЖЕ **МОРГНУТЬ.**" — "to blink"
- The eye never blinks; it holds static.
- **f418 transition:** hard cut, 6 frames before "Следом" (next).

**SHOT 6, f418–475 (1.93 s): heat wave**

- Left two-thirds: six vertical wavy neon-red lines.
  - Wave period about 150 px, spacing about 60 px.
  - The phase shifts fast, about a quarter period per frame, so it reads as heat shimmer.
  - This is the most frame-to-frame motion anywhere in the video.
- Right side: a smaller X-ray man. The rim on his left side glows red.
- Captions:
  - f419 "СЛЕДОМ" — "Next"
  - f442 "**ТЕПЛОВОЙ УДАР.**" — "heat blast"
- **f476 transition:** hard cut.

**SHOT 7, f476–553 (2.6 s): skin cross-section**

- A rounded rectangle about 50% of frame width, from y 43% to 63%, made of three bands:
  - thin epidermis;
  - a middle band with three pink wavy lines;
  - a dark band.
- It has a 2 px white outline with red glow, and a small grey "КОЖА" (skin) label.
- f477–505: blister domes pop up left to right, one every 5 frames, scaling from 0 with a slight overshoot.
- f522: all blisters burst together into red glowing droplets that rise and fade over 6 frames. The burst comes 7 frames before the word "лопается" (bursts).
- Captions:
  - f477 "КОЖА ВЗДУВАЕТСЯ" — "Skin swells"
  - f506 "**ПУЗЫРЯМИ** И" — "into blisters and"
  - f528 "**ЛОПАЕТСЯ.**" — "bursts"
- **f554 transition:** hard cut.

**SHOT 8, f554–776 (7.43 s): kimono-print torso, then the ad**

- A torso shape about 40% of frame width:
  - dark brown fill (`#44140E`);
  - thin diagonal white stripes;
  - five white five-petal flowers;
  - neon-red outline.
- f574: a parallelogram band of thick glowing orange 45° stripes (`#DD6922`) snaps on behind the torso instantly.
- From f584 the flowers burn from white to orange-brown (`#E07A3A`).
- Captions:
  - f556 "**УЗОРЫ** С ОДЕЖДЫ" — "Patterns from clothing"
  - f584 "ВЫЖИГАЮТСЯ ПРЯМО" — "are burned right"
  - f613 "НА **ТЕЛЕ.**" — "into the body"
- **Ad opens:**
  - f639: a navy dot appears on the torso.
  - f640–644: it grows into a "SN" logo coin.
  - f645–650: the coin stretches into a pill, then a full-width card from y 39% to 61% with about 40 px corner radius.
  - The card is fully open at f651, as the ad voice-over starts at f652.
- **Ad content:** a pre-rendered 3D space scene (a squirrel mascot in a suit on a satellite, and a padlock).
  - Headlines in a wide white typeface: "ОБХОД / БЕЛЫХ / СПИСКОВ" (bypass whitelists), each word fading up from a blur.
  - Lightning cracks the padlock (f681–690), then it shatters (f697), and the headline becomes "ОБХОД ГЛУШИЛОК" (bypass jammers).
  - A satellite sends out a sonar ring (f710–716).
  - Then a dissolve to a "Ищи в Telegram" (search in Telegram) search field, which types "South" (f726–736).
  - A result row for "South Networks VPN" with a button slides in, and a cursor clicks it (f737–749).
- **Ad closes, f764–773:** the exact reverse — card, then pill, then coin, then dot, then gone.
- The caption stays frozen on "НА ТЕЛЕ." from f613 to f778, and the ad voice-over is not captioned. The scene underneath stays live.
- **f777 transition:** hard cut.

**SHOT 9, f777–814 (1.27 s): neon timer**

- Red neon digits "00:01" (cap height about 60 px) at y≈43%, with a small "СЕКУНДЫ" (seconds) label underneath.
- The digits hard-switch to 00:02 at f789 and 00:03 at f800.
- f779 "**ТРЕТЬЯ СЕКУНДА.**" — "Third second"
- **f815 transition:** hard cut.

**SHOT 10, f815–854 (1.33 s): shockwave**

- A neon-outlined skyline at y≈52%, with the X-ray man's arms raised.
- f816 "**УДАРНАЯ ВОЛНА!**" — "Shock wave!"
- f821: a double neon ring arc enters from the left and crosses the frame at about 40 px per frame (f823–830), then holds.
- Buildings shear in sequence from left to right. The figure is blown over, rotating about 65° (f823–832).
- **f855 transition:** hard cut.

**SHOT 11, f855–921 (2.23 s): ear**

- A neon ear (white core, red tube) with an ear canal leading to an eardrum disc with spokes.
- Sound-wave arcs ")" travel into the ear about every 10 frames.
- f868: the eardrum ruptures and red blood beads boil and jitter until the cut.
- Captions:
  - f856 "БАРАБАННЫЕ" — "ear" (first half of "eardrums")
  - f876 "**ПЕРЕПОНКИ**" — "drums"
  - f894 "ЛОПАЮТСЯ." — "burst" (here the verb is white)
- **f922 transition:** hard cut.

**SHOT 12, f922–1019 (3.27 s): window glass**

- A navy glass window (`#2C3A4A`) upper-left and the X-ray man on the right.
- f922: an impact dot.
- f923–933: a crack web draws on.
- f934: white flash at about 55% that decays in 7 frames. The glass explodes into blue-white glowing shards that stream right into the figure (f939–960). He raises his arm to shield himself.
- f960–985: red blood splotches spread over the body.
- Captions:
  - f923 "**СТЁКЛА** ВПИВАЮТСЯ" — "Glass shards dig"
  - f953 "В КОЖУ СОТНЯМИ" — "into the skin by the hundreds"
  - f982 "**ОСКОЛКОВ.**" — "of shards"
- **f1020 transition:** hard cut.

**SHOT 13, f1020–1119 (3.33 s): grey stone wall**

- A desaturated taupe brick wall (`#716761`) with a stone step, a dark floor (`#272221`) and a black gradient across the top 20%.
- The X-ray man is drawn in black and white only, hand to forehead. A gold pocket watch lies on the step.
- There is a small push-in at the start.
- f1068–1080: the body tints dark red.
- f1081: white flash at 90%, slow decay over about 30 frames.
- f1087–1109: the body crumbles into orange embers blowing right, leaving a dark shadow silhouette (`#231E1B`) on the wall.
- Captions:
  - f1021 "А НА КАМЕННОЙ" — "And on the stone"
  - f1042 "**СТЕНЕ** ЗА ТОБОЙ…" — "wall behind you…"
  - f1082 "ОСТАЁТСЯ **ТЕНЬ.**" — "a shadow remains"
- **f1120 transition:** jump reframe, about 8% tighter and lower.

**SHOT 14, f1120–1332 (7.1 s): push to the watch, then black**

- f1120–1225: slow push-in, about +33% scale with ease-out, with dust specks floating.
- f1230–1251: fast push and tilt down (about 21 frames, ease-in-out) to the pocket watch:
  - gold case, cream face;
  - hands at **8:15**;
  - red second hand;
  - cracked glass.
- f1264–1290: fade to black (ease-in).
- Caption fades out f1300–1306, then pure black f1306–1332. No end card.
- Captions:
  - f1122 "**ТЕНЬ** ЧЕЛОВЕКА," — "the shadow of a person,"
  - f1156 "КОТОРЫМ ТЫ БЫЛ" — "that you were"
  - f1184 "СЕКУНДУ **НАЗАД.**" — "a second ago"
  - f1230 "А ПОТОМ" — "And then"
  - f1251 "НАСТУПАЕТ" — "comes"
  - f1269 "**ТЕМНОТА.**" — "darkness"

## 2. LOOK

**Palette**

| Role             | Colour                                                                          |
| ---------------- | ------------------------------------------------------------------------------- |
| Background       | black `#000`–`#050202` (33–56% of pixels darker than 16)                        |
| Floor glow       | `#CC1D0B` (bottom), `#A61809`, `#8F150C`, `#4E0901`; corners `#660F06`          |
| Neon line        | body `#FF4A4E`–`#FF646B`, core `#F7EBF1`, falloff to `#2E0C0F` over about 20 px |
| Captions         | red `#FF4040`, white `#F5F5F5`                                                  |
| Orange accents   | `#FF9B4F`, `#DD6922`, `#E8501E`, `#E07A3A`                                      |
| Dark fills       | `#801F0C`, `#44140E`, `#141010`; building outline `#E8706A`                     |
| Blue accents     | `#5A78FF`, `#9FC8FF`, glass `#2C3A4A`                                           |
| Eye              | sclera `#ECE6E5`, iris `#D32620`, burnt pupil `#FFF1DC`                         |
| Wall (final act) | `#716761`–`#796C64`, floor `#272221`, shadow `#231E1B`                          |
| Watch            | gold `#C9A464`, face `#E9E1D2`                                                  |
| Flash            | cream `#FDF3E8`                                                                 |

**Lighting and contrast**

- One light source: a red glow from below/behind at about (50%, 105%). The top third of the frame is pure black.
- Objects light themselves (neon). The only shadow in the video is the wall shadow in the story.
- Measured vignette: −15 to −65.
- Contrast is very high: mean brightness 20–50 in the red scenes, clipped highlights under 1.5% except during flashes.
- No grain: flat-area noise standard deviation is 0.06 and temporal noise is 0.

**Glow construction:** a white core about 5 px, a red band about 7 px on each side, then a soft glow about 20 px on each side. Solid filled objects get only the outer glow on their contour plus thin cream inner lines (1.5–2 px at 576 px width).

**Character (the X-ray man):**

- Blocky black body with tapered stick limbs.
- White bones: rib arcs, a spine of small circles, pelvis as two circles, knee circles.
- Dark grey egg-shaped head (`#3A3536`), red angry brows, boxed teeth.
- Reused in six scenes.
- Everything is 2D except the sponsor clip, which is 3D.

## 3. MOTION

- **Camera:** static in 12 of 14 shots. No shake, whip pans or handheld. Impacts are shown with flashes.
- **One hero action per shot**, landing 0–7 frames before the stressed word.
- **Durations:**

| Move            | Timing                                          |
| --------------- | ----------------------------------------------- |
| Pop-ins         | 3–7 frames, back-out ease                       |
| Rings           | about 7 frames each, staggered 5–6 frames       |
| Sweeps          | about 10 frames at about 40 px/frame, then hold |
| Transformations | 40–60 frames, ease-in-out                       |
| Disintegration  | 10–30 frames, left to right, drifting right     |
| Flashes         | 7–30 frames, exponential ×0.8–0.95 per frame    |

- **Idle motion:**
  - embers drift at 1–3 px per frame;
  - wind dashes move at 3–6 px per frame;
  - blood beads jitter;
  - sound arcs loop;
  - heat lines shimmer;
  - dust specks float.
- Something new happens about every 1 s.
- Camera moves appear only in the final act:
  - slow push of about 0.3% per frame;
  - fast push of 21 frames;
  - 26-frame fade.

## 4. EDIT RHYTHM

**Shot lengths (frames):**

| Shot                | Frames |
| ------------------- | ------ |
| 1                   | 41     |
| 2                   | 136    |
| 3                   | 69     |
| 4                   | 30     |
| 5                   | 142    |
| 6                   | 58     |
| 7                   | 78     |
| 8 (includes the ad) | 223    |
| 9                   | 38     |
| 10                  | 40     |
| 11                  | 67     |
| 12                  | 98     |
| 13                  | 100    |
| 14                  | 213    |

**Statistics**

- Mean 3.17 s, median 2.45 s, minimum 1.0 s, maximum 7.4 s.
- 2.9 cuts per 10 s.
- Caption changes average about 1 per second, so the felt pace is roughly one beat per second.

**Cuts and transitions**

- Cuts land 1–6 frames before a sentence starts, never in the middle of a phrase.
- Transitions used:
  - hard cuts only (11);
  - flashes at f0, f41, f246, f934 and f1081;
  - one jump reframe;
  - one final fade to black.

**Hook and ending**

- Hook:
  - 2 white frames;
  - then a 1.3 s action teaser before any voice-over;
  - then a flash cut to the iconic mushroom cloud with the question in 2-word chunks;
  - no separate title bar.
- Ending:
  - a slow push on the shadow;
  - the 8:15 watch;
  - a 0.87 s fade;
  - 0.9 s of black, which loops into the white opening.

## 5. CAPTION SPEC

- **Font:** Roboto Condensed Bold, all caps, centred on one line.
- **Position:** visual centre at y = 13.0% of frame height (cap-height band 119–147 of 1024).
- **Size:** cap height 2.7% of frame height. Font size ≈ 40 px at 576 px wide, which is about 6.9% of width (75 px at 1080).
- **Width:** at most 76% of frame width, never wraps, at most about 17 characters.
- **Colours:** white `#F5F5F5` and red `#FF4040`, with a near-black outline of about 2 px.
- **In-animation:** appears at 110% scale and settles to 100% in 3 frames. No fade, no exit; the next caption replaces it on the same frame.
- **Chunks:**
  - 39 captions, 1–3 words each (average 1.9): 12 one-word, 18 two-word, 9 three-word.
  - Prepositions are left dangling at the end of a chunk ("…В", "…ОТ", "…И").
  - Numbers are written as numerals.
- **Timing:**
  - on screen for a median of 29 frames (range 18–46), except 166 frames frozen during the ad;
  - appears on average 2 frames before the word (range 5 frames early to 2 frames late).
- **Red accent:** in 64% of captions, on the payload word — the shocking noun or verb, the place, the number, or a whole exclamation. Setup chunks are white, so the pattern usually alternates white setup, red payload.
- **Diagram labels:** about 13–16 px. The timer digits are about 60 px cap height with a red glow.

## 6. SOUND CUES (inferred)

| Frame(s)         | Inferred sound                                   |
| ---------------- | ------------------------------------------------ |
| f0               | boom                                             |
| f20–30           | crackle and wind                                 |
| f41              | impact, then drone                               |
| f179, f185, f190 | sonar pings                                      |
| f196             | pop                                              |
| f246             | flash hit with tinnitus decaying about 1 s       |
| f290–345         | sizzle / whine                                   |
| f418             | heat roar                                        |
| f477–505         | 5 blips                                          |
| f522             | wet pop                                          |
| f574             | sizzle                                           |
| f639–651         | UI pop and whoosh (ad SFX inside)                |
| f764             | close whoosh                                     |
| f777, f789, f800 | ticks                                            |
| f821             | bass boom and sweep                              |
| f868             | pop, then muffled tinnitus                       |
| f922–933         | creak                                            |
| f934             | shatter                                          |
| f955             | thuds                                            |
| f1081            | final boom and crackle                           |
| f1230            | whoosh                                           |
| after f1230      | a watch tick that stops, then silence into black |

## 7. REPRODUCTION RECIPE (HyperFrames at 1080x1920; multiply 576-wide measurements by 1.875)

**Stage background**

```css
background:
  radial-gradient(
    ellipse 75% 45% at 50% 106%,
    #d21e0b 0%,
    #a51809 18%,
    #6e1006 38%,
    #2a0603 60%,
    #000 78%
  ),
  #000;
```

Keep the top 30% pure black for the captions.

**Neon path (SVG)** — draw three copies:

1. Glow: stroke `#ff2a2a`, width 18, opacity 0.55, blur stdDev about 10.
2. Body: stroke `#ff4a4e`, width 11, `drop-shadow(0 0 6px #ff3040)`.
3. Core: stroke `#f8ecf2`, width 4.

Use round caps and joins. Optional extra halo:

```css
filter: drop-shadow(0 0 4px #ff3040) drop-shadow(0 0 18px #ff2030)
  drop-shadow(0 0 40px rgba(255, 30, 30, 0.45));
```

Use the same recipe in `#5a78ff` / `#9fc8ff` for cool elements.

**Filled objects:** flat fills (`#801f0c`, `#44140e`, `#0b0909`), inner lines `#f3e6dc` at 3 px, plus one neon contour.

**X-ray man (SVG symbol):**

- 3 px white bones; rig the limbs with transform-origins at the joints.
- Contour `drop-shadow(0 0 8px #ff5060)`; switch to white during flashes.
- Arm raise: 4–6 frames, `back.out(1.4)`.

**Flash:** a full-frame `#fdf3e8` div above the scene but below the captions.

- Set opacity 0.9 on the hit, then animate to 0 with `expo.out` over 0.9 s (big hit), 0.5 s (cut flash) or 0.25 s (small hit).
- At the very start, hold 2 frames at opacity 1 first.

**Disintegration**

- Seed 400–800 particle points inside the silhouette.
- Mask the figure left to right (`clip-path: inset`) over 0.35–1 s.
- Release particles as the mask passes:
  - 2–3 px orange (`#ff9a4a` → `#e2501e`);
  - velocity x +2 to +6, y ±1 px per frame;
  - fade over 15–25 frames.
- Leave a `#231e1b` shadow silhouette underneath for the wall beat.

**Element animations**

| Element    | Animation                                                                                                                                            |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rings      | `attr r` 0→R, 0.23 s `power3.out`, stagger 0.18 s                                                                                                    |
| Labels     | scale 0→1, 0.15 s `back.out(2)`                                                                                                                      |
| Pupil      | r → iris radius, 1.8 s `power2.inOut`                                                                                                                |
| Blisters   | scale 0→1 from the bottom, 0.17 s `back.out(2)`, stagger 0.17 s; burst = 40 red dots rising 20–60 px and fading in 0.2 s                             |
| Heat lines | `x = A·sin(2πy/150 + φ)`, φ += 1.5 rad per frame, driven by the timeline                                                                             |
| Shockwave  | circles centred at cx = −200, r 0→900 over 0.35 s `power2.out`; buildings skewX 0→18° from the bottom, staggered by x; figure rotates 65° over 0.3 s |

**Idle layers (seeded random)**

- 15–25 embers `#ff6a2a`, 1.5–3 px radius.
- White wind dashes, 2 × 16–40 px, moving at 4–6 px per frame and wrapping around.

**Camera**

- Static wrapper by default.
- Ending sequence:
  - scale 1→1.33 over 3.5 s (`sine.out`);
  - then scale to 3.2 with y −900 over 0.7 s (`power2.inOut`) onto the watch;
  - black overlay to opacity 1 over 0.87 s (`power1.in`);
  - captions fade 0.2 s later;
  - hold 0.9 s of black.

**Caption CSS**

```css
.cap {
  position: absolute;
  top: 13%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  text-align: center;
  font: 700 75px/1 "Roboto Condensed";
  text-transform: uppercase;
  color: #f5f5f5;
  -webkit-text-stroke: 3px #111;
  paint-order: stroke fill;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
}
.cap .hl {
  color: #ff4040;
}
```

**Caption timing**

- Show each caption 2 frames before its first word, and swap at the next chunk's first word.
- Entry: `fromTo` scale 1.1→1 over 0.1 s, `power2.out`.
- Red goes on one payload word per sentence; short exclamations are fully red.
- English example: "WHAT'S IT LIKE / TO BE IN / **HIROSHIMA** THE MOMENT / THE ATOMIC BOMB / **DROPS?**", "YOU'RE **500** / METERS FROM / **GROUND ZERO.**"

**Scene template**

- One idea per scene, 1–4.7 s.
- Hard cut 2–5 frames before the sentence.
- One action 0–7 frames before the stressed word, then hold with idle particles.
- About 5 flashes per 45 s.

**Sponsor template**

- A small coin pops onto the hero object and stretches (0.1 s pop, 0.2 s stretch) into a full-width card: radius about 70 px, height 22% of the frame, vertically centred.
- The scene stays live underneath. Close by reversing the open.
- Place it at an act break.
- Better than the reference: keep the captions running during the ad.

## 8. WHAT WORKS / WEAK SPOTS

**What works**

- A strict palette (black, one red, one orange, white). Blue appears only for "foreign" things.
- One literal diagram per sentence.
- A locked camera with one decisive action on each stressed word.
- Flashes used as punctuation.
- A recurring "you" mascot that pays off in the shadow ending.
- A tonal shift to grey, the 8:15 watch and black.
- The red payload words alone tell the story to a muted viewer.

**Weak spots**

- Static holds of 4.5–4.7 s on the mushroom and the eye. The mushroom shot needs a slow push.
- The caption is frozen for 5.5 s during the ad, and the 3D ad style clashes with the 2D look.
- The first frame is pure white, which makes a poor thumbnail.
- The timer counts 1→3 in 0.75 s, too fast to read as seconds.
- The skin and torso diagrams fill only 40–50% of the frame width.
- The mascot's scale jumps between shots without a reason.
- There is no re-hook after the ad.

Supporting files in `/tmp/claude-0/-home-user-hyperframes/dc37cee6-8f3e-5ef7-b6ea-f227cc435783/scratchpad/ref/v1/`:

- `full/` — full-resolution PNG frames
- `textcrop.png` — caption outline detail
- `heat_seq.png` — four consecutive heat-wave frames
- `cmp_1119_1120.png` — the f1120 jump reframe and slow push compared
