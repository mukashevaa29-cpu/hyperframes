"""Episode 06 — How does it feel? When the asteroid that killed the dinosaurs hits the Earth."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
BLUE = "#5A78FF"


def stars(seed=1, n=120):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(380, 1500):.0f}" r="{r.choice([1.5, 2, 3])}" fill="#F2EEEA" opacity="{r.uniform(0.3, 0.9):.2f}"/>' for _ in range(n))


def rock(gid, cx, cy, s=1.0):
    r = random.Random(9)
    pts = " ".join(f"{cx + math.cos(a) * s * r.uniform(80, 115):.0f},{cy + math.sin(a) * s * r.uniform(80, 115):.0f}" for a in [i * 2 * math.pi / 11 for i in range(11)])
    craters = "".join(f'<circle cx="{cx + r.uniform(-50, 50) * s:.0f}" cy="{cy + r.uniform(-50, 50) * s:.0f}" r="{r.uniform(10, 20) * s:.0f}" fill="none" stroke="#F2EEEA" stroke-width="3" opacity="0.5"/>' for _ in range(4))
    trail = (f'<path d="M {cx - 60 * s:.0f} {cy - 70 * s:.0f} L {cx - 900 * s:.0f} {cy - 1100 * s:.0f} L {cx - 700 * s:.0f} {cy - 1250 * s:.0f} L {cx + 70 * s:.0f} {cy - 60 * s:.0f} Z" '
             f'fill="url(#ast-trail)" opacity="0.9"/>')
    return (f'<g id="{gid}">{trail}<g filter="url(#glowO)"><polygon points="{pts}" fill="#2a1208" stroke="#FFB070" stroke-width="10"/></g>{craters}</g>')


DEFS = ('<defs><linearGradient id="ast-trail" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFE2B8"/><stop offset="0.3" stop-color="#FF6A3A" stop-opacity="0.8"/>'
        '<stop offset="1" stop-color="#FF2A33" stop-opacity="0"/></linearGradient></defs>')


def horizon(y=1500, trees=False):
    out = glow(N(f"M -40 {y} L 1120 {y}", sw=10, cw=3))
    if trees:
        r = random.Random(3)
        for k in range(14):
            x = 30 + k * 78 + r.uniform(-10, 10)
            h = r.uniform(70, 130)
            out += f'<path class="tree" d="M {x:.0f} {y} L {x - 26:.0f} {y} L {x:.0f} {y - h:.0f} L {x + 26:.0f} {y} Z" fill="#0c0a0c" stroke="#E8706A" stroke-width="4"/>'
    return out


# ---------------------------------------------------------------- S01 cold open: the rock streaks in → impact
s, e = 0.0, cut(14)
svg = DEFS + stars(1) + horizon(1500, trees=True) + rock("s01-rock", 700, 900, 1.0) + f'<g id="s01-dome" opacity="0"><ellipse cx="760" cy="1500" rx="300" ry="260" fill="url(#sunGrad)" filter="url(#glowO)"/></g>'
ep.scene("s01", s, e, svg, origin="62% 47%", custom_cam=True, fx=[(s, e, "embers", dict(n=30, x0=300, x1=1080, y0=500, y1=1500, sp=200))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:1.8}},{{scale:1.9,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ti = W(11)
ep.js(f'tl.fromTo("#s01-rock",{{x:-60,y:-80}},{{x:60,y:560,scale:0.5,svgOrigin:"700 900",duration:{ti - W(4):.3f},ease:"power2.in",immediateRender:false}},{W(4):.3f});')
ep.js(f'tl.set("#s01-rock",{{opacity:0}},{ti:.3f});')
ep.js(f'tl.fromTo("#s01-dome",{{opacity:1,scale:0.05,svgOrigin:"760 1500"}},{{scale:1.6,duration:{e - ti:.3f},ease:"expo.out",immediateRender:false}},{ti:.3f});')
ep.flash(ti, 1.0, 0.9)
ep.shake("#s01-shake", ti, e - ti, 18)
ep.floor(0, 0.4, 0.2, 0.01)
ep.floor(ti, 0.2, 1.0, 0.1)
ep.cue("whoosh-cinematic.mp3", 0, 0.6)
ep.cue("sfx_open_roar.mp3", ti, 1.0)
ep.cue("sub.wav", ti, 1.0)
ep.cue("impact-bass-2.mp3", ti, 0.9)

# ---------------------------------------------------------------- S02 66 million years ago
s, e = cut(14), cut(18)
html = '<div class="num" id="s02-n" style="top:780px;font-size:260px;">0</div><div class="lbl" style="top:1060px;">MILLION YEARS AGO</div>'
ep.scene("s02", s, e, stars(2, 80), html, origin="50% 50%")
ep.counter("#s02-n", s + 0.05, WE(17) - s, 0, 66)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S03 a rock ten kilometers wide (vs Everest)
s, e = cut(18), cut(23)
ev = glow(N("M 560 1500 L 760 1060 L 820 1130 L 880 1000 L 1040 1500 Z", fill="#0c0a0c", red="#9FC8FF", core="#E6EEFF", sw=8, cw=3), f="glowB")
svg = DEFS + horizon(1500) + rock("s03-rock", 300, 1220, 2.5).replace('<path d="M', '<path opacity="0" d="M', 1) + ev
html = '<div class="lbl" style="top:1540px;left:60px;width:480px;color:#FFB070;">ASTEROID · 10 KM</div><div class="lbl" style="top:1540px;left:560px;width:480px;color:#9FC8FF;">EVEREST · 8.8 KM</div>'
ep.scene("s03", s, e, svg, html, origin="50% 60%")
ep.pop("#s03-rock", W(20) - 0.05, 0.25, 0.3)
ep.floor(s, 0.5, 0.2)

# ---------------------------------------------------------------- S04 twenty kilometers per second
s, e = cut(23), cut(30)
streaks = "".join(f'<line class="s04-st" x1="{x}" y1="{y}" x2="{x - 260}" y2="{y - 260}" stroke="#FFB070" stroke-width="4" opacity="0.7"/>' for x, y in [(900, 700), (700, 600), (1000, 1000), (500, 900), (820, 1300), (300, 1200)])
html = '<div class="num" id="s04-n" style="top:780px;font-size:240px;">0</div><div class="lbl" style="top:1040px;">KILOMETERS PER SECOND</div>'
ep.scene("s04", s, e, stars(4, 80) + streaks, html, origin="50% 50%")
ep.counter("#s04-n", W(26) - 0.1, WE(29) - W(26), 0, 20)
ep.js(f'tl.fromTo(".s04-st",{{x:600,y:600}},{{x:-600,y:-600,duration:0.35,repeat:{int((e - s) / 0.35)},ease:"none",immediateRender:false}},{s:.3f});')
ep.cue("riser.mp3", W(26) - 0.3, 0.4)
ep.floor(s, 0.4, 0.3)

# ---------------------------------------------------------------- S05 crosses the atmosphere in a few seconds
s, e = cut(30), cut(39)
bands = "".join(f'<rect x="0" y="{560 + k * 180}" width="1080" height="180" fill="#5A78FF" opacity="{0.04 + k * 0.035:.3f}"/>' + label(1040, 560 + k * 180 + 50, lab, 26, "#9FC8FF", "end")
                for k, lab in enumerate(["EXOSPHERE", "THERMOSPHERE", "MESOSPHERE", "STRATOSPHERE", "TROPOSPHERE"]))
svg = DEFS + bands + horizon(1460) + rock("s05-rock", 300, 520, 0.6)
ep.scene("s05", s, e, svg, origin="50% 50%")
ep.js(f'tl.fromTo("#s05-rock",{{x:0,y:-100}},{{x:420,y:930,duration:{WE(38) - W(31):.3f},ease:"power1.in",immediateRender:false}},{W(31):.3f});')
ep.cue("whoosh-cinematic.mp3", W(31), 0.6)
ep.floor(s, 0.4, 0.3)

# ---------------------------------------------------------------- S06 you're a thousand kilometers away (map)
s, e = cut(39), cut(44)
coast = '<path d="M -40 760 C 200 800 300 980 380 1100 C 420 1180 470 1240 560 1230 C 640 1220 700 1160 780 1180 C 860 1200 900 1300 1120 1320" fill="none" stroke="#9FC8FF" stroke-width="6" opacity="0.8" filter="url(#glowB)"/>'
ring = f'<g id="s06-ring" filter="url(#glow)"><circle cx="560" cy="1200" r="360" fill="none" stroke="#FB2945" stroke-width="8"/><circle cx="560" cy="1200" r="360" fill="none" stroke="#F2EEEA" stroke-width="3"/></g>'
svg = coast + ring + '<circle cx="560" cy="1200" r="22" fill="#FF3B36" filter="url(#glow)"/>' + label(560, 1270, "IMPACT", 28, "#FF6A5A") + f'<g id="s06-you"><circle cx="305" cy="945" r="16" fill="#FFF" filter="url(#glowB)"/>' + label(305, 900, "YOU", 32, "#FFF") + '</g>' + label(760, 900, "1,000 KM", 32, "#F5F5F5")
ep.scene("s06", s, e, svg, origin="50% 60%", drift=0.02)
ep.js(f'tl.fromTo("#s06-ring",{{scale:0,svgOrigin:"560 1200"}},{{scale:1,duration:0.35,ease:"power3.out",immediateRender:false}},{s + 0.05:.3f});')
ep.pop("#s06-you", W(40), 0.2, 0.2)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S07 first, the flash. brighter than the sun
s, e = cut(44), cut(51)
svg = horizon(1500, trees=True) + mascot("m7", 540, 1500, 0.8, pose=dict(uarmR=-130, farmR=-80, head=-10)) + f'<g filter="url(#glowO)"><circle cx="880" cy="700" r="40" fill="url(#sunGrad)"/></g>' + label(880, 790, "THE SUN", 26, GREY)
ep.scene("s07", s, e, svg, origin="50% 60%")
ep.flash(W(46) - 0.05, 1.0, 1.4)
ep.cue("impact-bass-1.mp3", W(46) - 0.05, 0.9)
ep.floor(s, 0.4, 0.4)

# ---------------------------------------------------------------- S08 more energy than billions of atomic bombs
s, e = cut(51), cut(61)
icons = ""
for k in range(48):
    x, y = 150 + (k % 8) * 112, 700 + (k // 8) * 120
    icons += f'<g class="s08-i"><circle cx="{x}" cy="{y - 16}" r="26" fill="#801F0C"/><rect x="{x - 8}" y="{y - 4}" width="16" height="40" fill="#801F0C"/></g>'
html = '<div class="num" id="s08-n" style="top:1440px;font-size:120px;">1</div><div class="lbl" style="top:1580px;">× HIROSHIMA BOMB</div>'
ep.scene("s08", s, e, f'<g filter="url(#glowO)">{icons}</g>', html, origin="50% 55%")
ep.js(f'tl.fromTo(".s08-i",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.12,stagger:0.03,ease:"back.out(2)",immediateRender:false}},{W(54):.3f});')
ep.js('tl.set(".s08-i",{opacity:0},0);')
ep.counter("#s08-n", W(54), WE(60) - W(54), 1, 4000000000, "c", "expo.in")
ep.floor(s, 0.4, 0.5)

# ---------------------------------------------------------------- S09 the ground shakes harder than any earthquake in history
s, e = cut(61), cut(72)
cracks = '<path id="s09-cr" d="M 540 1500 L 500 1580 L 560 1650 L 510 1760 M 300 1500 L 330 1600 L 290 1700 M 800 1500 L 760 1620 L 820 1720" fill="none" stroke="#FF6A3A" stroke-width="7" stroke-dasharray="900" stroke-dashoffset="900" filter="url(#glowO)"/>'
svg = horizon(1500, trees=True) + cracks + label(90, 760, "SEISMOGRAPH", 30, GREY, "start")
ep.scene("s09", s, e, svg, origin="50% 60%", fx=[(s, e, "ecg", dict(x0=60, x1=1020, y=980, amp=420))])
ep.js(f'tl.to("#s09-cr",{{strokeDashoffset:0,duration:0.6}},{W(63):.3f});')
ep.shake("#s09-shake", W(62), e - W(62), 14)
ep.cue("sfx_open_roar.mp3", W(62), 0.7)
ep.cue("sub.wav", W(63), 0.9)
ep.floor(s, 0.4, 0.6)

# ---------------------------------------------------------------- S10 molten rock rains from the sky
s, e = cut(72), cut(88)
svg = horizon(1500, trees=True)
ep.scene("s10", s, e, svg, origin="50% 60%", fx=[(W(75), e, "stones", dict(n=46, x0=0, x1=1080, sp=1300)), (W(75), e, "ash", dict(n=140, sp=900, color="#FFB070")), (W(75), e, "embers", dict(n=40, x0=0, x1=1080, y0=900, y1=1500, sp=160))])
ep.js(f'tl.to("#floorH",{{opacity:1,duration:{e - W(75):.3f}}},{W(75):.3f});')
ep.cue("sfx_stones.mp3", W(75), 0.6)
ep.floor(s, 0.4, 0.4)

# ---------------------------------------------------------------- S11 the air heats up like an oven
s, e = cut(88), cut(95)
waves = "".join(f'<path class="s11-w" d="M -300 {800 + k * 140} ' + " ".join(f"Q {-300 + i * 120 + 60} {800 + k * 140 + (-26 if i % 2 == 0 else 26)} {-300 + (i + 1) * 120} {800 + k * 140}" for i in range(16)) + f'" fill="none" stroke="#FF6A3A" stroke-width="6" opacity="0.6" filter="url(#glowO)"/>' for k in range(5))
svg = '<rect x="0" y="0" width="1080" height="1920" fill="#5a0c03" opacity="0.35"/>' + waves + horizon(1500, trees=True)
ep.scene("s11", s, e, svg, origin="50% 60%", fx=[(s, e, "ash", dict(n=50, sp=800, color="#FFB070"))])
ep.js(f'tl.fromTo(".s11-w",{{x:0}},{{x:-240,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.cue("roar.mp3", s, 0.6)
ep.floor(s, 0.2, 1.0)

# ---------------------------------------------------------------- S12 forests burst into flames across the continent
s, e = cut(95), cut(102)
svg = horizon(1500, trees=True)
fx = [(W(96) + k * 0.12, e + 0.1, "fire", dict(cx=60 + k * 140, base=1505, w=180, h=260, n=5, grow=0.4, amp=1.0, sp=7, nofade=True)) for k in range(8)]
ep.scene("s12", s, e, svg, origin="50% 65%", fx=fx + [(s, e, "smoke", dict(n=12, cx=540, base=1300, w=900, h=700, r0=60, r1=220, life=3, alpha=0.35))])
ep.cue("sfx_whoosh.mp3", W(96), 0.6)
ep.cue("roar.mp3", W(96), 0.7)
ep.floor(s, 0.2, 1.0)

# ---------------------------------------------------------------- S13 a wave over a hundred meters tall
s, e = cut(102), cut(112)
WAVE = "M -40 1500 L -40 1260 C 120 1260 200 900 420 780 C 560 700 680 760 700 860 C 640 820 560 840 540 920 C 620 900 700 960 720 1500 Z"
svg = (f'<g id="s13-wave">' + glow(N(WAVE, fill="#0b1430", red=BLUE, core="#E6EEFF"), f="glowB") + '</g>' + horizon(1500)
       + mascot("m13", 900, 1500, 0.22) + line(980, 1500, 980, 780, GREY, 3, 'stroke-dasharray="10 10"') + label(1000, 760, "100+ M", 34, "#F5F5F5", "end"))
ep.scene("s13", s, e, svg, origin="60% 70%", drift=0.02)
ep.js(f'tl.fromTo("#s13-wave",{{x:-300,scaleY:0.4,svgOrigin:"300 1500"}},{{x:120,scaleY:1,svgOrigin:"300 1500",duration:{WE(111) - s:.3f},ease:"power2.in",immediateRender:false}},{s:.3f});')
ep.cue("roar.mp3", s, 0.8)
ep.floor(s, 0.4, 0.0)

# ---------------------------------------------------------------- S14 the soot rises and blocks out the sun
s, e = cut(112), cut(121)
svg = f'<g id="s14-sun" filter="url(#glowO)"><circle cx="540" cy="860" r="170" fill="url(#sunGrad)"/></g>' + horizon(1500, trees=True)
ep.scene("s14", s, e, svg, origin="50% 55%", fx=[(W(113), e, "smoke", dict(n=26, cx=540, base=1500, w=1000, h=1100, r0=120, r1=420, life=3.2, alpha=0.75, rgb="40,34,32"))])
ep.js(f'tl.to("#s14-sun",{{opacity:0.08,duration:{e - W(116):.3f},ease:"power1.in"}},{W(116):.3f});')
ep.floor(s, 0.5, 0.2)
ep.floor(W(117), 0.08, 0.0, 1.0)

# ---------------------------------------------------------------- S15 day turns to night, for months, maybe years
s, e = cut(121), cut(129)
html = '<div class="num" id="s15-n" style="top:780px;font-size:240px;color:#9a928c;text-shadow:none;">0</div><div class="lbl" style="top:1040px;">MONTHS WITHOUT SUN</div>'
ep.scene("s15", s, e, horizon(1500, trees=True), html, origin="50% 55%", fx=[(s, e, "ash", dict(n=60, sp=60, color="#6a605a"))])
ep.counter("#s15-n", W(125), WE(128) - W(125), 0, 24, "n", "power1.in")
ep.floor(s, 0.05, 0.0)

# ---------------------------------------------------------------- S16 three quarters of all species disappear
s, e = cut(129), cut(137)
DINO = "M 0 40 Q 10 10 40 8 L 70 8 Q 90 10 92 24 L 80 26 L 76 36 L 60 40 L 58 62 L 50 62 L 50 44 L 30 44 L 28 62 L 20 62 L 18 44 Q 0 50 -34 30 Q -10 36 0 40 Z"
grid = ""
order = list(range(20))
random.Random(16).shuffle(order)
dead = set(order[:15])
for k in range(20):
    x, y = 170 + (k % 4) * 220, 640 + (k // 4) * 180
    grid += f'<g id="s16-d{k}" transform="translate({x - 30},{y}) scale(1.5)">' + N(DINO, sw=6, cw=2) + '</g>'
html = '<div class="num" id="s16-p" style="top:1560px;font-size:110px;">0%</div>'
ep.scene("s16", s, e, f'<g filter="url(#glowS)">{grid}</g>', html, origin="50% 55%")
for j, k in enumerate(sorted(dead, key=lambda q: order.index(q))):
    t = W(131) + j * (WE(136) - W(131)) / 15
    ep.js(f'tl.to("#s16-d{k}",{{opacity:0.12,duration:0.15}},{t:.3f});')
ep.counter("#s16-p", W(131), WE(136) - W(131), 0, 75, "pct", "none")
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(137), 140)
ep.write(red=["asteroid", "dinosaurs", "flash", "sun", "earthquake", "wave", "soot", "species"])
