"""Episode 07 — How does it feel? When you climb into Everest's death zone."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa
from lib import brain as brain_svg


def hand_pos(x, y, s, pose, side):
    """forward kinematics of the mascot rig: centre of the fist in scene coords."""
    sx = -84 if side == "L" else 84
    a = math.radians(pose.get("uarm" + side, 0))
    b = math.radians(pose.get("uarm" + side, 0) + pose.get("farm" + side, 0))
    ex, ey = sx - 118 * math.sin(a), -458 + 118 * math.cos(a)
    hx, hy = ex - 122 * math.sin(b), ey + 122 * math.cos(b)
    return x + hx * s, y + hy * s

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
ICE, ICE_CORE = "#5A78FF", "#E6EEFF"
SNOW = dict(n=110, sp=260, color="#E6EEFF")


def ridge(y=1500, gid=""):
    d = f"M -40 {y + 200} L 120 {y} L 300 {y - 160} L 460 {y - 60} L 640 {y - 380} L 760 {y - 300} L 900 {y - 520} L 1120 {y - 140} L 1120 {y + 900} L -40 {y + 900} Z"
    return glow(N(d, fill="#0a0c14", red=ICE, core=ICE_CORE, sw=12, cw=4), f="glowB", gid=gid)


def climber(mid, x, y, s=0.6, pose=None, style="neon"):
    p = dict(uarmL=-20, farmL=-40, uarmR=30, farmR=20, thighL=25, shinL=-35, head=-6)
    p.update(pose or {})
    return mascot(mid, x, y, s, pose=p, style=style)


# ---------------------------------------------------------------- S01 cold open: on the ridge in the wind → pull out
s, e = 0.0, cut(11)
flag = '<path d="M 900 980 L 900 880 L 960 900 L 900 920" fill="#FB2945" stroke="#F2EEEA" stroke-width="4"/>'
svg = ridge(1500) + flag + climber("m1", 640, 1125, 0.55)
ep.scene("s01", s, e, svg, origin="60% 52%", custom_cam=True, fx=[(s, e, "ash", dict(SNOW, n=160, sp=520))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.3}},{{scale:2.4,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
r1 = random.Random(1)
for k in range(int(e / 0.5)):
    ep.rot("#m1-head", k * 0.5, 0.5, r1.uniform(-14, 4), "sine.inOut", about="0,-492")
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("roar.mp3", 0, 0.8)
ep.cue("sub.wav", 0, 0.6)

# ---------------------------------------------------------------- S02 8,000 meters — above this line the body starts dying
s, e = cut(11), cut(21)
base = 1560
my = lambda m: base - m / 9000 * 1000
ruler = line(150, base, 150, my(9000), CORE, 5) + "".join(line(150, my(m), 186, my(m), CORE, 5) + label(200, my(m) + 10, f"{m:,} M", 26, GREY, "start") for m in range(0, 9001, 1000))
zone = f'<g id="s02-zone" opacity="0"><rect x="150" y="{my(8848):.0f}" width="900" height="{my(8000) - my(8848):.0f}" fill="#FB2945" opacity="0.18"/>' + line(150, my(8000), 1040, my(8000), "#FB2945", 6, 'stroke-dasharray="18 12"') + label(1030, my(8000) - 20, "DEATH ZONE", 34, "#FF3B36", "end") + '</g>'
mount = glow(N(f"M 300 {base} L 640 {my(8848):.0f} L 980 {base} Z", fill="#0a0c14", red=ICE, core=ICE_CORE, sw=10, cw=3), f="glowB")
html = '<div class="num" id="s02-n" style="top:1260px;left:300px;width:680px;font-size:130px;">0 M</div>'
ep.scene("s02", s, e, glow(ruler, f="glowS") + mount + zone, html, origin="50% 55%")
ep.counter("#s02-n", s + 0.05, WE(12) - s, 0, 8000, "c")
ep.show("#s02-zone", W(13) - 0.05, 0.3)
ep.cue("riser.mp3", s, 0.35)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S03 every breath brings a third of the oxygen
s, e = cut(21), cut(33)


def o2_panel(x, n, title, cls):
    r = random.Random(n)
    dots = "".join(f'<g class="{cls}"><circle cx="{x + r.uniform(-150, 150):.0f}" cy="{r.uniform(800, 1250):.0f}" r="30" fill="{ICE}" filter="url(#glowB)"/></g>' for _ in range(n))
    box = glow(N(f"M {x - 200} 740 L {x + 200} 740 L {x + 200} 1320 L {x - 200} 1320 Z", fill="none", red=ICE, core=ICE_CORE, sw=8, cw=3), f="glowB")
    return box + dots + label(x, 1390, title, 30, "#9FC8FF")


svg = o2_panel(300, 9, "SEA LEVEL", "s03-a") + o2_panel(780, 3, "8,000 M", "s03-b")
ep.scene("s03", s, e, svg, origin="50% 55%")
ep.js(f'tl.fromTo(".s03-a",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:0.15,stagger:0.04,ease:"back.out(2)",immediateRender:false}},{s + 0.1:.3f});')
ep.js(f'tl.fromTo(".s03-b",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:0.15,stagger:0.12,ease:"back.out(2)",immediateRender:false}},{W(26) - 0.1:.3f});')
ep.js('gsap.set(".s03-b",{scale:0,transformOrigin:"50% 50%"});')
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S04 your heart races even standing still
s, e = cut(33), cut(41)
HEART = "M 540 960 C 400 860 330 780 360 690 C 390 600 500 600 540 690 C 580 600 690 600 720 690 C 750 780 680 860 540 960 Z"
html = '<div class="num" id="s04-bpm" style="top:1010px;font-size:140px;">70</div><div class="lbl" style="top:1160px;">BEATS PER MINUTE</div>'
ep.scene("s04", s, e, glow(N(HEART, fill="#2a0a0c"), gid="s04-h"), html, origin="50% 50%",
         fx=[(s, e, "ecg", dict(x0=60, x1=1020, y=1450, amp=140, period=400, period1=230, dur=e - s, speed=380))])
ep.counter("#s04-bpm", s + 0.1, e - s - 0.2, 70, 150, "n", "power1.out")
t, gap = s, 0.6
while t < e - 0.1:
    ep.js(f'tl.fromTo("#s04-h",{{scale:1.1,svgOrigin:"540 800"}},{{scale:1,duration:0.22,ease:"power2.out",immediateRender:false}},{t:.3f});')
    ep.cue("heart.wav", t, 0.5)
    t += gap
    gap = max(0.38, gap * 0.93)
ep.floor(s, 0.45, 0.0)

# ---------------------------------------------------------------- S05 each step takes three, four, five breaths
s, e = cut(41), cut(48)
puffs_ = "".join(f'<g id="s05-p{k}" opacity="0"><circle cx="530" cy="955" r="22" fill="none" stroke="#E6EEFF" stroke-width="5"/><circle cx="565" cy="935" r="14" fill="none" stroke="#E6EEFF" stroke-width="4"/></g>' for k in range(5))
html = '<div class="num" id="s05-n" style="top:560px;left:560px;width:500px;font-size:160px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">1</div><div class="lbl" style="top:740px;left:560px;width:500px;">BREATHS PER STEP</div>'
svg = ridge(1500) + climber("m5", 460, 1290, 0.6) + puffs_
ep.scene("s05", s, e, svg, html, origin="45% 60%", fx=[(s, e, "ash", SNOW)])
for k, (wi, v) in enumerate([(41, 2), (44, 3), (45, 4), (46, 5)]):
    ep.counter("#s05-n", W(wi) - 0.03, 0.05, v - 0.4, v, "n", "none")
    ep.js(f'tl.to("#m5",{{x:{(k + 1) * 26},y:{-(k + 1) * 14},duration:0.25,ease:"power2.out"}},{W(wi):.3f});')
    ep.cue("whoosh-short.mp3", W(wi), 0.15)
for k in range(5):
    ep.js(f'tl.fromTo("#s05-p{k}",{{opacity:1,x:0,y:0}},{{opacity:0,x:80,y:-60,duration:0.6,ease:"power1.out",immediateRender:false}},{s + 0.15 + k * 0.42:.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S06 fluid leaks into your lungs, the cough gurgles
s, e = cut(48), cut(59)
ep.lungs("s06", s, e, t_flood=W(50) - 0.1, t_burn=W(51), t_burn_end=WE(53) + 0.4, flood_color="#5A78FF", burn_color="#1a2a6a", label_txt="FLUID IN THE LUNGS")
ep.cue("sizzle.wav", W(55), 0.25)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S07 then your brain begins to swell
s, e = cut(59), cut(65)
skull = glow(N("M 540 700 C 340 700 250 860 260 1020 C 270 1180 380 1290 540 1290 C 700 1290 810 1180 820 1020 C 830 860 740 700 540 700 Z", fill="none", sw=14, cw=5))
gyri = "".join(f'<path d="M {380 + k * 46} 820 Q {400 + k * 46} 920 {380 + k * 46} 1020 Q {360 + k * 46} 1120 {380 + k * 46} 1200" fill="none" stroke="#F2EEEA" stroke-width="4" opacity="0.6"/>' for k in range(8))
brain = brain_svg(540, 995, 410, 360, gid="s07-b")
svg = skull + brain + label(540, 1380, "BRAIN SWELLING", 32, "#FF6A5A")
ep.scene("s07", s, e, svg, origin="50% 52%")
ep.js(f'tl.to("#s07-b",{{scale:1.16,svgOrigin:"540 1000",duration:{e - W(61):.3f},ease:"power1.in"}},{W(61):.3f});')
ep.js(f'tl.to("#s07-b path:first-child",{{attr:{{fill:"#7a1418"}},duration:{e - W(61):.3f}}},{W(61):.3f});')
ep.shake("#s07-shake", e - 0.6, 0.6, 5)
ep.floor(s, 0.4, 0.2)

# ---------------------------------------------------------------- S08 you forget why you're here; voices that aren't there
s, e = cut(65), cut(76)
ghosts = "".join(f'<g class="s08-g" opacity="0">{mascot(f"g8{k}", x, 1500, 0.5, style="dim")}</g>' for k, x in enumerate([180, 900, 280, 820]))
marks = "".join(f'<text class="s08-q" x="{x}" y="{y}" fill="#9FC8FF" font-family="Roboto Condensed" font-weight="900" font-size="{sz}" text-anchor="middle" opacity="0">?</text>' for x, y, sz in [(430, 720, 90), (650, 780, 70), (540, 640, 110)])
svg = ghosts + climber("m8", 540, 1500, 0.75, pose=dict(uarmL=10, farmL=0, uarmR=-10, farmR=0, thighL=0, shinL=0)) + marks
ep.scene("s08", s, e, svg, origin="50% 55%", fx=[(s, e, "ash", SNOW)])
ep.js(f'tl.fromTo(".s08-q",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.2,stagger:0.15,immediateRender:false}},{W(66):.3f});')
ep.js(f'tl.fromTo(".s08-g",{{opacity:0}},{{opacity:0.55,duration:0.5,stagger:0.25,immediateRender:false}},{W(71):.3f});')
for k in range(int((e - s) / 0.6)):
    ep.rot("#m8-head", s + k * 0.6, 0.5, 14 if k % 2 else -14, "sine.inOut", about="0,-492")
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S09 the cold eats your fingers: white, then black
s, e = cut(76), cut(86)
fingers = ""
for k, (fx, top) in enumerate([(412, 700), (492, 660), (572, 672), (652, 730)]):
    fingers += f'<g class="s09-f"><path d="M {fx - 32} 1000 L {fx - 32} {top + 32} A 32 32 0 0 1 {fx + 32} {top + 32} L {fx + 32} 1000 Z" fill="#2a1a1a" stroke="#FB2945" stroke-width="12"/></g>'
thumb = '<g class="s09-f"><path d="M 380 1180 Q 300 1120 260 1020 A 34 34 0 0 1 318 990 Q 360 1080 420 1110 Z" fill="#2a1a1a" stroke="#FB2945" stroke-width="12"/></g>'
svg = f'<g filter="url(#glow)">{fingers}{thumb}' + N("M 372 990 L 700 990 Q 716 1180 680 1320 L 420 1320 Q 368 1200 372 990 Z", fill="#2a1a1a") + '</g>' + label(540, 1420, "FROSTBITE", 32, "#9FC8FF")
ep.scene("s09", s, e, svg, origin="50% 55%", fx=[(s, e, "ash", SNOW)])
ep.js(f'tl.to(".s09-f path",{{attr:{{fill:"#ECE6E5",stroke:"#9FC8FF"}},duration:0.4,stagger:0.08}},{W(82) - 0.1:.3f});')
ep.js(f'tl.to(".s09-f path",{{attr:{{fill:"#0a0808",stroke:"#3a3532"}},duration:0.4,stagger:0.08}},{W(85) - 0.1:.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S10 some climbers suddenly feel warm and take off their gloves
s, e = cut(86), cut(96)
P10 = dict(uarmL=30, farmL=-60, uarmR=-30, farmR=60, thighL=0, shinL=0)
gl_pos = [hand_pos(540, 1520, 0.78, P10, sd) for sd in ("L", "R")]
gloves = "".join(f'<g id="s10-gl{k}"><path d="M {gx - 30:.0f} {gy - 30:.0f} Q {gx - 34:.0f} {gy + 30:.0f} {gx:.0f} {gy + 34:.0f} Q {gx + 34:.0f} {gy + 30:.0f} {gx + 30:.0f} {gy - 30:.0f} Z" fill="#FB2945" stroke="#F2EEEA" stroke-width="5"/>'
                 f'<path d="M {gx + (-38 if k == 0 else 38):.0f} {gy - 6:.0f} q {(-14 if k == 0 else 14)} 10 0 24" fill="none" stroke="#F2EEEA" stroke-width="10" stroke-linecap="round"/></g>' for k, (gx, gy) in enumerate(gl_pos))
html = '<div class="num" id="s10-t" style="top:470px;left:540px;width:520px;font-size:130px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">−30°C</div><div class="lbl" id="s10-w" style="top:640px;left:540px;width:520px;color:#FF6A5A;">FEELS WARM</div>'
svg = f'<g id="s10-aura" opacity="0"><ellipse cx="540" cy="1150" rx="300" ry="440" fill="#FF6A3A" opacity="0.3" filter="url(#soft)"/></g>' + climber("m10", 540, 1520, 0.78, pose=P10) + gloves
ep.scene("s10", s, e, svg, html, origin="50% 55%", fx=[(s, e, "ash", SNOW)])
ep.show("#s10-aura", W(89), 0.5)
ep.pop("#s10-w", W(89), 0.2, 0.5)
for k in range(2):
    gx, gy = gl_pos[k]
    ep.js(f'tl.to("#s10-gl{k}",{{x:{-60 if k == 0 else 60},y:-30,duration:0.2,ease:"power2.out"}},{W(92) + k * 0.15:.3f});')
    ep.js(f'tl.to("#s10-gl{k}",{{y:420,rotation:{60 if k else -60},svgOrigin:"{gx:.0f} {gy:.0f}",duration:0.6,ease:"power2.in"}},{W(92) + k * 0.15 + 0.2:.3f});')
ep.floor(s, 0.0, 0.2)

# ---------------------------------------------------------------- S11 you just want to sit down in the snow, to rest
s, e = cut(96), cut(110)
drift = '<path id="s11-snow" d="M -40 1600 Q 200 1530 420 1570 Q 640 1520 860 1570 Q 1000 1540 1120 1600 L 1120 1980 L -40 1980 Z" fill="#cfd8ee" stroke="#E6EEFF" stroke-width="4"/>'
svg = ridge(1560) + climber("m11", 540, 1560, 0.75, pose=dict(uarmL=10, farmL=0, uarmR=-10, farmR=0, thighL=0, shinL=0)) + drift
ep.scene("s11", s, e, svg, origin="50% 65%", drift=0.025, fx=[(s, e, "ash", dict(SNOW, n=140))])
ep.js(f'tl.to("#m11",{{y:150,duration:0.8,ease:"power2.inOut"}},{W(100) - 0.1:.3f});')
ep.rot("#m11-thighL", W(100) - 0.1, 0.8, "rotate(14) scale(1,0.32)")
ep.js(f'tl.to("#m11-head",{{attr:{{transform:"rotate(22,0,-492)"}},duration:1.2,ease:"sine.inOut"}},{W(107):.3f});')
ep.js(f'tl.fromTo("#s11-snow",{{y:60}},{{y:-60,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S12 more than three hundred people have died; many are still up there
s, e = cut(110), cut(127)
r12 = random.Random(12)
RIDGE = [(120, 0), (300, -160), (460, -60), (640, -380), (760, -300), (900, -520), (1120, -140)]


def ridge_y(x, y=1500):
    for (xa, ya), (xb, yb) in zip(RIDGE, RIDGE[1:]):
        if xa <= x <= xb:
            return y + ya + (yb - ya) * (x - xa) / (xb - xa)
    return y


marks = ""
for k in range(60):
    x = r12.uniform(140, 1100)
    marks += f'<circle class="s12-m" cx="{x:.0f}" cy="{ridge_y(x) + r12.uniform(12, 60):.0f}" r="7" fill="#FF3B36" opacity="0"/>'
html = '<div class="num" id="s12-n" style="top:460px;font-size:180px;">0</div><div class="lbl" style="top:650px;">DEATHS ON EVEREST</div>'
ep.scene("s12", s, e, ridge(1500) + marks, html, origin="50% 55%", fx=[(s, e, "ash", SNOW)])
ep.counter("#s12-n", W(111), WE(119) - W(111), 0, 300, "n", "power2.out")
ep.js(f'tl.to(".s12-m",{{opacity:1,duration:0.1,stagger:0.05}},{W(111):.3f});')
ep.js(f'tl.to(".s12-m",{{attr:{{r:11}},duration:0.3,repeat:{int((e - W(120)) / 0.3)},yoyo:true}},{W(120):.3f});')
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(127), 130)
ep.write(red=["everest", "death", "oxygen", "heart", "lungs", "brain", "voices", "black", "warm", "rest", "mountain"])
