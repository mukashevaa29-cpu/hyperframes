# 16_Oby1F0t1kJA: "In this hospital you must NOT answer if at 3:13 you are called by name. 13 rules of the night orderly"

28:36 long (1716 s), 1920x1080 at 30 fps. One of the channel's newest uploads (2026-11-11) and **the most re-engineered edit in the set**.
Sources: all 12 t-sheets, all 37 cuts sheets, full-size frames (shots 0007 and 0017; extracted frames f_70.5, f_276.5, f_1022, f_1085, f_1141, f_1195, f_1440, f_1663, f_1708) and 6 frame-by-frame sequences in `review/` (`flash_3.8`, `seq_9`, `seq_35`, `seq_69`, `seq_rule1`, `seq_728`), plus shots.json, the transcript (4051 words, **142 wpm**) and the YouTube chapters.

**Reading shots.json correctly:** it reports 445 shots and 15.6 cuts/min, but 117 of those "shots" are 0.13–0.33 s long. They are the **blend frames of 4–10-frame cross-dissolves**, not real shots. Re-counting real scene changes (shot-start frames compared with HUD and caption rows masked out; `review/realcuts.py`) gives about **297 real cuts, 10.4/min, median shot 5.1 s** (p10 2.3 s, p90 10.2 s). For comparison, the same method gives 7.0/min and a median of 8.0 s for video 13. So the edit is ≈1.5× faster than 13–15, not 2×. **What really changed is that the camera is almost never still.**

Other summary numbers: pop-ins 44/min (the highest in my set), caption changes 47.6/min, luma median 64.7, dark frames 17.9%, vignette 42.7 (the lowest), integrated loudness −19.9 LUFS.

## 1. Structure

- **Cold open, 0:00–1:09 (69 s), told as a dense pitch.** "You get a job as night orderly… the work is simple… but in your locker lies the previous orderly's notebook." The beats, with the time of each image:
  - hospital exterior at dusk (0:00)
  - a 3-panel job triptych "ОБХОДЫ · КАТАЛКИ / БЕЛЬЁ / ПЛАТЯТ КАЖДОЕ УТРО" (0:04)
  - locker no. 7 with the notebook (0:09)
  - "5 НОЧЕЙ … на шестую пропал" with 6 dots, the 6th red (0:13)
  - the notebook spread with rules 1–12 (truncated), a big red "13" and a red stamp "4 ЭТАЖ" (0:17)
  - the corridor with the numberless door ringed red, "БЕЗ НОМЕРА" (0:21)
  - the nurses' post call panel with "03:13" in a red LED box, "ВЫЗОВ ОТТУДА" (0:28)
  - "6 НОЧЕЙ" over an icon row (lights, lift, a patient, phone receiver) (0:36)
  - the patient list with "НОВАЯ ФАМИЛИЯ — ТВОЯ" in big red (0:46)
  - a torn page "13 = ?" with the red stamp "ВЫРВАНА" and "УЗНАЕШЬ В ШЕСТУЮ НОЧЬ" (0:52)
- **The retention ask is spoken and shown (1:02–1:08):** "it's worth listening to the end / memorise the rules with me / now from the very beginning", as three tags (red / green / white) beside the notebook (shot 0017). Explicit retention copy like this did not appear in 13–15.
- **Chapters = 6 nights plus a rule per chapter entry.** The YouTube chapter list names every rule, not just nights (20 chapters).
- **Chapter card (new design, f_70.5):**
  - **Plaque:** a **cream enamel door-plaque** (#d9d4c6, 4 screws, 2px dark border, scratches) reading "НОЧЬ 1" in black heavy caps (≈8% of frame height).
  - **Below it:** the title in light-grey heavy caps (≈11% of frame height, "ТЕТРАДЬ"), a red underline (≈33% W), and a 6-dot night row (current red #c0283a).
  - **Corner:** a small red LED "03:13" box bottom-right.
  - **Background:** a dim corridor in perspective with a red floor glow (not the streaked stage of 13–15).
  - **Duration:** 2.5–3.5 s.
- **Rule cards (13), redesigned as a notebook page (f_276.5):**
  - **Paper:** cream graph paper (#e6e1d6, 18 px grid at 960p) with a red margin line, coffee rings and stains.
  - **Number:** a **red numeral inside a double hand-drawn red circle** with ink spatter (≈45% of frame height incl. circle).
  - **Text:** "ПРАВИЛО" in near-black heavy caps, and the rule on a **black tag with white text tilted −2°** (the 01-12 style was a yellow tag).
  - **Signature:** "Толик" in blue with a blue ballpoint pen lying diagonally. A 13-dot row sits at y≈90% behind the caption.
  - **Duration:** 3–12 s. The card often builds **extra sub-tags** while the narrator explains (rule 11 adds "ВСЕ — В КРОВАТЯХ" and red "КТО В КОРИДОРЕ — ТОГО ПОЗОВУТ", 23:48–23:57).
  - **Last rule (13, 27:54):** the numeral and circle are **blue** (the hero's own pen), the heading reads "ПОСЛЕДНЕЕ ПРАВИЛО" and the signature is "— Т.".
- **The rule as handwriting first:** before most cards, the narrator "remembers the page". The notebook page cuts in **blank** and the rule **writes itself in blue ballpoint, line by line** (seq_rule1, 4:31–4:34), then a red tag "НЕ БЕГИ" is stamped and the glitch wipe takes us to the card.
- **HUD (redesigned, three elements, f_1085):**
  - **Pill 1 (top-left, ≈20% W):** a dark rect with a clock icon and white caps "НОЧЬ 4 · ПОСТ" / "НОЧЬ 6 · 03:05" / "УТРО · 1 ЭТАЖ". It holds **night plus place or time**, i.e. the time pill merged into the chapter pill.
  - **Pill 2 (≈25% W):** a dark-red rect with a red dot and white caps. It shows **the current subject**, changing every 1–3 min ("ПАЛАТА БЕЗ НОМЕРА", "ПРАВИЛ В ТЕТРАДИ: 12", "ЛЕСТНИЦА", "ТЕЛЕФОН БЕЗ ПРОВОДА", "ЗОВУТ ПО ИМЕНИ"). It acts like a running "case file" label.
  - **Top-right:** 13 numbered circles. Done ones are red with a white number, future ones dark, and the 13th is an empty ring that turns yellow at the end.
- **Mid-roll engagement card (16:06):** a dark frame with the call panel, a closed door and a big red "?", white "КТО НАЖИМАЕТ КНОПКУ ВЫЗОВА?", yellow "И что случилось с Толиком?" and a red tag "ТВОЯ ВЕРСИЯ — В КОММЕНТАРИЯХ", while the narrator asks for comments. New: 13–15 only ask at the end.
- **Ending:**
  - **The 1968 backstory reveal:** a fire, 12 patients locked in by the head nurse Zinaida, old Prokhor who did not open the damper.
  - **The loop:** Tolik returns covered in ash; ward 413's list gains a 14th line "санитар ночной смены" in fresh blue pen ("ТВОЙ ПОЧЕРК", 27:09); a new ad at the bus stop reads "ТРЕБУЕТСЯ санитар в ночную смену".
  - **Recap:** the notebook spread with all 13 rules in blue handwriting and red "СЛЕДУЮЩИЙ САНИТАР — ТЫ?" (28:15).
  - **End card (28:21–28:36):** the same template as 13–15 ("THE LAST RULE", question, yellow "13 ПРАВИЛ НОЧНОГО САНИТАРА", dots, "ПИШИ В КОММЕНТАРИЯХ", red "ПОДПИСАТЬСЯ" pill clicked by the cursor and turning into "ВЫ ПОДПИСАНЫ" plus a yellow bell, slogan).

## 2. Characters

- **The biggest cast in my set**, each with one signature colour:
  - the orderly (you): teal scrubs #3f6f7c, a red-and-white ID badge, dark hair
  - nurse Dasha: red hair, freckles, a white coat, a red watch
  - doctor Gleb: dark curly hair, white coat, stethoscope, often smoking
  - head nurse Nina
  - old Prokhor: a striped sailor vest, white hair
  - Zinaida: a **very tall white cap**, a thin-lipped grey face
  - Tolik: a pale blond ghost, later **ash-grey with a smoke texture**
  - the photo-board staff of 1968 in monochrome sepia
- **Build:** head to body ≈1:3. No outline. 2-tone flat fills with a darker side-plane.
- **Face:** dot eyes with small highlights, thick short brows, a nose bump and a mouth that switches between a line and an **open "o"** (shock) — 2 states, no lip sync.
- **Scale — new:** besides full figures at 25–35% of frame height, 16 uses **medium shots (character to the chest, ≈60% of frame height, f_1022)** and **face close-ups** (the head fills ≈40% of frame height, 9:40, 18:39). That gives a wide / medium / close-up ladder that 13–15 almost never used.
- **Ghost treatment:** desaturated grey-sepia figures at ≈60–70% opacity (Tolik in the corridor, the 1968 staff photo) and **ash-grey textured** Tolik with "кх-кх" cough text.
- **Body-part inserts carry the horror:**
  - a grey hand with a yellow toe-tag
  - a grey naked wrist vs Dasha's real wrist with a red watch ("СМОТРИ НА РУКИ", the double test)
  - a hand with keys on a ring
  - a hand switching the light
  - wet bare footprints
- **Animation:** pose swaps, the arm extends to grab or point, walking frontally toward camera in the corridor (2–3 frame bob). The "o" mouth pops on impact words.

## 3. Backgrounds & locations

- **Locations:**
  - hospital exterior: dark-brick block with lit window grid, ambulance, orange dusk (0:00)
  - locker room: blue-grey lockers, locker 7 lit (0:09, 22:51)
  - **4th-floor corridor:**
    - **Side elevation (about 80 visits):** cream wall #e8e1cf over a green dado #2f5d47, doors 410–415 with frosted windows, a red fire-alarm box, posters "МОЙТЕ РУКИ", "ТИШИНА", "ГРИПП".
    - **One-point perspective (about 40 visits, new):** brown linoleum floor, ceiling lamps, a green "ВЫХОД" sign at the vanishing point and **an arched dark vignette that makes the corridor read as a tunnel** (f_1440, f_1022).
  - nurses' post: a call-panel bar with 18 lamps numbered 401–418, wall clock, rotary phone, desk lamp, duty board, calendar (≈60 visits)
  - stairwell: diagonal railing
  - lift: a brown door with a grille
  - wards: rows of iron beds, sleeping patients, "count the heads" scenes
  - morgue: grey tile, steel tables, white sheets, the ledger
  - archive basement: floor-to-ceiling shelves of folders
  - 1968 boiler room: dark brown with a damper and lamp dots
  - CCTV monitors: grey static, "КАМ 4", REC, timecodes
  - bus stop at dusk (the end)
- **Paper close-ups as their own locations:** the notebook (graph paper), the ward 413 typed list (yellowed paper with an "АРХИВ" stamp), the morgue ledger and the shift log.
- **Perspective:** mostly side view, plus **the one-point corridor**, the frontal hero walking toward camera, and top-down inserts (hands, the call panel).
- **Texture:** fine grain, sparse floating dust, **paper stains and coffee rings** on the notebook, scuffed linoleum. The detail level is the highest of my four (poster text, numbered lamps, ward numbers).

## 4. Light & shadow

- **Night interior:** mostly a warm-dim night interior, not pitch black (dark frames 17.9%). Luma rises in mornings at the post (big windows with pine trees outside).
- **Light sources:** the corridor ceiling lamps (soft radial pools on the floor), the call-panel lamps (**a red lamp lights up with a large soft red bloom ≈8% of the frame**), the desk lamp, a candle in ward 412 (a warm orange pool), the CCTV screens, torch beams.
- **"Lamps go out one by one":** a corridor beat where the frame darkens in 3 steps (cuts rows 45–59). The last stage is a black void with only the hero lit.
- **The red-tint impact — signature effect of this video:** on every hard sound ("ЛЯЗГ" lift, "ХРЯСЬ" door, "БУХ", "ЩЁЛК", "ДЗЫНЬ", heartbeat), the **whole frame flushes rose-red (≈+25% red, −20% green/blue) for 5–10 frames** and fades back. It is usually paired with a 2–4 px shake and a grey onomatopoeia word (seq_728, 12:08). It occurs dozens of times (the cuts sheets show it in about 1 in 6 rows).
- **Darkening for dread:** night scenes run a ≈15% darker grade with a cold-green cast. Scenes with "the double" get a blue-grey wash.
- **Shadows:** soft foot ellipses. Ghosts and the double have none.
- **Vignette:** lower than other videos (42.7), but the perspective corridor adds the arched black ceiling-and-wall vignette.

## 5. Contrast & colour

- **Palette:**
  - **Darks:** warm brown-blacks #282020 / #130d0e / #3c3432 (59%), plus #534a44 / #6d645b.
  - **Light surfaces:** cream #b4ac9f.
  - **Accent:** blood-red #933e35 (the alarm boxes, the red tints). Corridor green #2f5d47 and teal scrubs give the cold counterpoint.
  - **Overall:** a much warmer palette than 13–15 (warm median +13).
- **Accent meanings — extended:**
  - **Red.** "НЕ", danger nouns ("НОМЕРА", "МОРГ", "ТРИНАДЦАТЬ"), stamps ("ВЫРВАНА", "ПРАВИЛО 11 НАРУШЕНО", "УВОЛИЛСЯ", "ПУСТО"), red LED clocks "03:13", rule numerals, the done dots.
  - **Yellow.** Key objects and the notebook's author ("ТЕТРАДИ", "КЛЮЧ", "ТОЛИК", "ЧАСЫ"), the yellow toe-tag.
  - **Green — new role.** **Character names** in captions ("ДАША", "ДЕД ПРОХОР", "ПРОХОРА"), "safe" tags.
  - **Blue.** Handwriting and the hero's own ink: the last rule, the 14th line, "СВЕЖАЯ · СИНЯЯ РУЧКА".
  - **Orange.** Sounds and smells ("ШАРКАНЬЕ", "ЛАМПЫ ГАСНУТ", "ПРАВДА").

## 6. Camera — how the new edit works

- **Rule 1: almost every shot moves.**
  - **Counts:** of the ≈328 shots ≥0.5 s, 183 push in, 32 pull out, 43 shake and 36 pan; only 93 are static. Camera motion is present in 46% of all frames, vs 12–17% in 13–15.
  - **Push-ins:** zoom median **1.062** (deciles 1.03 → 1.17) over a median of **5.5 s**, i.e. ≈1.1%/s. The move is linear-looking and runs for the whole shot, so the cut lands while the camera is still moving. The next shot starts with fresh motion.
- **Rule 2: push + lateral drift.**
  - **Size:** 36 shots add a horizontal drift of 25–30 px at 480p (≈5–6% of frame width) during the push.
  - **Direction:** mostly rightward (27 right vs 9 left), giving a slow diagonal "drift into the scene".
  - **Extremes:** the biggest drifts (≈110–125 px at 480p, ≈25% W) are reveal moves across a wide room: the morgue tables, the archive shelves.
- **Rule 3: scale ladder.** Consecutive shots alternate wide → medium → insert → close-up on the same location (post wide, Dasha medium, her watch insert, the hero's face close-up). A push-in on each makes the edit feel like a moving camera rather than slides.
- **Rule 4: impacts.**
  - **Shake:** 2–4 px at 480p, 0.3–0.6 s, always with the red tint and an onomatopoeia.
  - **Push spikes:** to 1.12–1.23 for big reveals (shot 11, 0:35, "6 НОЧЕЙ", 1.174; the 1968 photo zooms).
- **Pull-outs (32, median 0.954):** used for resets — morning shots, the end of a sequence, "empty corridor".
- **No parallax layers.** The drift moves the flat image as one plane.

## 7. Transitions & cuts

- **Default seam = 4–6-frame cross-dissolve, not a hard cut.**
  - **Evidence:** seq_9 and nearly every cuts-sheet row show one or two blended frames (both images at ~50%) between shots. shots.json logs those blends as 0.13 s micro-shots (117 of them) and labels 23 slightly longer ones (8–10 frames) "animated/dissolve".
  - **Effect:** the dissolve softens the ≈10 cuts/min so the rhythm feels fluid, not choppy.
- **Glitch-bar wipe into and out of every chapter card and rule card (seq_69, seq_rule1):**
  - **Length:** 6–9 frames.
  - **Look:** 3–6 horizontal light-grey bars (≈3–5% of frame height each, 40–80% W) slide across. The incoming card (graph paper or plaque) is revealed in **horizontal strips that slide in from the right**, with a slight RGB-offset ghost.
  - **Exit:** the card leaves by the same strips into the next scene.
  - **Contrast with 13–15:** they used an empty dark stage there.
- **Fade to black:** for "lights out" or "silence", 0.3 s to black and then the next shot builds on black (seq_35: the post scene fades to black, then "6 НОЧЕЙ" builds on an empty dark stage with icons drawing in).
- **Cut timing:** cuts sit on the **last word of a sentence or clause**. The new caption usually appears with the new shot. Many shots last exactly one short sentence (≈5 s at 142 wpm and ≈5.1 words per sentence).
- **Build after cut:** shots open with the set, and 1–3 tags pop in within 0.3–1.5 s (as in 13–15), but there are more of them (44/min).

## 8. Overlays, text & effects

- **Captions:**
  - **Size:** white heavy caps, **cap height ≈5% of frame height** (bigger than ≈4.2% in 13–15), baseline y≈90%, centred, 1–6 words, single line.
  - **Colour:** red ("НЕ", danger), yellow (objects), **green (names)**.
- **Tags:** black-with-white (most), red, green, blue and orange. Tilted 0 to −4°. Height ≈4% of frame height (larger than 13–15). Usually 2–4 on screen, labelling the parts of the frame ("КОЛПАК / ТОНКИЕ ГУБЫ / КЛЮЧИ" around a red-ellipse-circled face, f_1195).
- **Dialogue tags:** small black boxes with white quotes, stacked top-centre, instead of speech bubbles. Each line is added as it is spoken.
- **Big in-scene words:**
  - **Red headline words** at ≈7% of frame height for threats ("ЗАНИМАЮТ", "СТЯНУЛИ ИЗНУТРИ", "САНИТАР!", "ЖДУТ САНИТАРА").
  - **Grey semi-transparent onomatopoeia** ("ЛЯЗГ", "ХРЯСЬ", "ШЛЁП", "ТОП ТОП ТОП").
  - **Orange sensory words** ("ШАРКАНЬЕ").
- **Diegetic UI:**
  - red LED clock boxes (03:13, 02:00, 03:05, 04:52)
  - the call panel with numbered lamps
  - CCTV frames with REC, a camera label and timecode, and **horizontal-noise glitch "ПОМЕХ"**
  - a heart-rate icon "ПУЛЬС 140"
  - an **audio waveform** (red bars on black) for "his voice" vs "another voice"
  - a stopwatch countdown "03:13 / 38 секунд до конца минуты"
  - a mute icon "50 ЛЕТ — И ВПЕРВЫЕ ТИХО"
- **Documents:** the notebook (blue ballpoint handwriting, writes in line by line), the typed lists, the shift log, a firing order with a red "УВОЛИЛСЯ" stamp, six staff photos 2014–2025 each stamped "УВОЛИЛСЯ" ("ВСЕГДА — 6-Я СМЕНА").
- **Marks:** red hand-drawn ellipses (the most used), red X, yellow ellipses, red arrows (a down arrow "ВНИЗ"), red numbered counters ("15" steps, "7" in the list, "6" sheets vs "5" in the book).
- **Particles:** sparse dust, smoke wisps (the fire flashback), cold breath.

## 9. Pacing

- **Event density:** a new visual event every ≈1.35 s (44 pop-ins/min). Combined with ≈10 real cuts/min and continuous camera motion, there is no static moment longer than ≈2 s except on the end card.
- **Sentences:** 792 segments over 28.6 min, so ≈27.7 caption-sentences/min. **Most shots are one sentence long.** That is the core of the new rhythm: one sentence = one shot = one push-in, with 1–3 tags inside it.
- **Night structure:** chapter plaque (3 s) → setup at the post → the notebook writes the rule (2–3 s) → glitch wipe → rule card (3–12 s) → incident with a red-tint scare → morning debrief → lore drop (archive, photos) → next night. Nights shrink from ≈6 min (night 1) to ≈3 min (nights 4–5), then the finale is long (night 6, 23:45–28:20).
- **Breather:** the mid-roll comment card at 16:06 sits at ≈56% of runtime, a natural retention valley.

## 10. Top 10 reusable techniques

1. **One sentence = one shot = one push-in.** Cut on the sentence's last word with a 4–6-frame cross-dissolve, and start every shot with a 3–8% linear push (≈1%/s), adding a 5% lateral drift on about 1 in 9 shots. A still flat illustration then reads as live camera work.
2. **The scale ladder:** wide → medium → insert (hands, watch, tag, panel lamp) → face close-up on the same set, each with its own push-in.
3. **The red-tint impact:** 5–10 frames of rose-red flush plus a 2–4 px shake plus a grey onomatopoeia word on every hard sound.
4. **The glitch-bar strip wipe** (6–9 frames) as the reserved transition into and out of cards, so cards feel like a different "layer".
5. **The rule card as the found object itself:** a graph-paper page with a hand-drawn circled numeral, a black tilted tag, the author's signature and pen; the last rule in the hero's blue ink. The rule is written in blue line by line before the card appears.
6. **The three-part HUD:** night + place/time pill, red "current subject" pill and the rule-dot row. The subject pill is a cheap way to re-orient viewers every 1–3 min.
7. **Spoken retention contract in the cold open** ("listen to the end, memorise the rules with me") and **a mid-roll comment question card** at ≈55% of runtime.
8. **Colour-coded caption words** including **green for character names**, which helps with a large cast.
9. **The diegetic evidence kit:** CCTV frames with timecode and noise glitch, an audio waveform for "voices", LED clocks, a call panel with lamps that bloom, a stamped photo grid.
10. **The one-point perspective corridor with an arched black vignette:** the hero walks toward camera, and lamps die one by one in 3 steps to black.

**Craft mistakes not to copy:**

- With motion on almost every shot, impacts lose contrast. Only the red tint separates a scare from routine drift.
- The 4-frame dissolves on dialogue reverse shots produce visible double-exposure frames with two sets of tags overlapping (rows 0207, 0371).
- The HUD is now 3 elements plus up to 4 tags plus a caption. Top-left pills overlap scene tags in several shots ("ДАЛЬШЕ НЕЛЬЗЯ" stamp under the pill at 24:21, the call-panel lamps hidden by the dot row at 27:33, f_1663).
- Rule-card dots at y≈90% sit directly behind the caption, so the caption covers dots 3–11 on every card (f_276.5).
- The grey onomatopoeia at ≈40% opacity on mid-grey walls is barely legible.
- Tolik's ghost and the 1968 photo use the same desaturated treatment as ordinary "memory" shots, so flashback vs apparition is ambiguous.
- The 28.6-min runtime with 6 nights produces 4 near-identical "morning at the post" debriefs.
