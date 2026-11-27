"""Episode 16 — How does it feel? When your elevator falls 75 floors (Betty Lou Oliver, Empire State Building, 1945)."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
ICE, ICE_CORE = "#5A78FF", "#E6EEFF"
LAMP, LAMP_CORE = "#E8B040", "#FFE08A"
STEEL = "#BDB5B5"


def esb(gid, x, base, s=1.0, lit=True):
    pts = [(-180, 0), (-180, -700), (-140, -700), (-140, -900), (-100, -900), (-100, -1060), (-60, -1060), (-60, -1140), (-20, -1140), (-10, -1290),
           (10, -1290), (20, -1140), (60, -1140), (60, -1060), (100, -1060), (100, -900), (140, -900), (140, -700), (180, -700), (180, 0)]
    d = "M " + " L ".join(f"{px} {py}" for px, py in pts) + " Z"
    r = random.Random(len(gid))
    wins = "".join(f'<rect x="{wx}" y="{wy}" width="14" height="20" fill="{LAMP_CORE}" opacity="{r.choice([0.15, 0.5, 0.9])}"/>'
                   for wy in range(-680, -20, 52) for wx in range(-160, 160, 40)) if lit else ""
    return f'<g id="{gid}"><g transform="translate({x},{base}) scale({s})">' + glow(N(d, fill="#0c0a0c", sw=10, cw=3)) + wins + '</g></g>'


def fog(gid, seed, y0=800, y1=1600, n=8, op=0.5):
    r = random.Random(seed)
    return f'<g id="{gid}">' + "".join(f'<ellipse cx="{r.uniform(-100, 1180):.0f}" cy="{r.uniform(y0, y1):.0f}" rx="{r.uniform(220, 420):.0f}" ry="{r.uniform(40, 90):.0f}" fill="#8a8f9a" opacity="{op * r.uniform(0.3, 0.7):.2f}" filter="url(#soft)"/>' for _ in range(n)) + '</g>'


def car(gid, x, y, s=1.0, pose=None, lying=False, cables=True):
    box = N("M -110 -150 L 110 -150 L 110 150 L -110 150 Z", fill="#0c0a0c", sw=12, cw=4)
    cab = "".join(line(dx, -150, dx, -1400, STEEL, 6) for dx in (-30, 0, 30)) if cables else ""
    who = (f'<g transform="translate(-80,110) rotate(90) scale(1)">{mascot(gid + "-m", 0, 0, 0.26, style="xray")}</g>' if lying
           else mascot(gid + "-m", 0, 140, 0.4, style="xray", pose=pose or {}))
    return f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})"><g id="{gid}-cab">{cab}</g><g filter="url(#glow)">{box}</g>{who}</g></g>'


def shaft(gid, x0=300, x1=780, floors=True, y0=-200, y1=2200, label0=0):
    walls = glow(f'<rect x="{x0 - 10}" y="{y0}" width="20" height="{y1 - y0}" fill="none"/>' + line(x0, y0, x0, y1, RED, 12) + line(x0, y0, x0, y1, CORE, 4)
                 + line(x1, y0, x1, y1, RED, 12) + line(x1, y0, x1, y1, CORE, 4))
    marks = ""
    if floors:
        for k, yy in enumerate(range(y0, y1, 160)):
            marks += line(x0 - 60, yy, x0, yy, "#6a5a5a", 5) + line(x1, yy, x1 + 60, yy, "#6a5a5a", 5)
    return f'<g id="{gid}">{walls}<g id="{gid}-mk">{marks}</g></g>'


def bomber(gid, x, y, s=1.0):
    d = "M -200 0 Q -180 -26 -120 -26 L 180 -20 Q 220 -12 230 0 Q 220 12 180 16 L -120 22 Q -180 22 -200 0 Z"
    wing = "M -20 -6 L 60 -170 L 100 -170 L 70 -6 Z M -20 6 L 60 170 L 100 170 L 70 6 Z"
    tail = "M -170 -10 L -210 -90 L -190 -90 L -150 -14 Z"
    return f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})">' + glow(N(d, fill="#0c0a0c", sw=8, cw=3) + N(wing, fill="#0c0a0c", sw=8, cw=3) + N(tail, fill="#0c0a0c", sw=8, cw=3)) + '</g></g>'


# ---------------------------------------------------------------- S01 cold open: inside the falling car, floors flashing past → pull out
s, e = 0.0, cut(10)
svg = shaft("sh1", 300, 780) + car("c1", 540, 1050, 1.6, pose=dict(uarmL=150, farmL=20, uarmR=-150, farmR=-20, thighL=30, shinL=-40, thighR=-20, shinR=30))
ep.scene("s01", s, e, svg, origin="50% 52%", custom_cam=True, fx=[(s, e, "sparks", dict(cx=540, cy=780, n=40, r=300, dur=0.7, color="#FFD27A", g=-300)),
                                                                  (0.8, e, "sparks", dict(cx=540, cy=780, n=40, r=300, dur=0.7, color="#FFD27A", g=-300))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:1.7}},{{scale:1.8,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#sh1-mk",{{y:0}},{{y:-160,duration:0.12,repeat:{int(e / 0.12)},ease:"none",immediateRender:false}},0);')
ep.js(f'tl.fromTo("#c1-m",{{y:0}},{{y:-60,duration:{e:.3f},ease:"power1.out",immediateRender:false}},0);')
ep.shake("#s01-shake", 0, e, 6)
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("shaft_fall.mp3", 0, 0.9)
ep.cue("sub.wav", 0, 0.6)

# ---------------------------------------------------------------- S02 New York, July 28th, 1945
s, e = cut(10), cut(15)
sky = "".join(f'<rect x="{x}" y="{1800 - h}" width="90" height="{h}" fill="#0c0a0c" stroke="#3a2a2a" stroke-width="4"/>' for x, h in ((20, 300), (130, 460), (240, 380), (760, 420), (870, 330), (980, 500)))
html = '<div class="num" id="s02-d" style="top:600px;font-size:130px;">JULY 28, 1945</div><div class="lbl" style="top:745px;">NEW YORK</div>'
ep.scene("s02", s, e, sky + esb("b2", 540, 1800, 0.72) + fog("s02-f", 2, 1100, 1700, 9), html, origin="50% 60%")
ep.pop("#s02-d", s + 0.02, 0.18, 0.8)
ep.js(f'tl.fromTo("#s02-f",{{x:0}},{{x:120,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')

# ---------------------------------------------------------------- S03 you're twenty, you run an elevator in the Empire State Building
s, e = cut(15), cut(27)
dial = glow(f'<path d="M 340 820 A 200 200 0 0 1 740 820" fill="none" stroke="{LAMP}" stroke-width="10"/>', f="glowG") + "".join(
    line(540 + 200 * math.cos(a), 820 - 200 * math.sin(a), 540 + 170 * math.cos(a), 820 - 170 * math.sin(a), LAMP_CORE, 5) for a in [math.pi * k / 10 for k in range(11)])
needle = f'<g transform="translate(540,820)"><g id="s03-nd" transform="rotate(-80)">' + line(0, 0, 0, -160, "#FF3B36", 7) + '</g><circle r="14" fill="#F2EEEA"/></g>'
svg = dial + needle + car("c3", 380, 1350, 1.0, pose=dict(uarmR=-60, farmR=-40), cables=False)
html = ('<div class="num" id="s03-n" style="top:1180px;left:540px;width:540px;font-size:180px;">20</div><div class="lbl" style="top:1370px;left:540px;width:540px;">YEARS OLD</div>'
        '<div class="lbl" id="s03-l" style="top:930px;color:#FFE08A;">EMPIRE STATE BUILDING</div>')
ep.scene("s03", s, e, svg, html, origin="50% 55%")
ep.counter("#s03-n", W(16) - 0.1, 0.5, 0, 20, "n")
ep.rot("#s03-nd", W(19), WE(26) - W(19), 75, "power1.inOut")
ep.show("#s03-l", W(24) - 0.05, 0.25)
ep.cue("beep.wav", W(26), 0.08)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S04 a foggy morning — a bomber crashes into the building
s, e = cut(27), cut(38)
hit_y = 1830 - 0.62 * 1290 * 0.95
tc = W(34) - 0.05
svg = esb("b4", 640, 1830, 0.95) + fog("s04-f", 4, 900, 1500, 10, 0.7) + bomber("bm4", -260, hit_y, 0.7)
ep.scene("s04", s, e, svg, origin="55% 55%", fx=[(tc, e, "fire", dict(cx=560, base=hit_y + 40, w=220, h=260, n=7, amp=1.0, sp=8, grow=0.3)),
                                                 (tc, tc + 0.8, "sparks", dict(cx=560, cy=hit_y, n=60, r=420, dur=0.8, color="#FFB040", g=300)),
                                                 (tc, e, "smoke", dict(n=12, cx=560, base=hit_y, w=160, h=600, r0=60, r1=220, life=2.5, alpha=0.45))])
ep.js(f'tl.fromTo("#bm4",{{x:0}},{{x:{560 + 260 - 180 * 0.7:.0f},duration:{tc - W(31):.3f},ease:"power1.in",immediateRender:false}},{W(31):.3f});')
ep.js(f'tl.set("#bm4",{{opacity:0}},{tc + 0.05:.3f});')
ep.js(f'tl.fromTo("#s04-f",{{x:0}},{{x:-160,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.flash(tc, 0.9, 0.6)
ep.shake("#s04-shake", tc, 0.7, 22)
ep.cue("whoosh-cinematic.mp3", W(31), 0.6)
ep.cue("metal_tear.mp3", tc, 1.0)
ep.cue("impact-bass-1.mp3", tc, 1.0)
ep.floor(tc, 0.4, 0.7, 0.1)

# ---------------------------------------------------------------- S05 fire rips through your floor — you're badly burned
s, e = cut(38), cut(46)
floor_l = hline(1500, -40, 1120, 10, 4)
svg = floor_l + f'<g id="s05-m">{mascot("m5", 540, 1490, 0.95, mouth_open=True, pose=dict(uarmL=60, farmL=60, uarmR=-60, farmR=-60))}</g>'
ep.scene("s05", s, e, svg, origin="50% 60%", fx=[(s, e, "fire", dict(cx=540, base=1500, w=1100, h=320, n=14, amp=1.0, sp=8, grow=0.6)),
                                                 (s, e, "embers", dict(n=50, x0=0, x1=1080, y0=600, y1=1500, sp=180)),
                                                 (s, e, "smoke", dict(n=10, cx=540, base=1200, w=900, h=700, r0=80, r1=240, life=3, alpha=0.3))])
ep.js(f'tl.to("#m5 path, #m5 ellipse",{{attr:{{fill:"#5a0f0c"}},duration:0.6}},{W(44) - 0.1:.3f});')
ep.cue("fire_ignite.mp3", s, 0.8)
ep.cue("sizzle.wav", W(44), 0.7)
ep.floor(s, 0.5, 1.0)

# ---------------------------------------------------------------- S06 rescuers put you into an elevator to get you down
s, e = cut(46), cut(56)
doors = (f'<rect id="s06-dl" x="430" y="900" width="110" height="300" fill="#1a1416" stroke="{STEEL}" stroke-width="5"/>'
         f'<rect id="s06-dr" x="540" y="900" width="110" height="300" fill="#1a1416" stroke="{STEEL}" stroke-width="5"/>')
svg = shaft("sh6", 300, 780, y0=300) + car("c6", 540, 1050, 1.0, lying=True) + doors + label(540, 1290, "FLOOR 75", 32, LAMP_CORE)
ep.scene("s06", s, e, svg, origin="50% 55%")
ep.js('gsap.set("#s06-dl",{scaleX:0,transformOrigin:"0% 50%"}); gsap.set("#s06-dr",{scaleX:0,transformOrigin:"100% 50%"});')
ep.js(f'tl.to("#s06-dl",{{scaleX:1,transformOrigin:"0% 50%",duration:0.5,ease:"power2.inOut"}},{W(53) - 0.1:.3f});')
ep.js(f'tl.to("#s06-dr",{{scaleX:1,transformOrigin:"100% 50%",duration:0.5,ease:"power2.inOut"}},{W(53) - 0.1:.3f});')
ep.cue("lid_knock.mp3", W(53) + 0.4, 0.5)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S07 the crash has damaged its cables
s, e = cut(56), cut(63)
r7 = random.Random(7)
fray = "".join(line(480 + k * 60 + r7.uniform(-6, 6), 980, 480 + k * 60 + r7.uniform(-40, 40), 980 + r7.uniform(30, 80), STEEL, 3) for k in range(3) for _ in range(5))
cables = f'<g id="s07-top">' + "".join(line(480 + k * 60, 300, 480 + k * 60, 990, STEEL, 16) for k in range(3)) + '</g>' + f'<g id="s07-bot">' + "".join(line(480 + k * 60, 990, 480 + k * 60, 1700, STEEL, 16) for k in range(3)) + fray + '</g>'
svg = cables + f'<circle cx="540" cy="990" r="120" fill="none" stroke="#FF3B36" stroke-width="6" stroke-dasharray="16 12" filter="url(#glowS)"/>'
ep.scene("s07", s, e, svg, origin="50% 52%", drift=0.04, fx=[(W(60), e, "sparks", dict(cx=540, cy=990, n=30, r=200, dur=0.5, color="#FFD27A", g=200))])
for k in range(int((e - s) / 0.18)):
    ep.js(f'tl.set("#s07-bot",{{x:{r7.uniform(-4, 4):.1f}}},{s + k * 0.18:.3f});')
ep.cue("hull_creak.mp3", W(59), 0.6)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S08 they snap
s, e = cut(63), cut(65)
ep.scene("s08", s, e, cables.replace("s07-", "s08-"), origin="50% 52%", fx=[(W(64) - 0.05, e, "sparks", dict(cx=540, cy=990, n=60, r=500, dur=0.7, color="#FFD27A", g=200))])
tsn = W(64) - 0.05
ep.js(f'tl.to("#s08-top",{{y:-500,duration:0.3,ease:"power3.out"}},{tsn:.3f});')
ep.js(f'tl.to("#s08-bot",{{y:900,duration:0.5,ease:"power3.in"}},{tsn:.3f});')
ep.flash(tsn, 0.7, 0.4)
ep.shake("#s08-shake", tsn, 0.4, 20)
ep.cue("cable_snap.mp3", tsn - 0.03, 1.0)

# ---------------------------------------------------------------- S09 you drop — seventy-five floors — more than three hundred meters
s, e = cut(65), cut(75)
html = ('<div class="num" id="s09-f" style="top:590px;font-size:130px;">75</div><div class="lbl" style="top:725px;">FLOOR</div>'
        '<div class="num" id="s09-m" style="top:1500px;font-size:110px;color:#FFE08A;text-shadow:0 0 18px rgba(232,176,64,.8);">0 M</div><div class="lbl" style="top:1620px;">FALLEN</div>')
svg = shaft("sh9", 300, 780) + car("c9", 540, 1100, 0.9, lying=True, cables=False)
ep.scene("s09", s, e, svg, html, origin="50% 60%")
ep.js(f'tl.fromTo("#sh9-mk",{{y:0}},{{y:-160,duration:0.1,repeat:{int((e - s) / 0.1)},ease:"none",immediateRender:false}},{s:.3f});')
dur9 = WE(74) - s
ep.counter("#s09-f", s + 0.05, dur9, 75, 0, "n", "power1.in")
ep.js(f'(function(){{var el=document.getElementById("s09-m");var o={{v:0}};tl.to(o,{{v:300,duration:{dur9:.3f},ease:"power1.in",onUpdate:function(){{el.textContent=Math.round(o.v)+" M";}}}},{s + 0.05:.3f});}})();')
ep.shake("#s09-shake", s, e - s, 7)
ep.cue("shaft_fall.mp3", s, 1.0)
ep.cue("shaft_fall.mp3", s + 3.8, 0.8)
ep.floor(s, 0.2, 0.0)

# ---------------------------------------------------------------- S10 then, two things save you
s, e = cut(75), cut(80)
html = '<div class="num" id="s10-n" style="top:820px;font-size:420px;color:#FFE08A;text-shadow:0 0 30px rgba(232,176,64,.9);">2</div><div class="lbl" style="top:1290px;">THINGS SAVE YOU</div>'
ep.scene("s10", s, e, "", html, origin="50% 50%")
ep.pop("#s10-n", W(76) - 0.05, 0.25, 1.8, "power3.out")
ep.cue("impact-bass-2.mp3", W(76), 0.6)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S11 the broken cable piles up at the bottom, like a giant spring
s, e = cut(80), cut(95)
coil = ""
for k in range(9):
    yy = 1640 - k * 26
    coil += f'<ellipse class="s11-c" cx="540" cy="{yy}" rx="200" ry="40" fill="none" stroke="{STEEL}" stroke-width="10"/>'
svg = shaft("sh11", 300, 780, floors=False) + hline(1680, 300, 780, 10, 4) + f'<g id="s11-coil">{coil}</g>' + f'<g id="s11-car">{car("c11", 540, 1200, 0.9, lying=True, cables=False)}</g>' + label(540, 1760, "COILED CABLE", 30, GREY, extra='id="s11-l"')
ep.scene("s11", s, e, svg, origin="50% 65%")
ep.js(f'tl.fromTo(".s11-c",{{opacity:0,y:-200}},{{opacity:1,y:0,duration:0.25,stagger:0.12,ease:"power2.in",immediateRender:false}},{W(81):.3f});')
ep.js('gsap.set(".s11-c",{opacity:0});')
ep.js(f'gsap.set("#s11-car",{{y:-900,opacity:0}});')
ep.js(f'tl.set("#s11-car",{{opacity:1}},{W(93) - 0.2:.3f});')
tl_ = W(93) - 0.2
ep.js(f'tl.to("#s11-car",{{y:200,duration:0.45,ease:"power3.in"}},{tl_:.3f});')
ep.js(f'tl.to("#s11-coil",{{scaleY:0.45,transformOrigin:"50% 100%",duration:0.3,ease:"power2.out"}},{tl_ + 0.45:.3f});')
ep.js(f'tl.to("#s11-car",{{y:240,duration:0.3,ease:"power2.out"}},{tl_ + 0.45:.3f});')
ep.show("#s11-l", W(82), 0.3)
ep.shake("#s11-shake", tl_ + 0.45, 0.4, 14)
ep.cue("impact-bass-1.mp3", tl_ + 0.45, 0.8)
ep.cue("cable_snap.mp3", W(82), 0.3)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S12 the air trapped beneath the car slows it, like a cushion
s, e = cut(95), cut(108)
r12 = random.Random(12)
air = "".join(f'<circle class="s12-a" cx="{r12.uniform(330, 750):.0f}" cy="{r12.uniform(1380, 1660):.0f}" r="{r12.uniform(8, 16):.0f}" fill="#9FC8FF" opacity="0.8" filter="url(#glowB)"/>' for _ in range(40))
arrows = "".join(f'<g class="s12-ar" filter="url(#glowB)">' + N(f"M {x} 1560 L {x} 1420 M {x - 26} 1450 L {x} 1420 L {x + 26} 1450", fill="none", red=ICE, core=ICE_CORE, sw=10, cw=3) + '</g>' for x in (400, 540, 680))
svg = shaft("sh12", 300, 780) + hline(1680, 300, 780, 10, 4) + f'<g id="s12-air">{air}</g>' + arrows + f'<g id="s12-car">{car("c12", 540, 1100, 0.9, lying=True, cables=False)}</g>'
html = '<div class="num" id="s12-n" style="top:600px;font-size:130px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">AIR CUSHION</div>'
ep.scene("s12", s, e, svg, html, origin="50% 62%")
ep.js(f'gsap.set("#s12-car",{{y:-700}});')
ep.js(f'tl.to("#s12-car",{{y:120,duration:{e - s - 0.3:.3f},ease:"expo.out"}},{s + 0.1:.3f});')
ep.js(f'tl.to("#s12-air",{{scaleY:0.55,transformOrigin:"50% 100%",duration:{e - s - 0.3:.3f},ease:"expo.out"}},{s + 0.1:.3f});')
ep.js(f'tl.fromTo(".s12-ar",{{opacity:0}},{{opacity:1,duration:0.2,stagger:0.1,immediateRender:false}},{W(97):.3f});')
ep.js('gsap.set(".s12-ar",{opacity:0});')
ep.pop("#s12-n", W(105) - 0.05, 0.2, 1.4, "power3.out")
ep.cue("whoosh-cinematic.mp3", s, 0.5)
ep.floor(s, 0.2, 0.0)

# ---------------------------------------------------------------- S13 pelvis, back and neck broken — but you're alive
s, e = cut(108), cut(118)
y0, sc = 1640, 1.35
spots = {"pel": (540, y0 - 276 * sc, 46), "back": (540, y0 - 380 * sc, 40), "neck": (540, y0 - 480 * sc, 30)}
marks = "".join(f'<circle id="s13-{k}" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#FF2A33" opacity="0" filter="url(#glow)"/>' for k, (x, y, r) in spots.items())
svg = mascot("m13", 540, y0, sc, style="xray") + marks
html = ('<div class="lbl" id="s13-a" style="top:1250px;left:690px;width:390px;text-align:left;color:#FF6A6A;">PELVIS</div>'
        '<div class="lbl" id="s13-b" style="top:1110px;left:720px;width:360px;text-align:left;color:#FF6A6A;">BACK</div>'
        '<div class="lbl" id="s13-c" style="top:960px;left:690px;width:390px;text-align:left;color:#FF6A6A;">NECK</div>')
ep.scene("s13", s, e, svg, html, origin="50% 55%", fx=[(W(115), e, "ecg", dict(x0=80, x1=1000, y=600, amp=90, period=360, speed=380))])
for sel, lab, t in (("#s13-pel", "#s13-a", W(109)), ("#s13-back", "#s13-b", W(110)), ("#s13-neck", "#s13-c", W(112))):
    ep.show(sel, t - 0.05, 0.15)
    ep.show(lab, t - 0.05, 0.15)
    ep.cue("impact-bass-2.mp3", t - 0.05, 0.5)
for t in (W(115), W(115) + 0.62, W(115) + 1.24):
    ep.cue("heart.wav", t, 0.6)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S14 still the longest elevator fall anyone has ever survived
s, e = cut(118), cut(128)
bar = f'<rect id="s14-bar" x="640" y="{1750 - 0.75 * 1290 * 0.8:.0f}" width="36" height="{0.75 * 1290 * 0.8:.0f}" fill="#FB2945" filter="url(#glow)"/>'
html = ('<div class="lbl" id="s14-l" style="top:600px;color:#FFE08A;font-size:44px;">WORLD RECORD</div>'
        '<div class="num" id="s14-n" style="top:1220px;left:700px;width:380px;font-size:80px;">75 FLOORS</div>')
ep.scene("s14", s, e, esb("b14", 400, 1750, 0.8) + bar, html, origin="50% 60%")
ep.js(f'tl.fromTo("#s14-bar",{{scaleY:0,transformOrigin:"50% 0%"}},{{scaleY:1,duration:0.8,ease:"power2.in",immediateRender:false}},{s + 0.1:.3f});')
ep.js('gsap.set("#s14-bar",{scaleY:0,transformOrigin:"50% 0%"});')
ep.pop("#s14-n", s + 0.9, 0.2, 1.3, "power3.out")
ep.pop("#s14-l", W(121) - 0.05, 0.2, 1.4, "power3.out")
ep.cue("impact-bass-2.mp3", W(121), 0.5)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(128), 131)
ep.write(red=["falls", "empire", "bomber", "fire", "burned", "cables", "snap", "drop", "spring", "cushion", "broken", "alive", "survived"])
