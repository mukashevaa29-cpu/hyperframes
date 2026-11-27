"""Episode 10 — How does it feel? When you get stuck upside down in a cave (Nutty Putty Cave, Utah, 2009)."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
ROCK = "#140808"
LAMP, LAMP_CORE = "#E8B040", "#FFE08A"
DUST = dict(n=60, sp=90, color="#8a7a70", y0=300)
HEART = "M 540 960 C 400 860 330 780 360 690 C 390 600 500 600 540 690 C 580 600 690 600 720 690 C 750 780 680 860 540 960 Z"


def walls(cx, y0, y1, w_top, w_bot, seed, gid="", fill=ROCK):
    """two jagged rock walls with a slot between them, width going w_top -> w_bot."""
    r = random.Random(seed)
    n = 14
    L, R = [f"M -120 {y0}"], [f"M 1200 {y0}"]
    for k in range(n + 1):
        f = k / n
        y = y0 + (y1 - y0) * f
        w = w_top + (w_bot - w_top) * f
        L.append(f"L {cx - w / 2 - r.uniform(0, 34):.0f} {y:.0f}")
        R.append(f"L {cx + w / 2 + r.uniform(0, 34):.0f} {y:.0f}")
    L.append(f"L -120 {y1} Z")
    R.append(f"L 1200 {y1} Z")
    i = lambda s: f' id="{gid}-{s}"' if gid else ""
    return (f'<g{i("L")}>' + glow(N(" ".join(L), fill=fill, sw=12, cw=4)) + '</g>'
            f'<g{i("R")}>' + glow(N(" ".join(R), fill=fill, sw=12, cw=4)) + '</g>')


def upside(mid, x, yfeet, s, pose=None, style="neon"):
    """mascot hanging head-down: feet at (x, yfeet), head below. Tween '#mid-w' in screen space."""
    p = dict(uarmL=-172, farmL=0, uarmR=172, farmR=0, thighL=4, thighR=-4)
    p.update(pose or {})
    return f'<g id="{mid}-w"><g transform="translate({x},{yfeet}) rotate(180)">{mascot(mid, 0, 0, s, pose=p, style=style)}</g></g>'


def head_y(yfeet, s):
    return yfeet + 556 * s


def hill(gid, fill_tunnel=False):
    """cross-section of the hill with the winding cave passage; returns (svg, tunnel path)."""
    ground = "M -40 900 L 180 880 L 300 860 Q 420 760 560 800 Q 700 830 820 880 L 1120 900 L 1120 1900 L -40 1900 Z"
    strata = "".join(f'<path d="M -40 {980 + k * 140} Q 300 {950 + k * 140} 540 {990 + k * 140} T 1120 {970 + k * 140}" fill="none" stroke="#3a1612" stroke-width="4" opacity="0.8"/>' for k in range(6))
    tunnel = "M 300 862 Q 330 960 260 1040 Q 190 1120 330 1180 Q 520 1250 640 1200 Q 760 1150 780 1270 Q 800 1380 640 1420 L 640 1520"
    t_svg = (f'<path d="{tunnel}" fill="none" stroke="{RED}" stroke-width="58" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>'
             f'<path d="{tunnel}" fill="none" stroke="#050303" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<g id="{gid}">' + glow(N(ground, fill=ROCK, sw=12, cw=4)) + strata + t_svg + '</g>'), tunnel


def lamp_dot(cls, x, y):
    return f'<g class="{cls}"><circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{LAMP_CORE}" filter="url(#glowG)"/></g>'


# ---------------------------------------------------------------- S01 cold open: hanging head-down in the slot, close on the face → pull out
s, e = 0.0, cut(13)
y1f, s1 = 640, 0.85
svg = (walls(540, 380, 1950, 420, 190, 1) + upside("m1", 540, y1f, s1) +
       f'<circle id="s01-blood" cx="540" cy="{head_y(y1f, s1):.0f}" r="70" fill="#FF1E2E" opacity="0.0" filter="url(#soft2)"/>')
ep.scene("s01", s, e, svg, origin="50% 64%", custom_cam=True, fx=[(s, e, "ash", DUST)])
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.2}},{{scale:2.3,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
for k in range(int(e / 0.62)):
    ep.js(f'tl.fromTo("#s01-blood",{{opacity:0.75}},{{opacity:0.2,duration:0.55,ease:"power2.out",immediateRender:false}},{k * 0.62:.3f});')
    ep.cue("heart.wav", k * 0.62, 0.55)
r1 = random.Random(1)
for k in range(int(e / 0.35)):
    ep.rot("#m1-head", k * 0.35, 0.3, r1.uniform(-9, 9), "sine.inOut", about="0,-492")
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("sub.wav", 0, 0.7)
ep.cue("cave_drip.mp3", 0, 0.6)
ep.cue("rock_scrape.mp3", 0.2, 0.5)

# ---------------------------------------------------------------- S02 Utah. Nutty Putty Cave. 2009.
s, e = cut(13), cut(18)
h_svg, tunnel = hill("s02-hill")
trail = f'<path id="s02-trail" d="{tunnel}" pathLength="1" fill="none" stroke="{LAMP_CORE}" stroke-width="8" stroke-dasharray="1" stroke-dashoffset="1" stroke-linecap="round" filter="url(#glowG)"/>'
html = ('<div class="num" id="s02-n" style="top:600px;font-size:170px;">2009</div>'
        '<div class="lbl" id="s02-l" style="top:540px;">NUTTY PUTTY CAVE · UTAH</div>')
ep.scene("s02", s, e, h_svg + trail, html, origin="50% 55%")
ep.pop("#s02-l", W(14) - 0.05, 0.18, 0.8)
ep.pop("#s02-n", W(17) - 0.05, 0.2, 1.4, "power3.out")
ep.js(f'tl.to("#s02-trail",{{strokeDashoffset:0,duration:{e - s - 0.2:.3f},ease:"power1.inOut"}},{s + 0.1:.3f});')
ep.cue("cave_drip.mp3", s, 0.5)
ep.cue("impact-bass-2.mp3", W(17), 0.5)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S03 you squeeze into a narrow passage — you think it's a tunnel — dead end
s, e = cut(18), cut(33)
top = "M -120 600 L -120 980 L 120 1000 L 260 1040 L 420 1060 L 560 1080 L 700 1096 L 760 1100 L 760 600 Z"
bot = "M -120 1700 L -120 1330 L 120 1300 L 260 1260 L 420 1240 L 560 1226 L 700 1214 L 760 1210 L 760 1700 Z"
end_wall = "M 740 600 L 760 1100 Q 790 1150 760 1210 L 740 1700 L 1200 1700 L 1200 600 Z"
dream = line(760, 1155, 1080, 1155, LAMP_CORE, 6, 'stroke-dasharray="26 18" id="s03-dream"')
crawler = f'<g id="s03-m"><g transform="translate(0,1160) rotate(90)">{mascot("m3", 0, 0, 0.32, pose=dict(uarmL=-170, uarmR=170, thighL=6, thighR=-6))}</g></g>'
svg = (glow(N(top, fill=ROCK, sw=12, cw=4)) + glow(N(bot, fill=ROCK, sw=12, cw=4)) + f'<g id="s03-end">' + glow(N(end_wall, fill=ROCK, sw=12, cw=4)) + '</g>'
       + f'<g filter="url(#glowG)">{dream}</g>' + crawler + label(900, 1060, "TUNNEL?", 32, LAMP_CORE, extra='id="s03-q"') +
       label(900, 1060, "DEAD END", 40, "#FF3B36", extra='id="s03-x"'))
ep.scene("s03", s, e, svg, origin="40% 60%", drift=0.02)
ep.js(f'tl.fromTo("#s03-m",{{x:-20}},{{x:560,duration:{W(31) - s:.3f},ease:"power1.inOut",immediateRender:false}},{s:.3f});')
for k in range(int((W(31) - s) / 0.3)):
    ep.js(f'tl.to("#s03-m",{{y:{-6 if k % 2 else 6},duration:0.3,ease:"sine.inOut"}},{s + k * 0.3:.3f});')
ep.show("#s03-dream", W(25) - 0.05, 0.3)
ep.show("#s03-q", W(25), 0.2)
ep.js(f'tl.to("#s03-dream, #s03-q",{{opacity:0,duration:0.1}},{W(31) - 0.05:.3f});')
ep.pop("#s03-x", W(31) - 0.02, 0.2, 1.8, "power3.out")
ep.shake("#s03-shake", W(31) - 0.02, 0.4, 14)
ep.flash(W(31) - 0.02, 0.25, 0.4)
ep.cue("rock_scrape.mp3", s + 0.2, 0.6)
ep.cue("impact-bass-1.mp3", W(31) - 0.02, 0.8)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S04 the gap is just 25 cm across — your shoulders are wider
s, e = cut(33), cut(40)
gl = "M -120 620 L 400 620 L 420 720 L 395 840 L 415 960 L 400 1080 L -120 1080 Z"
gr = "M 1200 620 L 680 620 L 660 720 L 688 840 L 662 960 L 680 1080 L 1200 1080 Z"
dims = (line(415, 1140, 665, 1140, CORE, 5) + line(415, 1115, 415, 1165, CORE, 5) + line(665, 1115, 665, 1165, CORE, 5))
sh = (f'<g id="s04-sh"><rect x="315" y="1440" width="450" height="46" rx="10" fill="#FB2945" filter="url(#glow)"/>'
      + line(415, 1420, 415, 1510, "#F2EEEA", 4, 'stroke-dasharray="10 8"') + line(665, 1420, 665, 1510, "#F2EEEA", 4, 'stroke-dasharray="10 8"')
      + label(540, 1565, "YOUR SHOULDERS: 45 CM", 32, "#FF6A6A") + '</g>')
html = '<div class="num" id="s04-n" style="top:1190px;font-size:140px;">0 CM</div>'
svg = f'<g id="s04-L">{glow(N(gl, fill=ROCK, sw=12, cw=4))}</g><g id="s04-R">{glow(N(gr, fill=ROCK, sw=12, cw=4))}</g>' + glow(dims, f="glowS") + sh
ep.scene("s04", s, e, svg, html, origin="50% 55%")
ep.js(f'tl.fromTo("#s04-L",{{x:-260}},{{x:0,duration:0.35,ease:"power3.in",immediateRender:false}},{s + 0.02:.3f});')
ep.js(f'tl.fromTo("#s04-R",{{x:260}},{{x:0,duration:0.35,ease:"power3.in",immediateRender:false}},{s + 0.02:.3f});')
ep.shake("#s04-shake", s + 0.37, 0.25, 10)
ep.cue("impact-bass-2.mp3", s + 0.37, 0.6)
ep.js(f'(function(){{var el=document.getElementById("s04-n");var o={{v:0}};tl.to(o,{{v:25,duration:{WE(38) - W(37):.3f},ease:"expo.out",onUpdate:function(){{el.textContent=Math.round(o.v)+" CM";}}}},{W(37) - 0.05:.3f});}})();')
ep.pop("#s04-sh", W(39) - 0.1, 0.25, 0.6)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S05 you slide in head first... and you're stuck. Upside down.
s, e = cut(40), cut(50)
y5f, s5 = 760, 0.7
svg = walls(540, 380, 1950, 460, 170, 5) + upside("m5", 540, y5f, s5, pose=dict(uarmL=-176, uarmR=176))
ep.scene("s05", s, e, svg, origin="50% 60%", fx=[(s, e, "ash", DUST)])
ep.js(f'gsap.set("#m5-w",{{y:-700,rotation:-28,svgOrigin:"540 {y5f}"}});')
ep.js(f'tl.to("#m5-w",{{y:-120,rotation:-14,svgOrigin:"540 {y5f}",duration:{W(44) - s:.3f},ease:"power1.in"}},{s:.3f});')
ep.js(f'tl.to("#m5-w",{{y:0,rotation:-6,svgOrigin:"540 {y5f}",duration:0.35,ease:"power4.in"}},{W(47) - 0.35:.3f});')
ep.js(f'tl.to("#m5-w",{{rotation:0,svgOrigin:"540 {y5f}",duration:0.5,ease:"power2.out"}},{W(48) - 0.1:.3f});')
ep.shake("#s05-shake", W(47), 0.45, 16)
ep.cue("rock_scrape.mp3", W(41), 0.7)
ep.cue("impact-bass-1.mp3", W(47), 0.9)
ep.cue("sub.wav", W(47), 0.6)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S06 arms pinned under your chest — can't go forward, can't go back
s, e = cut(50), cut(63)
y6f, s6 = 820, 1.05
arrow_dn = f'<g id="s06-fw"><g filter="url(#glow)">' + N("M 150 1260 L 150 1460 M 100 1400 L 150 1460 L 200 1400", fill="none", sw=12, cw=4) + '</g>' + label(150, 1530, "FORWARD", 28, GREY) + '</g>'
arrow_up = f'<g id="s06-bk"><g filter="url(#glow)">' + N("M 930 1460 L 930 1260 M 880 1320 L 930 1260 L 980 1320", fill="none", sw=12, cw=4) + '</g>' + label(930, 1530, "BACK", 28, GREY) + '</g>'
xs = lambda gid, x: f'<g id="{gid}">' + line(x - 70, 1290, x + 70, 1430, "#FF3B36", 16) + line(x + 70, 1290, x - 70, 1430, "#FF3B36", 16) + '</g>'
svg = (walls(540, 380, 1950, 330, 260, 6, gid="s06w") + upside("m6", 540, y6f, s6, pose=dict(uarmL=-178, uarmR=178)) +
       arrow_dn + arrow_up + f'<g filter="url(#glow)">{xs("s06-x1", 150)}{xs("s06-x2", 930)}</g>')
ep.scene("s06", s, e, svg, origin="50% 62%", drift=0.025)
for k in range(5):
    t = s + 0.3 + k * ((e - s - 0.3) / 5)
    ep.js(f'tl.to("#s06w-L",{{x:{6 + k * 5},duration:0.25,ease:"power2.in"}},{t:.3f});')
    ep.js(f'tl.to("#s06w-R",{{x:{-6 - k * 5},duration:0.25,ease:"power2.in"}},{t:.3f});')
ep.cue("rock_scrape.mp3", s + 0.3, 0.45)
ep.show("#s06-fw", W(55) - 0.05, 0.15)
ep.pop("#s06-x1", W(58) - 0.05, 0.16, 1.6, "power3.out")
ep.show("#s06-bk", W(59) - 0.05, 0.15)
ep.pop("#s06-x2", W(62) - 0.05, 0.16, 1.6, "power3.out")
ep.cue("impact-bass-2.mp3", W(58) - 0.05, 0.6)
ep.cue("impact-bass-2.mp3", W(62) - 0.05, 0.7)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S07 blood floods your head
s, e = cut(63), cut(67)
y7f, s7 = 560, 1.3
hy = head_y(y7f, s7)
r7 = random.Random(7)
cells = "".join(f'<circle class="s07-c" cx="{540 + r7.uniform(-60, 60):.0f}" cy="{r7.uniform(700, 1150):.0f}" r="{r7.uniform(9, 16):.0f}" fill="#FF2A33" filter="url(#glowS)"/>' for _ in range(26))
svg = (upside("m7", 540, y7f, s7, style="xray", pose=dict(uarmL=-178, uarmR=178)) + cells +
       f'<ellipse id="s07-pool" cx="540" cy="{hy:.0f}" rx="74" ry="92" fill="#FF1E2E" opacity="0" filter="url(#glow)"/>'
       + label(540, 1760, "BLOOD PRESSURE IN YOUR HEAD ↑", 30, "#FF6A6A"))
ep.scene("s07", s, e, svg, origin="50% 70%", drift=0.04)
REP7 = int((e - s) / 0.7)
ep.js(f'tl.fromTo(".s07-c",{{y:0,opacity:0}},{{y:420,opacity:1,duration:0.7,stagger:{{each:0.05,repeat:{REP7}}},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo("#s07-pool",{{opacity:0,scale:0.5,transformOrigin:"50% 50%"}},{{opacity:0.85,scale:1,duration:{e - s - 0.3:.3f},ease:"power1.in",immediateRender:false}},{s + 0.1:.3f});')
ep.cue("heart.wav", s, 0.7)
ep.cue("heart.wav", s + 0.55, 0.75)
ep.cue("heart.wav", s + 1.05, 0.8)
ep.floor(s, 0.5, 0.3)

# ---------------------------------------------------------------- S08 every breath, the rock squeezes your ribs
s, e = cut(67), cut(74)
ep.lungs("s08", s, e, t_breath=W(67), label_txt="LUNGS")
ep.scenes[-1]["svg"] += (f'<g id="s08-L">' + glow(N("M -120 600 L 250 600 L 230 800 L 270 1000 L 236 1200 L 262 1400 L 240 1600 L -120 1600 Z", fill=ROCK, sw=12, cw=4)) + '</g>'
                         f'<g id="s08-R">' + glow(N("M 1200 600 L 830 600 L 850 800 L 812 1000 L 846 1200 L 818 1400 L 840 1600 L 1200 1600 Z", fill=ROCK, sw=12, cw=4)) + '</g>')
tq = W(71) - 0.05
ep.js(f'tl.to("#s08-L",{{x:70,duration:0.5,ease:"power3.in"}},{tq:.3f});')
ep.js(f'tl.to("#s08-R",{{x:-70,duration:0.5,ease:"power3.in"}},{tq:.3f});')
ep.js(f'tl.to("#s08-lungs",{{scaleX:0.8,scaleY:1.04,transformOrigin:"50% 50%",duration:0.5,ease:"power3.in"}},{tq:.3f});')
ep.shake("#s08-shake", tq + 0.5, 0.3, 10)
ep.cue("rock_scrape.mp3", tq, 0.7)
ep.cue("impact-bass-2.mp3", tq + 0.5, 0.6)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S09 your heart pumps against gravity, hour after hour
s, e = cut(74), cut(82)
html = '<div class="num" id="s09-n" style="top:1010px;font-size:170px;">1</div><div class="lbl" style="top:1195px;">HOURS STUCK</div>'
ep.scene("s09", s, e, glow(N(HEART, fill="#2a0a0c"), gid="s09-h"), html, origin="50% 50%",
         fx=[(s, e, "ecg", dict(x0=60, x1=1020, y=1440, amp=130, period=380, period1=300, dur=e - s, speed=380))])
t, k = s, 0
while t < e - 0.1:
    ep.js(f'tl.fromTo("#s09-h",{{scale:1.12,svgOrigin:"540 780"}},{{scale:1,duration:0.35,ease:"power2.out",immediateRender:false}},{t:.3f});')
    ep.cue("heart.wav", t, 0.55)
    t += 0.62
ep.js(f'tl.fromTo("#s09-h",{{y:0}},{{y:24,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.counter("#s09-n", W(79) - 0.1, e - W(79), 1, 12, "n", "power1.in")
ep.cue("tick.wav", W(79), 0.5)
ep.floor(s, 0.4, 0.2)

# ---------------------------------------------------------------- S10 more than a hundred rescuers try to pull you out
s, e = cut(82), cut(92)
h_svg, tunnel = hill("s10-hill")
pts = [(300, 870), (322, 930), (300, 1000), (262, 1040), (220, 1090), (240, 1150), (330, 1180), (420, 1215), (520, 1232), (600, 1215), (690, 1170), (760, 1190), (785, 1270), (770, 1340), (720, 1400)]
lamps = "".join(lamp_dot("s10-l", x + dx, y + dy) for (x, y) in pts for dx, dy in ((-6, -4), (6, 5)))
surf = "".join(lamp_dot("s10-l", 120 + k * 46, 850 + (k % 3) * 6) for k in range(5))
fig = upside("m10", 640, 1440, 0.16)
rope = line(640, 1420, 640, 1440, CORE, 3)
html = '<div class="num" id="s10-n" style="top:580px;font-size:160px;">0</div><div class="lbl" style="top:745px;">RESCUERS</div>'
ep.scene("s10", s, e, '<g transform="translate(0,110)">' + h_svg + fig + rope + lamps + surf + '</g>', html, origin="60% 70%", drift=0.02)
ep.js(f'tl.fromTo(".s10-l",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.12,stagger:{(WE(86) - W(82)) / 35:.3f},ease:"back.out(3)",immediateRender:false}},{W(82):.3f});')
ep.js('gsap.set(".s10-l",{opacity:0});')
ep.js(f'(function(){{var el=document.getElementById("s10-n");var o={{v:0}};tl.to(o,{{v:100,duration:{WE(86) - W(82) + 0.2:.3f},ease:"expo.out",onUpdate:function(){{var n=Math.round(o.v);el.textContent=n>=100?"100+":String(n);}}}},{W(82):.3f});}})();')
ep.cue("riser.mp3", W(82), 0.4)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S11 then a rope anchor breaks — you slide back down
s, e = cut(92), cut(101)
y11f, s11 = 980, 0.62
pulley = glow(f'<circle cx="540" cy="640" r="44" fill="{DARK}" stroke="{RED}" stroke-width="12"/><circle cx="540" cy="640" r="12" fill="{CORE}"/>' + line(430, 600, 650, 600, CORE, 8))
rope_top = f'<g id="s11-rt">' + line(540, 684, 540, 830, LAMP_CORE, 7) + '</g>'
rope_bot = f'<g id="s11-rb">' + line(540, 830, 540, y11f + 10, LAMP_CORE, 7) + '</g>'
svg = walls(540, 380, 1950, 420, 180, 11) + pulley + f'<g filter="url(#glowG)">{rope_top}{rope_bot}</g>' + upside("m11", 540, y11f, s11, pose=dict(uarmL=-176, uarmR=176))
ep.scene("s11", s, e, svg, origin="50% 55%", fx=[(W(96) - 0.05, W(96) + 0.6, "sparks", dict(cx=540, cy=830, n=34, r=260, dur=0.6, color="#FFD27A", g=260)),
                                                    (W(97), e, "ash", DUST)])
for k in range(int((W(96) - s) / 0.25)):
    ep.js(f'tl.set("#m11-w, #s11-rb",{{y:{-3 if k % 2 else -9}}},{s + k * 0.25:.3f});')
tb = W(96) - 0.05
ep.js(f'tl.to("#s11-rt",{{scaleY:0,svgOrigin:"540 684",duration:0.25,ease:"power3.out"}},{tb:.3f});')
ep.js(f'tl.to("#s11-rb, #m11-w",{{y:330,duration:0.7,ease:"power3.in"}},{tb + 0.05:.3f});')
ep.shake("#s11-shake", tb, 0.5, 18)
ep.shake("#s11-shake", tb + 0.75, 0.4, 12)
ep.flash(tb, 0.35, 0.4)
ep.cue("rope_snap.mp3", tb - 0.05, 1.0)
ep.cue("rock_scrape.mp3", tb + 0.15, 0.8)
ep.cue("impact-bass-1.mp3", tb + 0.75, 0.9)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S12 twenty-seven hours upside down
s, e = cut(101), cut(105)
ep.timer("s12", s, e, W(101) - 0.1, WE(102), 0, 27, "n", "HOURS UPSIDE DOWN", 1.0)
ep.floor(s, 0.4, 0.0)

# ---------------------------------------------------------------- S13 your heart gives out
s, e = cut(105), cut(109)
ep.scene("s13", s, e, glow(N(HEART, fill="#2a0a0c"), gid="s13-h"), origin="50% 50%",
         fx=[(s, e, "ecg", dict(x0=60, x1=1020, y=1300, amp=130, period=420, period1=700, dur=e - s, speed=380, flat_at=W(107), flat_dur=0.6))])
for t in (s, s + 0.8, s + 1.75):
    if t < W(107):
        ep.js(f'tl.fromTo("#s13-h",{{scale:1.1,svgOrigin:"540 780"}},{{scale:1,duration:0.4,ease:"power2.out",immediateRender:false}},{t:.3f});')
        ep.cue("heart.wav", t, 0.6)
ep.js(f'tl.to("#s13-h path",{{attr:{{stroke:"#3a3532"}},duration:0.6}},{W(107):.3f});')
ep.js(f'tl.to("#s13-h",{{scale:0.92,svgOrigin:"540 780",y:30,duration:0.8,ease:"power2.in"}},{W(107):.3f});')
ep.cue("beep.wav", W(107) + 0.3, 0.18)
ep.floor(s, 0.25, 0.0)
ep.floor(W(107), 0.0, 0.0, 0.6)

# ---------------------------------------------------------------- S14 they sealed the cave with concrete — you're still inside
s, e = cut(109), cut(118)
h_svg, tunnel = hill("s14-hill")
concrete = f'<path id="s14-c" d="{tunnel}" pathLength="1" fill="none" stroke="#8a837e" stroke-width="40" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
fig = upside("m14", 640, 1440, 0.16)
plaque = ('<div id="s14-pl" style="position:absolute;left:250px;top:600px;width:580px;padding:22px 0;border:4px solid #8a837e;background:#151313;text-align:center;'
          'font-weight:700;color:#d8d2cc;letter-spacing:5px;font-size:40px;line-height:58px;">JOHN EDWARD JONES<br><span style="font-size:34px;color:#BDB5B5;">1983 – 2009</span></div>')
ep.scene("s14", s, e, h_svg + fig + concrete, plaque, origin="59.3% 75.3%", custom_cam=True)
ep.js(f'tl.fromTo("#s14-cam",{{scale:1}},{{scale:1.04,duration:{W(115) - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s14-cam",{{scale:3.4,duration:{e - W(115):.3f},ease:"power2.inOut"}},{W(115) - 0.1:.3f});')
ep.js(f'tl.to("#s14-c",{{strokeDashoffset:0.42,duration:{WE(114) - W(110) + 0.3:.3f},ease:"power1.inOut"}},{W(110) - 0.1:.3f});')
ep.js(f'tl.to("#s14-pl",{{opacity:0,duration:0.3}},{W(115) - 0.1:.3f});')
ep.show("#s14-pl", W(109) + 0.1, 0.3)
ep.cue("concrete_pour.mp3", W(110) - 0.1, 0.7)
ep.cue("sub.wav", W(115), 0.6)
ep.floor(s, 0.2, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(118), 121)
ep.write(red=["stuck", "dead", "upside", "down", "forward", "back", "blood", "ribs", "gravity", "rescuers", "breaks", "heart", "concrete", "inside"])
