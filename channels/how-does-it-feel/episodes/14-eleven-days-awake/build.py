"""Episode 14 — How does it feel? When you don't sleep for eleven days (Randy Gardner, San Diego, 1963-64)."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa
from lib import brain as brain_svg

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
GOLD, GOLD_CORE = "#E8B040", "#FFE08A"
HAND = ("M -70 120 L -70 0 Q -70 -20 -55 -24 L -55 -150 Q -55 -170 -38 -170 Q -22 -170 -22 -150 L -22 -40 L -12 -40 L -12 -185 Q -12 -205 5 -205 Q 22 -205 22 -185 "
        "L 22 -40 L 32 -40 L 32 -165 Q 32 -185 49 -185 Q 66 -185 66 -165 L 66 -30 L 76 -30 L 76 -120 Q 76 -140 92 -140 Q 108 -140 108 -120 L 108 40 Q 108 80 90 120 Z")
TROPHY = ("M 420 900 L 660 900 Q 664 1060 540 1110 Q 416 1060 420 900 Z M 420 930 Q 340 930 350 1000 Q 360 1050 430 1050 M 660 930 Q 740 930 730 1000 Q 720 1050 650 1050 "
          "M 525 1110 L 525 1180 L 555 1180 L 555 1110 M 460 1180 L 620 1180 L 620 1220 L 460 1220 Z")


def face(gid, cx=540, cy=1150, s=1.0, veins=True, frown=False, blank=False):
    head = glow(f'<ellipse cx="{cx}" cy="{cy}" rx="{300 * s:.0f}" ry="{370 * s:.0f}" fill="#2A2426" stroke="{RED}" stroke-width="18"/><ellipse cx="{cx}" cy="{cy}" rx="{300 * s:.0f}" ry="{370 * s:.0f}" fill="none" stroke="{CORE}" stroke-width="5"/>')
    eyes = ""
    for sx in (-1, 1):
        ex, ey = cx + sx * 120 * s, cy - 60 * s
        vv = ""
        if veins:
            vv = "".join(f'<path d="M {ex + sx * 76 * s:.0f} {ey + k * 12 - 12:.0f} Q {ex + sx * 50 * s:.0f} {ey + k * 16 - 20:.0f} {ex + sx * 36 * s:.0f} {ey + k * 8 - 6:.0f}" fill="none" stroke="#C2181E" stroke-width="3"/>' for k in range(3))
        iris = "#6a6462" if blank else "#D32620"
        eyes += (f'<g class="{gid}-eye"><ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{82 * s:.0f}" ry="{60 * s:.0f}" fill="#ECE6E5" stroke="{CORE}" stroke-width="5"/>{vv}'
                 f'<circle class="{gid}-iris" cx="{ex:.0f}" cy="{ey:.0f}" r="{34 * s:.0f}" fill="{iris}"/><circle class="{gid}-pup" cx="{ex:.0f}" cy="{ey:.0f}" r="{12 * s:.0f}" fill="#160404"/></g>')
    if frown:
        mouth = f'<path id="{gid}-mouth" d="M {cx - 80 * s:.0f} {cy + 190 * s:.0f} Q {cx} {cy + 120 * s:.0f} {cx + 80 * s:.0f} {cy + 190 * s:.0f}" fill="none" stroke="{CORE}" stroke-width="8" stroke-linecap="round"/>'
    else:
        mouth = f'<path id="{gid}-mouth" d="M {cx - 70 * s:.0f} {cy + 170 * s:.0f} L {cx + 70 * s:.0f} {cy + 170 * s:.0f}" fill="none" stroke="{CORE}" stroke-width="8" stroke-linecap="round"/>'
    bags = "".join(f'<path d="M {cx + sx * 120 * s - 60 * s:.0f} {cy + 10 * s:.0f} Q {cx + sx * 120 * s:.0f} {cy + 40 * s:.0f} {cx + sx * 120 * s + 60 * s:.0f} {cy + 10 * s:.0f}" fill="none" stroke="#6a2a3a" stroke-width="6"/>' for sx in (-1, 1))
    return f'<g id="{gid}">{head}{bags}<g filter="url(#glowS)">{eyes}</g>{mouth}</g>'


def day(n, sid, t):
    """'DAY n' card under the captions; returns html and schedules its pop."""
    ep.pop(f"#{sid}-day", t, 0.2, 1.5, "power3.out")
    ep.cue("tick.wav", t, 0.6)
    ep.cue("impact-bass-2.mp3", t, 0.45)
    return f'<div class="num" id="{sid}-day" style="top:570px;font-size:130px;">DAY {n}</div>'


def trophy(gid, x=0, y=0, s=1.0):
    return f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})">' + glow(N(TROPHY, fill="#2a2006", red=GOLD, core=GOLD_CORE, sw=12, cw=4), f="glowG") + '</g></g>'


def bigx(gid, x, y, r=70, w=16):
    return f'<g id="{gid}" filter="url(#glow)">' + line(x - r, y - r, x + r, y + r, "#FF3B36", w) + line(x + r, y - r, x - r, y + r, "#FF3B36", w) + '</g>'


# ---------------------------------------------------------------- S01 cold open: bloodshot eyes that won't close, glitching → pull out to the clock
s, e = 0.0, cut(11)
cx, cy, R = 540, 1520, 120
ticks = "".join(line(cx + (R - 8) * math.cos(a), cy + (R - 8) * math.sin(a), cx + (R - 26) * math.cos(a), cy + (R - 26) * math.sin(a), CORE, 5) for a in [i * math.pi / 6 for i in range(12)])
clock = glow(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#0C0A0C" stroke="{RED}" stroke-width="12"/>{ticks}') + f'<g transform="translate({cx},{cy})"><g id="s01-mh">' + line(0, 0, 0, -95, "#FF3B36", 7) + '</g><g id="s01-hh">' + line(0, 0, 0, -60, CORE, 10) + '</g><circle r="10" fill="#F2EEEA"/></g>'
svg = face("s01f", 540, 980, 0.9) + clock
ep.scene("s01", s, e, svg, origin="50% 46%", custom_cam=True)
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.4}},{{scale:2.5,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#s01-mh",{{attr:{{transform:"rotate(0)"}}}},{{attr:{{transform:"rotate(4320)"}},duration:{e:.3f},ease:"power1.in",immediateRender:false}},0);')
ep.js(f'tl.fromTo("#s01-hh",{{attr:{{transform:"rotate(0)"}}}},{{attr:{{transform:"rotate(360)"}},duration:{e:.3f},ease:"power1.in",immediateRender:false}},0);')
r1 = random.Random(1)
for t in (0.4, 1.3, 2.2, 3.6):
    ep.shake("#s01-shake", t, 0.15, 14)
    ep.flash(t, 0.12, 0.15)
    ep.cue("glitch.mp3", t, 0.5)
for k in range(int(e / 0.25)):
    ep.js(f'tl.set(".s01f-pup",{{attr:{{r:{r1.choice([8, 11, 14])}}}}},{k * 0.25:.3f});')
t = 0.0
while t < e:
    ep.cue("tick.wav", t, 0.4)
    t += 0.25
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("sub.wav", 0, 0.6)

# ---------------------------------------------------------------- S02 San Diego, 1963 — you're seventeen — you want a world record
s, e = cut(11), cut(22)
html = ('<div class="num" id="s02-y" style="top:620px;font-size:150px;">1963</div><div class="lbl" id="s02-c" style="top:785px;">SAN DIEGO</div>'
        '<div class="num" id="s02-a" style="top:1380px;left:0;width:540px;font-size:120px;">17</div><div class="lbl" id="s02-al" style="top:1510px;left:0;width:540px;font-size:30px;">YEARS OLD</div>'
        '<div class="lbl" id="s02-tl" style="top:1510px;left:540px;width:540px;font-size:30px;color:#FFE08A;">WORLD RECORD</div>')
svg = mascot("m2", 300, 1340, 0.62) + trophy("s02-t", 210, 160, 0.82)
ep.scene("s02", s, e, svg, html, origin="50% 55%")
ep.pop("#s02-y", s + 0.02, 0.2, 1.4, "power3.out")
ep.show("#s02-c", W(11), 0.2)
ep.pop("#s02-a", W(15) - 0.05, 0.18, 1.5, "power3.out")
ep.show("#s02-al", W(15), 0.2)
ep.pop("#s02-t", W(20) - 0.1, 0.25, 0.3)
ep.show("#s02-tl", W(20), 0.2)
ep.cue("riser.mp3", W(19), 0.35)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S03 no sleep — not even a nap
s, e = cut(22), cut(28)
bed = glow(N("M 220 1300 L 220 1080 M 220 1180 L 860 1180 L 860 1300 M 220 1240 L 860 1240", fill="none", sw=12, cw=4)
           + N("M 260 1180 L 260 1120 Q 260 1100 290 1100 L 400 1100 Q 430 1100 430 1130 L 430 1180", fill="#2a0a0c", sw=10, cw=3))
zz = label(700, 1010, "Z", 60, GREY) + label(770, 950, "Z", 46, GREY) + label(820, 900, "Z", 34, GREY)
html = '<div class="num" id="s03-n" style="top:1400px;font-size:110px;">0 HOURS</div><div class="lbl" style="top:1520px;">OF SLEEP</div>'
svg = bed + f'<g id="s03-z">{zz}</g>' + bigx("s03-x", 540, 1150, 220, 22)
ep.scene("s03", s, e, svg, html, origin="50% 55%")
ep.pop("#s03-x", W(23) - 0.05, 0.18, 1.6, "power3.out")
ep.js(f'tl.to("#s03-z",{{opacity:0,y:-60,duration:0.4}},{W(23):.3f});')
ep.cue("impact-bass-1.mp3", W(23) - 0.05, 0.7)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S04 day two — your eyes stop focusing
s, e = cut(28), cut(34)
html = day(2, "s04", W(28) - 0.05)
svg = f'<g id="s04-g1" opacity="0.75">{face("s04a", 540, 1240, 0.85)}</g><g id="s04-g2" opacity="0">{face("s04b", 540, 1240, 0.85)}</g>'
ep.scene("s04", s, e, svg, html, origin="50% 60%")
ep.js(f'tl.to("#s04-g2",{{opacity:0.55,x:46,y:-10,duration:{e - W(31):.3f},ease:"sine.inOut"}},{W(31) - 0.1:.3f});')
ep.js(f'tl.to("#s04-g1",{{x:-30,duration:{e - W(31):.3f},ease:"sine.inOut"}},{W(31) - 0.1:.3f});')
ep.js(f'tl.set("#s04-g1, #s04-g2",{{attr:{{filter:"url(#soft2)"}}}},{W(32):.3f});')
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S05 day three — clumsy, moody, your thoughts slip away
s, e = cut(34), cut(44)
html = day(3, "s05", W(34) - 0.05)
bub = "".join(f'<g class="s05-tb"><circle cx="{x}" cy="{y}" r="{r}" fill="#1a1416" stroke="{CORE}" stroke-width="5" filter="url(#glowS)"/></g>' for x, y, r in ((700, 900, 24), (760, 840, 34), (840, 760, 60)))
svg = f'<g id="s05-m">{mascot("m5", 470, 1560, 0.95, pose=dict(uarmL=30, uarmR=-40))}</g>' + bub
ep.scene("s05", s, e, svg, html, origin="50% 60%")
for k in range(int((W(39) - s) / 0.35)):
    ep.js(f'tl.to("#s05-m",{{rotation:{[-7, 6, -4, 8][k % 4]},svgOrigin:"470 1560",duration:0.35,ease:"sine.inOut"}},{s + k * 0.35:.3f});')
ep.js(f'tl.to("#s05-m",{{rotation:0,svgOrigin:"470 1560",duration:0.3}},{W(39) - 0.1:.3f});')
ep.js(f'tl.to("#m5-mouth",{{attr:{{ry:4}},duration:0.2}},{W(39):.3f});')
ep.js(f'tl.to("#m5 path, #m5 ellipse",{{attr:{{stroke:"#FF2A33"}},duration:0.3}},{W(39):.3f});')
ep.js(f'tl.fromTo(".s05-tb",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.2,stagger:0.1,immediateRender:false}},{W(40) - 0.1:.3f});')
ep.js('gsap.set(".s05-tb",{opacity:0});')
ep.js(f'tl.to(".s05-tb",{{x:240,y:-160,opacity:0,duration:0.9,stagger:0.1,ease:"power2.in"}},{W(42):.3f});')
ep.cue("rock_scrape.mp3", s + 0.6, 0.25)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S06 day four — a street sign turns into a person
s, e = cut(44), cut(53)
html = day(4, "s06", W(44) - 0.05)
sign = (f'<g id="s06-sign">' + glow('<rect x="470" y="880" width="140" height="700" fill="none"/>' + N("M 540 1560 L 540 900", fill="none", red=GOLD, core=GOLD_CORE, sw=14, cw=5), f="glowG")
        + glow(N("M 290 800 L 790 800 L 790 950 L 290 950 Z", fill="#0e2412", red="#4ACF7A", core="#CFF5DA", sw=12, cw=4), f="glowS") + label(540, 900, "MAIN ST", 56, "#CFF5DA") + '</g>')
person = f'<g id="s06-p" opacity="0">{mascot("m6", 540, 1560, 1.05, style="xray", pose=dict(uarmL=10, uarmR=-10))}</g>'
ep.scene("s06", s, e, sign + person, html, origin="50% 60%")
tm = W(49) - 0.1
for k, op in enumerate((1, 0, 1, 0, 1)):
    ep.js(f'tl.set("#s06-p",{{opacity:{op}}},{tm + k * 0.07:.3f});')
    ep.js(f'tl.set("#s06-sign",{{opacity:{1 - op}}},{tm + k * 0.07:.3f});')
ep.shake("#s06-shake", tm, 0.35, 16)
ep.flash(tm, 0.2, 0.3)
ep.cue("glitch.mp3", tm, 0.9)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S07 you're sure you're a famous football player
s, e = cut(53), cut(60)
ball = f'<g id="s07-ball" transform="translate(800,1000) rotate(-30)"><ellipse rx="90" ry="54" fill="#5a2a14" stroke="{CORE}" stroke-width="6"/>' + line(-40, 0, 40, 0, CORE, 5) + "".join(line(x, -12, x, 12, CORE, 4) for x in (-24, -8, 8, 24)) + '</g>'
jersey = f'<text x="540" y="1100" fill="#F2EEEA" font-family="Roboto Condensed" font-weight="900" font-size="120" text-anchor="middle">23</text>'
flashes = "".join(f'<circle class="s07-fl" cx="{x}" cy="{y}" r="10" fill="#FFFFFF" opacity="0"/>' for x, y in ((120, 700), (260, 640), (900, 680), (980, 780), (160, 860), (940, 900), (320, 760)))
svg = mascot("m7", 540, 1560, 1.25, pose=dict(uarmL=150, farmL=10, uarmR=-30, farmR=-20)) + jersey + f'<g filter="url(#glowG)">{ball}</g>' + flashes
ep.scene("s07", s, e, svg, origin="50% 55%", drift=0.03)
ep.pop("#s07-ball", W(57) - 0.1, 0.25, 0.3)
r7 = random.Random(7)
for k in range(int((e - W(57)) / 0.15)):
    ep.js(f'tl.set("#s07-cam .s07-fl",{{opacity:{r7.choice([0, 0.9, 0.4])}}},{W(57) + k * 0.15:.3f});')
ep.cue("riser.mp3", W(56), 0.4)
ep.floor(s, 0.4, 0.0)

# ---------------------------------------------------------------- S08 your brain starts shutting down in pieces, for seconds at a time
s, e = cut(60), cut(72)
spots = ((420, 900, 90), (640, 980, 100), (500, 1120, 90), (700, 860, 70), (380, 1060, 70), (600, 1180, 70))
html = '<div class="lbl" id="s08-l" style="top:1420px;color:#FF6A6A;font-size:44px;">MICROSLEEP</div>'
svg = brain_svg(540, 1020, 520, 440, gid="s08-b", seed=8) + "".join(f'<circle id="s08-o{k}" cx="{x}" cy="{y}" r="{r}" fill="#010101" opacity="0"/>' for k, (x, y, r) in enumerate(spots))
ep.scene("s08", s, e, svg, html, origin="50% 55%")
r8 = random.Random(8)
t = W(62)
while t < e - 0.3:
    k = r8.randint(0, 5)
    ep.js(f'tl.fromTo("#s08-o{k}",{{opacity:0.95}},{{opacity:0,duration:0.7,ease:"power3.in",immediateRender:false}},{t:.3f});')
    t += 0.35
ep.show("#s08-l", W(64) - 0.1, 0.2)
for k in range(int((e - W(67)) / 0.6)):
    ep.js(f'tl.fromTo("#s08-l",{{opacity:1}},{{opacity:0.25,duration:0.5,immediateRender:false}},{W(67) + k * 0.6:.3f});')
ep.cue("glitch.mp3", W(62), 0.5)
ep.cue("glitch.mp3", W(67), 0.5)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S09 while your eyes are still open
s, e = cut(72), cut(78)
svg = face("s09f", 540, 1200, 0.95) + '<rect id="s09-off" x="-100" y="-100" width="1280" height="2200" fill="#010101" opacity="0"/>'
html = '<div class="lbl" id="s09-l" style="top:1700px;color:#FF6A6A;font-size:40px;">BRAIN: OFF</div>'
ep.scene("s09", s, e, svg, html, origin="50% 55%", drift=0.03)
for t, op in ((W(73), 0.7), (W(73) + 0.6, 0.0), (W(75), 0.75), (W(75) + 0.7, 0.0)):
    ep.js(f'tl.to("#s09-off",{{opacity:{op},duration:0.25}},{t:.3f});')
ep.js(f'tl.to(".s09f-pup",{{attr:{{r:22}},duration:0.6}},{s:.3f});')
ep.show("#s09-l", W(73), 0.2)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S10 day seven — your hands tremble — your speech slurs
s, e = cut(78), cut(86)
html = day(7, "s10", W(78) - 0.05)
hands = (f'<g id="s10-h"><g transform="translate(340,1180) scale(-1.3,1.3)">' + glow(N(HAND, fill="#2a0a0c", sw=12, cw=4)) + '</g>'
         f'<g transform="translate(740,1180) scale(1.3)">' + glow(N(HAND, fill="#2a0a0c", sw=12, cw=4)) + '</g></g>')
ep.scene("s10", s, e, hands, html, origin="50% 55%", fx=[(W(83) - 0.1, e, "ecg", dict(x0=80, x1=1000, y=1520, amp=110))])
r10 = random.Random(10)
for k in range(int((e - W(80)) * 15)):
    ep.js(f'tl.set("#s10-h",{{x:{r10.uniform(-7, 7):.1f},y:{r10.uniform(-6, 6):.1f}}},{W(80) + k / 15:.3f});')
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S11 day eleven — 264 hours awake
s, e = cut(86), cut(94)
ep.timer("s11", s, e, W(88) - 0.1, WE(93), 0, 264, "n", "HOURS AWAKE", 1.0)
ep.scenes[-1]["html"] += '<div class="num" id="s11-day" style="top:1340px;font-size:100px;">DAY 11</div>'
ep.pop("#s11-day", W(86) - 0.05, 0.2, 1.5, "power3.out")
ep.cue("impact-bass-2.mp3", W(86) - 0.05, 0.45)
ep.floor(s, 0.4, 0.3)

# ---------------------------------------------------------------- S12 your face goes blank — you can't finish a sentence
s, e = cut(94), cut(103)
svg = face("s12f", 540, 1100, 0.8, veins=True, blank=True)
html = ('<div id="s12-tx" style="position:absolute;left:0;top:1520px;width:1080px;text-align:center;font-weight:700;font-size:58px;letter-spacing:3px;color:#F5F5F5;">'
        + "".join(f'<span class="s12-ch" style="opacity:0">{c}</span>' for c in "I'M GOING TO...") + '<span id="s12-cur" style="color:#FB2945;">|</span></div>')
ep.scene("s12", s, e, svg, html, origin="50% 55%", drift=0.02)
ep.js(f'tl.to(".s12-ch",{{opacity:1,duration:0.01,stagger:0.09}},{W(98):.3f});')
for k in range(int((e - W(98)) / 0.3)):
    ep.js(f'tl.set("#s12-cur",{{opacity:{k % 2}}},{W(98) + k * 0.3:.3f});')
ep.js(f'tl.to(".s12-ch:nth-last-child(-n+4)",{{opacity:0,duration:0.01,stagger:{{each:0.12,from:"end"}}}},{WE(102) - 0.4:.3f});')
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S13 you did it — the record is yours
s, e = cut(103), cut(110)
html = '<div class="num" id="s13-n" style="top:1310px;font-size:140px;color:#FFE08A;text-shadow:0 0 20px rgba(232,176,64,.9);">264 HOURS</div><div class="lbl" style="top:1460px;color:#FFE08A;">WORLD RECORD</div>'
ep.scene("s13", s, e, trophy("s13-t", -270, -710, 1.5), html, origin="50% 55%",
         fx=[(W(103), W(103) + 1.2, "sparks", dict(cx=540, cy=900, n=70, r=600, dur=1.2, color="#FFE08A", g=500)),
             (W(107), W(107) + 1.2, "sparks", dict(cx=540, cy=900, n=60, r=560, dur=1.2, color="#FB2945", g=500))])
ep.pop("#s13-t", W(103) - 0.05, 0.3, 0.3)
ep.pop("#s13-n", W(107) - 0.05, 0.2, 1.4, "power3.out")
ep.cue("riser.mp3", s, 0.4)
ep.cue("impact-bass-1.mp3", W(103), 0.6)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S14 you finally close your eyes
s, e = cut(110), cut(115)
svg = face("s14f", 540, 1150, 0.9)
ep.scene("s14", s, e, svg, origin="50% 55%", drift=0.03)
ep.js(f'tl.to(".s14f-eye",{{scaleY:0.04,transformOrigin:"50% 50%",duration:{e - W(112) + 0.1:.3f},ease:"power2.in"}},{W(112):.3f});')
ep.floor(s, 0.2, 0.0)
for t in (s, s + 1.2):
    ep.cue("heart.wav", t, 0.4)

# ---------------------------------------------------------------- ending
ep.ending(cut(115), 118)
ep.write(red=["sleep", "record", "nap", "focusing", "clumsy", "moody", "person", "football", "pieces", "open", "tremble", "slurs", "awake", "blank", "sentence", "yours", "eyes"])
