I could not write report.md: the harness refuses report files from subagents. The full report is below, after this summary. I read all 74 sheets (s000–s073) and all cut pairs, and measured everything else with OpenCV and python. Intermediate data is in /tmp/claude-0/-home-user-hyperframes/dc37cee6-8f3e-5ef7-b6ea-f227cc435783/scratchpad/ref/v2 (diff.json, shake.json, caps.py, notes/, fr/).

## Summary (most important findings)

- **Look:** flat 2D vector neon line-art. Pure black #010101 with no grain, and a red floor glow rising from the bottom centre (#861204 → #330601 → black by 60 % of height). Every object has a dark fill, a cream 2.5 px outline (#f6efee) and a double red outer glow. Electricity is the only cool colour: white fractal lightning plus blurred blue plasma (#668fd5 / #8a9cff), redrawn every frame. The characters are gore-free skeletons ("you"). The wood is #46302c.
- **Camera:** static about 85 % of the time. The signature move is a **cut-in scale-settle** on about 14 of the cuts: the new shot starts at 0.889 scale and reaches 1.0 in 5 frames (+4.9/+3.3/+2.1/+1.2/+0.4 %), like power2.out.
  - Other moves: the opening pull-out (2.35×→1×, 0.75 s), one truck (1.65×, 187 px), +27 % step punch-ins, and 10–37 px single-frame jolts on emphasis words.
  - The violence comes from the 30 fps electric "boil" (luma ±7–10 per frame), not from camera shake.
- **Edit:** 31 shots in 73.9 s, mean 2.38 s. Bright chair scenes alternate with dark infographic inserts every 2–4 s: title card, "№1", switch, voltmeter, timer, generator %, heart/ECG, eye. The voltmeter and timer come back in bigger versions for the second shock.
  - **The cut burst at frames 435–449 is a spotlight strike flicker:** the stage lights go on and off in 2-frame steps (on f440, off f442, on f444, off f446, on from f449).
- **Hook:** it opens in the middle of the electrocution, in close-up, with crackle and no caption for 1.67 s, then pulls out to the wide stage. The question caption lands word by word on the voice-over.
- **Ending:** the heart flatlines, the eye closes into a red line, the line extends full-width like a monitor flatline, then a 14-frame linear fade to black. No card, no CTA.
- **Captions:**
  - Position and font: single line centred at y = 12.9 % of height (cap height 29 px = 5 % of width, about 40 px font), ALL CAPS, Roboto Condensed Bold / Oswald look.
  - Colour: white #F5F5F5, accent red #F54341. 30 % of words are red: sentence-final nouns and verbs, numbers, names, visceral words.
  - Timing: 1.86 words per caption on average, about 0.9 s each, hard swaps with no animation. They land 0–5 frames before the word onset, never late.
- **Sponsor (34.1–38.7 s):** the background freezes on the close-up. A round "SN" badge appears on the skeleton's eye socket and morphs into a full-width rounded pill banner (y 39–61 %, a navy 3D render). It reverses back into the badge at the end. The main caption stays frozen on "СУДОРОГОЙ." the whole time.

The full report follows.

---

# FULL REPORT — "How does it feel to be executed in the electric chair" (Russian Short, 576x1024, 30 fps, 2217 frames = 73.9 s)

Frame numbers are source indices (f); t = f/30. Caption colour marks: [R] = accent red word, otherwise white.

## Definitions used in the log

**Cut-in scale-settle (CSS).** The new shot appears at 0.889 scale around the frame centre. It reaches 1.0 in 5 frames with an ease-out. Measured at f158, 250, 435, 619, 711, 783, 929, 1307, 1346, 1445, 1664, 1829, 1891 and 2104.

**WIDE-STAGE.** The master composition that recurs through the video:

- the chair centred, its bottom at about 83 % of height;
- two grey translucent spotlight cones from the top corners, with an elliptical light pool on the floor;
- a red floor with faint perspective lines;
- black above.

## 1. SECOND-BY-SECOND LOG

### Act 1 — Hook (s0–s5)

**s0 (f0–29).**

- On screen: an extreme close-up of the skeleton in the chair. The brown slatted chair back fills the frame, with red glowing uprights at the edges. A white fractal lightning web comes off the helmet and is redrawn every frame.
- Camera: the close-up holds f0–16 with jitter. **The pull-out runs f17–39** (2.35×→1×, peak speed around f28–31, ease-in-out).
- Blue plasma appears from f20; the red floor from f27.
- Caption: none. Voice-over: "[electric crackle]" f0–48.

**s1 (f30–59).**

- The pull-out lands on WIDE-STAGE (settles f39).
- On screen: the skeleton is arched. Blue-white plasma "flames" shoot left and right, and white lightning crawls over the chair. Everything is redrawn every frame and luma flickers ±7–8 per frame.
- Camera: static (global motion under 0.4 px per frame).
- Caption: f50 "[R]КАКОВО ЭТО", exactly on the voice-over at f50.

**s2–s4 (f60–149).**

- The same wide shot under electrocution, with a slight push.
- Captions:
  - f81 "КОГДА ТЕБЯ КАЗНЯТ" (on the voice-over at f81);
  - f111 "НА [R]ЭЛЕКТРИЧЕСКОМ";
  - f137 "[R]СТУЛЕ?".

**s5 (f150–157).** Same shot. **Hard cut at f158.**

### Act 2 — Setup: place, time, identity (s5–s14)

**s5–s7 (f158–249). Title card.**

- On screen: black with many thin vertical red lines that brighten toward the bottom, and a faint horizon line at 37 %. White "НЬЮ-ЙОРК" sits at 41 % with a red dashed underline (8 dashes) at 51 %.
- CSS on the label, f158–163.
- Caption f159 "[R]НЬЮ-ЙОРК.": 4 frames before the voice-over, and a duplicate of the on-screen label.
- **f189:** a huge red neon "1890" pops on in a single frame, with "ТЮРЬМА ОБЕРН" in tiny type under it. Caption f189 "[R]1890 ГОД." (voice-over at f193).
- The card is static for about 2 s.

**s8–s10 (f250–313). Mugshot.** The cut at f250 was not picked up by the cut detector.

- On screen:
  - faint height-chart lines labelled 190–150;
  - the red floor glow;
  - the skeleton holding a black placard with a white border and red glow: "У. КЕММЛЕР" and "№1 · 1890".
- CSS on f250–255.
- The floor glow flares like a camera flash at f262–266.
- Captions: f251 "ТЕБЯ ЗОВУТ УИЛЬЯМ" (voice-over f252), then f288 "[R]КЕММЛЕР.".

**f314. CRT-style collapse.** One frame of black with a single blue dot.

**s10–s14 (f314–434). "№1" insert.**

- On screen: "№1" in red neon plus a lightning-bolt icon (white core, blue glow, navy fill).
- It scales in from 0.2 over 5 frames (per-frame 1.82, 1.32, 1.16, 1.07), an expo-out.
- Captions: f315 "И ТЫ СТАНЕШЬ" (voice-over f316), f338 "[R]ПЕРВЫМ ЧЕЛОВЕКОМ", f363 "В ИСТОРИИ,", f388 "КОТОРОГО УБЬЮТ" (on the voice-over).
- From f386, blue-violet lightning arcs crawl along y 55–60 %.
- f390–395: the sub-label "ПЕРВАЯ КАЗНЬ ТОКОМ" scales in.
- The arcs strike the "№1" letters, with white-hot cracks at f393, 397, 399, 404, 409 and 413.
- Caption f414 "[R]ТОКОМ.".
- **Hard cut at f435.**

### Act 3 — Preparation (s14–s26)

**s14 (f435–449). Empty chair, dark stage.**

- CSS on f435–440.
- **Spotlight strike flicker:** ON f440–441, OFF f442–443, ON f444–445, OFF f446–448, ON from f449. This is the "burst of cuts" (luma toggles between 21 and 37).
- Caption f436 "ТЕБЯ УСАЖИВАЮТ В", exactly on the voice-over.

**s15–s16 (f450–509).**

- The chair sits under the spotlights. At **f457** the skeleton pops on seated, with no tween.
- Camera: static.
- Captions: f464 "ТЯЖЁЛОЕ", f477 "ДЕРЕВЯННОЕ", f493 "[R]КРЕСЛО.".

**s17–s18 (f510–571). Punch-in and truck.**

- **f514:** a one-frame punch-in.
- The camera then trucks and pans to the right forearm and strap: 1.65× scale and −187 px over f514–540.
- **The pan peaks at −19 px per frame at f531–533**, on the word "ЗАТЯГИВАЮТ", then eases to zero by f543.
- Captions: f516 "РЕМНЯМИ", f531 "ЗАТЯГИВАЮТ [R]РУКИ.".

**s19 (f572–594).**

- **Hard cut at f572** to the seat and legs.
- Ankle straps pop on at f575 and f578–580: brown buckles with a red glow.
- Caption f572 "[R]НОГИ.", 5 frames before the voice-over.

**s19–s20 (f595–618).**

- Cut to a medium shot of the torso. No CSS here.
- The chest strap pops on at f598.
- Caption f596 "[R]ГРУДЬ.".

**s20–s23 (f619–710).**

- Cut to a slightly wider shot with CSS.
- The helmet (grey dome, white rivet band, a cable running up and out of frame) descends f630→652, about 0.73 s with an ease-out.
- Captions:
  - f620 "НА ГОЛОВУ";
  - f636 "НАДЕВАЮТ";
  - f649 "МЕТАЛЛИЧЕСКИЙ";
  - f667 "[R]ШЛЕМ С МОКРОЙ";
  - f690 "[R]ГУБКОЙ.".

**s23–s26 (f711–782).**

- **Cut to a close-up (about 1.4×)** with CSS, then a slow push of about 1.7 %.
- A pale-blue callout "ВОДА" (#b8d0ff) with a leader line points at the sponge. Blue water droplets drip from the helmet.
- Captions: f712 "[R]ВОДА НУЖНА," (voice-over f715), f733 "ЧТОБЫ ТОК ПРОШЁЛ", f762 "ЛУЧШЕ.".
- **Hard cut at f783.**

### Act 4 — First shock (s26–s34)

**f783–838. Knife switch.**

- On screen: a dark #141416 card with a white stroke and a red glow, labelled "ВЫКЛ" (white) and "ВКЛ" (red). The executioner's black handle enters from the right.
- CSS on f783–789.
- The lever moves **slowly f784–795, then accelerates f796–808** (ease-in).
- **Contact at f809:** a white star-burst spark plus a blue flash, then crackles until f838.
- Captions: f784 "ПАЛАЧ ОПУСКАЕТ" (on the voice-over), f812 "[R]РУБИЛЬНИК.".

**f839–849. Voltmeter.**

- On screen: a dark semicircular dial with white ticks for 0–2000, a red zone from 1500 to 2000, and the label "ВОЛЬТ".
- **The needle goes 0→1000 in 4 frames with an overshoot**, then trembles.
- Caption f841 "[R]1000 [R]ВОЛЬТ!".
- **Hard cut at f850.**

**f850–928. WIDE-STAGE, electrocution #1.**

- Heavy plasma and lightning, with a per-frame boil.
- A jolt at f873–875 (dy 37 px) on the word "МЫШЦЫ".
- Captions: f874 "ВСЕ [R]МЫШЦЫ", f893 "СЖИМАЮТСЯ РАЗОМ.".
- **Hard cut at f929.**

**f929–1021. Close-up electrocution.**

- On screen: the slatted chair back fills the frame. White lightning sprouts above the helmet, with no blue in this shot.
- CSS with lateral jolts (f931–933, f999–1000, f1014–1015).
- **f977:** a +27 % step punch-in on the word "ЧЕЛЮСТЬ".
- Captions:
  - f931 "ТЫ НЕ МОЖЕШЬ" (on the voice-over);
  - f951 "ДАЖЕ [R]ЗАКРИЧАТЬ";
  - f977 "ЧЕЛЮСТЬ СВЕЛО";
  - f998 "[R]СУДОРОГОЙ.".

### Act 5 — Sponsor (f1022–1160)

**s34 (f1022–1049).**

- The background freezes on a tighter close-up (frame difference drops to 0.1–0.4).
- **f1022:** a round navy "SN" badge appears on the skeleton's eye socket.
- **f1027–1031:** it morphs into a pill, then into a rounded rectangle at x 8–568, y 398–625 (39–61 % of height), radius about 40 px.
- The banner is a 3D navy space scene:
  - a padlock labelled "ДОСТУП ОГРАНИЧЕН";
  - a squirrel in a suit standing on an "SN" satellite;
  - the Earth's horizon.
- Text in a wide extended sans: "ОБХОД" (f1033), then "БЕЛЫХ" (f1044) and "СПИСКОВ" typing in.

**s35 (f1050–1079).**

- Lightning strikes the lock (f1063–1068) and it shatters.
- The text swaps to "ГЛУШИЛОК".

**s36 (f1080–1109).**

- Magenta signal streaks, then a blue ring shockwave (f1092–1099).
- "Ищи в Telegram" appears with a search field; "@south" types in.

**s37 (f1110–1139).**

- A result row "South Networks VPN" with an "ОТКРЫТЬ" button (f1119).
- A cursor clicks (f1129–1133).

**s38 (f1140–1160).**

- Reverse morph f1147–1154 back into the badge. The badge disappears at f1155.
- The close-up resumes for 6 frames.

Throughout the ad:

- the caption stays frozen on "[R]СУДОРОГОЙ." for 164 frames;
- the voice-over is the ad read over "[музыка]" (f1035–1135).

### Act 6 — Aftermath of the first shock (s38–s50)

**f1161–1262. WIDE-STAGE, body arched.**

- Plasma on the right; the wrist straps glow red.
- Captions:
  - f1162 "ТЕЛО [R]ВЫГИБАЕТСЯ";
  - f1187 "ТАК СИЛЬНО,";
  - f1207 "ЧТО РЕМНИ";
  - f1224 "ВПИВАЮТСЯ В [R]КОЖУ.".

**f1263–1306. Timer.**

- On screen: a red neon "00:00" with the label "СЕКУНД". A blue electric ring draws itself around the timer.
- It counts to 00:17 over 38 frames.
- Caption f1264 "[R]17 СЕКУНД.".

**f1307–1444. Power off.**

- WIDE-STAGE with no electricity: the skeleton slumped, dark smoke rising. CSS at the start.
- Caption f1309 "ТОК [R]ОТКЛЮЧАЮТ.", exactly on the voice-over.
- **f1345:** a one-frame pull-back to 0.707× plus CSS.
- A doctor skeleton in a top hat walks in from the right (f1346–1371, about 4 px per frame) and leans toward the chair.
- Captions: f1347 "ВРАЧ ПОДХОДИТ К", f1372 "ТЕБЕ И ОБЪЯВЛЯЕТ:".
- **Stamp slam at f1411:** a red neon "МЁРТВ" stamp rotated −12° goes from 2.5× to 1× in 4 frames (ease-in), with no shake.
- Caption f1412 "[R]МЁРТВ.".

**f1445–1500. Medium shot of the skeleton.**

- The stamp is still visible but faded. CSS plus a slow push.
- Caption f1447 "НО ТЫ...".
- **f1473:** the stamp is replaced by an X-ray: red glowing lungs and a thin red scanner circle, pulsing like breathing.
- Caption f1475 "[R]ДЫШИШЬ.".

### Act 7 — Waiting (s50–s58)

**f1501–1576. Witnesses.**

- On screen: five skeletons behind a railing, with red "!" particles above them.
- Captions: f1502 "СВИДЕТЕЛИ [R]КРИЧАТ.", f1529 "КТО-ТО ПАДАЕТ В".
- Witness 4 tilts f1532–1538 and falls f1538–1545.
- Caption f1555 "[R]ОБМОРОК.".

**f1577–1663. Generator.**

- On screen: a spoked wheel with a red rim, two copper coils, and a blue (#4a6cff) glowing progress bar labelled "ЗАРЯД 2→34 %". It rises about 1 % every 2.5 frames and stops at f1655.
- Captions:
  - f1579 "А [R]ГЕНЕРАТОРУ";
  - f1598 "НУЖНО ВРЕМЯ,";
  - f1617 "ЧТОБЫ СНОВА";
  - f1634 "НАБРАТЬ [R]ЗАРЯД.".

**f1664–1757. The wait.**

- WIDE-STAGE plus a neon wall clock. Only the clock hand moves, for 3.1 s.
- Captions:
  - f1666 "ТЫ СИДИШЬ,";
  - f1685 "[R]ПРИВЯЗАННЫЙ К";
  - f1708 "КРЕСЛУ.";
  - f1731 "И [R]ЖДЁШЬ.".

### Act 8 — Second shock (s58–s67)

**f1758–1770. Voltmeter again.**

- The needle goes 0→2000 in 5 frames and pegs.
- Caption f1760 "[R]ВТОРОЙ УДАР!".

**f1771–1828. WIDE-STAGE, electrocution #2.**

- This cut is the biggest brightness jump in the video (luma 17→58).
- Full-width plasma; luma strobes between 56 and 68.
- Smoke appears from f1817.
- Caption f1791 "[R]2000 [R]ВОЛЬТ!".

**f1829–1890. Medium close-up.**

- The body is arched; lightning, plasma on the right, smoke. CSS, body jitter of ±15–30 px, and a slow push.
- Captions: f1831 "ОТ ТВОЕЙ ГОЛОВЫ", f1857 "ПОДНИМАЕТСЯ [R]ДЫМ.".

**f1891–1952. Extreme wide.**

- On screen: a small chair with two pairs of witnesses. A grey smoke cloud grows like a mushroom and fills the top half.
- Captions: f1892 "В КОМНАТЕ ПАХНЕТ", f1920 "ГОРЕЛЫМ [R]МЯСОМ.".

**f1953–2011. Timer again.**

- It counts 00:17→01:12 at +1 per frame (reaching 01:12 at f2007), inside the electric ring.
- Captions: f1954 "ТОК НЕ ОТКЛЮЧАЮТ", f1981 "БОЛЬШЕ [R]МИНУТЫ.".

### Act 9 — Death and ending (s67–s73)

**f2012–2103. Heart and ECG.**

- On screen: a red neon heart over a full-width chaotic ECG trace with a white leading dot. The trace is redrawn every frame and the heart jitters.
- Captions: f2014 "[R]СЕРДЦЕ ДЁРГАЕТСЯ...", f2059 "И" (5 frames only), f2064 "[R]ОСТАНАВЛИВАЕТСЯ.".
- f2070–2103: the flatline grows from the right at about 3 px per frame, and the heart dims.

**f2104–2148. Bloodshot eye.**

- On screen: a big eye. The background glow is halved. CSS at the start.
- The lid closes f2137–2148.
- Captions: f2105 "А ПОТОМ", f2128 "НАСТУПАЕТ".

**f2149–2216. Flatline and fade.**

- f2149: the eye becomes a short red line, which extends to full width at f2150.
- Caption f2149 "[R]ТЕМНОТА.". Voice-over: "[звук монитора]".
- f2196–2210: a linear fade to black.
- f2210–2216: pure black.

## 2. LOOK

**Palette:**

| Role          | Hex                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------- |
| Background    | #010101                                                                                         |
| Floor glow    | #861204 (centre bottom) → #4e0b03 (at 75 % height) → #330601 (corners) → black (at 60 % height) |
| Chair wood    | #46302c                                                                                         |
| Chair slats   | #a3938e                                                                                         |
| Outlines      | #f6efee                                                                                         |
| Red glow      | #cc4d4d → #8e1407 → #560c04                                                                     |
| Caption red   | #F54341                                                                                         |
| Numerals red  | #f33633                                                                                         |
| Plasma        | #ebf2f3 core with #668fd5 / #8a9cff glow                                                        |
| Generator bar | #4a6cff                                                                                         |
| Ad banner     | navy #0b1a4a                                                                                    |
| Eye sclera    | #ece2e1                                                                                         |

**Light.**

- Top-corner grey spotlight cones at about 25 % alpha.
- A red under-glow from the floor, plus red rim glows on every object.
- The plasma acts as a second light source: luma goes from about 45 to 65 and flickers ±7–10 per frame.

**Contrast and finish.**

- Crushed blacks: 23–70 % of pixels below 16.
- Clipping 0.2–6 %.
- No grain (noise std is 0).
- Any "vignette" comes from the composition, not an effect.

**Glow build-up.**

- A 2.5 px line;
- a tight ~3 px red glow;
- a wide 12–20 px deep-red glow.
- Neon type is a red fill with a double bloom.
- Electricity is a white core with a 20–40 px blue bloom.

**Illustration.**

- Flat 2D, front-on, symmetric.
- Uniform rounded line weight.
- Skeleton design: a black silhouette with white bones and an oval skull with teeth.
- Props are built from primitives.
- The only 3D is the fake-perspective floor and the ad render.

## 3. MOTION LANGUAGE

**Camera.**

- Static about 85 % of the time.
- The CSS (0.889→1 in 5 frames) is the signature move.
- Other moves:
  - rare step punch-ins (+27 %, +41 %);
  - one 0.9 s truck with ease-in-out, peaking on the beat word;
  - slow push-ins of about 1.7 % over 2.3 s on close-ups;
  - single-frame 10–37 px jolts on emphasis words.

**Element animation.**

| Element      | Motion                                    |
| ------------ | ----------------------------------------- |
| Hero inserts | scale 0.2→1 in 5 frames, expo-out         |
| Props        | pop on in one frame                       |
| Needles      | 4–5 frames with an overshoot, then jitter |
| Lever        | 25 frames, power3.in, then a spark burst  |
| Helmet       | 22 frames, ease-out                       |
| Stamp        | 4 frames, ease-in, from 2.5×              |
| Counters     | roll fast: +1 per 1–2 frames              |

**Idle motion.**

- Electricity is redrawn every frame (30 fps boil).
- The floor glow breathes.
- Neon flickers.
- Particles, the clock hand, the lung pulse and the wheel spin.

**Tension device.** Long stillness, such as the 3 s wait shot where only the clock moves.

**Rule of thumb.** A new caption or prop event about every 0.9 s.

## 4. EDIT RHYTHM

**Shots.** 31 visual shots:

- mean 2.38 s, median 2.27 s;
- the shortest is 0.2 s (the return from the ad), then 0.37 s and 0.43 s (the voltmeters);
- the longest is 5.27 s (the opening).

**Cuts per 10 s:** 2, 5, 5, 4, 3, 5, 4, 2.

**Transitions.**

- Hard cuts only.
- The exceptions:
  - the spotlight strike flicker;
  - a one-frame CRT dot;
  - the morph into the ad;
  - the 14-frame final fade.

**Brightness alternation.** Chair scenes sit at luma 50–68 and inserts at 17–25. The last 10 s darken steadily, down to luma 1.

**Recurring assets.** The voltmeter, the timer and WIDE-STAGE each come back, and each escalates on the second pass.

**Hook.** It opens on the climax image with crackle SFX, then pulls out to reveal "you" in the chair. The question caption comes in word by word.

**Ending.** A metaphor chain closes the video: heart, then eye, then line, then black. There is no card, no CTA and no top title.

## 5. CAPTION SPEC

**Position.**

- Single line, centred at y = 132 px (12.9 % of height); cap top at 118 px, baseline at 146 px.
- It sits on black: every scene keeps its top 11–15 % black, or uses a 100–160 px gradient.

**Font.**

- Roboto Condensed Bold / Oswald look, ALL CAPS.
- Cap height 29 px = 5 % of width, so about 40 px font size.
- At most about 19 characters per line. The widest caption is 65 % of the frame width.

**Colour.**

- White #F5F5F5 and red #F54341.
- No stroke, no shadow, no glow.

**Animation.** None: hard swaps.

**Words per caption.** 74 captions in total:

- 24 with 1 word;
- 36 with 2 words;
- 14 with 3 words.

**Duration.** Mean 27 frames (0.9 s); minimum 5 frames, maximum 164 frames (frozen during the ad).

**Sync.** 0–7 frames before the word onset, never late.

**Red words.** 30 % of all words. 40 of the 74 captions contain red, and 17 are fully red. Red goes to:

- the sentence-final noun or verb;
- numbers;
- names and places;
- visceral opener words.

In mixed captions, red is on the last word 14 times and the first word 9 times.

**Punctuation.** Kept as spoken.

**Diegetic labels.** These are separate from the captions: small white or red text inside the graphics.

## 6. SOUND CUES (inferred from the picture)

- Crackle under the cold open and every plasma shot.
- Three lamp clunks at f440, 444 and 449.
- A mugshot flash pop at f262.
- A whoosh on the "№1" pop and zaps when the arcs hit it (f393–413).
- Ticks as the straps pop on, a whir as the helmet lowers, drips.
- A lever creak, a clack and spark sizzle at f809.
- A needle whoosh, then a big surge hit at f850 and an even bigger one at f1771.
- Stingers on the jolt frames (f875, 931, 999, 1014).
- In the ad: a music bed, a lock shatter, typing and a UI click.
- Fast clock ticks under both timers.
- A stamp thud at f1411, a breathing whoosh, crowd gasps, a body-fall thud around f1545.
- A rising generator hum while the charge climbs.
- A near-silent clock tick during the wait.
- Erratic heart-monitor beeps, ending in a continuous flatline tone that fades with the picture.

## 7. REPRODUCTION RECIPE (values at 576x1024; multiply by 1.875 for 1080x1920)

### Background

- Body: `#010101`.
- Floor glow: `radial-gradient(ellipse 72% 46% at 50% 102%, #861204 0%, #5a0c03 35%, #2a0501 65%, transparent 100%)`.
- Perspective floor lines: white at 7 % opacity, 1 px.
- Spotlight cones: SVG polygons with a white gradient from 13 % to 3 % alpha, plus a floor pool ellipse (#ff6a5a, 12 % opacity, blurred).
- Keep the top 120 px black. Close-ups get a `linear-gradient(#010101 0 100px, transparent 160px)` overlay.

### Objects

- SVG paths:
  - fill `#2a2a2e` (bodies) or `#46302c` (wood);
  - stroke `#f6efee`, width 2.5, round joins.
- Hot red edge: `filter: drop-shadow(0 0 2px #ff4a4a) drop-shadow(0 0 8px #e0302a) drop-shadow(0 0 18px rgba(142,20,7,.8))`.
- Neon type: colour `#ff3a3a` with `text-shadow: 0 0 4px #ff5a50, 0 0 12px #ff2a2a, 0 0 28px rgba(200,20,10,.7)`.
- Blue neon: stroke `#fff` with `drop-shadow(0 0 3px #9fb6ff) drop-shadow(0 0 12px #5a8cff) drop-shadow(0 0 24px #3a5cff)`.
- Build one skeleton SVG symbol with three poses: upright, arched, slumped.

### Electricity

A canvas redrawn every frame from a PRNG seeded on the frame number (for example `mulberry32(frame * 7919)`; never `Math.random`).

- **Lightning:** recursive midpoint displacement.
  - Displacement 0.35 × segment length, 5–6 subdivisions, branch probability 0.3.
  - Draw a 1.5 px `#fff` line, then a 4 px light-blue pass.
- **Plasma:** 2–4 noisy polylines 12–25 px thick, stroked `#dfe9ff`, with blurred copies composited using `lighter`:
  - 14 px blur, `#668fd5`, alpha 0.9;
  - 30 px blur, `#3a5cff`, alpha 0.5.
- **Brightness flicker:** a screen-blended `#9fb6ff` overlay at 0–8 % opacity per frame.
- **Body convulsion:** ±3–8 px offset and ±4° head rotation per frame.
- **Word jolts:** move the scene 10–35 px for one frame, then snap back.
- **Second shock:** double the plasma and multiply the floor glow by 1.3.
- **Smoke:** grey blurred circles (opacity 0.25, 18 px blur) rising and scaling from 0.6 to 2.2 over 2 s.

### GSAP

```js
// cut-in scale-settle on every scene start (scene wrapper only, never the caption layer)
tl.fromTo(scene, { scale: 0.889 }, { scale: 1, duration: 5 / 30, ease: "power2.out" }, tStart);
// slow push on close-ups
tl.to(scene, { scale: "+=0.017", duration: 2.3, ease: "none" }, tStart + 5 / 30);
// opening: hold the close-up 0.55 s, then pull out
tl.fromTo(scene, { scale: 2.35 }, { scale: 1, duration: 0.75, ease: "power2.inOut" }, 0.55);
// truck across the arm on the strap beat
tl.to(scene, { scale: 1.65, x: -187, duration: 0.9, ease: "power2.inOut" }, tStrap);
// step punch-in on an emphasis word
tl.set(scene, { scale: 1.27 }, tWord);
// hero insert pop
tl.from(el, { scale: 0.2, duration: 5 / 30, ease: "expo.out" }, t);
```

- Props appear with `tl.set(el, {opacity: 1})` (no tween).
- Needle: 4 frames with `back.out(2)`, then seeded ±2° jitter.
- Lever: 25 frames with `power3.in`, then 10 radial white spark lines over 6 frames.
- Stamp: from scale 2.5 and rotation −12° to scale 1 in 4 frames, `power2.in`.
- Counters: tween a number with `snap: 1`.
- Spotlight strike: cone opacity on 2 frames, off 2, on 2, off 3, then on.
- ECG: noisy trace with a clip that shrinks while a flat segment grows at about 3 px per frame.
- Eye close: lid path over 12 frames with `power2.in`, then a line that goes `scaleX 0.3 → 1` in one frame.
- Ending: a linear fade to black over 14 frames.

### Captions

```css
.cap {
  position: absolute;
  top: 118px;
  left: 0;
  right: 0;
  text-align: center;
  font:
    700 40px/1 "Roboto Condensed",
    "Oswald",
    sans-serif;
  letter-spacing: 0.01em;
  text-transform: uppercase;
  color: #f5f5f5;
}
.cap .r {
  color: #f54341;
}
```

- Swap with `tl.set` on the word onset, or 0–5 frames before it.
- Keep the caption layer outside the scaled scene wrapper.

### Ad or CTA slot

1. Freeze the background.
2. Pop a 34 px badge onto a facial feature.
3. Morph it in 5 frames to 560×227 with radius 40 px, centred at y 511, `power3.out`.
4. Reverse it over 8 frames at the end.

## 8. STRENGTHS AND WEAK SPOTS

**Strengths**

- A strict palette: blue only ever means current.
- Every number becomes a glowing infographic, giving the viewer a new object every 2–3 s. The second passes escalate.
- A gore-free second-person avatar keeps it platform-safe while the captions and SFX carry the visceral detail.
- Tight voice-over lock and punchy 1–3 word captions.
- Stillness set against a 30 fps boil makes the shocks hit harder.
- The CSS gives every cut a subtle "landing".
- The ending is a strong metaphor chain that needs no outro.
- The ad is grown out of the character, so viewers are not pulled out of the story.

**Weak spots**

- 3–4.6 s static holds (mugshot, doctor, generator, clock) are long for Shorts. Add micro-motion.
- The caption froze for 5.5 s during the ad.
- The "НЬЮ-ЙОРК" caption duplicates the on-screen label.
- WIDE-STAGE is reused 5 or more times. A couple of new angles would add variety.
- On the close-ups the lightning has no blue bloom, so it reads less well than in the wide shots.
- With no texture at all it can feel "template-y". Optional fix: about 3 % grain.
- For English: keep 1–3 words and at most 19 characters per caption, and use Latin+Cyrillic fonts (Roboto Condensed or Oswald).
