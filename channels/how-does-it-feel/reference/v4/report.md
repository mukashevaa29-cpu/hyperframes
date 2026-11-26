**Note:** I could not create report.md. The environment refused the write ("Subagents should return findings as text"), so the full report is below the summary, ready for you to save to /tmp/claude-0/-home-user-hyperframes/dc37cee6-8f3e-5ef7-b6ea-f227cc435783/scratchpad/ref/v4/report.md. I read all 66 contact sheets in order. Full-resolution sample frames are in /tmp/claude-0/-home-user-hyperframes/dc37cee6-8f3e-5ef7-b6ea-f227cc435783/scratchpad/ref/v4/fr/.

## Summary of the key style findings

- **There are 28 hard cuts, not zero.** The detector missed them because ~70 % of every frame is pure black. Each is a single-frame change at f136, 187, 272, 332, 396, 434, 482, 527, 624, 676, 759, 799, 834, 1028, 1100, 1160, 1205, 1251, 1358, 1398, 1477, 1525, 1597, 1681, 1737, 1791, 1835 and 1889. No dissolves, wipes or fades are used between scenes.
- **Shot length:** 29 shots, mean 2.28 s, median 1.87 s, shortest 1.17 s. Cuts land 0–5 frames before the start of each spoken sentence, so every sentence gets its own pictogram.
- **Look:** neon infographic on true black (#010101). Objects have a #0D0E11 fill, a white core line (#FFE5E7), a red stroke (#FB2945) and a ~25 px red glow. Flames are pink-white, not orange.
  - A red glow rises from the bottom edge: #5B0008 normally, #A10112 in heat scenes. It dims one notch per scene in the last 10 s and is cut to black when the eye closes.
  - The only off-palette element is the navy sponsor card. Everything is flat 2D vector.
- **Camera is locked** in 27 of 29 shots. The exceptions are a 0.55 s ease-out pull-out at f30–46, one jump reframe at f187, and a ±5 px shake on the brain-alarm shot.
- **How things move:** each scene has 1–2 short animations (4–10 frames) that show the sentence, and each one lands on the key word. Lines draw on, objects grow with a small overshoot, counters slow as they land, waveforms die to a flat line, objects switch off by turning grey, sparks burst. Calm scenes are completely still; only the fire scenes flicker every frame.
- **Captions:** Roboto Condensed Bold style, all caps, one line centred at 12.9 % of the height. Cap-height is 4.9 % of the width (about 73 px font at 1080 wide). Text is white #F5F5F5 with one red #FF2B3F accent word, which is the sentence's subject or its final consequence word.
  - 1–3 words per caption, median hold 0.77 s, swapped hard with no animation, 0–5 frames before the voice.
- **Hook:** 1.3 s of the screaming figure in the fire with no caption, then the pull-out and "HOW DOES IT FEEL…ALIVE?". The video then cuts back to the calm "before" state and runs forward in time.
  - On-screen timers act as chapter cards: 00:00–05 (shown at 3x speed), 00:20, 01:00, then a 3-2-1 countdown.
- **Ending:** the eye closes and its lid line becomes a full-width red line. The glow dies, the line and the last caption fade out over 12 frames, and the video ends on black. It does not loop.
- **Sponsor (f889–1022):** the scene freezes on the cliffhanger caption "СТРАННОЕ." ("something strange happens"). An "SN" logo badge pops onto the timer's colon and grows into a full-width rounded card for about 4 s, then shrinks back into the badge. An electronic beep marks the entry.
- **Weak spots:** long completely still holds in the middle, tiny diagram labels you can't read on a phone, the sponsor's navy 3D clashing with the flat red style, and banding in the red gradients.

---

# FULL REPORT (save as report.md)

# v4 — "How does it feel to be burned at the stake" — forensic style breakdown

Source: 576x1024, 30 fps, 1980 frames (66.0 s). I read all 66 contact sheets (s000–s065) in order and pulled full-resolution frames for colour sampling (fr/).

**A correction to the brief.** The automatic detector found no cuts, but there are **28 hard cuts**. Each one is a single-frame change, with diff 8–36 and hist_dist 0.14–0.34. The detector missed them because the frames are ~70 % pure black, so the global histogram barely moves.

No cross-dissolves, fades or wipes are used between scenes. The only soft transitions are inside scenes: the opening pull-out, the sponsor card that grows out of a badge and shrinks back, the blur ramp, and the final fade to black.

Frame numbers are 0-based. A caption frame is the first frame on which the caption is visible. The speech frame comes from transcript.txt.

## 1. Second-by-second shot log

Recurring terms:

- **Neon-line** means a dark fill, a 2–3 px near-white core stroke, a 5–6 px red stroke and a ~25 px red outer glow.
- **Floor glow** is the red radial gradient that rises from the bottom edge.
- **Caption** means the top caption. Captions always swap hard, with no in or out animation.

| s     | frames    | On screen / action                                                                                                                                                                                                                                                                                                                                                                                                       | Camera          | FX                                                                    | Caption (start frame) ↔ speech                                                                 | Out           |
| ----- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------- |
| 0     | 0–29      | **Cold open.** Tight shot: the burning figure fills ~85 % of the height. It is a black mannequin stick figure with a white inner contour, a red neon rim, ribs and spine drawn as white pills, chained at chest and thighs to a black post. Screaming face: red "> <" eyes, an "O" mouth. Spiky pink/salmon/white-hot flames cover the bottom third. The figure flails with a pose change every frame (motion 4–6 px/f). | Static          | Ember dots drifting up, faint smoke puffs, flames flicker every frame | none (screams)                                                                                 | –             |
| 1     | 30–59     | **Pull-out** f30–46, ease-out: scale ~1.22→1.0, pivot near the top (post top stays at y≈25 %). Reveals the log pile, the glowing floor ellipse and a row of white-hot flame tips.                                                                                                                                                                                                                                        | Pull-out 0.55 s | Floor glow at max (#9B0113)                                           | f39 **КАКОВО** ЭТО ↔ f39                                                                       | –             |
| 2     | 60–89     | Wide burning loop                                                                                                                                                                                                                                                                                                                                                                                                        | Static          | Embers                                                                | f68 КОГДА ТЕБЯ ↔ f69; f86 СЖИГАЮТ НА КОСТРЕ                                                    | –             |
| 3     | 90–119    | Same                                                                                                                                                                                                                                                                                                                                                                                                                     | Static          |                                                                       | f114 **ЗАЖИВО?** (all red)                                                                     | –             |
| 4     | 120–149   | Head lolls f128–134. **Cut f136** to a calm frontal figure with no fire, larger, red dot eyes and a flat mouth. The chest chain slides in from the left f136–139; the leg chain f145–150.                                                                                                                                                                                                                                | Static          | Floor glow drops to base #5B0008                                      | f136 ТЕБЯ ПРИКОВЫВАЮТ ↔ f137                                                                   | Hard cut      |
| 5     | 150–179   | Frozen hold                                                                                                                                                                                                                                                                                                                                                                                                              | Static          | –                                                                     | f162 К **СТОЛБУ.**                                                                             | –             |
| 6     | 180–209   | **Jump reframe f187**: the figure scales to ~0.75 and moves up, with the head soft-masked off at the top. From f189 to f205, logs (black rods with white outline and red glow) fly in from both sides every 2–3 f, rotating, and stack criss-cross.                                                                                                                                                                      | 1-frame reframe | –                                                                     | f189 ПОД НОГАМИ ↔ f189; f206 **ХВОРОСТ.**                                                      | Hard reframe  |
| 7     | 210–239   | Logs settle by ~f217; 1-frame jump at f228                                                                                                                                                                                                                                                                                                                                                                               | Static          | –                                                                     | f229 ПАЛАЧ ПОДНОСИТ ↔ f230                                                                     | –             |
| 8     | 240–269   | The torch slides in diagonally from the right f242–251 (ease-out). Flame licks ignite on the logs from f258.                                                                                                                                                                                                                                                                                                             | Static          | Floor glow rises                                                      | f252 **ФАКЕЛ.**                                                                                | –             |
| 9     | 270–299   | **Cut f272** to timer "00:00": huge red condensed digits at y≈51 %, tiny grey "СЕКУНДЫ" under them, 5 dim sine-wave heat lines. It ticks every 10 f (01 f283, 02 f293), so time runs at 3x.                                                                                                                                                                                                                              | Static          | Waves drift                                                           | f274 ПЕРВЫЕ СЕКУНДЫ ↔ f274                                                                     | Hard cut      |
| 10    | 300–329   | 03 f303, 04 f313, 05 f323. The waves brighten and thicken, and the floor glow goes 88→144.                                                                                                                                                                                                                                                                                                                               | Static          | Heat ramp                                                             | f305 ТОЛЬКО **ТЕПЛО.**                                                                         | –             |
| 11    | 330–359   | **Cut f332** to one eye (~50 % of the width, y≈52 %): sclera #EAE6E6, striated red iris, catch-light, tick-stroke lashes, red rim. The pupil darts left and right.                                                                                                                                                                                                                                                       | Static          | –                                                                     | f333 ТЫ ДАЖЕ НЕ ↔ f333; f350 СРАЗУ ПОНИМАЕШЬ,                                                  | Hard cut      |
| 12    | 360–389   | Blink f360–365 (2 f closing, 3 f opening)                                                                                                                                                                                                                                                                                                                                                                                | Static          | –                                                                     | f370 ЧТО **НАЧАЛОСЬ.** ↔ f370                                                                  | –             |
| 13    | 390–419   | **Cut f396** to timer 00:15 (no waves). It counts with ease-out: 16@398, 17@399, 18@401, 19@404, 20@414.                                                                                                                                                                                                                                                                                                                 | Static          | –                                                                     | f398 ЧЕРЕЗ ДВАДЦАТЬ ↔ f399; f418 **СЕКУНД**                                                    | Hard cut      |
| 14    | 420–449   | Hold on 00:20. **Cut f434** to a side-profile neon foot. Four teardrop flames scale up from a dashed line f435–444, staggered.                                                                                                                                                                                                                                                                                           | Static          | Glow ramps                                                            | f434 **ОГОНЬ** ДОБИРАЕТСЯ                                                                      | Hard cut      |
| 15    | 450–479   | The flames flicker                                                                                                                                                                                                                                                                                                                                                                                                       | Static          | –                                                                     | f456 ДО **СТУПНЕЙ.**                                                                           | –             |
| 16    | 480–509   | **Cut f482** to a thermometer plus a number counting 20→600 °C over f482–508 (expo-out). The mercury rises in sync.                                                                                                                                                                                                                                                                                                      | Static          | Glow to its brightest (161)                                           | f483 **ШЕСТЬСОТ** ↔ f487; f500 **ГРАДУСОВ.**                                                   | Hard cut      |
| 17    | 510–539   | Hold 600 °C with bloom. **Cut f527** to a skin cross-section (ЭПИДЕРМИС / ДЕРМА / ЖИР labels). Blisters grow one at a time (~6 f apart).                                                                                                                                                                                                                                                                                 | Static          | –                                                                     | f528 КОЖА ПОКРЫВАЕТСЯ ↔ f529                                                                   | Hard cut      |
| 18    | 540–569   | 4 blisters complete by f548                                                                                                                                                                                                                                                                                                                                                                                              | Static          | –                                                                     | f553 **ПУЗЫРЯМИ,**                                                                             | –             |
| 19    | 570–599   | f575: the blisters burst into ~30 red sparks that rise and fade over 8 f, leaving jagged red crack lines                                                                                                                                                                                                                                                                                                                 | Static          | Particle burst                                                        | f574 ЛОПАЕТСЯ И ↔ f578; f598 **ЧЕРНЕЕТ.**                                                      | –             |
| 20    | 600–629   | **Cut f624** to a spine of 18 vertebra pills. Red glow pulses travel upward.                                                                                                                                                                                                                                                                                                                                             | Static          | –                                                                     | f625 **МОЗГ** ПОЛУЧАЕТ ↔ f629                                                                  | Hard cut      |
| 21    | 630–659   | A pulse launches every ~8 f and climbs the column in ~15 f                                                                                                                                                                                                                                                                                                                                                               | Static          | –                                                                     | f646 СИГНАЛ **БОЛИ** ТАКОЙ                                                                     | –             |
| 22    | 660–689   | **Cut f676** to a top-view brain (wavy gyri, maroon fill) inside 3 perspective glowing rings, with 6 "!" badges orbiting. The group shakes ±3–6 px and the rings pulse every ~20 f.                                                                                                                                                                                                                                      | Shake           | Floor glow alternates 160/107 every 10 f                              | f673 СИЛЫ,; f683 ЧТО ТЫ НЕ (16 f early)                                                        | Hard cut      |
| 23–24 | 690–749   | Same                                                                                                                                                                                                                                                                                                                                                                                                                     | Shake           |                                                                       | f701 МОЖЕШЬ ДУМАТЬ НИ; f727 О ЧЁМ ДРУГОМ.                                                      | –             |
| 25    | 750–779   | **Cut f759** back to the wide burning figure, thrashing                                                                                                                                                                                                                                                                                                                                                                  | Static          | Flames flicker                                                        | f760 ТЫ ПЫТАЕШЬСЯ ↔ f760; f777 **ВЫРВАТЬСЯ.**                                                  | Hard cut      |
| 26    | 780–809   | **Cut f799** to a full-width neon chain at y≈37 % with a padlock. The chain jerks ~6 px f800–803.                                                                                                                                                                                                                                                                                                                        | Static          | –                                                                     | f800 НО **ЦЕПЬ** ДЕРЖИТ. ↔ f802                                                                | Hard cut      |
| 27    | 810–839   | Hold. **Cut f834** to timer 00:59 "МИНУТА". A ring draws clockwise from 12 o'clock f834–843.                                                                                                                                                                                                                                                                                                                             | Static          | Draw-on                                                               | f835 ЧЕРЕЗ МИНУТУ ↔ f837                                                                       | Hard cut      |
| 28    | 840–869   | 01:00 at f845 with a 3-frame bloom flare                                                                                                                                                                                                                                                                                                                                                                                 | Static          | –                                                                     | f854 ПРОИСХОДИТ; f868 **СТРАННОЕ.**                                                            | –             |
| 29    | 870–899   | **Sponsor in.** At f889 a blue round "SN" badge pops onto the timer's colon. From f895 to f899 it stretches into a full-width rounded card (y≈398–625, ~22 % of H).                                                                                                                                                                                                                                                      | Static          | Badge morph                                                           | Caption frozen on СТРАННОЕ. ↔ beep f880–901                                                    | Morph         |
| 30    | 900–929   | Navy 3D space scene inside the card: Earth, satellite, padlock, squirrel mascot in a suit. Wide extended white type appears line by line: ОБХОД / БЕЛЫХ / СПИСКОВ. The red timer ring stays visible above and below the card.                                                                                                                                                                                            | –               | –                                                                     | ↔ "Обход белых списков"                                                                        | –             |
| 31    | 930–959   | Lightning strikes, the lock shatters, the text becomes ОБХОД ГЛУШИЛОК                                                                                                                                                                                                                                                                                                                                                    | –               | –                                                                     | ↔ "обход глушилок"                                                                             | –             |
| 32    | 960–989   | A Telegram search screen types "South", and a "South Networks VPN" result appears                                                                                                                                                                                                                                                                                                                                        | –               | –                                                                     | ↔ "Ищи South в Telegram"                                                                       | –             |
| 33    | 990–1019  | A cursor clicks. From f1014 to f1022 the card shrinks back into the badge.                                                                                                                                                                                                                                                                                                                                               | –               | –                                                                     | still СТРАННОЕ.                                                                                | Reverse morph |
| 34    | 1020–1049 | The badge is gone at f1023. **Cut f1028** to a nerve tree: a pulsing trunk labelled "К МОЗГУ", 6 glowing endings above flames, embers.                                                                                                                                                                                                                                                                                   | Static          | –                                                                     | f1029 **ОГОНЬ** СЖИГАЕТ ↔ f1032                                                                | Hard cut      |
| 35    | 1050–1079 | The endings turn grey one by one f1057–1072. The trunk's pulse breaks into dashes.                                                                                                                                                                                                                                                                                                                                       | Static          | –                                                                     | f1057 **НЕРВНЫЕ**; f1072 ОКОНЧАНИЯ.                                                            | –             |
| 36    | 1080–1109 | **Cut f1100** to a leg icon with 4 flickering red pain dashes                                                                                                                                                                                                                                                                                                                                                            | Static          | –                                                                     | f1101 И НОГИ… ↔ f1102                                                                          | Hard cut      |
| 37    | 1110–1139 | f1123: the dashes vanish and the leg outline turns grey. A red X draws on: stroke 1 f1124–1128, stroke 2 f1129–1131.                                                                                                                                                                                                                                                                                                     | Static          | –                                                                     | f1123 ПЕРЕСТАЮТ **БОЛЕТЬ.**                                                                    | –             |
| 38    | 1140–1169 | **Cut f1160** to an oscilloscope "СИГНАЛ БОЛИ" with a noisy waveform scrolling                                                                                                                                                                                                                                                                                                                                           | Static          | –                                                                     | f1161 ТЫ ИХ ПРОСТО ↔ f1162                                                                     | Hard cut      |
| 39    | 1170–1199 | The waveform decays into a flat line growing from the right                                                                                                                                                                                                                                                                                                                                                              | Static          | –                                                                     | f1179 НЕ **ЧУВСТВУЕШЬ.**                                                                       | –             |
| 40    | 1200–1229 | **Cut f1205** to the burning figure. The flames grow to the chest over f1205–1250.                                                                                                                                                                                                                                                                                                                                       | Static          | Floor glow to its maximum (173)                                       | f1207 **ПЛАМЯ** ПОДНИМАЕТСЯ ↔ f1209                                                            | Hard cut      |
| 41    | 1230–1259 | **Cut f1251** to a single-line head profile with an airway; white air dots flow into the mouth                                                                                                                                                                                                                                                                                                                           | Static          | –                                                                     | f1233 ВЫШЕ.; f1253 ТЫ ДЕЛАЕШЬ **ВДОХ** ↔ f1254                                                 | Hard cut      |
| 42–44 | 1260–1349 | At f1288 the dots become red glowing balls and the airway floods red, on "горячий"                                                                                                                                                                                                                                                                                                                                       | Static          | –                                                                     | f1284 И ГОРЯЧИЙ ВОЗДУХ ↔ f1286; f1312 ОБЖИГАЕТ **ГОРЛО**; f1336 ИЗНУТРИ.                       | –             |
| 45    | 1350–1379 | **Cut f1358** to an airway cross-section with HUD brackets and the label "ДЫХАТЕЛЬНЫЕ ПУТИ". The opening shrinks steadily.                                                                                                                                                                                                                                                                                               | Static          | –                                                                     | f1359 ОНО НАЧИНАЕТ ↔ f1361; f1378 **ОТЕКАТЬ.**                                                 | Hard cut      |
| 46    | 1380–1409 | **Cut f1398** to a bar chart "ВДОХ". Bar 1 grows f1401–1404 with overshoot and settles by f1409.                                                                                                                                                                                                                                                                                                                         | Static          | –                                                                     | f1400 КАЖДЫЙ СЛЕДУЮЩИЙ ↔ f1401                                                                 | Hard cut      |
| 47–48 | 1410–1469 | Bars 2–5 at f1411/1421/1431/1441, each smaller. A trend line draws between the bar tops.                                                                                                                                                                                                                                                                                                                                 | Static          | –                                                                     | f1427 **ВДОХ МЕНЬШЕ**; f1448 ПРЕДЫДУЩЕГО.                                                      | –             |
| 49    | 1470–1499 | **Cut f1477** to neon lungs. Grey smoke fills them bottom-up f1484–1514.                                                                                                                                                                                                                                                                                                                                                 | Static          | –                                                                     | f1478 **ДЫМ** ЗАПОЛНЯЕТ ↔ f1483                                                                | Hard cut      |
| 50    | 1500–1529 | Smoke reaches the top. **Cut f1525** to 6 red blood cells, each with an O₂ badge.                                                                                                                                                                                                                                                                                                                                        | Static          | –                                                                     | f1503 **ЛЁГКИЕ.**; f1527 УГАРНЫЙ ГАЗ ↔ f1529                                                   | Hard cut      |
| 51–52 | 1530–1589 | Grey CO badges knock the O₂ badges off; the cells dim                                                                                                                                                                                                                                                                                                                                                                    | Static          | –                                                                     | f1545 ВЫТЕСНЯЕТ; f1559 **КИСЛОРОД** ИЗ; f1577 КРОВИ.                                           | –             |
| 53–55 | 1590–1679 | **Cut f1597** to a neon heart, a scrolling ECG and a red BPM counter going 90→209 (slowing as it lands). The heart pops to ~1.06 scale on each beat.                                                                                                                                                                                                                                                                     | Static          | –                                                                     | f1598 **СЕРДЦЕ** БЬЁТСЯ ВСЁ ↔ f1602; f1627 **БЫСТРЕЕ,**; f1640 ПЫТАЯСЬ СПАСТИ; f1663 **МОЗГ.** | Hard cut      |
| 56–57 | 1680–1739 | **Cut f1681** to an audio waveform labelled "ЗВУК". The amplitude shrinks, the colour fades to grey-pink and the glow dies (sound going muffled). **Cut f1737** to a fire close-up.                                                                                                                                                                                                                                      | Static          | Desaturate                                                            | f1683 ЗВУКИ ТОЛПЫ ↔ f1686; f1701 СТАНОВЯТСЯ; f1716 **ГЛУХИМИ.**; f1739 СВЕТ ОГНЯ ↔ f1742       | Hard cuts     |
| 58–59 | 1740–1799 | From f1764 a blur ramps 0→~8 px over ~10 f. **Cut f1791** to the bloodshot eye (~60 % of the width).                                                                                                                                                                                                                                                                                                                     | Static          | Blur ramp                                                             | f1764 **РАЗМЫТЫМ.**; f1792 ТЫ ВСЁ ЕЩЁ ↔ f1793                                                  | Hard cut      |
| 60    | 1800–1829 | The upper lid droops slowly from f1818                                                                                                                                                                                                                                                                                                                                                                                   | Static          | Floor glow dims to 69                                                 | f1810 В **СОЗНАНИИ.**                                                                          | –             |
| 61–62 | 1830–1889 | **Cut f1835** to a 3-2-1 countdown. The ring empties counter-clockwise over ~53 f; 2 at f1854, 1 at f1872. **Cut f1889** to the eye, closer.                                                                                                                                                                                                                                                                             | Static          | Floor glow 61→51                                                      | f1836 ЕЩЁ НЕСКОЛЬКО ↔ f1840; f1859 **СЕКУНД.**                                                 | Hard cuts     |
| 63    | 1890–1919 | The eye holds still                                                                                                                                                                                                                                                                                                                                                                                                      | Static          | –                                                                     | f1890 А ПОТОМ ↔ f1891; f1909 НАСТУПАЕТ                                                         | –             |
| 64    | 1920–1949 | The eye closes over 9 f (f1920–1929). At f1930 the lash line becomes a straight full-width red neon line and the floor glow drops to pure black.                                                                                                                                                                                                                                                                         | Static          | –                                                                     | f1924 **ТЕМНОТА.**                                                                             | –             |
| 65    | 1950–1979 | The line holds. Line and caption fade out together f1960–1972. Black to the end, with the final beep.                                                                                                                                                                                                                                                                                                                    | –               | Fade to black                                                         | –                                                                                              | End           |

### Cut and word sync

- **Scene cuts land on sentence starts**, 0–5 frames before the first spoken word.
- **Caption swaps lead the word** by 0–5 frames (median ~2).
- The in-scene "payoff" animation always lands on the key word: blisters pop on "лопается", nerves go grey on "нервные", the X draws on "перестают болеть", the line goes flat on "не чувствуешь", hot air turns red on "горячий", the blur starts on "размытым", the eye closes on "темнота".

## 2. LOOK

**Colours**

| Role                               | Hex                                     |
| ---------------------------------- | --------------------------------------- |
| Background                         | #010101 (60–90 % of pixels below 16)    |
| Floor glow, normal (bottom centre) | #5B0008, edges #330003                  |
| Floor glow, heat scenes            | #A10112–#AD0114                         |
| Caption accent red                 | #FF2B3F                                 |
| Timer digits                       | #FA2335                                 |
| Neon stroke                        | #FB2945                                 |
| Neon core                          | #FFE5E7                                 |
| Glow falloff (outward)             | #910D1C → #470608 → #1E0003 over ~25 px |
| Object fill                        | #0D0E11                                 |
| Caption white                      | #F5F5F5                                 |
| Tiny labels                        | ~#BDBDBD                                |
| Flames                             | #FF4D6D / #FFB0A0 / #FFF4E8 cores       |
| Sclera                             | #EAE6E6                                 |

- **Overall:** average luma 19/255; red saturation 130–160; warm +6, tint +13.
- **Light:** no scene lighting and no shadows. Light comes only from the floor glow and the self-lit neon objects. The edges sit 20–60 levels darker than the centre.
- **The floor glow tells the story:** it brightens with heat (88 → 143–173 at 1/16 scale), dims scene by scene in the last 10 s (69 → 61 → 51 → 46), and drops to 0 when the eye closes.
- **"Dead" state:** when something stops working, its red stroke and glow are removed and only a thin grey line is left.
- **Texture:** none. No grain, chromatic aberration or glitch. There is some compression banding in the gradients.
- **Style:** flat 2D vector pictograms with an even line weight and rounded corners. Each icon is centred and 45–70 % of the frame width.
  - The character is a faceless black mannequin with white anatomy lines. Emotion comes only from the red eyes and the mouth.
  - The only 3D is the sponsor render.

## 3. MOTION LANGUAGE

- **Camera:** locked in 27 of 29 shots. The exceptions are the opening pull-out (f30–46, ~18 % scale, ease-out), one jump reframe (f187) and the brain-alarm shake (±5 px every frame).
- **Animation durations:**
  - Lines drawing on: 4–10 f.
  - Objects growing in with overshoot: ~4 f plus a ~5 f settle.
  - Counters that slow as they land: °C 26 f, BPM ~80 f. The fire timer ticks every 10 f.
  - Slow changes (heat build, smoke fill, airway shrinking, blur, colour fade): linear over 20–40 f.
  - Logs and torch flying in: 6–10 f, staggered 2–3 f.
  - Spark bursts: 8 f.
- **Idle motion:** fire scenes flicker every frame (flames and embers redrawn; the figure changes pose every 1–2 f). Every other scene is completely still, apart from blinks, pupil darts, a slight drift on the blood cells and the heartbeat pop.
- **Frequency:** something changes roughly every 0.5–1 s, counting caption swaps.

## 4. EDIT RHYTHM

- **Shots:** 29 shots, 28 hard cuts. That is ~4.2 cuts per 10 s overall and ~4.9 excluding the sponsor.
- **Shot length:** mean 2.28 s, median 1.87 s, min 1.17 s. The longest is 6.47 s (timer plus sponsor); without the sponsor it is 3.57 s.
- **Anchor shots:** the burning figure returns at 0 s, 25 s and 40 s, then as fire only at 58 s, each time at a later stage. The eye returns at 11 s, 60 s and 63 s.
- **Hook:** 1.3 s of screaming with no caption, then the 0.55 s pull-out reveal and the question caption. At 4.5 s it cuts back to the calm "before" state and the story runs forward from there.
- **Chapter cards:** the timers mark time passing (0–5 s at 3x speed, 20 s, 1 min), then the 3-2-1 countdown.
- **Ending:** no loop, no end card, no call to action. The eye closes, the lid becomes a flat line, the glow dies and a 12 f fade leads to black.
- **Sponsor:** sits inside the frozen timer scene under the cliffhanger caption. The logo badge grows into the card and shrinks back, with a beep at the start; the story then resumes with a hard cut.

## 5. TEXT / CAPTION SYSTEM

- **Font:** Roboto Condensed Bold look, all caps, normal letter spacing. One line, centred horizontally.
- **Position:** cap top y=118, baseline y=146 at 1024 high, so the centre is 12.9 % of the height. Never moves, never wraps.
- **Size:** cap-height 4.9 % of the width, about 39 px font at 576 wide and about 73 px at 1080 wide. Line widths run from 31 % to 66 % of the frame.
- **Colour:** white #F5F5F5 with one red #FF2B3F accent in about half the captions. A one-word caption that ends a sentence is fully red. No stroke, shadow or box.
- **Which word is red:** the sentence's subject (ОГОНЬ, МОЗГ, ДЫМ, СЕРДЦЕ, ПЛАМЯ) or its final consequence word (ЗАЖИВО?, ЧЕРНЕЕТ., ТЕМНОТА.).
- **Chunking:** 1–3 words per caption (mostly 2), keeping the sentence's punctuation.
- **Timing:** 77 captions; median hold 23 f, range 10–42 f. They swap hard, 0–5 f before the word. Only the last caption fades out.
- **Small labels** inside diagrams are 9–12 px grey caps; the BPM readout is red bold ~16 px.

## 6. SOUND CUES (inferred)

- **Fire and story beats:**
  - Screams for the first 1.2 s.
  - A fire crackle and roar bed under every fire scene.
  - Thuds for the logs.
  - A whoosh and ignite for the torch.
  - Clock ticks every 10 f on the timers.
  - A rising tone for the thermometer, with a hit at 600.
  - A pop for the blisters.
  - Electric zaps on the spine pulses.
  - Alarm beeps on the brain-ring pulses, over a low drone.
  - A chain rattle.
- **Sponsor:**
  - Electronic beeps in and out.
  - Typing and a click.
- **Body and ending:**
  - Descending blips as the nerves switch off.
  - Two swishes for the X.
  - A flatline tone.
  - A sizzle on the hot air.
  - Heartbeat and ECG beeps that speed up with the counter.
  - Crowd noise that turns muffled (low-pass) under the shrinking waveform.
  - A final beep, then silence on black.

## 7. REPRODUCTION RECIPE (HyperFrames, 1080x1920)

**Stage**

- Base colours: `#stage{background:#010101}`.
- Two floor-glow layers, cross-faded (12–20 f) when heat starts or builds:
  - Normal: `radial-gradient(ellipse 75% 42% at 50% 104%, #5B0008 0%, #2a0004 55%, transparent)`.
  - Heat: `radial-gradient(ellipse 80% 48% at 50% 104%, #A80114, #3d0006 55%, transparent)`.
- Flicker the heat layer on a 20 f period for the alarm scene.
- In the final 10 s, step the glow opacity down per scene (1 → .8 → .7 → .58 → .5) and set it to 0 when the eye closes.

**Caption**

```css
.cap {
  position: absolute;
  top: 248px;
  width: 100%;
  text-align: center;
  font: 700 73px/1 "Roboto Condensed";
  text-transform: uppercase;
  color: #f5f5f5;
  letter-spacing: 0;
  white-space: nowrap;
}
.cap .acc {
  color: #ff2b3f;
}
```

- Swap captions with `tl.set()` only, starting each one 2 f before the word.
- Chunk into 1–3 words, held 0.6–1.0 s, with one red accent per sentence.

**Neon icon (SVG)**

- Path with `fill:#0D0E11`, `stroke:#FB2945`, `stroke-width:11`, round joins and caps.
- Duplicate path with `stroke:#FFE5E7`, `stroke-width:4`, no fill.
- Group filter: `feGaussianBlur` at 9 and 22 merged with SourceGraphic.
- Anatomy details: white 3–4 px lines with no glow.
- "Dead" state: stroke #555 at 2 px, filter removed, over 6 f.

**Big numbers**

- Roboto Condensed 700, ~230 px, colour #FA2335.
- Glow: `text-shadow:0 0 12px rgba(255,30,60,.9), 0 0 40px rgba(255,0,40,.6)`.
- Counters: tween a proxy value and round it each frame with `expo.out`. Sped-up timers tick every 10 f.
- Landing flare: 3 f of `blur(3px) brightness(1.4)`.
- Grey sub-label: 22–26 px, #BDBDBD.

**Scene grammar**

- One centred pictogram per sentence, hard cut 1–3 f before the sentence starts.
- One explanatory animation per scene, landing on the key word.
- Reuse the character-in-fire and eye shots as anchors, each time at a worse stage.

**GSAP presets**

- **Grow in:** `from {scale:0}`, transform origin at the bottom, 0.14 s, `back.out(2.2)`, stagger 0.07–0.33 s.
- **Line draw-on:** `strokeDashoffset` over 0.15–0.33 s, `power2.out`; rings start at 12 o'clock.
- **Fly-ins:** from x ±700 with ±40° rotation, 0.22 s `power3.out`, stagger 0.08 s.
- **Slow changes:** linear over 0.7–1.3 s.
- **Sparks:** 20–30 dots from a seeded random generator, rising 20–60 px and fading over 0.27 s.
- **Alarm shake:** seeded ±5 px offset every frame.
- **Burning figure flicker:** 4–6 pre-drawn arm/head poses swapped every 2 f in a seeded order. Flame shapes swap every frame, or scale vertically 0.85–1.15 with a seeded phase per flame. Embers rise 1–2 px/f.
- **Opening:** scale 1.22 → 1, origin 50% 22%, 0.55 s `power2.out`, starting at 1.0 s.
- **Ending:** the eyelid morphs shut (0.3 s `power2.in`), becomes a 6 px full-width red line, holds 1 s, then the line and caption fade out over 0.4 s, then 0.25 s of black.
- **Blur beat:** `blur(0 → 16px)` over 0.35 s.

**Sponsor**

- Freeze the scene on a cliffhanger caption.
- Pop a 64 px badge onto the focal object.
- Grow it into a full-width card (radius ~80 px, ~22 % of the height) in 0.2 s `power3.out`.
- Play the ad for at most 4.5 s, reverse the grow, then hard-cut back. Beeps in and out.

**English captions:** for example "HOW DOES IT FEEL" (HOW in red), then "TO BE BURNED", "AT THE STAKE", "ALIVE?" (all red). Use Roboto Condensed Bold or Oswald 600 at the same cap-height.

## 8. Strengths and weak spots

**Strengths**

- **Each sentence is one pictogram that changes on the key word.** That reads with the sound off and gives a small payoff about every 2 s.
- **The black/red/white palette makes the hard cuts feel like one continuous stage.** The floor glow quietly carries the emotional temperature.
- **Climbing numbers build tension:** timers, temperature, heart rate, shrinking bars and the countdown.
- **The video is bookended:** it opens on the climax, then rewinds. It ends on the eye becoming a flat line and true black.
- **The sponsor grows out of the story object and keeps the palette visible.**
- **It is cheap to template.**

**Weak spots**

- Long completely still holds: the chained figure f136–186, the 00:20 hold, the padlock, the X, and the eye f1791–1919.
- The caption is small, with no stroke.
- Diagram labels can't be read on a phone.
- The caption is frozen for 5.4 s during the sponsor, and the navy 3D card clashes with the flat red style.
- The opening figure's pose-swap jitter looks a little cheap.
- Gradient banding; a 1–2 % noise layer would hide it.
- No call to action and no loop.
