"""Episode 12 — How does it feel? When you fall into lava."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
ORANGE, OR_CORE = "#FF6A1A", "#FFE0A0"
ROCK = "#140808"
EMBERS = dict(n=60, x0=0, x1=1080, y0=500, y1=1700, sp=170)
HAND = ("M -70 120 L -70 0 Q -70 -20 -55 -24 L -55 -150 Q -55 -170 -38 -170 Q -22 -170 -22 -150 L -22 -40 L -12 -40 L -12 -185 Q -12 -205 5 -205 Q 22 -205 22 -185 "
        "L 22 -40 L 32 -40 L 32 -165 Q 32 -185 49 -185 Q 66 -185 66 -165 L 66 -30 L 76 -30 L 76 -120 Q 76 -140 92 -140 Q 108 -140 108 -120 L 108 40 Q 108 80 90 120 Z")


def lava(y, gid, seed=1, h=1300):
    r = random.Random(seed)
    grad = (f'<defs><linearGradient id="{gid}-lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB040"/><stop offset="0.12" stop-color="#FF5A14"/>'
            f'<stop offset="0.5" stop-color="#C21A06"/><stop offset="1" stop-color="#4A0702"/></linearGradient></defs>')
    crust = ""
    for k in range(22):
        cx, cy = r.uniform(-40, 1120), y + r.uniform(30, 520)
        rr = r.uniform(40, 110) * (0.6 + (cy - y) / 900)
        pts = " ".join(f"{cx + rr * math.cos(a) * r.uniform(0.7, 1.1):.0f},{cy + rr * 0.45 * math.sin(a) * r.uniform(0.7, 1.1):.0f}" for a in [i * math.pi / 3.5 for i in range(7)])
        crust += f'<polygon points="{pts}" fill="#2a0a04" stroke="#FF8A3A" stroke-width="3" opacity="0.85"/>'
    top = f"M -100 {y} " + " ".join(f"Q {-100 + i * 160 + 80} {y + (-10 if i % 2 else 10)} {-100 + (i + 1) * 160} {y}" for i in range(9))
    edge = f'<path d="{top}" fill="none" stroke="{ORANGE}" stroke-width="12"/><path d="{top}" fill="none" stroke="{OR_CORE}" stroke-width="4"/>'
    return (grad + f'<g id="{gid}"><rect x="-100" y="{y}" width="1280" height="{h}" fill="url(#{gid}-lg)"/>'
            f'<g class="{gid}-cr">{crust}</g><g filter="url(#glowO)">{edge}</g></g>')


def crater(y_rim=820, y_lava=1300):
    L = f"M -120 {y_rim - 40} L 180 {y_rim} L 260 {y_rim + 120} L 230 {y_lava - 140} L 300 {y_lava + 40} L -120 {y_lava + 40} Z"
    R = f"M 1200 {y_rim - 120} L 900 {y_rim - 60} L 830 {y_rim + 100} L 870 {y_lava - 160} L 780 {y_lava + 40} L 1200 {y_lava + 40} Z"
    return glow(N(L, fill=ROCK, sw=12, cw=4)) + glow(N(R, fill=ROCK, sw=12, cw=4))


def heat_waves(gid, x0=200, x1=880, y0=700, y1=1250, n=5):
    out = ""
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        d = f"M {x:.0f} {y1} " + " ".join(f"Q {x + (24 if i % 2 == 0 else -24):.0f} {y1 - (i + 0.5) * 70} {x:.0f} {y1 - (i + 1) * 70}" for i in range(int((y1 - y0) / 70)))
        out += f'<path class="{gid}" d="{d}" fill="none" stroke="#FF8A3A" stroke-width="5" opacity="0.55" filter="url(#glowO)"/>'
    return out


def lying(mid, x_feet, y_axis, s, pose=None, style="neon"):
    p = dict(uarmL=0, farmL=0, uarmR=0, farmR=0)
    p.update(pose or {})
    return f'<g id="{mid}-w"><g transform="translate({x_feet},{y_axis}) rotate(90)">{mascot(mid, 0, 0, s, pose=p, style=style)}</g></g>'


def bigx(gid, x, y, r=70, w=16):
    return f'<g id="{gid}" filter="url(#glow)">' + line(x - r, y - r, x + r, y + r, "#FF3B36", w) + line(x + r, y - r, x - r, y + r, "#FF3B36", w) + '</g>'


FLAIL = dict(uarmL=150, farmL=30, uarmR=-150, farmR=-30, thighL=20, shinL=-30, thighR=-10, shinR=20)

# ---------------------------------------------------------------- S01 cold open: falling toward the lava, close → pull out
s, e = 0.0, cut(9)
svg = crater(820, 1340) + lava(1340, "l1", 1) + f'<g id="s01-m">{mascot("m1", 540, 1000, 0.62, pose=FLAIL, mouth_open=True)}</g>'
ep.scene("s01", s, e, svg, origin="50% 45%", custom_cam=True, fx=[(s, e, "embers", EMBERS),
                                                                  (s, e, "fire", dict(cx=540, base=1360, w=900, h=150, n=12, amp=0.8, sp=6, nofade=True))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.0}},{{scale:2.1,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#s01-m",{{y:-120}},{{y:150,duration:{e:.3f},ease:"power1.in",immediateRender:false}},0);')
r1 = random.Random(1)
for k in range(int(e / 0.2)):
    ep.rot("#m1-uarmL", k * 0.2, 0.2, 150 + r1.uniform(-25, 25), "sine.inOut")
    ep.rot("#m1-uarmR", k * 0.2, 0.2, -150 + r1.uniform(-25, 25), "sine.inOut")
ep.floor(0, 0.4, 1.0, 0.01)
ep.cue("lava_bubble.mp3", 0, 0.8)
ep.cue("whoosh-cinematic.mp3", 0, 0.5)
ep.cue("sub.wav", 0, 0.6)

# ---------------------------------------------------------------- S02 you slip at the edge of the crater
s, e = cut(9), cut(17)
svg = crater(820, 1340) + lava(1340, "l2", 2) + f'<g id="s02-m">{mascot("m2", 150, 820, 0.42)}</g>'
ep.scene("s02", s, e, svg, origin="30% 50%", fx=[(s, e, "embers", EMBERS),
                                                 (W(10), W(10) + 2.5, "stones", dict(n=8, x0=220, x1=320, sp=500, fill="#2a1a12", stroke="#FF6A1A"))])
ts = W(10) - 0.05
ep.js(f'tl.to("#s02-m",{{rotation:-35,svgOrigin:"190 820",duration:0.25,ease:"power2.in"}},{ts:.3f});')
ep.js(f'tl.to("#s02-m",{{x:190,y:420,rotation:-160,svgOrigin:"190 820",duration:{e - ts - 0.25:.3f},ease:"power2.in"}},{ts + 0.25:.3f});')
ep.cue("rock_scrape.mp3", ts, 0.7)
ep.cue("whoosh-cinematic.mp3", ts + 0.25, 0.6)
ep.floor(s, 0.4, 0.8)

# ---------------------------------------------------------------- S03 below you, a lake of molten rock
s, e = cut(17), cut(24)
bubbles = "".join(f'<circle class="s03-b" cx="{x}" cy="{y}" r="22" fill="#FFB040" stroke="{OR_CORE}" stroke-width="4" opacity="0"/>' for x, y in ((220, 1060), (520, 1200), (800, 1120), (380, 1420), (700, 1520), (920, 1350), (160, 1600)))
svg = lava(900, "l3", 3, 1200) + bubbles
ep.scene("s03", s, e, svg, origin="50% 60%", fx=[(s, e, "embers", dict(EMBERS, y0=600)),
                                                 (s, e, "smoke", dict(n=10, cx=540, base=980, w=900, h=500, r0=80, r1=220, life=3, alpha=0.25, rgb="120,60,40"))])
ep.js(f'tl.fromTo(".l3-cr",{{x:0}},{{x:-60,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo(".s03-b",{{scale:0,opacity:1,transformOrigin:"50% 50%"}},{{scale:1.6,opacity:0,duration:0.6,stagger:{{each:0.35,repeat:{int((e - s) / 2.5)}}},ease:"power2.out",immediateRender:false}},{s + 0.1:.3f});')
ep.cue("lava_bubble.mp3", s, 0.8)
ep.floor(s, 0.4, 1.0)

# ---------------------------------------------------------------- S04 twelve hundred degrees Celsius
s, e = cut(24), cut(28)
ep.thermometer("s04", s, e, W(24) - 0.1, WE(27), 20, 1200, top=1400, label_txt="CELSIUS")

# ---------------------------------------------------------------- S05 in the movies you sink — in reality, you don't
s, e = cut(28), cut(37)
clipL = '<defs><clipPath id="s05-cl"><rect x="0" y="300" width="536" height="1003"/></clipPath><clipPath id="s05-cr"><rect x="544" y="300" width="536" height="1003"/></clipPath></defs>'
left = (f'<g clip-path="url(#s05-cl)"><g id="s05-ml">{mascot("m5a", 270, 1300, 0.42, pose=dict(uarmL=160, uarmR=-160))}</g></g>')
right = (f'<g id="s05-rp"><g clip-path="url(#s05-cr)"><g id="s05-mr">{lying("m5b", 680, 1268, 0.38)}</g></g></g>')
svg = (clipL + lava(1300, "l5", 5) + left + right + f'<rect x="536" y="560" width="8" height="1400" fill="#010101"/>'
       + label(270, 700, "MOVIES", 40, GREY) + f'<g id="s05-rl">' + label(810, 700, "REALITY", 40, "#FFE0A0") + '</g>'
       + bigx("s05-x", 270, 980, 60, 12))
ep.scene("s05", s, e, svg, origin="50% 60%", fx=[(s, e, "embers", dict(EMBERS, y0=700))])
ep.js(f'tl.fromTo("#s05-ml",{{y:-200}},{{y:420,duration:{W(33) - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.show("#s05-rp", W(33) - 0.1, 0.2)
ep.show("#s05-rl", W(33) - 0.1, 0.2)
ep.js(f'tl.fromTo("#s05-mr",{{y:-500}},{{y:0,duration:0.4,ease:"power3.in",immediateRender:false}},{W(35) - 0.3:.3f});')
ep.js(f'tl.to("#s05-mr",{{y:-26,duration:0.18,ease:"power2.out",yoyo:true,repeat:1}},{W(35) + 0.1:.3f});')
ep.pop("#s05-x", W(34) - 0.05, 0.18, 1.6, "power3.out")
ep.cue("impact-bass-2.mp3", W(35) + 0.1, 0.7)
ep.floor(s, 0.3, 0.6)

# ---------------------------------------------------------------- S06 lava is three times denser than your body
s, e = cut(37), cut(45)
col = lambda x, h, gid, fill, stroke: f'<rect id="{gid}" x="{x}" y="{1450 - h}" width="200" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="6"/>'
svg = (glow(col(220, 690, "s06-a", "#C21A06", "#FFB040"), f="glowO") + glow(col(660, 230, "s06-b", "#2a0a0c", RED))
       + hline(1450, 140, 940, 8, 3) + label(320, 1520, "LAVA", 34, "#FFB040") + label(760, 1520, "YOU", 34, GREY)
       + label(320, 1590, "2.7 G/CM³", 26, GREY) + label(760, 1590, "1.0 G/CM³", 26, GREY))
html = '<div class="num" id="s06-n" style="top:560px;left:540px;width:440px;font-size:180px;">3×</div>'
ep.scene("s06", s, e, svg, html, origin="50% 60%")
ep.js(f'tl.fromTo("#s06-a, #s06-b",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:0.5,stagger:0.15,ease:"power3.out",immediateRender:false}},{s + 0.05:.3f});')
ep.pop("#s06-n", W(39) - 0.05, 0.22, 1.5, "power3.out")
ep.cue("impact-bass-2.mp3", W(39) - 0.05, 0.6)
ep.floor(s, 0.3, 0.5)

# ---------------------------------------------------------------- S07 you land on top of it, like a mattress of fire
s, e = cut(45), cut(56)
svg = lava(1300, "l7", 7) + lying("m7", 290, 1262, 0.75, pose=dict(uarmL=30, uarmR=-30, thighL=8, thighR=-8))
ep.scene("s07", s, e, svg, origin="50% 65%", fx=[(s, e, "embers", EMBERS),
                                                 (W(46), W(46) + 0.7, "sparks", dict(cx=540, cy=1290, n=50, r=420, dur=0.7, color="#FFB040", g=500)),
                                                 (W(53) - 0.2, e, "fire", dict(cx=540, base=1305, w=820, h=260, n=12, amp=1.0, sp=7, grow=0.6))])
ep.js(f'tl.fromTo("#m7-w",{{y:-900}},{{y:0,duration:0.45,ease:"power3.in",immediateRender:false}},{W(46) - 0.4:.3f});')
ep.js(f'tl.to("#m7-w",{{y:-30,duration:0.2,ease:"power2.out",yoyo:true,repeat:1}},{W(46) + 0.05:.3f});')
ep.shake("#s07-shake", W(46) + 0.05, 0.5, 18)
ep.cue("impact-bass-1.mp3", W(46) + 0.05, 1.0)
ep.cue("sizzle.wav", W(46) + 0.1, 0.8)
ep.cue("fire_ignite.mp3", W(53) - 0.2, 0.9)
ep.floor(s, 0.4, 1.0)

# ---------------------------------------------------------------- S08 before you even touch it, the heat sets your clothes on fire
s, e = cut(56), cut(68)
svg = lava(1440, "l8", 8) + heat_waves("s08-hw", 160, 920, 700, 1420, 6) + f'<g id="s08-m">{mascot("m8", 540, 1250, 0.6, pose=FLAIL, mouth_open=True)}</g>'
html = '<div class="num" id="s08-n" style="top:600px;left:640px;width:420px;font-size:90px;color:#FFB040;">40°</div><div class="lbl" style="top:700px;left:640px;width:420px;font-size:30px;">AIR AT YOUR SKIN</div>'
ep.scene("s08", s, e, svg, html, origin="50% 60%", fx=[(s, e, "embers", EMBERS),
                                                       (W(63) - 0.1, e, "fire", dict(cx=540, base=1260, w=230, h=420, n=7, amp=1.0, sp=8, grow=0.5))])
ep.js(f'tl.fromTo(".s08-hw",{{y:0}},{{y:-140,duration:0.9,repeat:{int((e - s) / 0.9)},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo("#s08-m",{{y:-260}},{{y:0,duration:{e - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.counter("#s08-n", W(61) - 0.1, W(64) - W(61), 40, 400, "deg", "power2.in")
ep.js(f'tl.to("#m8 path, #m8 line",{{attr:{{stroke:"#FFB040"}},duration:0.4}},{W(63):.3f});')
ep.cue("fire_ignite.mp3", W(63) - 0.15, 1.0)
ep.cue("riser.mp3", W(59), 0.4)
ep.floor(s, 0.4, 1.0)

# ---------------------------------------------------------------- S09 the gas burns your throat — sulfur — every breath is acid
s, e = cut(68), cut(78)
ep.lungs("s09", s, e, t_breath=W(69), t_flood=W(69), t_burn=W(70), t_burn_end=W(77), flood_color="#E8D040", burn_color="#5a4a0a", label_txt="LUNGS")
ep.scenes[-1]["html"] += '<div class="num" id="s09-so" style="top:1450px;font-size:120px;color:#E8D040;text-shadow:0 0 18px rgba(232,208,64,.8);">SO₂</div><div class="lbl" id="s09-sl" style="top:1580px;font-size:30px;">SULFUR DIOXIDE</div>'
ep.pop("#s09-so", W(73) - 0.05, 0.2, 1.5, "power3.out")
ep.show("#s09-sl", W(73) - 0.05, 0.2)
ep.cue("steam_hiss.mp3", W(69), 0.5)
ep.floor(s, 0.35, 0.5)

# ---------------------------------------------------------------- S10 the water in your body flashes into steam
s, e = cut(78), cut(86)
r10 = random.Random(10)
drops = "".join(f'<circle class="s10-d" cx="{540 + r10.uniform(-70, 70):.0f}" cy="{r10.uniform(820, 1420):.0f}" r="{r10.uniform(8, 14):.0f}" fill="#5A78FF" filter="url(#glowB)"/>' for _ in range(34))
html = '<div class="num" id="s10-n" style="top:560px;left:620px;width:440px;font-size:120px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">60%</div><div class="lbl" style="top:690px;left:620px;width:440px;font-size:30px;">OF YOU IS WATER</div>'
svg = mascot("m10", 540, 1600, 1.1, style="xray") + drops
ep.scene("s10", s, e, svg, html, origin="50% 55%", fx=[(W(83) - 0.1, e, "smoke", dict(n=22, cx=540, base=1350, w=300, h=900, r0=50, r1=200, life=1.6, alpha=0.5, rgb="235,235,240"))])
ep.js(f'tl.fromTo(".s10-d",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:0.15,stagger:0.03,immediateRender:false}},{s + 0.05:.3f});')
ep.js(f'tl.to(".s10-d",{{y:-260,opacity:0,scale:2.2,transformOrigin:"50% 50%",duration:0.5,stagger:{{each:0.02,from:"random"}},ease:"power2.in"}},{W(83) - 0.1:.3f});')
ep.counter("#s10-n", W(83), e - W(83), 60, 0, "pct", "power2.in")
ep.cue("steam_hiss.mp3", W(83) - 0.1, 1.0)
ep.floor(s, 0.3, 0.6)

# ---------------------------------------------------------------- S11 your skin blisters, then blackens
s, e = cut(86), cut(91)
r11 = random.Random(11)
blisters = "".join(f'<circle class="s11-b" cx="{r11.uniform(140, 940):.0f}" cy="{r11.uniform(830, 1240):.0f}" r="{r11.uniform(18, 44):.0f}" fill="#E8B0A0" stroke="#FFE0D0" stroke-width="4" opacity="0.9"/>' for _ in range(22))
skin = glow(N("M 100 800 L 980 800 L 980 1280 L 100 1280 Z", fill="#8a3a2a", sw=12, cw=4), gid="s11-skin")
svg = f'<g id="s11-all">{skin}{blisters}</g>' + label(540, 1360, "SKIN", 34, GREY)
ep.scene("s11", s, e, svg, origin="50% 55%", fx=[(W(89), e, "embers", dict(EMBERS, y0=800, y1=1300))])
ep.js(f'tl.fromTo(".s11-b",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:0.18,stagger:{{each:0.04,from:"random"}},ease:"back.out(3)",immediateRender:false}},{W(87):.3f});')
ep.js('gsap.set(".s11-b",{scale:0,transformOrigin:"50% 50%"});')
ep.js(f'tl.to("#s11-skin path:first-child, .s11-b",{{attr:{{fill:"#120806"}},duration:0.6}},{W(90) - 0.1:.3f});')
ep.js(f'tl.to(".s11-b",{{attr:{{stroke:"#3a2a22"}},duration:0.6}},{W(90) - 0.1:.3f});')
ep.cue("sizzle.wav", W(87), 0.8)
ep.floor(s, 0.4, 1.0)

# ---------------------------------------------------------------- S12 push yourself up — your hands sink in, just a little — and stick
s, e = cut(91), cut(106)
hand = f'<g id="s12-h"><g transform="translate(540,1160) scale(1.5,-1.5)">' + glow(N(HAND, fill="#2a0a0c", sw=12, cw=4)) + '</g></g>'
svg = hand + lava(1300, "l12", 12, 700)
ep.scene("s12", s, e, svg, origin="50% 65%", fx=[(s, e, "embers", dict(EMBERS, y0=800)),
                                                 (W(99), e, "smoke", dict(n=12, cx=540, base=1300, w=300, h=500, r0=40, r1=140, life=1.8, alpha=0.35))])
ep.js(f'gsap.set("#s12-h",{{y:-560}});')
ep.js(f'tl.to("#s12-h",{{y:-180,duration:{W(99) - s - 0.2:.3f},ease:"power2.in"}},{s + 0.2:.3f});')
ep.js(f'tl.to("#s12-h",{{y:-95,duration:{W(103) - W(99):.3f},ease:"power2.out"}},{W(99) - 0.05:.3f});')
for k in range(4):
    ep.js(f'tl.to("#s12-h",{{y:{-125 if k % 2 == 0 else -95},duration:0.12,ease:"power2.inOut"}},{W(105) - 0.05 + k * 0.12:.3f});')
ep.shake("#s12-shake", W(105) - 0.05, 0.4, 10)
ep.js(f'tl.to("#s12-h path",{{attr:{{stroke:"#FFB040"}},duration:0.5}},{W(99):.3f});')
ep.cue("sizzle.wav", W(99), 0.8)
ep.cue("impact-bass-2.mp3", W(105) - 0.05, 0.7)
ep.floor(s, 0.4, 1.0)

# ---------------------------------------------------------------- S13 you can't swim in it — you can't climb out of it
s, e = cut(106), cut(117)
swim = label(260, 760, "SWIM", 36, GREY) + glow(N("M 180 900 Q 220 860 260 900 Q 300 940 340 900", fill="none", red="#FF8A3A", core=OR_CORE, sw=10, cw=3), f="glowO")
climb = label(820, 760, "CLIMB", 36, GREY) + glow(N("M 820 960 L 820 840 M 780 880 L 820 840 L 860 880", fill="none", red="#FF8A3A", core=OR_CORE, sw=10, cw=3), f="glowO")
svg = lava(1300, "l13", 13) + lying("m13", 310, 1262, 0.65, pose=dict(uarmL=120, farmL=20, uarmR=-60)) + swim + climb + bigx("s13-x1", 260, 880) + bigx("s13-x2", 820, 900)
ep.scene("s13", s, e, svg, origin="50% 60%", fx=[(s, e, "embers", EMBERS),
                                                 (s, e, "fire", dict(cx=540, base=1305, w=760, h=200, n=11, amp=0.9, sp=7, nofade=True))])
for k in range(int((e - s) / 0.3)):
    ep.rot("#m13-uarmL", s + k * 0.3, 0.3, 120 + (30 if k % 2 else -30), "sine.inOut")
ep.pop("#s13-x1", W(108) - 0.05, 0.18, 1.6, "power3.out")
ep.pop("#s13-x2", W(113) - 0.05, 0.18, 1.6, "power3.out")
ep.cue("impact-bass-2.mp3", W(108) - 0.05, 0.6)
ep.cue("impact-bass-2.mp3", W(113) - 0.05, 0.7)
ep.cue("lava_bubble.mp3", s, 0.6)
ep.floor(s, 0.4, 1.0)

# ---------------------------------------------------------------- S14 within seconds, you stop feeling anything
s, e = cut(117), cut(123)
bar = (f'<rect x="190" y="1080" width="700" height="70" fill="#1a1416" stroke="#F2EEEA" stroke-width="3"/>'
       f'<rect id="s14-bar" x="190" y="1080" width="700" height="70" fill="#FB2945" filter="url(#glow)"/>' + label(540, 1040, "PAIN SIGNALS", 34, GREY))
nerves = "".join(f'<path class="s14-nv" d="M 540 820 Q {540 + dx} {880 + abs(dx) * 0.3} {540 + dx * 1.6} 960" fill="none" stroke="#FF6A6A" stroke-width="5" filter="url(#glowS)"/>' for dx in (-220, -120, -40, 40, 120, 220))
svg = brain(540, 700, 360, 300, gid="s14-br", seed=14) + nerves + bar
ep.scene("s14", s, e, svg, origin="50% 55%")
ep.js(f'tl.to("#s14-bar",{{scaleX:0,transformOrigin:"0% 50%",duration:{WE(122) - W(119):.3f},ease:"power2.in"}},{W(119) - 0.1:.3f});')
ep.js(f'tl.to(".s14-nv",{{opacity:0.08,duration:{WE(122) - W(119):.3f},stagger:0.08,ease:"power2.in"}},{W(119):.3f});')
ep.js(f'tl.to("#s14-br",{{opacity:0.4,duration:{e - W(120):.3f}}},{W(120):.3f});')
ep.floor(s, 0.35, 0.3)
ep.floor(W(120), 0.2, 0.0, 1.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(123), 126)
ep.write(red=["lava", "slip", "molten", "sink", "don't", "denser", "fire", "heat", "throat", "sulfur", "acid", "steam", "blackens", "stick", "swim", "climb", "anything"])
