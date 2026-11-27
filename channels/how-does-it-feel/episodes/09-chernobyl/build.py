"""Episode 09 — How does it feel? When you're at Chernobyl the night the reactor explodes."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
BLUE = "#5A78FF"
YEL, YEL_CORE = "#E8B040", "#FFE08A"


def plant(gid, roof=True, y=1500):
    body = glow(N(f"M 140 {y} L 140 {y - 420} L 820 {y - 420} L 820 {y} Z", fill="#0c0a0c"), gid=f"{gid}-body")
    stack = glow(N(f"M 900 {y} L 920 {y - 900} L 980 {y - 900} L 1000 {y} Z", fill="#0c0a0c", sw=10, cw=3)) + "".join(line(915 - k * 1.5, y - 860 + k * 120, 985 + k * 1.5, y - 860 + k * 120, "#FB2945", 6) for k in range(7))
    windows = "".join(f'<rect x="{180 + k * 70}" y="{y - 330 + (k % 2) * 120}" width="34" height="50" fill="#FFD27A" opacity="0.8"/>' for k in range(9))
    roof_svg = f'<g id="{gid}-roof">' + glow(N(f"M 400 {y - 420} L 400 {y - 520} L 700 {y - 520} L 700 {y - 420} Z", fill="#0c0a0c", sw=10, cw=3)) + '</g>' if roof else ""
    label_ = label(560, y - 450 if not roof else y - 545, "REACTOR 4", 30, GREY, extra=f'id="{gid}-lab"')
    return f'<g id="{gid}">{stack}{body}{windows}{roof_svg}{label_}</g>'


def beam(gid, x=550, y=980, op=0.0):
    return (f'<g id="{gid}" opacity="{op}"><path d="M {x - 70} {y} L {x - 160} 300 L {x + 160} 300 L {x + 70} {y} Z" fill="url(#beamG)"/></g>'
            '<defs><linearGradient id="beamG" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#9FC8FF" stop-opacity="0.85"/><stop offset="1" stop-color="#5A78FF" stop-opacity="0"/></linearGradient></defs>')


def trefoil(cx, cy, r, gid=""):
    blades = ""
    for k in range(3):
        a0 = math.radians(-90 + k * 120 - 30)
        a1 = math.radians(-90 + k * 120 + 30)
        ri = r * 0.28
        blades += (f'<path d="M {cx + ri * math.cos(a0):.0f} {cy + ri * math.sin(a0):.0f} L {cx + r * math.cos(a0):.0f} {cy + r * math.sin(a0):.0f} '
                   f'A {r} {r} 0 0 1 {cx + r * math.cos(a1):.0f} {cy + r * math.sin(a1):.0f} L {cx + ri * math.cos(a1):.0f} {cy + ri * math.sin(a1):.0f} '
                   f'A {ri} {ri} 0 0 0 {cx + ri * math.cos(a0):.0f} {cy + ri * math.sin(a0):.0f} Z" fill="#1a1406" stroke="{YEL}" stroke-width="8"/>')
    i = f' id="{gid}"' if gid else ""
    return f'<g{i} filter="url(#glowG)">{blades}<circle cx="{cx}" cy="{cy}" r="{r * 0.18:.0f}" fill="#1a1406" stroke="{YEL}" stroke-width="8"/></g>'


def geiger(t0, t1, rate0=6, rate1=30, seed=9):
    """Geiger counter bed: 5 s click loops, slow then fast as the dose climbs."""
    t = t0
    while t < t1 - 0.3:
        frac = (t - t0) / max(0.1, t1 - t0)
        ep.cue("geiger_fast.mp3" if rate0 + (rate1 - rate0) * frac > 18 else "geiger_slow.mp3", t, 0.5)
        t += 5.0


# ---------------------------------------------------------------- S01 cold open: the burning reactor, blue column of light → pull out
s, e = 0.0, cut(13)
svg = plant("p1", roof=False) + beam("s01-beam", op=1.0)
ep.scene("s01", s, e, svg, origin="50% 55%", custom_cam=True, fx=[(s, e, "fire", dict(cx=550, base=1090, w=300, h=200, n=8, amp=1.0, sp=7, nofade=True)),
                                                                  (s, e, "smoke", dict(n=14, cx=550, base=1000, w=200, h=800, r0=60, r1=260, life=3, alpha=0.4)),
                                                                  (s, e, "embers", dict(n=40, x0=300, x1=800, y0=500, y1=1100, sp=160))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:1.35}},{{scale:1.4,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
geiger(0, e, 10, 25, 1)
ep.floor(0, 0.4, 0.6, 0.01)
ep.cue("roar.mp3", 0, 0.6)
ep.cue("sub.wav", 0, 0.7)

# ---------------------------------------------------------------- S02 April 26th, 1986 — 1:23 in the morning
s, e = cut(13), cut(20)
cx, cy = 540, 1150
ticks = "".join(line(cx + 190 * math.cos(a), cy + 190 * math.sin(a), cx + 215 * math.cos(a), cy + 215 * math.sin(a), CORE, 5) for a in [i * math.pi / 6 for i in range(12)])
clock = glow(f'<circle cx="{cx}" cy="{cy}" r="230" fill="#0C0A0C" stroke="#FB2945" stroke-width="14"/>{ticks}')
hands = (f'<g transform="translate({cx},{cy})"><g id="s02-hh" transform="rotate(0)">' + line(0, 0, 0, -110, CORE, 12) + '</g>'
         f'<g id="s02-mh" transform="rotate(0)">' + line(0, 0, 0, -170, "#FF3B36", 7) + '</g><circle r="14" fill="#F2EEEA"/></g>')
html = '<div class="num" id="s02-d" style="top:600px;font-size:110px;">APRIL 26, 1986</div>'
ep.scene("s02", s, e, clock + hands, html, origin="50% 55%")
ep.pop("#s02-d", s + 0.02, 0.16, 0.8)
ep.js(f'tl.to("#s02-hh",{{attr:{{transform:"rotate(41.5)"}},duration:{WE(19) - s - 0.2:.3f},ease:"power2.inOut"}},{s + 0.15:.3f});')
ep.js(f'tl.to("#s02-mh",{{attr:{{transform:"rotate(498)"}},duration:{WE(19) - s - 0.2:.3f},ease:"power2.inOut"}},{s + 0.15:.3f});')
ep.cue("tick.wav", W(16), 0.5)
ep.floor(s, 0.4, 0.0)

# ---------------------------------------------------------------- S03 a blast tears the roof off reactor number four
s, e = cut(20), cut(29)
svg = plant("p3") + beam("s03-beam")
tb = W(21) - 0.05
ep.scene("s03", s, e, svg, origin="50% 55%", fx=[(tb, e + 0.1, "fire", dict(cx=550, base=1090, w=300, h=200, n=8, grow=0.4, amp=1.0, sp=7, nofade=True)),
                                                 (tb, e, "sparks", dict(cx=550, cy=980, n=50, r=420, dur=1.0, color="#FFB070", g=500))])
ep.js(f'tl.to("#p3-roof",{{y:-900,rotation:-40,svgOrigin:"550 980",duration:0.9,ease:"power2.out"}},{tb:.3f});')
ep.js(f'tl.to("#s03-beam",{{opacity:1,duration:0.6}},{tb + 0.2:.3f});')
ep.js(f'tl.to("#p3-lab",{{opacity:0,duration:0.1}},{tb:.3f});')
ep.flash(tb, 0.95, 0.8)
ep.shake("#s03-shake", tb, 0.8, 18)
ep.cue("sfx_open_roar.mp3", tb, 1.0)
ep.cue("impact-bass-2.mp3", tb, 0.9)
ep.cue("sub.wav", tb, 1.0)
ep.floor(s, 0.4, 0.0)
ep.floor(tb, 0.3, 0.9, 0.2)

# ---------------------------------------------------------------- S04 you run toward the fire
s, e = cut(29), cut(34)
svg = f'<g transform="translate(540,1200) scale(0.55) translate(-540,-1200)">{plant("p4", roof=False)}</g>' + hline(1560) + mascot("m4", 160, 1560, 0.55)
ep.scene("s04", s, e, svg, origin="50% 60%", fx=[(s, e, "fire", dict(cx=545, base=1250, w=170, h=120, n=6, amp=1.0, sp=7, nofade=True))])
ep.js(f'tl.fromTo("#m4",{{x:0}},{{x:330,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
for k in range(int((e - s) / 0.16)):
    a = 32 if k % 2 == 0 else -32
    t = s + k * 0.16
    ep.rot("#m4-thighL", t, 0.16, a, "sine.inOut")
    ep.rot("#m4-thighR", t, 0.16, -a, "sine.inOut")
    ep.rot("#m4-uarmL", t, 0.16, -a, "sine.inOut")
    ep.rot("#m4-uarmR", t, 0.16, a, "sine.inOut")
geiger(s, e, 15, 30, 4)
ep.floor(s, 0.3, 0.8)

# ---------------------------------------------------------------- S05 a strange taste in your mouth, like metal
s, e = cut(34), cut(43)
mouth = glow(N("M 220 900 Q 540 760 860 900 Q 900 1060 760 1180 Q 540 1290 320 1180 Q 180 1060 220 900 Z", fill="#120607"))
tongue = f'<g id="s05-t">' + glow(N("M 330 1080 Q 540 980 750 1080 Q 760 1170 640 1200 Q 540 1215 440 1200 Q 320 1170 330 1080 Z", fill="#8a1c22", red="#FF6A7A", core="#FFD0D8", sw=10, cw=3)) + '</g>'
teeth = "".join(f'<rect x="{300 + k * 62}" y="905" width="46" height="46" rx="8" fill="#ECE6E5"/>' for k in range(8))
shine = '<rect id="s05-sh" x="200" y="980" width="60" height="260" fill="#E6EEFF" opacity="0.6" transform="rotate(18 230 1100)" filter="url(#soft2)"/>'
svg = mouth + teeth + tongue + f'<defs><clipPath id="s05-c"><path d="M 330 1080 Q 540 980 750 1080 Q 760 1170 640 1200 Q 540 1215 440 1200 Q 320 1170 330 1080 Z"/></clipPath></defs><g clip-path="url(#s05-c)">{shine}</g>' + label(540, 1330, "METALLIC TASTE", 32, "#9FC8FF")
ep.scene("s05", s, e, svg, origin="50% 55%", drift=0.025)
ep.js(f'tl.to("#s05-t path",{{attr:{{fill:"#6a6a78"}},duration:1.2}},{W(36) - 0.1:.3f});')
ep.js(f'tl.fromTo("#s05-sh",{{x:0}},{{x:620,duration:0.9,repeat:{int((e - W(36)) / 0.9)},ease:"power1.inOut",immediateRender:false}},{W(36) - 0.1:.3f});')
ep.js(f'tl.to("#s05-t",{{y:12,duration:0.4,repeat:{int((e - s) / 0.4)},yoyo:true,ease:"sine.inOut"}},{s:.3f});')
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S06 your face tingles, like pins and needles
s, e = cut(43), cut(50)
face = mascot("m6", 540, 2260, 2.4, pose=dict(head=-4))
ep.scene("s06", s, e, face, origin="50% 45%", drift=0.02,
         fx=[(W(44) + k * 0.12, e, "sparks", dict(cx=420 + (k % 4) * 80, cy=840 + (k % 3) * 90, n=14, r=80, dur=0.35, color="#FFFFFF", sz=6)) for k in range(int((e - W(44)) / 0.12))])
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S07 you can't see it, can't feel it — but it goes straight through you
s, e = cut(50), cut(65)
rays = "".join(f'<line class="s07-r" x1="-200" y1="{700 + k * 80}" x2="80" y2="{700 + k * 80}" stroke="#9FC8FF" stroke-width="5" opacity="0" filter="url(#glowB)"/>' for k in range(10))
svg = trefoil(880, 620, 110, "s07-tf") + mascot("m7", 540, 1520, 0.95) + rays
ep.scene("s07", s, e, svg, origin="50% 55%")
ep.pop("#s07-tf", s + 0.05, 0.2, 0.3)
ep.js(f'tl.fromTo(".s07-r",{{x:0,opacity:0.45}},{{x:1300,duration:0.5,stagger:0.05,repeat:{int((e - s) / 0.7)},repeatDelay:0.2,ease:"none",immediateRender:false}},{s + 0.3:.3f});')
ep.js(f'tl.to(".s07-r",{{opacity:1,duration:0.2}},{W(58):.3f});')
ep.js(f'tl.fromTo("#s07-tf",{{scale:1}},{{scale:1.12,svgOrigin:"880 620",duration:0.4,repeat:{int((e - s) / 0.4)},yoyo:true,ease:"sine.inOut",immediateRender:false}},{s + 0.3:.3f});')
ep.js('tl.set(".s07-r",{opacity:0},0);')
ep.js(f'tl.to("#m7 line, #m7 path, #m7 ellipse",{{attr:{{stroke:"#9FC8FF"}},duration:0.3}},{W(61):.3f});')
geiger(s, e, 8, 45, 7)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S08 in one hour, more radiation than most people get in a lifetime
s, e = cut(65), cut(79)
bars = (label(100, 790, "A LIFETIME", 40, "#F5F5F5", "start") + f'<rect x="100" y="830" width="40" height="80" fill="#E8B040" filter="url(#glowG)"/>'
        + label(100, 1060, "ONE HOUR AT THE REACTOR", 40, "#FF6A5A", "start") + f'<rect id="s08-b" x="100" y="1100" width="880" height="80" fill="#FB2945" filter="url(#glow)"/>')
ep.scene("s08", s, e, bars + trefoil(540, 1400, 90), origin="50% 55%")
ep.js(f'tl.fromTo("#s08-b",{{scaleX:0.045,transformOrigin:"0% 50%"}},{{scaleX:1,duration:{WE(78) - s - 0.1:.3f},ease:"power2.in",immediateRender:false}},{s + 0.1:.3f});')
ep.js('gsap.set("#s08-b",{scaleX:0.02,transformOrigin:"0% 50%"});')
geiger(W(67), e, 10, 60, 8)
ep.floor(s, 0.35, 0.3)

# ---------------------------------------------------------------- S09 within the hour, you start vomiting
s, e = cut(79), cut(85)
svg = hline(1560) + mascot("m9", 540, 1560, 0.85, pose=dict(head=30, uarmL=-40, farmL=-90, uarmR=40, farmR=90, thighL=10, thighR=-10)) + '<ellipse id="s09-st" cx="540" cy="1260" rx="70" ry="50" fill="#FB2945" opacity="0" filter="url(#glow)"/>'
ep.scene("s09", s, e, svg, origin="50% 60%")
ep.js(f'tl.fromTo("#s09-st",{{opacity:0}},{{opacity:0.8,duration:0.25,repeat:{int((e - W(83)) / 0.25)},yoyo:true,immediateRender:false}},{W(83) - 0.1:.3f});')
ep.js(f'tl.to("#m9",{{rotation:14,svgOrigin:"540 1560",duration:0.3,ease:"power2.in"}},{W(84) - 0.1:.3f});')
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S10 a few days later you feel better — it's a trick
s, e = cut(85), cut(95)
html = '<div class="num" id="s10-n" style="top:780px;font-size:240px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">2</div><div class="lbl" id="s10-l" style="top:1040px;">DAYS LATER · FEELING BETTER</div>'
ep.scene("s10", s, e, "", html, origin="50% 50%")
ep.counter("#s10-n", s + 0.1, WE(88) - s, 2, 4, "n", "power1.out")
tt = W(92) - 0.05
ep.js(f'tl.to("#s10-n",{{color:"#FA2335",textShadow:"0 0 18px rgba(255,40,50,.9),0 0 50px rgba(255,20,40,.6)",duration:0.1}},{tt:.3f});')
ep.shake("#s10-shake", tt, 0.35, 14)
ep.js(f'tl.set("#s10-l",{{color:"#FF6A5A"}},{tt:.3f});')
ep.cue("impact-bass-1.mp3", tt, 0.7)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S11 your bone marrow has stopped making new blood
s, e = cut(95), cut(103)
bone = glow(N("M 300 860 Q 240 800 300 760 Q 360 730 400 800 L 680 800 Q 720 730 780 760 Q 840 800 780 860 L 780 1040 Q 840 1100 780 1140 Q 720 1170 680 1100 L 400 1100 Q 360 1170 300 1140 Q 240 1100 300 1040 Z", fill="#ECE6E5", red="#F2EEEA", core="#ffffff", sw=8, cw=3), f="glowS")
marrow = '<rect id="s11-m" x="400" y="880" width="280" height="140" rx="40" fill="#C2181E" filter="url(#glow)"/>'
cells = "".join(f'<circle class="s11-c" id="s11-c{i}" cx="540" cy="950" r="14" fill="#FF3B36" opacity="0"/>' for i in range(12))
svg = bone + marrow + cells + label(540, 1240, "BONE MARROW", 32, GREY)
ep.scene("s11", s, e, svg, origin="50% 55%")
r11 = random.Random(11)
tstop = W(99) - 0.1
for k in range(int((tstop - s) / 0.15)):
    cx_, cy_ = r11.uniform(150, 930), r11.uniform(600, 1400)
    ep.js(f'tl.fromTo("#s11-c{k % 12}",{{opacity:1,attr:{{cx:540,cy:950}}}},{{opacity:0,attr:{{cx:{cx_:.0f},cy:{cy_:.0f}}},duration:0.7,ease:"power1.out",immediateRender:false}},{s + k * 0.15:.3f});')
ep.js(f'tl.to("#s11-m",{{attr:{{fill:"#3a3532"}},duration:{e - tstop:.3f}}},{tstop:.3f});')
ep.cue("beep.wav", tstop + 0.3, 0.06)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S12 your skin blisters and peels away
s, e = cut(103), cut(109)
skin = glow(N("M 180 960 L 900 960 L 900 1260 L 180 1260 Z", fill="#1a0a0a")) + "".join(f'<path d="M 200 {1030 + k * 60} Q 380 {1000 + k * 60} 540 {1030 + k * 60} T 880 {1030 + k * 60}" fill="none" stroke="#E87A8A" stroke-width="4" opacity="0.7"/>' for k in range(3))
blis = "".join(f'<g id="s12-b{k}" opacity="0"><path d="M {210 + k * 110} 962 A 46 52 0 0 1 {300 + k * 110} 962 Z" fill="#E8A0A0" stroke="#FFF1DC" stroke-width="5" filter="url(#glowS)"/></g>' for k in range(6))
peel = '<path id="s12-peel" d="M 180 960 L 900 960 L 900 990 L 180 990 Z" fill="#E8A0A0" stroke="#FFF1DC" stroke-width="4" opacity="0"/>'
svg = skin + blis + peel + label(540, 860, "SKIN", 30, GREY)
ep.scene("s12", s, e, svg, origin="50% 52%", drift=0.025)
for k in range(6):
    ep.js(f'tl.fromTo("#s12-b{k}",{{opacity:1,scale:0,svgOrigin:"{255 + k * 110} 962"}},{{scale:1,duration:0.16,ease:"back.out(2)",immediateRender:false}},{W(105) - 0.05 + k * 0.07:.3f});')
    ep.js(f'tl.set("#s12-b{k}",{{opacity:0}},0);')
ep.js(f'tl.set("#s12-peel",{{opacity:1}},{W(107) - 0.1:.3f});')
ep.js(f'tl.to("#s12-peel",{{rotation:-9,svgOrigin:"900 975",y:-24,duration:0.7,ease:"power2.out"}},{W(107) - 0.1:.3f});')
ep.js(f'tl.to("#s12 [id^=s12-b]",{{opacity:0,duration:0.3}},{W(107):.3f});')
ep.floor(s, 0.35, 0.2)

# ---------------------------------------------------------------- S13 of the first responders, twenty-eight die within months
s, e = cut(109), cut(117)
helmets = "".join(f'<g class="s13-h"><circle cx="{150 + (k % 7) * 130}" cy="{700 + (k // 7) * 160}" r="22" fill="#1a1416" stroke="#FB2945" stroke-width="6"/>'
                  f'<path d="M {150 + (k % 7) * 130 - 34} {700 + (k // 7) * 160 + 34} L {150 + (k % 7) * 130 + 34} {700 + (k // 7) * 160 + 34} L {150 + (k % 7) * 130 + 26} {700 + (k // 7) * 160 + 100} L {150 + (k % 7) * 130 - 26} {700 + (k // 7) * 160 + 100} Z" fill="#1a1416" stroke="#FB2945" stroke-width="6"/></g>' for k in range(28))
html = '<div class="num" id="s13-n" style="top:1360px;font-size:150px;">1</div><div class="lbl" style="top:1520px;">FIRST RESPONDERS DIED</div>'
ep.scene("s13", s, e, f'<g filter="url(#glowS)">{helmets}</g>', html, origin="50% 55%")
ep.js(f'tl.fromTo(".s13-h",{{opacity:0,scale:0.4,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.12,stagger:0.07,ease:"back.out(2)",immediateRender:false}},{W(110):.3f});')
ep.js('tl.set(".s13-h",{opacity:0},0);')
ep.counter("#s13-n", W(110), WE(116) - W(110), 1, 28, "n", "none")
ep.js(f'tl.to(".s13-h path, .s13-h circle",{{attr:{{stroke:"#555"}},duration:0.6}},{W(114):.3f});')
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(117), 120)
ep.write(red=["chernobyl", "reactor", "fire", "metal", "radiation", "lifetime", "trick", "blood", "twenty-eight"])
