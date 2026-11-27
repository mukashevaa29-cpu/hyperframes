"""Episode 11 — How does it feel? When you wake up buried alive."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa
from lib import brain as brain_svg

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
SOIL, WOOD = "#120a07", "#1c0f08"
GRAIN = "#8a5a36"
LAMP, LAMP_CORE = "#E8B040", "#FFE08A"
DIRT = dict(n=50, sp=120, color="#6a5446", y0=780)


def ground(y=760, seed=1):
    r = random.Random(seed)
    soil = f'<rect x="-100" y="{y}" width="1280" height="1300" fill="{SOIL}"/>'
    strata = "".join(f'<path d="M -40 {y + 120 + k * 150} Q 300 {y + 100 + k * 150} 540 {y + 130 + k * 150} T 1120 {y + 110 + k * 150}" fill="none" stroke="#3a1a10" stroke-width="4" opacity="0.8"/>' for k in range(7))
    stones = "".join(f'<ellipse cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(y + 60, y + 1100):.0f}" rx="{r.uniform(8, 22):.0f}" ry="{r.uniform(6, 14):.0f}" fill="#2a1a12" stroke="#4a2a1a" stroke-width="3"/>' for _ in range(26))
    grass = "".join(line(x, y, x + r.uniform(-8, 8), y - r.uniform(14, 30), "#FB2945", 4) for x in range(0, 1081, 26))
    return soil + strata + stones + glow(grass, f="glowS") + hline(y, sw=10, cw=4)


def tombstone(x, y, gid=""):
    d = f"M {x - 80} {y} L {x - 80} {y - 170} Q {x - 80} {y - 240} {x} {y - 240} Q {x + 80} {y - 240} {x + 80} {y - 170} L {x + 80} {y} Z"
    i = f' id="{gid}"' if gid else ""
    return f'<g{i}>' + glow(N(d, fill="#151313", red="#9a928c", core="#d8d2cc", sw=8, cw=3), f="glowStone") + label(x, y - 140, "R.I.P.", 26, "#BDB5B5") + '</g>'


def coffin_side(x0, y0, x1, y1, gid=""):
    """side cross-section of the box: lid, floor, ends, planks."""
    i = f' id="{gid}"' if gid else ""
    planks = "".join(line(x0 + 20, y0 + k * (y1 - y0) / 4, x1 - 20, y0 + k * (y1 - y0) / 4, "#3a2214", 3) for k in range(1, 4))
    box = N(f"M {x0} {y0} L {x1} {y0} L {x1} {y1} L {x0} {y1} Z", fill="none", sw=12, cw=4)
    return f'<g{i}><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#070404"/>{planks}' + glow(box) + '</g>'


def lying(mid, x_feet, y_axis, s, pose=None, style="neon"):
    """mascot lying on its back, side view: feet left, head right."""
    p = dict(uarmL=0, farmL=0, uarmR=0, farmR=0)
    p.update(pose or {})
    return f'<g id="{mid}-w"><g transform="translate({x_feet},{y_axis}) rotate(90)">{mascot(mid, 0, 0, s, pose=p, style=style)}</g></g>'


def face(gid, cx=540, cy=1150, mouth_open=False):
    head = glow(f'<ellipse cx="{cx}" cy="{cy}" rx="300" ry="370" fill="#2A2426" stroke="{RED}" stroke-width="18"/><ellipse cx="{cx}" cy="{cy}" rx="300" ry="370" fill="none" stroke="{CORE}" stroke-width="5"/>')
    eyes = ""
    for sx in (-1, 1):
        ex = cx + sx * 120
        eyes += (f'<g class="{gid}-eye"><ellipse cx="{ex}" cy="{cy - 60}" rx="78" ry="56" fill="#ECE6E5" stroke="{CORE}" stroke-width="5"/>'
                 f'<circle class="{gid}-iris" cx="{ex}" cy="{cy - 60}" r="34" fill="#D32620"/><circle class="{gid}-pup" cx="{ex}" cy="{cy - 60}" r="14" fill="#160404"/></g>')
    mouth = (f'<ellipse id="{gid}-mouth" cx="{cx}" cy="{cy + 170}" rx="{70 if mouth_open else 60}" ry="{90 if mouth_open else 14}" fill="#0a0505" stroke="{CORE}" stroke-width="5"/>')
    return f'<g id="{gid}">{head}<g filter="url(#glowS)">{eyes}</g>{mouth}</g>'


HAND = ("M -70 120 L -70 0 Q -70 -20 -55 -24 L -55 -150 Q -55 -170 -38 -170 Q -22 -170 -22 -150 L -22 -40 L -12 -40 L -12 -185 Q -12 -205 5 -205 Q 22 -205 22 -185 "
        "L 22 -40 L 32 -40 L 32 -165 Q 32 -185 49 -185 Q 66 -185 66 -165 L 66 -30 L 76 -30 L 76 -120 Q 76 -140 92 -140 Q 108 -140 108 -120 L 108 40 Q 108 80 90 120 Z")


def hand(gid, x, y, s=1.0, flip=False):
    sx = -s if flip else s
    return f'<g id="{gid}"><g transform="translate({x},{y}) scale({sx},{s})">' + glow(N(HAND, fill="#2a0a0c", sw=12, cw=4)) + '</g></g>'


# ---------------------------------------------------------------- S01 cold open: the coffin under the earth, close → pull out
s, e = 0.0, cut(10)
svg = (ground(760) + tombstone(540, 762) + coffin_side(230, 1290, 850, 1450, "s01-box")
       + lying("m1", 250, 1370, 0.5, pose=dict(uarmL=24, farmL=6, uarmR=0)))
ep.scene("s01", s, e, svg, origin="50% 71%", custom_cam=True, fx=[(s, e, "ash", dict(DIRT, n=40, sp=80, y0=800))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.5}},{{scale:2.6,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
for k, t in enumerate((0.05, 0.55, 1.1, 2.1, 2.6)):
    if t < e:
        ep.shake("#s01-shake", t, 0.2, 8)
        ep.cue("lid_knock.mp3", t, 0.8)
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("sub.wav", 0, 0.7)
ep.cue("dirt_thud.mp3", W(6), 0.6)

# ---------------------------------------------------------------- S02 you open your eyes — total darkness
s, e = cut(10), cut(16)
svg = face("s02f") + '<rect id="s02-black" x="-100" y="-100" width="1280" height="2200" fill="#010101" opacity="0"/>'
ep.scene("s02", s, e, svg, origin="50% 55%", drift=0.03)
ep.js(f'gsap.set(".s02f-eye",{{scaleY:0.06,transformOrigin:"50% 50%"}});')
ep.js(f'tl.to(".s02f-eye",{{scaleY:1,transformOrigin:"50% 50%",duration:0.35,ease:"power3.out"}},{W(11) - 0.05:.3f});')
ep.js(f'tl.to(".s02f-pup",{{attr:{{r:30}},duration:0.6,ease:"power2.out"}},{W(14):.3f});')
ep.js(f'tl.to("#s02-black",{{opacity:0.93,duration:0.5,ease:"power2.in"}},{W(14):.3f});')
ep.cue("sub.wav", W(14), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S03 you reach up — wood — inches from your face
s, e = cut(16), cut(24)
x0, x1, lid, flo = 60, 1020, 1040, 1330
sc = 0.95
grain = "".join(f'<path class="s03-g" d="M {x0 + 30} {lid - 40 + k * 14} Q 300 {lid - 50 + k * 14} 540 {lid - 36 + k * 14} T {x1 - 30} {lid - 44 + k * 14}" fill="none" stroke="{GRAIN}" stroke-width="3" opacity="0"/>' for k in range(4))
lid_board = f'<rect x="{x0}" y="{lid - 70}" width="{x1 - x0}" height="70" fill="{WOOD}"/>' + grain + glow(N(f"M {x0} {lid} L {x1} {lid}", sw=12, cw=4), gid="s03-lid")
gap = f'<g id="s03-gap">' + line(870, lid + 6, 870, 1112, "#FFE08A", 5) + line(850, lid + 22, 870, lid + 6, "#FFE08A", 5) + line(890, lid + 22, 870, lid + 6, "#FFE08A", 5) + line(850, 1096, 870, 1112, "#FFE08A", 5) + line(890, 1096, 870, 1112, "#FFE08A", 5) + label(910, 1090, "INCHES", 30, LAMP_CORE, "start") + '</g>'
svg = (coffin_side(x0, lid, x1, flo) + lid_board + lying("m3", 140, 1210, sc) + gap)
ep.scene("s03", s, e, svg, origin="50% 60%", drift=0.02)
ep.rot("#m3-uarmL", W(17) - 0.1, 0.45, 14, "power2.out")
ep.rot("#m3-farmL", W(17) - 0.1, 0.45, 10, "power2.out")
ep.js(f'tl.to(".s03-g",{{opacity:0.9,duration:0.2}},{W(19) - 0.05:.3f});')
ep.flash(W(19) - 0.05, 0.15, 0.3)
ep.shake("#s03-shake", W(19) - 0.05, 0.2, 6)
ep.cue("lid_knock.mp3", W(19) - 0.08, 0.9)
ep.show("#s03-gap", W(20) - 0.05, 0.2)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S04 you're in a coffin — six feet under
s, e = cut(24), cut(31)
yg, ycof = 700, 1430
ruler = (line(980, yg, 980, ycof, CORE, 5) + "".join(line(960, yg + k * (ycof - yg) / 6, 1000, yg + k * (ycof - yg) / 6, CORE, 5) for k in range(7)))
html = '<div class="num" id="s04-n" style="top:1490px;left:640px;width:420px;font-size:120px;text-align:right;">0 FT</div>'
svg = ground(yg, 4) + tombstone(540, yg + 2) + coffin_side(250, ycof - 140, 830, ycof + 20) + lying("m4", 270, ycof - 60, 0.45) + glow(ruler, f="glowS")
ep.scene("s04", s, e, svg, html, origin="50% 70%", fx=[(s, e, "ash", dict(DIRT, y0=yg + 20))])
ep.js(f'(function(){{var el=document.getElementById("s04-n");var o={{v:0}};tl.to(o,{{v:6,duration:{WE(30) - W(28) + 0.2:.3f},ease:"power2.out",onUpdate:function(){{el.textContent=Math.round(o.v)+" FT";}}}},{W(28) - 0.1:.3f});}})();')
for t in (s + 0.2, W(27), W(29)):
    ep.cue("dirt_thud.mp3", t, 0.55)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S05 you scream — no one hears you
s, e = cut(31), cut(37)
rings = "".join(f'<ellipse class="s05-r" cx="540" cy="1360" rx="120" ry="60" fill="none" stroke="#FF3B36" stroke-width="6" filter="url(#glowS)" opacity="0"/>' for _ in range(5))
walker = f'<g id="s05-wk">{mascot("m5w", 0, 0, 0.22, style="dim", pose=dict(thighL=20, thighR=-20, uarmL=15, uarmR=-15))}</g>'
svg = ground(760, 5) + tombstone(540, 762) + coffin_side(250, 1290, 830, 1450) + lying("m5", 270, 1370, 0.45, pose=dict(uarmL=24, farmL=6)) + rings + f'<g transform="translate(760,760)">{walker}</g>'
ep.scene("s05", s, e, svg, origin="50% 60%")
ep.js(f'tl.fromTo(".s05-r",{{scale:0.3,opacity:1,svgOrigin:"540 1360"}},{{scale:3.2,opacity:0,svgOrigin:"540 1360",duration:1.1,stagger:0.22,ease:"power2.out",immediateRender:false}},{W(32) - 0.1:.3f});')
ep.js(f'tl.fromTo("#s05-wk",{{x:0}},{{x:-1000,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
for k in range(int((e - s) / 0.25)):
    ep.rot("#m5w-thighL", s + k * 0.25, 0.25, 22 if k % 2 else -22, "sine.inOut")
    ep.rot("#m5w-thighR", s + k * 0.25, 0.25, -22 if k % 2 else 22, "sine.inOut")
ep.shake("#s05-shake", W(32) - 0.1, 0.5, 10)
ep.cue("impact-bass-2.mp3", W(32) - 0.1, 0.6)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S06 a coffin holds about five hours of air — if you stay calm
s, e = cut(37), cut(49)
ep.timer("s06", s, e, W(41) - 0.1, WE(42), 0, 5, "h", "HOURS OF AIR", 1.0)
ep.scenes[-1]["html"] += '<div class="lbl" id="s06-calm" style="top:1360px;color:#FFE08A;font-size:46px;">IF YOU STAY CALM</div>'
ep.pop("#s06-calm", W(45) - 0.05, 0.2, 0.7)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S07 but you don't — you panic, you breathe faster
s, e = cut(49), cut(59)
ep.lungs("s07", s, e, t_breath=W(54), label_txt="LUNGS")
ep.scenes[-1]["html"] += ('<div class="num" id="s07-n" style="top:1440px;font-size:120px;">12</div><div class="lbl" style="top:1570px;font-size:32px;">BREATHS PER MINUTE</div>'
                          '<div class="num" id="s07-h" style="top:600px;left:640px;width:400px;font-size:80px;color:#FFE08A;text-shadow:0 0 18px rgba(232,176,64,.8);">5:00</div>'
                          '<div class="lbl" style="top:690px;left:640px;width:400px;font-size:30px;">HOURS OF AIR</div>')
t, per = W(54), 0.7
while t < e - 0.1:
    ep.js(f'tl.fromTo("#s07-lungs",{{scale:1.1,transformOrigin:"50% 40%"}},{{scale:0.96,duration:{per * 0.9:.3f},ease:"sine.inOut",immediateRender:false}},{t:.3f});')
    t += per
    per = max(0.28, per * 0.86)
ep.counter("#s07-n", W(54), e - W(54), 12, 40, "n", "power1.in")
ep.js(f'(function(){{var el=document.getElementById("s07-h");var o={{v:300}};tl.to(o,{{v:90,duration:{e - W(55):.3f},ease:"power2.in",onUpdate:function(){{var n=Math.round(o.v);el.textContent=Math.floor(n/60)+":"+(n%60<10?"0":"")+(n%60);}}}},{W(55):.3f});}})();')
ep.cue("riser.mp3", W(54), 0.5)
ep.floor(s, 0.35, 0.3)

# ---------------------------------------------------------------- S08 every breath fills the box with carbon dioxide
s, e = cut(59), cut(67)
HEX = "M 540 640 L 700 760 L 660 1640 L 420 1640 L 380 760 Z"
box = glow(N(HEX, fill="#070404", sw=12, cw=4)) + f'<clipPath id="s08-cp"><path d="{HEX}"/></clipPath>'
gas = f'<g clip-path="url(#s08-cp)"><rect id="s08-gas" x="300" y="640" width="480" height="1000" fill="#7a8a5a" opacity="0.0"/></g>'
body = f'<g transform="translate(540,1600) scale(1)">{mascot("m8", 0, 0, 1.25, pose=dict(uarmL=8, uarmR=-8))}</g>'
bar = (f'<rect x="790" y="760" width="56" height="700" fill="#1a1416" stroke="#F2EEEA" stroke-width="3"/>'
       f'<rect id="s08-bar" x="790" y="760" width="56" height="700" fill="#9aae6a" opacity="0.9"/>' + label(818, 1520, "CO₂", 34, "#C8D8A0"))
svg = box + body + gas + bar
ep.scene("s08", s, e, svg, origin="50% 55%", fx=[(W(60), e, "smoke", dict(n=16, cx=540, base=1500, w=220, h=700, r0=40, r1=140, life=2.2, alpha=0.35, rgb="150,170,110"))])
ep.js(f'gsap.set("#s08-bar",{{scaleY:0.04,transformOrigin:"50% 100%"}});')
ep.js(f'tl.to("#s08-bar",{{scaleY:1,transformOrigin:"50% 100%",duration:{e - W(60):.3f},ease:"power1.in"}},{W(60):.3f});')
ep.js(f'tl.to("#s08-gas",{{opacity:0.35,duration:{e - W(60):.3f},ease:"power1.in"}},{W(60):.3f});')
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S09a your head starts pounding
s, e = cut(67), cut(71)
ep.scene("s09", s, e, brain_svg(540, 1000, 520, 440, gid="s09-b", seed=11), origin="50% 50%")
t = s
while t < e - 0.05:
    ep.js(f'tl.fromTo("#s09-b",{{scale:1.14,svgOrigin:"540 1000"}},{{scale:1,duration:0.3,ease:"power3.out",immediateRender:false}},{t:.3f});')
    ep.flash(t, 0.12, 0.25)
    ep.cue("heart.wav", t, 0.8)
    t += 0.42
ep.floor(s, 0.5, 0.5)

# ---------------------------------------------------------------- S09b your hands go numb
s, e = cut(71), cut(75)
svg = hand("s10-hL", 330, 1180, 1.4, flip=True) + hand("s10-hR", 750, 1180, 1.4)
ep.scene("s10", s, e, svg, origin="50% 55%", fx=[(s, e, "sparks", dict(cx=540, cy=1050, n=40, r=380, dur=0.9, color="#E6EEFF", g=0)),
                                                  (W(73), e, "sparks", dict(cx=540, cy=1050, n=30, r=380, dur=0.9, color="#E6EEFF", g=0))])
ep.js(f'tl.to("#s10-hL path, #s10-hR path",{{attr:{{stroke:"#6a6462"}},duration:{e - W(73):.3f}}},{W(73):.3f});')
ep.js(f'tl.to("#s10-hL path, #s10-hR path",{{attr:{{fill:"#151313"}},duration:{e - W(73):.3f}}},{W(73):.3f});')
ep.floor(s, 0.3, 0.0)
ep.floor(W(73), 0.1, 0.0, 0.8)

# ---------------------------------------------------------------- S10 you claw at the lid until your nails break
s, e = cut(75), cut(84)
planks = "".join(f'<rect x="-40" y="{560 + k * 230}" width="1160" height="222" fill="{WOOD}" stroke="#3a2214" stroke-width="6"/>' for k in range(6))
grain = "".join(f'<path d="M -40 {600 + k * 46} Q 300 {580 + k * 46} 560 {610 + k * 46} T 1120 {590 + k * 46}" fill="none" stroke="#3a2214" stroke-width="3"/>' for k in range(28))
r10 = random.Random(10)
scr = ""
for k in range(14):
    x = 300 + k * 36 + r10.uniform(-10, 10)
    y0 = r10.uniform(820, 900)
    scr += f'<path class="s11-s" d="M {x:.0f} {y0:.0f} Q {x + r10.uniform(-20, 20):.0f} {y0 + 180:.0f} {x + r10.uniform(-30, 30):.0f} {y0 + r10.uniform(320, 420):.0f}" fill="none" stroke="#FF3B36" stroke-width="{r10.uniform(4, 8):.1f}" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" filter="url(#glowS)"/>'
svg = planks + grain + scr + hand("s11-h", 540, 1500, 1.3)
ep.scene("s11", s, e, svg, origin="50% 55%", drift=0.03)
ep.js(f'tl.to(".s11-s",{{strokeDashoffset:0,duration:0.3,stagger:{(W(83) - W(76)) / 14:.3f},ease:"power2.out"}},{W(76):.3f});')
for k in range(int((W(83) - s) / 0.3)):
    ep.js(f'tl.to("#s11-h",{{y:{-160 if k % 2 == 0 else 60},x:{(k % 3 - 1) * 40},duration:0.3,ease:"sine.inOut"}},{s + k * 0.3:.3f});')
ep.cue("scratch_wood.mp3", W(76), 0.9)
ep.cue("scratch_wood.mp3", W(76) + 2.6, 0.9)
tb = W(83) - 0.05
ep.js(f'tl.to(".s11-s",{{attr:{{"stroke-width":12}},duration:0.15}},{tb:.3f});')
ep.shake("#s11-shake", tb, 0.4, 14)
ep.flash(tb, 0.3, 0.4)
ep.cue("impact-bass-1.mp3", tb, 0.8)
ep.floor(s, 0.35, 0.2)

# ---------------------------------------------------------------- S11 in the 1800s they built coffins with a bell — a string ran to your hand
s, e = cut(84), cut(111)
post = (glow(N("M 640 760 L 640 560 L 760 560", fill="none", red="#9a928c", core="#d8d2cc", sw=10, cw=4), f="glowStone")
        + f'<g id="s12-bell"><g transform="translate(760,560)">' + glow(f'<path d="M -46 110 Q -44 30 0 24 Q 44 30 46 110 Z" fill="#3a2a0a" stroke="{LAMP}" stroke-width="7"/><circle cx="0" cy="124" r="12" fill="{LAMP_CORE}"/>' + line(0, 0, 0, 24, LAMP, 5), f="glowG") + '</g></g>')
string = f'<path id="s12-str" d="M 760 690 L 760 760 L 760 1330 L 700 1330" pathLength="1" fill="none" stroke="{LAMP_CORE}" stroke-width="4" stroke-dasharray="1" stroke-dashoffset="1" filter="url(#glowG)"/>'
html = '<div class="num" id="s12-y" style="top:620px;left:0;width:620px;font-size:120px;">1800s</div>'
svg = ground(760, 12) + coffin_side(250, 1290, 830, 1450) + lying("m12", 270, 1370, 0.45) + post + string
ep.scene("s12", s, e, svg, html, origin="62% 62%", drift=0.012)
ep.pop("#s12-y", W(86) - 0.05, 0.2, 1.4, "power3.out")
ep.pop("#s12-bell", W(98) - 0.1, 0.25, 0.3)
ep.cue("bell_small.mp3", W(98), 0.5)
ep.js(f'tl.to("#s12-str",{{strokeDashoffset:0,duration:{WE(104) - W(100):.3f},ease:"power1.inOut"}},{W(100) - 0.05:.3f});')
for k in range(8):
    ep.js(f'tl.to("#s12-bell",{{rotation:{18 if k % 2 == 0 else -18},svgOrigin:"760 560",duration:0.12,ease:"sine.inOut"}},{W(108) - 0.1 + k * 0.12:.3f});')
ep.js(f'tl.to("#s12-bell",{{rotation:0,svgOrigin:"760 560",duration:0.2}},{W(108) - 0.1 + 8 * 0.12:.3f});')
ep.cue("bell_small.mp3", W(108) - 0.1, 0.8)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S12 you have no bell
s, e = cut(111), cut(115)
xx = f'<g id="s13-x" filter="url(#glow)">' + line(600, 380 + 60, 920, 640 + 60, "#FF3B36", 18) + line(920, 380 + 60, 600, 640 + 60, "#FF3B36", 18) + '</g>'
svg = ground(760, 12) + coffin_side(250, 1290, 830, 1450) + lying("m13", 270, 1370, 0.45) + post.replace("s12-bell", "s13-bell") + xx
ep.scene("s13", s, e, svg, origin="62% 40%", drift=0.03)
ep.pop("#s13-x", W(113) - 0.05, 0.18, 1.8, "power3.out")
ep.js(f'tl.to("#s13-bell",{{opacity:0.25,duration:0.4}},{W(114):.3f});')
ep.cue("impact-bass-2.mp3", W(113) - 0.05, 0.7)
ep.floor(s, 0.2, 0.0)

# ---------------------------------------------------------------- S13 your breathing slows — your thoughts drift away
s, e = cut(115), cut(122)
svg = face("s14f") + '<rect id="s14-dim" x="-100" y="-100" width="1280" height="2200" fill="#010101" opacity="0"/>'
ep.scene("s14", s, e, svg, origin="50% 55%", fx=[(W(118), e, "embers", dict(n=30, x0=300, x1=780, y0=500, y1=1100, sp=70))],
         custom_cam=True)
ep.js(f'tl.fromTo("#s14-cam",{{scale:1.0}},{{scale:0.86,duration:{e - s:.3f},ease:"sine.inOut",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo(".s14f-eye",{{scaleY:1,transformOrigin:"50% 50%"}},{{scaleY:0.35,transformOrigin:"50% 50%",duration:{e - s:.3f},ease:"sine.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s14-dim",{{opacity:0.55,duration:{e - s:.3f},ease:"sine.in"}},{s:.3f});')
for t in (s, s + 1.4, s + 3.2):
    ep.cue("heart.wav", t, 0.45)
ep.floor(s, 0.2, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(122), 125)
ep.write(red=["buried", "darkness", "wood", "coffin", "under", "scream", "air", "calm", "panic", "faster", "carbon", "pounding", "numb", "nails", "bell", "help", "slows"])
