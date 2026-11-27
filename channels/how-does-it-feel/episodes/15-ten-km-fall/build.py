"""Episode 15 — How does it feel? When you fall ten kilometers without a parachute (Vesna Vulović, 1972)."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
ICE, ICE_CORE = "#5A78FF", "#E6EEFF"
LAMP, LAMP_CORE = "#E8B040", "#FFE08A"
SNOW = dict(n=90, sp=200, color="#E6EEFF")


def clouds(gid, seed, n=10, y0=600, y1=1800):
    r = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y, w = r.uniform(-100, 1180), r.uniform(y0, y1), r.uniform(160, 320)
        out += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w:.0f}" ry="{w * 0.32:.0f}" fill="#1a2030" opacity="0.8" filter="url(#soft2)"/>'
    return f'<g id="{gid}">{out}</g>'


def streaks(gid, seed, n=26):
    r = random.Random(seed)
    return f'<g id="{gid}">' + "".join(line(x, y, x, y + r.uniform(120, 260), "#9FB4E6", 3, 'opacity="0.5"') for x, y in ((r.uniform(0, 1080), r.uniform(400, 1900)) for _ in range(n))) + '</g>'


def plane(gid, x, y, s=1.0):
    win = lambda a, b: "".join(f'<circle cx="{xx}" cy="-12" r="7" fill="{LAMP_CORE}"/>' for xx in range(a, b, 34))
    tail = (N("M -150 -50 L -360 -50 L -400 -10 L -400 30 L -360 50 L -150 50 Z", fill="#0c0a0c", sw=10, cw=3)
            + N("M -330 -50 L -385 -210 L -335 -210 L -280 -50 Z", fill="#0c0a0c", sw=10, cw=3)
            + N("M -430 -210 L -290 -210", fill="none", sw=10, cw=3)
            + f'<ellipse cx="-250" cy="-78" rx="62" ry="22" fill="#0c0a0c" stroke="{RED}" stroke-width="8"/>')
    mid = N("M -150 -50 L 150 -50 L 150 50 L -150 50 Z", fill="#0c0a0c", sw=10, cw=3) + N("M -50 30 L 60 30 L 170 120 L 120 120 Z", fill="#0c0a0c", sw=8, cw=3)
    nose = N("M 150 -50 L 330 -50 Q 410 -40 422 10 Q 410 50 330 50 L 150 50 Z", fill="#0c0a0c", sw=10, cw=3) + '<path d="M 350 -30 L 395 -22 L 400 -8 L 352 -10 Z" fill="#9FC8FF"/>'
    return (f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})">'
            f'<g id="{gid}-a" transform="translate(0 0) rotate(0 -150 0)"><g filter="url(#glow)">{tail}</g>{win(-140, -150 + 1)}</g>'
            f'<g id="{gid}-b" transform="translate(0 0) rotate(0 0 0)"><g filter="url(#glow)">{mid}</g>{win(-130, 140)}</g>'
            f'<g id="{gid}-c" transform="translate(0 0) rotate(0 150 0)"><g filter="url(#glow)">{nose}</g>{win(170, 330)}</g></g></g>')


def piece(gid, x, y, s=1.0, inside=True):
    """the broken cabin section with you inside, pinned by a food cart."""
    shell = N("M -230 -120 L 230 -120 L 250 -60 L 230 0 L 250 60 L 230 120 L -230 120 L -250 60 L -230 0 L -250 -60 Z", fill="#0c0a0c", sw=12, cw=4)
    seats = "".join(f'<path d="M {sx} 100 L {sx} 30 L {sx + 30} 30 L {sx + 30} 70 L {sx + 60} 70 L {sx + 60} 100" fill="none" stroke="#6a5a5a" stroke-width="6"/>' for sx in (-200, -110))
    you = f'<g transform="translate(60,96) rotate(-90)">{mascot(gid + "-m", 0, 0, 0.22, style="xray", mouth_open=True, pose=dict(uarmL=150, uarmR=-150))}</g>' if inside else ""
    cart = f'<g><rect x="120" y="40" width="80" height="62" rx="6" fill="#2a2426" stroke="{LAMP}" stroke-width="5"/><circle cx="135" cy="108" r="9" fill="{LAMP}"/><circle cx="185" cy="108" r="9" fill="{LAMP}"/></g>'
    return f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})"><g filter="url(#glow)">{shell}</g>{seats}{you}{cart}</g></g>'


def mountain(gid=""):
    i = f' id="{gid}"' if gid else ""
    slope = "M -100 1700 L 300 1250 L 520 1380 L 900 1000 L 1180 1200 L 1180 2000 L -100 2000 Z"
    trees = "".join(f'<path d="M {x} {y} L {x - 30} {y + 70} L {x + 30} {y + 70} Z M {x} {y + 30} L {x - 40} {y + 110} L {x + 40} {y + 110} Z" fill="#0a140e" stroke="#4ACF7A" stroke-width="4"/>'
                    for x, y in ((140, 1420), (230, 1330), (440, 1360), (620, 1270), (760, 1140), (880, 1060), (1000, 1110), (560, 1330)))
    return f'<g{i}>' + glow(N(slope, fill="#d8dce6", red=ICE, core=ICE_CORE, sw=10, cw=3), f="glowB") + f'<g filter="url(#glowS)">{trees}</g></g>'


# ---------------------------------------------------------------- S01 cold open: the cabin piece tumbling through clouds, close → pull out
s, e = 0.0, cut(12)
svg = clouds("s01-cl", 1, 14, 300, 2200) + streaks("s01-st", 1) + piece("p1", 540, 1050, 1.3)
ep.scene("s01", s, e, svg, origin="55% 55%", custom_cam=True)
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.2}},{{scale:2.3,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#p1",{{rotation:-20,svgOrigin:"540 1050"}},{{rotation:200,svgOrigin:"540 1050",duration:{e:.3f},ease:"none",immediateRender:false}},0);')
ep.js(f'tl.fromTo("#s01-cl",{{y:300}},{{y:-900,duration:{e:.3f},ease:"none",immediateRender:false}},0);')
ep.js(f'tl.fromTo("#s01-st",{{y:0}},{{y:-1400,duration:{e:.3f},ease:"none",immediateRender:false}},0);')
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("wind_roar.mp3", 0, 0.9)
ep.cue("sub.wav", 0, 0.6)

# ---------------------------------------------------------------- S02 January 26th, 1972
s, e = cut(12), cut(15)
html = '<div class="num" id="s02-d" style="top:600px;font-size:120px;">JANUARY 26, 1972</div><div class="lbl" style="top:740px;">ALTITUDE 10,160 M</div>'
svg = clouds("s02-cl", 2, 8, 1300, 1800) + plane("pl2", 540, 1100, 1.0)
ep.scene("s02", s, e, svg, html, origin="50% 55%")
ep.pop("#s02-d", s + 0.02, 0.18, 0.8)
ep.js(f'tl.fromTo("#s02-cl",{{x:0}},{{x:-260,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S03 you're a flight attendant, twenty-two years old
s, e = cut(15), cut(22)
cap = '<path d="M -50 -626 L 50 -626 L 40 -660 L -40 -660 Z" fill="#1a2a5a" stroke="#E6EEFF" stroke-width="4"/>'
svg = mascot("m3", 360, 1520, 1.0, pose=dict(uarmL=10, uarmR=-10)) + f'<g transform="translate(360,1520)">{cap}</g>'
html = ('<div class="lbl" id="s03-l" style="top:760px;left:540px;width:540px;color:#FFE08A;">FLIGHT ATTENDANT</div>'
        '<div class="num" id="s03-n" style="top:900px;left:540px;width:540px;font-size:200px;">22</div><div class="lbl" style="top:1110px;left:540px;width:540px;">YEARS OLD</div>')
ep.scene("s03", s, e, svg, html, origin="50% 55%")
ep.show("#s03-l", W(17) - 0.05, 0.2)
ep.counter("#s03-n", W(19) - 0.1, 0.5, 0, 22, "n")
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S04 at ten thousand meters a bomb tears the plane apart
s, e = cut(22), cut(32)
html = '<div class="num" style="top:600px;font-size:110px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">10,000 M</div>'
svg = clouds("s04-cl", 4, 8, 1350, 1800) + plane("pl4", 540, 1050, 1.05)
tb = W(27) - 0.05
ep.scene("s04", s, e, svg, html, origin="50% 55%", fx=[(tb, tb + 0.8, "sparks", dict(cx=470, cy=1050, n=60, r=500, dur=0.8, color="#FFB040", g=200)),
                                                       (tb, e, "fire", dict(cx=470, base=1100, w=200, h=220, n=6, amp=1.0, sp=8, grow=0.3)),
                                                       (tb, e, "smoke", dict(n=12, cx=470, base=1050, w=200, h=500, r0=50, r1=180, life=2, alpha=0.4))])
ep.js(f'tl.to("#pl4-a",{{attr:{{transform:"translate(-150 150) rotate(-35 -150 0)"}},duration:{e - tb:.3f},ease:"power2.out"}},{tb:.3f});')
ep.js(f'tl.to("#pl4-b",{{attr:{{transform:"translate(-20 200) rotate(45 0 0)"}},duration:{e - tb:.3f},ease:"power2.in"}},{tb:.3f});')
ep.js(f'tl.to("#pl4-c",{{attr:{{transform:"translate(150 90) rotate(25 150 0)"}},duration:{e - tb:.3f},ease:"power2.out"}},{tb:.3f});')
ep.flash(tb, 0.9, 0.6)
ep.shake("#s04-shake", tb, 0.6, 22)
ep.cue("metal_tear.mp3", tb - 0.05, 1.0)
ep.cue("impact-bass-1.mp3", tb, 0.9)
ep.cue("wind_roar.mp3", tb + 0.4, 0.5)
ep.floor(s, 0.0, 0.0)
ep.floor(tb, 0.4, 0.6, 0.1)

# ---------------------------------------------------------------- S05 outside it's minus fifty degrees — almost no air
s, e = cut(32), cut(43)
html = ('<div class="num" id="s05-t" style="top:600px;font-size:200px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">0°C</div><div class="lbl" style="top:810px;">AIR TEMPERATURE</div>'
        '<div class="lbl" style="top:1160px;">AIR PRESSURE</div><div class="num" id="s05-p" style="top:1330px;font-size:110px;color:#F5F5F5;">100%</div>')
bar = f'<rect x="190" y="1220" width="700" height="70" fill="#1a1416" stroke="#F2EEEA" stroke-width="3"/><rect id="s05-bar" x="190" y="1220" width="700" height="70" fill="{ICE}" filter="url(#glowB)"/>'
ep.scene("s05", s, e, bar, html, origin="50% 55%", fx=[(s, e, "ash", SNOW)])
ep.js(f'(function(){{var el=document.getElementById("s05-t");var o={{v:0}};tl.to(o,{{v:-50,duration:{WE(36) - W(34) + 0.2:.3f},ease:"expo.out",onUpdate:function(){{var n=Math.round(o.v);el.textContent=(n<0?"−":"")+Math.abs(n)+"°C";}}}},{W(34) - 0.1:.3f});}})();')
ep.js(f'tl.to("#s05-bar",{{scaleX:0.26,transformOrigin:"0% 50%",duration:{WE(42) - W(38) + 0.2:.3f},ease:"power2.out"}},{W(38) - 0.1:.3f});')
ep.counter("#s05-p", W(38) - 0.1, WE(42) - W(38) + 0.2, 100, 26, "pct", "power2.out")
ep.cue("wind_roar.mp3", s, 0.4)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S06 trapped in a piece of the cabin, pinned by a food cart
s, e = cut(43), cut(56)
svg = piece("p6", 540, 1100, 2.0)
ep.scene("s06", s, e, svg, origin="62% 62%", fx=[(s, e, "ash", dict(SNOW, n=40))], custom_cam=True)
ep.js(f'tl.fromTo("#s06-cam",{{scale:1.0}},{{scale:1.06,duration:{W(51) - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s06-cam",{{scale:1.6,duration:0.6,ease:"power2.inOut"}},{W(51) - 0.1:.3f});')
for k in range(int((e - s) / 0.4)):
    ep.js(f'tl.to("#p6",{{rotation:{[-4, 3, -2, 5][k % 4]},svgOrigin:"540 1100",duration:0.4,ease:"sine.inOut"}},{s + k * 0.4:.3f});')
ep.cue("metal_tear.mp3", W(51), 0.4)
ep.cue("wind_roar.mp3", s, 0.6)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S07 and you fall — ten kilometers, straight down
s, e = cut(56), cut(63)
html = '<div class="num" id="s07-n" style="top:600px;font-size:150px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">10,160 M</div>'
svg = clouds("s07-cl", 7, 16, 300, 2600) + streaks("s07-st", 7, 40) + piece("p7", 540, 1150, 0.9)
ep.scene("s07", s, e, svg, html, origin="50% 55%")
ep.js(f'tl.fromTo("#s07-cl",{{y:600}},{{y:-1600,duration:{e - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo("#s07-st",{{y:0}},{{y:-2200,duration:{e - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo("#p7",{{rotation:0,svgOrigin:"540 1150"}},{{rotation:-540,svgOrigin:"540 1150",duration:{e - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'(function(){{var el=document.getElementById("s07-n");var o={{v:10160}};tl.to(o,{{v:0,duration:{e - s - 0.1:.3f},ease:"power1.in",onUpdate:function(){{el.textContent=Math.round(o.v).toLocaleString("en-US")+" M";}}}},{s + 0.05:.3f});}})();')
ep.cue("shaft_fall.mp3", s, 0.5)
ep.cue("wind_roar.mp3", s, 0.9)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S08 the wreckage smashes into a snowy, wooded mountainside
s, e = cut(63), cut(71)
ti = W(65)
svg = mountain() + f'<g id="s08-fall"><g id="s08-rot" transform="rotate(-160 520 1270)">{piece("p8", 520, 1270, 0.55)}</g></g>'
ep.scene("s08", s, e, svg, origin="50% 62%", fx=[(ti, ti + 0.9, "sparks", dict(cx=520, cy=1290, n=70, r=420, dur=0.9, color="#E6EEFF", g=300)),
                                                 (s, e, "ash", dict(SNOW, n=60, sp=120))])
ep.js(f'gsap.set("#s08-fall",{{x:-500,y:-1000}});')
ep.js(f'tl.to("#s08-fall",{{x:0,y:0,duration:{ti - s:.3f},ease:"power2.in"}},{s:.3f});')
ep.js(f'tl.to("#s08-rot",{{attr:{{transform:"rotate(-12 520 1270)"}},duration:{ti - s:.3f},ease:"power1.in"}},{s:.3f});')
ep.shake("#s08-shake", ti, 0.7, 24)
ep.flash(ti, 0.5, 0.5)
ep.cue("snow_impact.mp3", ti - 0.05, 1.0)
ep.cue("impact-bass-1.mp3", ti, 0.9)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S09 a man hears screaming — it's you
s, e = cut(71), cut(77)
beam = '<path id="s09-beam" d="M 230 1290 L 560 1180 L 560 1340 Z" fill="#FFF1C8" opacity="0" filter="url(#soft2)"/>'
rings = "".join(f'<ellipse class="s09-r" cx="620" cy="1260" rx="60" ry="40" fill="none" stroke="#FF3B36" stroke-width="6" filter="url(#glowS)" opacity="0"/>' for _ in range(5))
svg = mountain() + piece("p9", 640, 1250, 0.5) + f'<g>{mascot("m9", 200, 1470, 0.4, style="dim", pose=dict(uarmR=-80, farmR=-10))}</g>' + beam + rings
ep.scene("s09", s, e, svg, origin="45% 65%", drift=0.03, fx=[(s, e, "ash", dict(SNOW, n=50, sp=100))])
ep.js(f'tl.fromTo(".s09-r",{{scale:0.4,opacity:1,svgOrigin:"620 1260"}},{{scale:4,opacity:0,svgOrigin:"620 1260",duration:1.0,stagger:0.25,ease:"power2.out",immediateRender:false}},{W(73) - 0.1:.3f});')
ep.js(f'tl.to("#s09-beam",{{opacity:0.55,duration:0.3}},{W(75) - 0.1:.3f});')
ep.cue("impact-bass-2.mp3", W(75), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S10 skull fractured, legs broken, three vertebrae crushed
s, e = cut(77), cut(89)
y0, sc = 1640, 1.35
crack = f'<g id="s10-sk" opacity="0" filter="url(#glowS)"><path d="M 520 {y0 - 600 * sc:.0f} L 548 {y0 - 570 * sc:.0f} L 530 {y0 - 545 * sc:.0f} L 556 {y0 - 520 * sc:.0f}" fill="none" stroke="#FFFFFF" stroke-width="7"/></g>'
legs = f'<g id="s10-lg" opacity="0" filter="url(#glowS)">' + "".join(line(x - 26, y0 - 130 * sc, x + 26, y0 - 110 * sc, "#FFFFFF", 7) for x in (490, 590)) + '</g>'
verts = f'<g id="s10-vt" opacity="0">' + "".join(f'<circle cx="540" cy="{y0 - (330 + k * 19) * sc:.0f}" r="13" fill="#FF2A33" filter="url(#glow)"/>' for k in range(3)) + '</g>'
svg = mascot("m10", 540, y0, sc, style="xray") + crack + legs + verts
html = ('<div class="lbl" id="s10-a" style="top:600px;left:640px;width:420px;text-align:left;color:#FF6A6A;">SKULL</div>'
        '<div class="lbl" id="s10-b" style="top:1430px;left:700px;width:380px;text-align:left;color:#FF6A6A;">LEGS</div>'
        '<div class="lbl" id="s10-c" style="top:1080px;left:730px;width:350px;text-align:left;color:#FF6A6A;">3 VERTEBRAE</div>')
ep.scene("s10", s, e, svg, html, origin="50% 55%")
for sel, t in (("#s10-sk", W(78)), ("#s10-a", W(78)), ("#s10-lg", W(82)), ("#s10-b", W(82)), ("#s10-vt", W(85)), ("#s10-c", W(85))):
    ep.show(sel, t - 0.05, 0.15)
for t in (W(78), W(82), W(85)):
    ep.shake("#s10-shake", t - 0.05, 0.25, 10)
    ep.cue("impact-bass-2.mp3", t - 0.05, 0.6)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S11 but you're alive — the only survivor out of 28
s, e = cut(89), cut(99)
icons = ""
for k in range(28):
    x, y = 210 + (k % 7) * 110, 860 + (k // 7) * 150
    cls = "s11-you" if k == 17 else "s11-p"
    icons += f'<g class="{cls}"><circle cx="{x}" cy="{y - 30}" r="18" fill="#2A2426" stroke="{RED}" stroke-width="5"/><path d="M {x - 28} {y + 40} Q {x} {y - 14} {x + 28} {y + 40} Z" fill="#2A2426" stroke="{RED}" stroke-width="5"/></g>'
html = '<div class="num" id="s11-n" style="top:1450px;font-size:130px;">1 OF 28</div><div class="lbl" id="s11-l" style="top:1590px;">SURVIVED</div>'
ep.scene("s11", s, e, f'<g filter="url(#glowS)">{icons}</g>', html, origin="50% 55%")
ep.js(f'tl.to(".s11-p",{{opacity:0.12,duration:0.15,stagger:{{each:0.06,from:"random"}}}},{W(92):.3f});')
ep.js(f'tl.fromTo(".s11-you",{{scale:1,transformOrigin:"50% 50%"}},{{scale:1.5,transformOrigin:"50% 50%",duration:0.4,ease:"back.out(2)",immediateRender:false}},{W(93):.3f});')
ep.pop("#s11-n", W(94) - 0.1, 0.2, 1.4, "power3.out")
ep.show("#s11-l", W(94) - 0.1, 0.2)
ep.cue("heart.wav", W(89), 0.6)
ep.cue("riser.mp3", W(92), 0.4)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S12 still the highest fall anyone has ever survived
s, e = cut(99), cut(108)
base = 1520
hgt = lambda m: m / 10160 * 820
bars = (f'<rect id="s12-ev" x="230" y="{base - hgt(8849):.0f}" width="220" height="{hgt(8849):.0f}" fill="#1a2030" stroke="{ICE}" stroke-width="6"/>'
        f'<rect id="s12-you" x="630" y="{base - hgt(10160):.0f}" width="220" height="{hgt(10160):.0f}" fill="#3a0a0c" stroke="{RED}" stroke-width="6" filter="url(#glow)"/>'
        + hline(base, 160, 920, 8, 3) + label(340, base + 60, "EVEREST", 30, "#9FC8FF") + label(340, base + 100, "8,849 M", 26, GREY)
        + label(740, base + 60, "YOUR FALL", 30, "#FF6A6A") + label(740, base + 100, "10,160 M", 26, GREY))
html = '<div class="lbl" id="s12-l" style="top:600px;color:#FFE08A;font-size:44px;">WORLD RECORD</div>'
ep.scene("s12", s, e, bars, html, origin="50% 60%")
ep.js(f'tl.fromTo("#s12-ev, #s12-you",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:0.6,stagger:0.25,ease:"power3.out",immediateRender:false}},{s + 0.05:.3f});')
ep.pop("#s12-l", W(102), 0.2, 1.4, "power3.out")
ep.cue("impact-bass-2.mp3", W(102), 0.5)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S13 you slip into a coma — you'll never remember the fall
s, e = cut(108), cut(118)
bed = glow(N("M 140 1380 L 140 1180 M 140 1300 L 940 1300 L 940 1380", fill="none", sw=12, cw=4))
svg = bed + f'<g transform="translate(0,0)"><g transform="translate(200,1250) rotate(90)">{mascot("m13", 0, 0, 0.55, style="xray")}</g></g>'
html = '<div class="lbl" id="s13-l" style="top:600px;color:#FF6A6A;font-size:46px;">COMA</div>'
ep.scene("s13", s, e, svg, html, origin="50% 60%", drift=0.02,
         fx=[(s, e, "ecg", dict(x0=80, x1=1000, y=900, amp=110, period=520, period1=760, dur=e - s, speed=300))])
ep.show("#s13-l", W(112) - 0.05, 0.3)
ep.js(f'tl.to("#m13",{{opacity:0.45,duration:{e - W(113):.3f}}},{W(113):.3f});')
for t in (s, s + 1.1, s + 2.4, s + 3.9):
    ep.cue("beep.wav", t, 0.08)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(118), 121)
ep.write(red=["parachute", "bomb", "apart", "breathe", "trapped", "fall", "down", "mountainside", "screaming", "fractured", "broken", "crushed", "alive", "survived", "coma"])
