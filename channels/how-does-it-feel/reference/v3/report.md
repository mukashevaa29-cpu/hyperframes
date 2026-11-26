I could not write report.md. The harness refused the Write ("Subagents should return findings as text"), so I did not work around it. The full report is below the summary; save it as report.md in the v3 directory if you want it on disk. My scratch notes (notes_a.txt, notes_b.txt), the full-res frames (fr/) and montage1.jpg / montage2.jpg are in /tmp/claude-0/-home-user-hyperframes/dc37cee6-8f3e-5ef7-b6ea-f227cc435783/scratchpad/ref/v3/. I read all 70 sheets, frames 0–2087.

## Summary (most important findings)

**Look**

- Flat 2D neon diagrams on true black (#010101).
- One light source: a red glow rising from the bottom centre (#861207 normally, #AE1703 in the fire / 400 °C beats). Everything above roughly 55 % of frame height stays black.
- Line art has three layers: a blurred red halo (stroke ≈12 px at 1080 W, 25 px falloff), then a solid fill that blocks the glow inside the shape, then a 5 px white core line. So glow only shows outside each shape.
- Characters are x-ray skeletons. Inside the bull they are drawn as red-tinted see-through bones.
- Heat is told through colour: the bull's fill goes from #0C0A0C to #450B09 to #871712, and the floor glow follows the temperature.
- Only red, black and white. No grain, no shake, nothing 3D except the ad.

**Camera and edit**

- The camera is locked off for 66 of 70 s. The only real move is the cold-open pull-out (f14–36, ease-out).
- There are 26 shot changes, all hard cuts or "punch" cuts (same artwork rescaled ×0.8–×2.3), each followed by a 3–4 frame scale settle. There are no dissolves, flashes or glitches.
- Median shot is 2.0 s (mean 2.6 s), about 4–5 cuts per 10 s.
- Each cut lands about 2 frames before the first word of a new phrase, and the audio has a whoosh or sub-hit on each one.
- In-shot actions are short: 4–15 frames.
- Infographic beats: a timer running +2 s per frame, a thermometer climbing 30→400 °C with expo ease-out, and waveforms drawn on with a bright dot at the leading edge.

**Captions**

- One line, centred at 12.9 % of frame height. Roboto Condensed Bold-style caps, cap height ≈2.8 % of height (about 75 px font at 1080×1920).
- White #F4F4F4 and red #F44241. Flat text: no box, stroke, shadow or animation, just hard swaps.
- 72 captions, 1.85 words each on average, 0.88 s each, never more than 17 characters. Once speech starts the band is never empty.
- Colour rule: the last chunk of each sentence carries red (31 of 33). A one-word sentence ending is fully red, otherwise only the payoff word. Key nouns are also red (БЫК, ТРУБКУ, КРИК, the opening КАКОВО).
- On-art labels are tiny grey small caps.

**Hook and ending**

- The video opens on the climax image (the screaming bull head with sound arcs) under a loud drone, with no text for 1.6 s. The first caption is the "you" question.
- At the end the eye closes over 12 frames into a full-width red flatline, with a 1 kHz flatline beep from f2031. It fades to black over 12 frames. No end card, CTA or loop.

**Sponsor (33–37.5 s, right after the first peak)**

- A small "SN" app badge pops onto the skeleton's chest, then stretches in 6 frames into a rounded pill-shaped video window (100 % W × 22 % H) sitting inside the scene.
- The caption freezes on the last story caption and the music bed drops out.
- It shrinks back to the badge in 5 frames, then punch-cuts into the next beat.
- The ad's navy-blue 3D palette clashes with the red world.

**Weak spots:** long holds with nothing moving (title card, thermometer), the same wide bull shot reused about 7 times, stiff stepped-pose character animation, no caption motion, and no loop at the end.

---

# FULL REPORT (intended content of report.md)

## Reference v3: "How does it feel to be locked inside the Brazen Bull?" (forensic style breakdown)

- **Source:** ../v3.mp4, 576x1024, 30 fps, 2088 frames (69.6 s).
- **Method:** I read all 70 contact sheets (every frame). For key frames I pulled full-res copies to measure colours and geometry, and computed metrics, flow and audio envelope/FFT in python.
- **Notation:** frames are 0-based. "VO" means the Russian voice-over, with frame numbers from transcript.txt. In captions, words written as [R]WORD are red.

**What it is:** a flat 2D neon-diagram explainer.

- Black space, glowing pink-red outlines with white core lines, x-ray skeleton characters.
- A single red "furnace" glow from the bottom.
- Big infographic data beats: timer, thermometer, waveform.
- One-line captions of 1–3 bold condensed caps near the top, with the last word of each sentence in red.
- The camera is locked off about 90 % of the time. Beats change with hard cuts or cut-plus-scale-pop, landing about 2 frames before the spoken phrase.

### 1. Second-by-second shot log

**Legend:**

- **CUT** = hard cut.
- **PUNCH** = hard cut to a tighter or looser crop of the same artwork, followed by a 3–4 frame scale settle (zoom-flow spikes +3…+7).
- **Cap f:** = the frame where that caption appears.

| Second         | What happens                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0 (f0–29)      | **Cold open in medias res.** Extreme close-up of the bull's head in profile (about 2.5x frame width): dark-red fill, thick pink-red neon outline, black horn, a dashed tube chain along the neck to the mouth. Three huge concentric red sound-wave arcs ")))" come out of the mouth and pulse on about a 4–6 f cycle. From f14 a fast pull-out and slide left (peak 20 px/f at f19–22, ease-out) reveals the fire, slab and lying skeleton by f24–29. No text. Audio: loud drone/roar (-11 dBFS, 290 Hz + 31 Hz sub). |
| 1 (30–59)      | The move settles by about f36 into the hero wide shot: the whole bull at about 85 % width, body at y 35–55 %, a belly cut-away ellipse with an x-ray skeleton lying head-left, flames under the belly on a black slab, and the bottom-centre red glow. Arcs at the mouth are small and pulsing; embers rise and smoke wisps drift above the back. **Cap f50:** "[R]КАКОВО ЭТО", on the same frame as the VO "Каково это".                                                                                              |
| 2 (60–89)      | Hold. Fire flickers on a 2–3 f stepped cycle, skeleton limbs twitch on 3–6 f holds. **Cap 78:** "КОГДА ТЕБЯ".                                                                                                                                                                                                                                                                                                                                                                                                          |
| 3 (90–119)     | Hold. **Cap 100:** "ЗАПИРАЮТ ВНУТРИ".                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 4 (120–149)    | Hold. **Cap 130:** "[R]МЕДНОГО БЫКА?" (all red).                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 5 (150–179)    | **CUT at 165**, 4 f before VO "Сицилия" (f169), with a high-frequency whoosh. Title card on black with the bottom glow: "VI ВЕК" huge neon red (cap ≈80 px = 7.8 % of height, condensed black weight, glow); "ДО Н.Э." smaller red; a glowing red underline bar (≈330×6 px at 66 % height). Scale pop 0.85→1 over 3–4 f. **Cap 166:** "[R]СИЦИЛИЯ."                                                                                                                                                                    |
| 6 (180–209)    | At 181–185 a white "СИЦИЛИЯ" sub-label (≈22 px) scales up from 40 % to 100 % (ease-out-back) between "ДО Н.Э." and the bar. **Cap 198:** "ШЕСТОЙ ВЕК ДО".                                                                                                                                                                                                                                                                                                                                                              |
| 7 (210–239)    | Static hold, only the glow. **Cap 221:** "НАШЕЙ ЭРЫ." (white, an exception to the colour rule).                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 8 (240–269)    | **CUT at 248** (VO f249) to the specimen shot: a black bull silhouette (fill #0C0A0C, 3 px white outline, red outer glow) with a small flank door, faint plank lines and a dark slab. A standing skeleton on the left gives scale (black body, white bones, glowing red head and eyes). Settle 0.95→1 over 248–251. **Cap 249:** "ПЕРЕД ТОБОЙ [R]БЫК".                                                                                                                                                                 |
| 9 (270–299)    | Hold. **Cap 278:** "В НАТУРАЛЬНУЮ".                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 10 (300–329)   | **Cap 302:** "ВЕЛИЧИНУ." At 328 the door is replaced by a thin dashed grey ellipse (the hollow cavity) and a small white "ПОЛЫЙ" label pops above the back. **Cap 328:** "[R]ПОЛЫЙ." (VO f329).                                                                                                                                                                                                                                                                                                                        |
| 11 (330–359)   | At 347 the label swaps to "БРОНЗА" (salmon #F5A07A). **Cap 348:** "ИЗ [R]БРОНЗЫ." From 349 to 373 a glowing red line tilted about 10° with a white core sweeps left to right across the bull at about 12 px/f (a metal-shine sweep).                                                                                                                                                                                                                                                                                   |
| 12 (360–389)   | The sweep exits around f373. **PUNCH-IN at 374** (×2.3, settle flow +3.8) to the flank: the body fills the frame, door centred, red glow between the legs. **Cap 375:** "В БОКУ ОТКРЫВАЮТ" (VO f377). At 386–393 the door swings open as a 2D squash toward its left hinge.                                                                                                                                                                                                                                            |
| 13 (390–419)   | Door open: a thin slab with 2 hinge dots and a black hole. **Cap 407:** "[R]ДВЕРЦУ."                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 14 (420–449)   | **PUNCH-OUT at 429** (×0.8), showing the rear and tail. **Cap 431:** "ТЕБЯ ЗАТАЛКИВАЮТ" (VO f430). From 432 a skeleton is shoved in from the left edge at about 3 px/f.                                                                                                                                                                                                                                                                                                                                                |
| 15 (450–479)   | The skeleton passes into the body and becomes a red x-ray, lying flat. **Cap 456:** "[R]ВНУТРЬ." At 460 the grey cavity ellipse fades in. **PUNCH-IN at 477** on the belly. **Cap 479:** "ДВЕРЦА" (VO f481).                                                                                                                                                                                                                                                                                                           |
| 16 (480–509)   | The door closes over 480–485 (5 f). **Cap 493:** "[R]ЗАКРЫВАЕТСЯ." From 495 the skeleton rotates upright over about 15 f.                                                                                                                                                                                                                                                                                                                                                                                              |
| 17 (510–539)   | The skeleton stands pressed in. **CUT at 525** to a slightly wider, darker grade (luma 30→18, floor glow drops) with the skeleton curled at the bottom-left. **Cap 526:** "[R]ТЕМНО." (VO f527).                                                                                                                                                                                                                                                                                                                       |
| 18 (540–569)   | **Cap 551:** "[R]ТЕСНО." At 552–557 the cavity ellipse brightens and gains a second concentric inner ellipse (walls closing in).                                                                                                                                                                                                                                                                                                                                                                                       |
| 19 (570–599)   | **Cap 575:** "ПАХНЕТ [R]МЕТАЛЛОМ." From 576 grey wavy "~~" smell squiggles drift at the top of the cavity.                                                                                                                                                                                                                                                                                                                                                                                                             |
| 20 (600–629)   | **CUT at 606** to the wide black bull with a seated x-ray skeleton; glow back to normal; settle over 606–611. **Cap 608:** "А ПОТОМ". **Cap 629:** "ПОД БРЮХОМ [R]БЫКА". From 629 the fire ignites: coals grow to full flames in about 12 f, and the floor glow ramps up (luma 19→30 over 625–655).                                                                                                                                                                                                                    |
| 21 (630–659)   | Full fire, embers rise into the belly, dark smoke above. **Cap 659:** "РАЗЖИГАЮТ [R]ОГОНЬ."                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 22 (660–689)   | Hold.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 23 (690–719)   | **CUT at 696** (VO f697) to the timer: neon red digits "00:00" (condensed, ≈95 px, glow), a grey "МИНУТЫ" label, and a red progress ring drawing clockwise from 12 o'clock. The count runs +2 s per frame. **Cap 698:** "ПЕРВЫЕ МИНУТЫ".                                                                                                                                                                                                                                                                               |
| 24 (720–749)   | The ring reaches about 80 %. **Cap 727:** "ПРОСТО [R]ТЕПЛО."                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 25 (750–779)   | The timer reaches 01:57 with the ring almost closed. **CUT at 755** (VO f756) to a close-up of the belly and fire: the bull is now dark brown-red, the skeleton seated, flames big; settle over 755–759. **Cap 757:** "ТЫ ЕЩЁ НЕ". **Cap 773:** "ПОНИМАЕШЬ,".                                                                                                                                                                                                                                                          |
| 26 (780–809)   | Hold, embers drifting. **Cap 786:** "ЧТО [R]ПРОИСХОДИТ."                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 27 (810–839)   | **CUT at 815** (VO f819) to the wide bull at about 60 % width with a settle. The body fill heats from #180A0B to #450B09. **Cap 816:** "НО БРОНЗА БЫСТРО".                                                                                                                                                                                                                                                                                                                                                             |
| 28 (840–869)   | Heating continues, the outline glow thickens. **Cap 847:** "[R]НАГРЕВАЕТСЯ."                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 29 (870–899)   | **CUT at 876** (VO f878) to the thermometer: a neon tube with rising mercury. Digits count 30→395 °C with expo ease-out (+35 per frame at first, +2 per frame later). Grey "СТЕНКИ" label. The floor glow tracks the temperature (luma 18→29). **Cap 877:** "ЧЕРЕЗ НЕСКОЛЬКО".                                                                                                                                                                                                                                         |
| 30 (900–929)   | Settles at 400 °C by f906 and holds. **Cap 901:** "МИНУТ СТЕНКИ". **Cap 921:** "[R]РАСКАЛЯЮТСЯ."                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 31 (930–959)   | **PUNCH cut at 948** (zoom flow +5.5) to the red-hot interior: fill #871712, pink outlines, skeleton on a chair, huge fire. **Cap 949:** "К НИМ НЕВОЗМОЖНО". From 955 the skeleton reaches out; at 959 a white sizzle burst of 8 radiating strokes appears at the wall.                                                                                                                                                                                                                                                |
| 32 (960–989)   | The burst flickers and rotates over 960–973 and the arm recoils. **Cap 974:** "[R]ПРИКОСНУТЬСЯ."                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 33 (990–1019)  | **Sponsor in.** At 997–1001 a small blue rounded "SN" badge pops onto the skeleton's chest. At 1002–1007 it stretches into a fully rounded pill-shaped video window (≈100 % W × 22 % H, centred at about 50 % height) inside the scene; the bull and fire stay visible around it. The ad is a navy 3D render: chrome padlock "ДОСТУП ОГРАНИЧЕН", a squirrel in a suit on a satellite, heavy extended white sans. "ОБХОД" types in. The caption "ПРИКОСНУТЬСЯ." stays frozen; ad VO starts at f1010.                    |
| 34 (1020–1049) | "ОБХОД / БЕЛЫХ / СПИСКОВ" appears word by word; the padlock cracks with lightning and shatters.                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 35 (1050–1079) | "ОБХОД ГЛУШИЛОК", blue sparkles, a ring shockwave from a dish at 1068–73, then a cross-fade to "Ищи в Telegram".                                                                                                                                                                                                                                                                                                                                                                                                       |
| 36 (1080–1109) | Telegram search types "@south" one letter per frame (1084–91); a "South Networks VPN" row with an OPEN button pops (1095–97); a cursor taps (1103–08).                                                                                                                                                                                                                                                                                                                                                                 |
| 37 (1110–1139) | The ad holds to 1121. At 1122–1126 the pill shrinks (ease-in, 5 f) back to the badge, which fades at 1130–31. The skeleton falls off the chair into a lying pose. **PUNCH at 1137** (16 px flow at the cut). **Cap 1139:** "А СТОЯТЬ БОЛЬШЕ" (VO f1140).                                                                                                                                                                                                                                                               |
| 38 (1140–1169) | The skeleton writhes, legs kicking on 3–4 f holds, with embers. **Cap 1163:** "[R]НЕГДЕ."                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 39 (1170–1199) | **PUNCH at 1182.** Horizontal red sine "heat" lines fill the cavity and undulate; the skeleton folds up. **Cap 1184:** "ВОЗДУХ ВНУТРИ" (VO f1188).                                                                                                                                                                                                                                                                                                                                                                     |
| 40 (1200–1229) | **Cap 1206:** "СТАНОВИТСЯ". **Cap 1221:** "ГОРЯЧИМ,".                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 41 (1230–1259) | **Cap 1234:** "КАК В [R]ПЕЧИ."                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 42 (1260–1289) | About 1 s of silent hold. **CUT at 1284** (VO f1287) to the lungs: a neon outline with white core and red glow, dark fill #1E0E12, blurry red smoke dots rising from the trachea, grey "ЛЁГКИЕ" label. **Cap 1285:** "КАЖДЫЙ ВДОХ".                                                                                                                                                                                                                                                                                    |
| 43 (1290–1319) | The lung fill reddens (luma 19→29 over 66 f). **Cap 1309:** "ОБЖИГАЕТ [R]ЛЁГКИЕ."                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 44 (1320–1349) | The colour ramp continues.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 45 (1350–1379) | **CUT at 1350** (VO f1351) to the wide red-hot bull with the skeleton lying head-right, inching toward the head. **Cap 1351:** "ТЫ НАХОДИШЬ". **Cap 1368:** "ЕДИНСТВЕННОЕ".                                                                                                                                                                                                                                                                                                                                            |
| 46 (1380–1409) | **Cap 1384:** "МЕСТО,". **Cap 1394:** "ГДЕ МОЖНО [R]ДЫШАТЬ".                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 47 (1410–1439) | At 1424–1427 a tube (a chain of white-outlined segments) draws on from the cavity to the mouth in about 4 f. **Cap 1425:** "[R]ТРУБКУ В ГОЛОВЕ".                                                                                                                                                                                                                                                                                                                                                                       |
| 48 (1440–1469) | **Cap 1450:** "[R]БЫКА." **PUNCH-IN at 1468** (about 2x, flow +5.7): thin tube with a round mouthpiece.                                                                                                                                                                                                                                                                                                                                                                                                                |
| 49 (1470–1499) | **Cap 1470:** "ПРИЖИМАЕШЬСЯ К". Over 1476–88 the skeleton slides its face to the mouthpiece. **Cap 1491:** "НЕЙ [R]ЛИЦОМ."                                                                                                                                                                                                                                                                                                                                                                                             |
| 50 (1500–1529) | **PUNCH-OUT at 1516** (flow -15, then a +7/+5 settle) to a mid shot with a thick chain tube to the head. The skeleton thrashes (local motion 5–7 px/f; the camera is static). **Cap 1518:** "И [R]КРИЧИШЬ!" Big high-frequency audio spike.                                                                                                                                                                                                                                                                            |
| 51 (1530–1559) | Red sound arcs pulse from the mouth over 1538–49. **CUT at 1550** (VO f1553) to the bull's head and front from a low 3/4 view, with embers. **Cap 1552:** "НО СНАРУЖИ СЛЫШАТ".                                                                                                                                                                                                                                                                                                                                         |
| 52 (1560–1589) | **Cap 1578:** "НЕ [R]КРИК."                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 53 (1590–1619) | **CUT at 1602** (VO f1604) to a converter diagram: a noisy jagged red waveform labelled "КРИК" (white) feeds a white-outlined coiled tube with red pulses inside, which outputs a clean sine labelled "РЁВ" (dim). Grey "ТРУБКИ" label. The noise jitters every frame. **Cap 1603:** "ТРУБКИ УСТРОЕНЫ".                                                                                                                                                                                                                |
| 54 (1620–1649) | Pulses travel along the tube. **Cap 1628:** "ТАК,". **Cap 1643:** "ЧТО ТВОЙ ГОЛОС".                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 55 (1650–1679) | **Cap 1669:** "[R]ПРЕВРАЩАЕТСЯ..." (all red).                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 56 (1680–1709) | **Cap 1708:** "В [R]РЁВ БЫКА." At 1709 the "РЁВ" label turns bright red, larger and glowing.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 57 (1710–1739) | The output sine grows in amplitude over about 6 f (ease-out) into tall glowing red waves.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 58 (1740–1769) | **CUT at 1746** (VO f1750) to the king scene: a skeleton king with a yellow crown and red eyes, laughing (mouth open, bobbing), on a tall throne with an orange-gold neon outline, two guest skeletons beside him. Salmon/red "ХА" texts in varied sizes and opacities pop and fade. **Cap 1748:** "ЦАРЬ И ГОСТИ".                                                                                                                                                                                                     |
| 59 (1770–1799) | **Cap 1772:** "[R]СМЕЮТСЯ." **CUT at 1796** (VO f1800) to the wide bull with red glowing musical notes rising from its mouth like smoke. **Cap 1797:** "ДЛЯ НИХ ЭТО".                                                                                                                                                                                                                                                                                                                                                  |
| 60 (1800–1829) | The notes drift up and wiggle. **Cap 1817:** "[R]МУЗЫКА."                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 61 (1830–1859) | **CUT at 1838** (VO f1840) to an oscilloscope: faint vertical grid, tiny grey "ГОЛОС" label top-left, a tall red neon waveform written left to right with a bright dot at the leading edge. **Cap 1839:** "ТВОЙ ГОЛОС". **Cap 1859:** "[R]СРЫВАЕТСЯ."                                                                                                                                                                                                                                                                  |
| 62 (1860–1889) | The amplitude breaks up and around f1885 collapses into a low noisy flat band (hoarse voice). **Cap 1887:** "[R]КРИК СТАНОВИТСЯ".                                                                                                                                                                                                                                                                                                                                                                                      |
| 63 (1890–1919) | The band jitters. **Cap 1913:** "[R]ХРИПОМ."                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 64 (1920–1949) | **CUT at 1935** (VO f1940) to the wide bull. The arcs at the mouth fade over about 1 s and dark smoke rises. **Cap 1937:** "[R]БЫК ЗАМОЛКАЕТ."                                                                                                                                                                                                                                                                                                                                                                         |
| 65 (1950–1979) | Hold with a slow global dim (luma 28→23).                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 66 (1980–2009) | **CUT at 1986** (VO f1988) to a huge eye at about 52 % height: pink-white sclera, red iris with radial striations, dark-red pupil, white highlight dot, red bloodshot veins, white tick-mark lashes, thick red neon rim. **Cap 1987:** "А ПОТОМ". **Cap 2008:** "НАСТУПАЕТ".                                                                                                                                                                                                                                           |
| 67 (2010–2039) | The lid closes over 2017–2028 (12 f, accelerating) into a curved line, then at 2029 snaps to a straight red neon line spanning the full width (an ECG flatline). **Cap 2025:** "[R]ТЕМНОТА." A 1 kHz beep starts at f2031.                                                                                                                                                                                                                                                                                             |
| 68 (2040–2069) | The flatline holds on near-black (luma 4.5).                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 69 (2070–2087) | The line and caption fade to black over 2070–2081 (linear), then stay black. No end card, CTA or logo.                                                                                                                                                                                                                                                                                                                                                                                                                 |

**About the cut detector:** it only flagged frames 755, 815 and 1284 (2067 and 2069 are the end fade). There are actually 26 changes, all cuts or punch cuts. The same palette across shots keeps the histogram distance low, which is why the detector missed them. No dissolves, whips, flashes or glitches are used, apart from the sponsor morph and the final fade.

### 2. Look

**Palette (measured):**

- Base: #010101. The top 50 % of every frame is pure black; 33–98 % of pixels are crushed below 16.
- Floor glow (normal): bottom-centre #861207 → #650D02 at 88 % height → #470A01 at 76 % → #280401 at 60 % → black above about 55 %.
- Floor glow in hot beats: #AE1703. In the ending: #3F0800.
- Caption red: #F44241. Caption white: #F4F4F4.
- Neon red core (title, timer, eye rim): #FA3936, hot spots #FF4D50.
- Glow falloff outside a shape, over about 25 px at 576 W: #E42D31 → #AE2321 → #701B1A → #510F0F → #340A0B → #1B0405.
- White line core: #F2F2EE, 2.5–3 px at 576 W.
- Bull fill as it heats: #0C0A0C → #180A0B → #450B09 → #871712. Cavity: #2B0704 to #340704.
- Fire: white core #FBFDFA, petals around #FF6A3D/#FF4B2E, dark-red edges.
- Labels: grey (≈#BDB5B5 at about 65 % opacity).
- Rare accents: crown yellow, throne gold #C99A5A, salmon #F5A07A.
- Sponsor (foreign to the palette): navy #0E1E4A–#1B3A8C, chrome, Telegram blue.

**Other properties:**

- Saturation is high but the hue is almost entirely red (sat 130–170/255, a\* up to +31). It is effectively monochrome red on black.
- Lighting: one implied red floor light at the bottom centre, matching the in-world fire. No top light.
- Contrast is extreme: p1 = 0, white cores at 240–255, clipping only 0.5–2.3 %, mean luma 17–50.
- The vignette (-15…-60) comes from the composition, not a separate layer.
- No shadows (everything is emissive), no grain, clean vector edges.
- Glow construction: blurred red stroke behind, solid fill on top (blocks the inner glow), thin white core stroke on top of that. Hot objects get a pinkish core and a wider halo. Numerals and title text are red fill with stacked red text-shadow and no white core.
- Illustration: flat 2D, uniform line weight, flat fills that change colour over time. Skeletons have a black body, white bone line-art (dotted spine, pill-shaped pelvis), an oval head with red glowing eyes and an open mouth, and turn into red x-rays inside objects. Props are geometric.
- 100 % 2D: the door "rotation" is a scaleX squash.
- Infographics are always one centred icon plus one big number or waveform plus one tiny grey label.

### 3. Motion language

- **Camera:** locked for 66 of 70 s; measured global pan is 0. The only move is the cold-open pull-out (f14–36, peak 20 px/f, ease-out). No shake, Ken Burns or parallax.
- **Every new shot scale-pops:** it starts at about 95–106 % and settles in 3–4 frames. Title elements pop from 0.85 with an ease-out-back over 4–5 frames.
- **Punch-in/out** (×0.8–×2.3) on the same artwork replaces camera moves. Ten of the shot changes are punches.
- **Short, literal in-shot actions:** door opens in 8 f and closes in 5 f; tube draws on in 4 f; eye closes in 12 f; sine grows in 6 f; fire ignites in 12 f; badge→pill in 6 f; pill→badge in 5 f. Appearances ease out (power2/3); exits ease in.
- **Value animations:**
  - The timer runs linear at +2 s per frame.
  - The thermometer uses expo ease-out over about 30 f, then holds.
  - Colour ramps (fills, floor glow) take 2–3 s.
- **Idle motion is always on:**
  - Fire on a stepped 2–3 f cycle.
  - Embers rising at 1–2 px/f.
  - Smoke wisps.
  - Limb poses held 3–6 f (animated on twos/threes).
  - Sound arcs pulsing on about 5 f.
  - Waveform noise changing every frame.
- **Something new about every 0.9 s** (the caption swap), plus an action or cut every 1–2.6 s.

### 4. Edit rhythm

- **Changes at frames:** 165, 248, 374, 429, 477, 525, 606, 696, 755, 815, 876, 948, 1002 (sponsor), 1137, 1182, 1284, 1350, 1468, 1516, 1550, 1602, 1746, 1796, 1838, 1935, 1986, and the 2029 morph.
- **27 shots:** mean 2.58 s, median 2.03 s, shortest 1.13 s, longest 5.5 s (the cold open).
- **Cuts per 10 s:** 2, 4, 5, 4, 3, 5, 3.
- **Sync rule:** the cut comes 1–4 frames (median 2) before the phrase onset, the caption 0–2 f after the cut, then the voice. A new clause gets a new picture; inside a sentence only the caption changes.
- **Hook:** the climax image (screaming bull head with sound waves) under a loud drone, no text for 1.6 s, a pull-out that reveals the whole machine, then the "you" question. The red first word sets the colour code. There is no persistent title or hook bar.
- **Story arc:**
  1. Climax flash-forward.
  2. Place and time card.
  3. Object with a human for scale.
  4. The procedure: door, push in, close, dark.
  5. Data escalation: timer, thermometer, touch.
  6. Sponsor at 33 s, right after the first peak.
  7. Second escalation: air, lungs, tube, scream.
  8. Twist: screams become music, the king laughs.
  9. Decay: voice breaks, the bull goes silent.
  10. Eye closes into a flatline with a beep, then fade.
- **Ending:** no card, no CTA, and not built as a seamless loop.

### 5. Text and caption system

- **Position and size:**
  - One centred line, cap band at 118–146 px of 1024, so the centre sits at **12.9 % of frame height**.
  - Cap height 28–29 px (4.9 % of width), font-size ≈40 px at 576 W.
  - At 1080×1920: **75 px font, ≈53 px cap height, centred at y = 248 px.**
- **Font:** condensed grotesque, Bold 700, all caps, tracking 0 to +1 %. Roboto Condensed Bold is the closest match; for English use Roboto Condensed 700 or Oswald 600.
- **Styling:** white #F4F4F4 and red #F44241, flat. No box, stroke, shadow or glow; the black top half provides the contrast.
- **Length:** at most 17 characters (widest line 63 % of width). Never wraps.
- **Count and chunking:** 72 captions. 1.85 words on average: 27 one-word, 29 two-word, 16 three-word. Chunks break at phrase boundaries and keep punctuation (. , ? ! ...).
- **Timing:**
  - Duration mean 26 f (0.88 s), median 25 f, range 10–56 f.
  - Each caption stays until the next replaces it, so the band is never empty after f50.
  - Captions are hard swaps with no in/out animation and no word-level karaoke.
  - They appear 0–3 f before the spoken word.
- **Accent rule:**
  1. The last chunk of each sentence carries red (31 of 33). A one-word sentence ending is entirely red; in a multi-word ending only the payoff word is red.
  2. Key nouns are red even mid-sentence: БЫК, ТРУБКУ, ДЫШАТЬ, КРИК, and the opening КАКОВО.
  3. Connectives and lead-ins stay white.
  4. Totals: 35 all-white, 17 mixed, 20 all-red captions. About half of captions contain red; about 22 % of words are red.
- **Secondary labels:** 12–16 px grey small caps placed inside the diagrams. They pop in with their object. A label can turn red and grow to become an accent (РЁВ at f1709).
- **Big numerals:** red neon, condensed black weight, ≈95–110 px at 576 W, centred, always paired with a tiny grey unit label.

### 6. Sound design (from the visuals and the audio)

- **Intro (0–1.6 s):** drone/roar at -11 dBFS (290 Hz plus a 31 Hz sub).
- **Music bed:** about -27 dBFS in the VO gaps, roughly 15 dB under the voice.
- **Cut hits:** high-frequency transients of +20…+38 dB at 165, 429, 525, 1516, 1746 and 1986. Low thumps at 248, 696, 755, 1137, 1602 and 1935. So every cut carries a whoosh or a sub-hit.
- **Implied effects:** door clank (386/480), fire ignition and crackle (629–), clock tick under the timer, sizzle at 959, muffled scream turning into a roar (1516–1740), laughter for the "ХА" pops, voice crack (1859–1913).
- **Ad section:** the music bed is cut (-34 to -44 dBFS in the gaps).
- **Ending:** a pure 1000 Hz flatline beep from f2031 to about 69.4 s, matching the red flatline picture.

### 7. Reproduction recipe (HyperFrames, 1080×1920 at 30 fps)

**Stage**

- Root background #010101.
- A `.floor` layer:
  `radial-gradient(ellipse 75% 48% at 50% 104%, #B01804 0%, #861207 18%, #4A0901 42%, #1A0200 70%, #010101 100%)`.
- Animate its opacity to represent heat: 0.35 for the ending, 0.7 normally, 1.0 for the fire and 400 °C beats.

**Neon object (SVG)**
Three `<use>` layers of the same path:

1. Halo: `stroke="#FF3B36"`, width 12, `filter="url(#glow)"`, where the filter merges `feGaussianBlur stdDeviation="14"` with a second blur of 4.
2. Fill: `#0C0A0C`. Tween it to #450B09 and then #871712 as it heats.
3. Core: `stroke="#F2F2EE"`, width 5, round joins.

Hot objects get a #FFB3B0 core and an 18 px halo. Neon text uses `text-shadow: 0 0 6px #FF3B36, 0 0 22px rgba(255,40,40,.75), 0 0 48px rgba(255,30,30,.35)`.

**Captions**
`.cap { position:absolute; top:248px; transform:translateY(-50%); width:100%; text-align:center; font:700 75px/1 "Roboto Condensed"; letter-spacing:.01em; text-transform:uppercase; color:#F4F4F4 }`, with `.a { color:#F44241 }` for accent words.

- Chunk word timestamps into 1–3 words and at most 17 characters, breaking on punctuation and on pauses of 200 ms or more.
- Set each chunk on at (onset − 1 frame) as a hard set, and keep it until the next chunk.
- Make the sentence-final word red (the whole chunk if it is one word), plus chosen key nouns.

**Cuts**

- Place each cut 2 frames before the phrase onset.
- New shot: `gsap.fromTo(shot, {scale:1.06}, {scale:1, duration:0.12, ease:"power2.out"})`. For punch-outs start from 0.95.
- Title elements: from scale 0.85, `back.out(2)`, 0.15 s.
- Punch cuts reuse the same SVG group, rescaled ×2.3 or ×0.8 around a target point.
- No crossfades. Put a 150–250 ms whoosh or sub-hit on every cut.

**Idle layers (seeded, deterministic)**

- **Fire:** 3–4 flame paths cycled with a 2-frame `steps(1)` cadence, plus a screen-blended blurred glow ellipse underneath.
- **Embers:** 15–25 dots of 2–4 px in #FF8A5A, rising 1–2 px per frame, fading out over 40–80 f.
- **Smoke:** blurred #1A1414 ellipses drifting up at 0.5 px per frame.
- **Characters:** limb poses held 3–6 f (`steps(1)`).
- **Sound arcs:** 14 px neon arcs, opacity 0.4↔1 on a 5-frame period.

**Data beats**

- **Timer:** 0→117 s over 60 f, linear, formatted mm:ss. The ring's `stroke-dashoffset` runs in sync from 12 o'clock.
- **Thermometer:** 30→400 over 30 f with `expo.out`. Mercury height and `.floor` brightness are linked to the value.
- **Waveforms:** seeded-noise polylines regenerated each frame, drawn on with `stroke-dashoffset` and a 6 px white dot at the leading edge. Tween the amplitude envelope for the "voice breaking" collapse.
- **Lungs and bull heating:** tween the fill colour over 2–3 s.

**Ending**

- An SVG eye whose upper lid is a clip-path closing over 12 f (`power2.in`).
- On the closing frame, a 6 px neon line goes from scaleX 0.35 to 1 in 1–2 f.
- Hold 1.4 s with a 1 kHz beep, then fade root opacity over 12 f, then 0.2 s of black.

**Sponsor pattern**

1. A 60 px brand badge pops onto the character (5 f, back.out).
2. Tween its width, height and border-radius over 6 f (power2.out) into a full-radius pill window at 100 % W × 22 % H, centred at 50 % height, inside the scene.
3. Freeze the caption band and drop the music bed.
4. Reverse the morph over 5 f (power2.in), fade the badge, then punch-cut into the next beat.

### 8. Strengths and weak spots

**Strengths**

- One-colour discipline: caption red and diagram red are the same hue, so the payoff word rhymes with the glowing object.
- The top half is always empty black, so captions read without boxes and the frame feels premium.
- Every clause gets a literal visual: hollow → dashed cavity, bronze → shine sweep, minutes → timer, hot walls → thermometer, scream → waveform through a tube, darkness → eye → flatline.
- Heat runs as a colour arc across the whole video.
- Tight sync (cuts 2 f ahead, captions about every 0.9 s, cut sound effects) makes a mostly static frame feel fast.
- A strong flash-forward cold open and a strong closing beat (flatline plus beep).
- A cheap but effective camera: punch cuts with a 3-frame settle.

**Weak spots**

- The camera is almost dead: 66 of 70 s are locked off, and the title card (≈2.7 s) and thermometer hold (≈1.4 s) have nothing moving but glow. A slow 1–2 % per second push-in on holds would help.
- The sponsor's blue 3D look clashes with the red world, and it sits at the dramatic peak for 4.5 s.
- The same wide bull shot is reused about 7 times.
- Captions have no motion. A 2-frame pop (1.04→1) per chunk, or a colour fill on the red word, would add energy.
- No loop or CTA; for example the flatline could turn into the bull-head outline from frame 0.
- Some captions are too short (10 f: "ТАК,", "МЕСТО,"), and "ПРИКОСНУТЬСЯ." stays frozen for about 5.5 s across the ad.
- Character animation is stiff (stepped pose swaps) and the faces have little expression.
