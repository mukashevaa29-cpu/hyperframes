"""Episode 05 — How does it feel? When you're thrown into space without a suit."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
BLUE, BLUE_CORE = "#5A78FF", "#E6EEFF"


def space(seed=1, earth=True, n=140):
    r = random.Random(seed)
    stars = "".join(f'<circle cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(380, 1920):.0f}" r="{r.choice([1.5, 2, 2.5, 3.5])}" fill="#F2EEEA" opacity="{r.uniform(0.3, 1):.2f}"/>' for _ in range(n))
    e = ""
    if earth:
        e = ('<g filter="url(#glowB)"><circle cx="540" cy="2700" r="1200" fill="#07102a" stroke="#5A78FF" stroke-width="10"/></g>'
             '<circle cx="540" cy="2700" r="1185" fill="none" stroke="#9FC8FF" stroke-width="3" opacity="0.6"/>'
             '<path d="M 120 1640 Q 300 1560 420 1600 T 700 1560 T 980 1600" fill="none" stroke="#2a4a9a" stroke-width="5" opacity="0.6"/>')
    return stars + e


def floating(mid, x, y, s, mouth=False, style="neon"):
    return mascot(mid, x, y, s, style=style, mouth_open=mouth, pose=dict(uarmL=60, farmL=30, uarmR=-70, farmR=-20, thighL=20, shinL=-30, thighR=-15, shinR=40, head=-8))


def lungs_shape(sid, fill=DARK):
    LL = "M 515 790 C 430 770 310 900 296 1150 C 284 1360 336 1440 430 1420 C 505 1404 515 1320 515 1150 Z"
    RL = "M 565 790 C 650 770 770 900 784 1150 C 796 1360 744 1440 650 1420 C 575 1404 565 1320 565 1150 Z"
    return (f'<g id="{sid}"><g filter="url(#glow)">'
            f'<path class="{sid}-l" d="{LL}" fill="{fill}" stroke="{RED}" stroke-width="16"/><path d="{LL}" fill="none" stroke="{CORE}" stroke-width="5"/>'
            f'<path class="{sid}-l" d="{RL}" fill="{fill}" stroke="{RED}" stroke-width="16"/><path d="{RL}" fill="none" stroke="{CORE}" stroke-width="5"/>'
            + line(540, 470, 540, 770, RED, 56) + line(540, 470, 540, 770, DARK, 40) + '</g></g>')


def bubbles(prefix, cx, cy, n=12, spread=150, seed=5):
    r = random.Random(seed)
    return "".join(f'<circle id="{prefix}{k}" cx="{cx + r.uniform(-spread, spread):.0f}" cy="{cy + r.uniform(-20, 20):.0f}" r="{r.uniform(8, 20):.0f}" '
                   f'fill="none" stroke="#E6EEFF" stroke-width="4" opacity="0"/>' for k in range(n))


def boil(prefix, t0, t1, n=12, rise=160, seed=6):
    r = random.Random(seed)
    for k in range(n):
        st = t0 + r.uniform(0, max(0.1, t1 - t0 - 0.6))
        ep.js(f'tl.fromTo("#{prefix}{k}",{{opacity:1,scale:0.2,y:0,transformOrigin:"50% 50%"}},{{opacity:0,scale:1.4,y:{-r.uniform(rise * 0.5, rise):.0f},duration:{r.uniform(0.5, 0.9):.2f},ease:"power1.out",immediateRender:false}},{st:.3f});')
    ep.js(f'tl.set("[id^={prefix}]",{{opacity:0}},0);')


# ---------------------------------------------------------------- S01 cold open: floating in space, face first → pull out
s, e = 0.0, cut(12)
hatch = glow(N("M 80 520 L 380 520 L 380 900 L 80 900 Z", fill="#0b1430", red=BLUE, core=BLUE_CORE), f="glowB") + '<rect x="110" y="550" width="240" height="320" fill="#000" stroke="#9FC8FF" stroke-width="3"/>'
svg = space(1) + hatch + f'<g id="s01-m">{floating("m1", 600, 1500, 0.95, mouth=True)}</g>' + bubbles("s01-b", 600, 980, 10, 40, 1)
ep.scene("s01", s, e, svg, origin="56% 51%", custom_cam=True)
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.6}},{{scale:2.7,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#s01-m",{{rotation:-6,svgOrigin:"600 1200"}},{{rotation:14,svgOrigin:"600 1200",duration:{e:.3f},ease:"sine.inOut"}},0);')
boil("s01-b", 0.0, e, 10, 120, 1)
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("sfx_open_roar.mp3", 0, 0.35)
ep.cue("sub.wav", 0, 0.7)

# ---------------------------------------------------------------- S02 hold your breath. Don't.
s, e = cut(12), cut(21)
svg = lungs_shape("s02-lg") + "".join(f'<circle class="s02-air" cx="{r_[0]}" cy="{r_[1]}" r="10" fill="#FFFFFF"/>' for r_ in [(420, 1000), (460, 1150), (400, 1250), (640, 1000), (620, 1160), (680, 1260), (540, 900)])
xmark = ('<path id="s02-x1" d="M 200 760 L 880 1460" stroke="#FF3B36" stroke-width="26" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="1000" filter="url(#glow)"/>'
         '<path id="s02-x2" d="M 880 760 L 200 1460" stroke="#FF3B36" stroke-width="26" stroke-linecap="round" stroke-dasharray="1000" stroke-dashoffset="1000" filter="url(#glow)"/>')
ep.scene("s02", s, e, svg + xmark + label(540, 1560, "HOLDING YOUR BREATH", 30, GREY), origin="50% 55%")
ep.js(f'tl.fromTo("#s02-lg",{{scale:1}},{{scale:1.1,transformOrigin:"50% 40%",duration:0.6,ease:"power2.out",immediateRender:false}},{W(17) - 0.1:.3f});')
ep.js(f'tl.to("#s02-x1",{{strokeDashoffset:0,duration:0.14,ease:"power2.out"}},{W(20) - 0.05:.3f});')
ep.js(f'tl.to("#s02-x2",{{strokeDashoffset:0,duration:0.14,ease:"power2.out"}},{W(20) + 0.1:.3f});')
ep.cue("impact-bass-2.mp3", W(20) - 0.05, 0.7)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S03 the air would tear your lungs apart
s, e = cut(21), cut(31)
cracks = '<path id="s03-cr" d="M 400 950 L 440 1020 L 410 1090 L 460 1160 M 680 960 L 640 1040 L 690 1110 L 650 1200" fill="none" stroke="#FFF1DC" stroke-width="7" stroke-dasharray="600" stroke-dashoffset="600" filter="url(#glowO)"/>'
gauge = label(540, 600, "PRESSURE INSIDE", 30, GREY)
svg = lungs_shape("s03-lg") + cracks + gauge
ep.scene("s03", s, e, svg, origin="50% 55%")
ep.js(f'tl.fromTo("#s03-lg",{{scale:1.1}},{{scale:1.32,transformOrigin:"50% 40%",duration:{W(28) - s:.3f},ease:"power2.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s03-cr",{{strokeDashoffset:0,duration:0.2,ease:"power2.out"}},{W(28) - 0.05:.3f});')
ep.js(f'tl.to(".s03-lg-l",{{fill:"#5a0d0a",duration:0.3}},{W(28):.3f});')
ep.shake("#s03-shake", W(28), 0.4, 14)
ep.cue("impact-bass-1.mp3", W(28), 0.7)
ep.floor(s, 0.5, 0.3)

# ---------------------------------------------------------------- S04 so you let it out, all of it, in one rush
s, e = cut(31), cut(42)
streams = "".join(f'<circle id="s04-a{k}" cx="540" cy="760" r="{random.Random(k).uniform(6, 12):.0f}" fill="#FFFFFF" opacity="0"/>' for k in range(30))
svg = space(4, earth=False, n=70) + lungs_shape("s04-lg") + streams
ep.scene("s04", s, e, svg, origin="50% 50%")
tr = W(33) - 0.05
ep.js(f'tl.fromTo("#s04-lg",{{scale:1.15}},{{scale:0.92,transformOrigin:"50% 40%",duration:0.9,ease:"power3.out",immediateRender:false}},{tr:.3f});')
rr = random.Random(4)
for k in range(30):
    ep.js(f'tl.fromTo("#s04-a{k}",{{attr:{{cx:540,cy:{rr.uniform(800, 1300):.0f}}},opacity:1}},{{keyframes:[{{attr:{{cx:540,cy:470}},duration:0.25,ease:"power1.in"}},{{attr:{{cx:{rr.uniform(-100, 1180):.0f},cy:{rr.uniform(-200, 300):.0f}}},opacity:0,duration:0.5,ease:"power2.out"}}],immediateRender:false}},{tr + k * 0.03:.3f});')
    ep.js(f'tl.set("#s04-a{k}",{{opacity:0}},0);')
ep.cue("whoosh-cinematic.mp3", tr, 0.7)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S05 three seconds
s, e = cut(42), cut(44)
ep.timer("s05", s, e, s + 0.05, WE(43), 0, 3, "ms", "SECONDS", 3 / 60, ring_color=BLUE)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S06 the water on your tongue starts to boil
s, e = cut(44), cut(52)
mouth = glow(N("M 220 900 Q 540 760 860 900 Q 900 1060 760 1180 Q 540 1290 320 1180 Q 180 1060 220 900 Z", fill="#120607"))
tongue = glow(N("M 330 1080 Q 540 980 750 1080 Q 760 1170 640 1200 Q 540 1215 440 1200 Q 320 1170 330 1080 Z", fill="#8a1c22", red="#FF6A7A", core="#FFD0D8", sw=10, cw=3))
teeth = "".join(f'<rect x="{300 + k * 62}" y="905" width="46" height="46" rx="8" fill="#ECE6E5"/>' for k in range(8))
svg = mouth + teeth + tongue + bubbles("s06-b", 540, 1090, 18, 170, 6) + label(540, 1320, "SALIVA BOILING", 30, "#9FC8FF")
ep.scene("s06", s, e, svg, origin="50% 55%", drift=0.025)
boil("s06-b", W(49) - 0.1, e, 18, 180, 6)
ep.cue("sizzle.wav", W(49), 0.35)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S07 your skin swells, but it holds you together
s, e = cut(52), cut(60)
svg = space(7, n=90) + f'<g id="s07-m">{floating("m7", 540, 1520, 1.05)}</g>' + f'<g id="s07-skin" opacity="0"><ellipse cx="540" cy="1100" rx="300" ry="520" fill="none" stroke="#9FC8FF" stroke-width="5" stroke-dasharray="20 14" filter="url(#glowB)"/></g>'
ep.scene("s07", s, e, svg, origin="50% 55%")
ep.js(f'tl.to("#s07-m",{{scale:1.16,svgOrigin:"540 1150",duration:1.2,ease:"power2.out"}},{W(54) - 0.1:.3f});')
ep.show("#s07-skin", W(57) - 0.05, 0.3)
ep.cue("riser.mp3", W(54) - 0.3, 0.3)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S08 your blood doesn't boil — your heart keeps it under pressure
s, e = cut(60), cut(70)
vessel = glow(N("M -40 1000 L 1120 1000 L 1120 1200 L -40 1200 Z", fill="#1a0507", sw=12, cw=4))
cells = "".join(f'<g class="s08-c"><ellipse cx="{-80 + k * 120}" cy="{1100 + (k % 3 - 1) * 40}" rx="40" ry="22" fill="#C2181E" stroke="#FF6A6A" stroke-width="4"/></g>' for k in range(12))
HEART = "M 540 860 C 440 790 390 730 410 670 C 430 610 510 610 540 670 C 570 610 650 610 670 670 C 690 730 640 790 540 860 Z"
svg = vessel + f'<defs><clipPath id="s08-cp"><rect x="-40" y="1006" width="1160" height="188"/></clipPath></defs><g clip-path="url(#s08-cp)"><g id="s08-flow">{cells}</g></g>' + glow(N(HEART, fill="#3a0a0c"), gid="s08-heart") + label(540, 1290, "BLOOD STAYS LIQUID", 32, "#FF6A6A")
ep.scene("s08", s, e, svg, origin="50% 55%")
ep.js(f'tl.fromTo("#s08-flow",{{x:0}},{{x:240,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
t = s
while t < e - 0.1:
    ep.js(f'tl.fromTo("#s08-heart",{{scale:1.12,svgOrigin:"540 760"}},{{scale:1,duration:0.3,ease:"power2.out",immediateRender:false}},{t:.3f});')
    ep.cue("heart.wav", t, 0.4)
    t += 0.8
ep.floor(s, 0.45, 0.0)

# ---------------------------------------------------------------- S09 no oxygen left to send to your brain
s, e = cut(70), cut(80)
gyri = "".join(f'<path d="M {360 + k * 52} 840 Q {380 + k * 52} 920 {360 + k * 52} 1000 Q {340 + k * 52} 1080 {360 + k * 52} 1160" fill="none" stroke="#F2EEEA" stroke-width="4" opacity="0.6"/>' for k in range(8))
brain = glow(N("M 540 800 C 380 780 300 880 310 1000 C 320 1140 420 1220 540 1210 C 660 1220 760 1140 770 1000 C 780 880 700 780 540 800 Z", fill="#3a0a0c") + gyri, gid="s09-brain")
o2 = ""
for k in range(8):
    a = k * math.pi / 4
    x, y = 540 + 330 * math.cos(a), 1000 + 300 * math.sin(a)
    o2 += f'<g id="s09-o{k}"><circle cx="{x:.0f}" cy="{y:.0f}" r="36" fill="{BLUE}" filter="url(#glowB)"/>' + label(round(x), round(y) + 12, "O₂", 30, "#FFFFFF") + '</g>'
svg = brain + o2
ep.scene("s09", s, e, svg, origin="50% 52%")
for k in range(8):
    t = W(72) + k * (W(79) - W(72)) / 8
    ep.js(f'tl.to("#s09-o{k}",{{opacity:0,scale:0.2,transformOrigin:"50% 50%",duration:0.25,ease:"power2.in"}},{t:.3f});')
ep.js(f'tl.to("#s09-brain path",{{attr:{{stroke:"#555"}},duration:{e - W(72):.3f}}},{W(72):.3f});')
ep.floor(s, 0.45, 0.0)


# ---------------------------------------------------------------- S10/S11 ten seconds: vision narrows · fifteen seconds: black out (POV)
def pov(sid, start, end, r0, r1, t0, t1, label_txt):
    svg = space(10, n=160)
    html = (f'<div id="{sid}-vig" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 58%, rgba(1,1,1,0) {r0}px, rgba(1,1,1,1) {r0 + 120}px);"></div>'
            f'<div class="num" id="{sid}-num" style="top:420px;font-size:150px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">{label_txt}</div>')
    ep.scene(sid, start, end, svg, html, origin="50% 58%", drift=0.01)
    ep.js(f'(function(){{var o={{r:{r0}}};var el=document.getElementById("{sid}-vig");tl.to(o,{{r:{r1},duration:{t1 - t0:.3f},ease:"power2.in",onUpdate:function(){{el.style.background="radial-gradient(circle at 50% 58%, rgba(1,1,1,0) "+o.r+"px, rgba(1,1,1,1) "+(o.r+120)+"px)";}}}},{t0:.3f});}})();')
    ep.pop(f"#{sid}-num", start + 0.02, 0.15, 0.6)


pov("s10", cut(80), cut(87), 900, 380, W(83), WE(86) + 0.1, "10 S")
pov("s11", cut(87), cut(92), 380, 0, W(89), WE(91), "15 S")
ep.cue("riser.mp3", W(83), 0.3)
ep.cue("sub.wav", W(90), 0.8)
ep.floor(cut(80), 0.0, 0.0)

# ---------------------------------------------------------------- S12 you don't freeze (body temperature barely moves)
s, e = cut(92), cut(102)
ep.thermometer("s12", s, e, W(96), WE(101), 37, 34, 40, "BODY · CELSIUS", hot_floor=False)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S13 the sunlight burns your skin through the silence
s, e = cut(102), cut(111)
rays = "".join(f'<path class="s13-ray" d="M 220 640 L {620 + k * 40} {1000 + k * 60}" stroke="#FFE2B8" stroke-width="6" stroke-dasharray="40 30" opacity="0.8" filter="url(#glowO)"/>' for k in range(6))
svg = space(13, earth=False, n=100) + f'<g filter="url(#glowO)"><circle cx="220" cy="640" r="140" fill="url(#sunGrad)"/></g>' + rays + f'<g id="s13-m">{floating("m13", 760, 1660, 0.85)}</g>'
ep.scene("s13", s, e, svg, origin="60% 60%")
ep.js(f'tl.fromTo(".s13-ray",{{strokeDashoffset:0}},{{strokeDashoffset:-280,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s13-m path, #s13-m ellipse",{{attr:{{fill:"#7a1a12"}},duration:1.0}},{W(105) - 0.05:.3f});')
ep.cue("sizzle.wav", W(105), 0.3)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S14 1966, a NASA technician, vacuum chamber
s, e = cut(111), cut(122)
chamber = glow(N("M 200 780 L 880 780 Q 940 780 940 840 L 940 1460 Q 940 1520 880 1520 L 200 1520 Q 140 1520 140 1460 L 140 840 Q 140 780 200 780 Z", fill="#0b0c12", red=BLUE, core=BLUE_CORE), f="glowB")
port = '<circle cx="540" cy="1080" r="170" fill="#000" stroke="#9FC8FF" stroke-width="10"/>'
suit = mascot("m14", 540, 1470, 0.62, pose=dict(uarmL=20, uarmR=-20, head=6))
html = ('<div class="big" id="s14-yr" style="top:560px;font-size:120px;">1966</div>'
        '<div class="lbl" id="s14-lab" style="top:1560px;color:#9FC8FF;">NASA VACUUM CHAMBER</div>')
svg = chamber + port + f'<g clip-path="url(#s14-c)">{suit}</g><defs><clipPath id="s14-c"><circle cx="540" cy="1080" r="165"/></clipPath></defs>'
ep.scene("s14", s, e, svg, html, origin="50% 55%", drift=0.02)
ep.pop("#s14-yr", s + 0.02, 0.16, 0.7)
ep.pop("#s14-lab", W(119), 0.2, 0.5)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S15 saliva on his tongue starting to bubble
s, e = cut(122), cut(136)
face = mascot("m15", 540, 2260, 2.4, mouth_open=True, pose=dict(head=-4))
svg = face + bubbles("s15-b", 540, 1000, 14, 50, 15)
ep.scene("s15", s, e, svg, origin="50% 40%", drift=0.02)
boil("s15-b", W(132), e, 14, 160, 15)
ep.cue("sizzle.wav", W(133), 0.3)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S16 he survived: air back in within seconds (pressure gauge)
s, e = cut(136), cut(147)
cx, cy, R = 540, 960, 300


def pol(v, r):
    a = math.radians(180 - v / 100 * 180)
    return cx + r * math.cos(a), cy - r * math.sin(a)


gt = "".join(line(*pol(v, R - 10), *pol(v, R - 50), CORE, 6) + label(round(pol(v, R - 90)[0]), round(pol(v, R - 90)[1]) + 10, v, 28, GREY) for v in range(0, 101, 25))
svg = (glow(N(f"M {cx - R} {cy} A {R} {R} 0 0 1 {cx + R} {cy}", fill="none", red=BLUE, core=BLUE_CORE) + gt, f="glowB")
       + f'<g transform="translate({cx},{cy})"><g id="s16-needle" transform="rotate(-90)"><g filter="url(#glowB)">' + N("M -12 0 L 0 -260 L 12 0 Z", fill="#9FC8FF", red=BLUE, core=BLUE_CORE, sw=8, cw=3)
       + f'<circle r="26" fill="{DARK}" stroke="{BLUE}" stroke-width="10"/></g></g></g>')
html = '<div class="lbl" style="top:1040px;color:#9FC8FF;">AIR PRESSURE · %</div><div class="big" id="s16-ok" style="top:1160px;font-size:90px;color:#9FC8FF;">HE SURVIVED</div>'
ep.scene("s16", s, e, svg, html, origin="50% 55%")
ep.js(f'tl.to("#s16-needle",{{attr:{{transform:"rotate(90)"}},duration:{W(146) - W(139):.3f},ease:"power2.out"}},{W(139):.3f});')
ep.pop("#s16-ok", W(137) - 0.05, 0.2, 0.6)
ep.cue("whoosh-cinematic.mp3", W(139), 0.5)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S17 about ninety seconds before it can't be undone
s, e = cut(147), cut(157)
ep.timer("s17", s, e, W(149), WE(156), 0, 90, "ms", "SECONDS", 90 / 120)
ep.floor(s, 0.45, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(157), 160)
ep.write(red=["space", "suit", "breath", "boil", "lungs", "brain", "nasa", "seconds", "survived", "undone"])
