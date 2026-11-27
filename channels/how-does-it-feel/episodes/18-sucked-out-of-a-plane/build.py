"""Episode 18 — How does it feel? When you're sucked out of a plane window (BA Flight 5390, 1990)."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
ICE, ICE_CORE = "#5A78FF", "#E6EEFF"
LAMP, LAMP_CORE = "#E8B040", "#FFE08A"


def streaks(gid, seed, n=34, y0=500, y1=1800):
    r = random.Random(seed)
    return f'<g id="{gid}">' + "".join(line(x, y, x + r.uniform(160, 340), y, "#9FB4E6", 3, 'opacity="0.55"') for x, y in ((r.uniform(-200, 2200), r.uniform(y0, y1)) for _ in range(n))) + '</g>'


def clouds(gid, seed, n=8, y0=1300, y1=1900):
    r = random.Random(seed)
    return f'<g id="{gid}">' + "".join(f'<ellipse cx="{r.uniform(0, 2200):.0f}" cy="{r.uniform(y0, y1):.0f}" rx="{r.uniform(160, 320):.0f}" ry="{r.uniform(40, 80):.0f}" fill="#1a2030" opacity="0.8" filter="url(#soft2)"/>' for _ in range(n)) + '</g>'


def nose(gid, out=True, s_m=0.5, pose=None, style="neon"):
    """side view of the cockpit section flying right; you lie along the roof outside the window, legs inside."""
    body = "M -200 1060 L 760 1060 Q 940 1060 1000 1150 Q 960 1240 760 1250 L -200 1250 Z"
    win = '<path d="M 800 1080 L 880 1090 L 910 1130 L 820 1125 Z" fill="#0a0c14" stroke="#9FC8FF" stroke-width="5"/>'
    p = dict(uarmL=170, farmL=10, uarmR=-170, farmR=-10, thighL=4, thighR=-4)
    p.update(pose or {})
    you = (f'<g id="{gid}-you"><g transform="translate(810,1095) rotate(-80)">{mascot(gid + "-m", 0, 0, s_m, pose=p, style=style, mouth_open=True)}</g></g>' if out else "")
    portholes = "".join(f'<circle cx="{x}" cy="1150" r="14" fill="{LAMP_CORE}" opacity="0.8"/>' for x in range(-160, 700, 70))
    return f'<g id="{gid}">' + glow(N(body, fill="#0c0a0c", sw=12, cw=4)) + portholes + win + you + '</g>'


def jet(gid, x, y, s=1.0, rot=0):
    d = "M -260 0 Q -250 -26 -200 -26 L 200 -26 Q 260 -20 280 0 Q 260 16 200 20 L -200 20 Z"
    wing = "M -40 6 L 60 6 L -20 110 L -70 110 Z"
    tail = "M -230 -20 L -280 -120 L -240 -120 L -190 -24 Z"
    return f'<g id="{gid}"><g transform="translate({x},{y}) rotate({rot}) scale({s})">' + glow(N(d, fill="#0c0a0c", sw=8, cw=3) + N(wing, fill="#0c0a0c", sw=8, cw=3) + N(tail, fill="#0c0a0c", sw=8, cw=3)) + '</g></g>'


def cockpit(gid, blown=False):
    """front view from the seat: two windscreen panes, the left one is yours."""
    frame = glow(N("M 120 700 L 960 700 L 1000 1300 L 80 1300 Z", fill="#06080f", sw=12, cw=4))
    left = f'<g id="{gid}-L"><path d="M 160 740 L 520 740 L 520 1180 L 130 1180 Z" fill="#14244a" stroke="#9FC8FF" stroke-width="6" opacity="0.85"/></g>'
    right = '<path d="M 560 740 L 920 740 L 950 1180 L 560 1180 Z" fill="#14244a" stroke="#9FC8FF" stroke-width="6" opacity="0.85"/>'
    dash = f'<rect x="80" y="1300" width="920" height="180" fill="#14161c" stroke="{RED}" stroke-width="6"/>' + "".join(f'<circle cx="{x}" cy="1390" r="36" fill="none" stroke="{CORE}" stroke-width="5"/>' for x in (240, 420, 660, 840))
    return frame + left + right + dash


def bigx(gid, x, y, r=60, w=14):
    return f'<g id="{gid}" filter="url(#glow)">' + line(x - r, y - r, x + r, y + r, "#FF3B36", w) + line(x + r, y - r, x - r, y + r, "#FF3B36", w) + '</g>'


def wind_anim(gid, s, e, dist=-1600, per=0.45):
    ep.js(f'tl.fromTo("#{gid}",{{x:0}},{{x:{dist},duration:{per},repeat:{int((e - s) / per)},ease:"none",immediateRender:false}},{s:.3f});')


# ---------------------------------------------------------------- S01 cold open: you, outside the window, pinned to the roof by the wind → pull out
s, e = 0.0, cut(12)
svg = clouds("s01-cl", 1, 10, 1300, 1900) + nose("n1") + streaks("s01-w", 1, 40)
ep.scene("s01", s, e, svg, origin="66% 55%", custom_cam=True)
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.2}},{{scale:2.3,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
wind_anim("s01-w", s, e)
ep.js(f'tl.fromTo("#s01-cl",{{x:0}},{{x:-1200,duration:{e:.3f},ease:"none",immediateRender:false}},0);')
r1 = random.Random(1)
for k in range(int(e / 0.12)):
    ep.rot("#n1-m-uarmL", k * 0.12, 0.12, 170 + r1.uniform(-25, 25), "none")
    ep.rot("#n1-m-uarmR", k * 0.12, 0.12, -170 + r1.uniform(-25, 25), "none")
ep.shake("#s01-shake", 0, e, 5)
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("wind_roar.mp3", 0, 1.0)
ep.cue("sub.wav", 0, 0.6)

# ---------------------------------------------------------------- S02 June 10th, 1990
s, e = cut(12), cut(15)
html = '<div class="num" id="s02-d" style="top:600px;font-size:130px;">JUNE 10, 1990</div>'
ep.scene("s02", s, e, clouds("s02-cl", 2, 9, 1350, 1850) + jet("j2", 540, 1150, 1.2, -12), html, origin="50% 55%")
ep.pop("#s02-d", s + 0.02, 0.18, 0.8)
ep.js(f'tl.fromTo("#s02-cl",{{x:0}},{{x:-400,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')

# ---------------------------------------------------------------- S03 you're the captain of a British Airways jet, climbing over England
s, e = cut(15), cut(26)
cap = '<path d="M -64 -620 L 64 -620 L 54 -660 Q 0 -690 -54 -660 Z" fill="#14244a" stroke="#E6EEFF" stroke-width="5"/><rect x="-70" y="-624" width="140" height="12" fill="#0c0a0c" stroke="#E6EEFF" stroke-width="3"/><circle cx="0" cy="-650" r="8" fill="#FFE08A"/>'
svg = mascot("m3", 300, 1560, 1.0) + f'<g transform="translate(300,1560)">{cap}</g>' + jet("j3", 760, 1250, 0.7, -20)
html = ('<div class="lbl" id="s03-l" style="top:760px;left:540px;width:540px;color:#FFE08A;font-size:46px;">CAPTAIN</div>'
        '<div class="num" id="s03-a" style="top:860px;left:540px;width:540px;font-size:90px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">0 M</div><div class="lbl" style="top:960px;left:540px;width:540px;font-size:30px;">ALTITUDE</div>')
ep.scene("s03", s, e, svg, html, origin="50% 55%")
ep.show("#s03-l", W(17) - 0.05, 0.2)
ep.js(f'tl.fromTo("#j3",{{x:-200,y:200}},{{x:60,y:-120,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'(function(){{var el=document.getElementById("s03-a");var o={{v:0}};tl.to(o,{{v:4600,duration:{e - s:.3f},ease:"none",onUpdate:function(){{el.textContent=(Math.round(o.v/10)*10).toLocaleString("en-US")+" M";}}}},{s:.3f});}})();')
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S04 at five kilometers, your windscreen blows out
s, e = cut(26), cut(33)
tb = W(31) - 0.05
html = '<div class="num" id="s04-a" style="top:560px;font-size:100px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">5,300 M</div>'
r4 = random.Random(4)
cracks = "".join(f'<path class="s04-cr" d="M 330 960 L {330 + 200 * math.cos(a):.0f} {960 + 200 * math.sin(a):.0f}" stroke="#FFFFFF" stroke-width="4" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>' for a in [r4.uniform(0, 6.28) for _ in range(9)])
ep.scene("s04", s, e, cockpit("ck4") + cracks, html, origin="30% 50%", fx=[(tb, tb + 0.9, "sparks", dict(cx=330, cy=960, n=80, r=600, dur=0.9, color="#E6EEFF", g=0))])
ep.js(f'tl.to(".s04-cr",{{strokeDashoffset:0,duration:0.25,stagger:0.03,ease:"power2.out"}},{W(30) - 0.1:.3f});')
ep.js(f'tl.to("#ck4-L",{{opacity:0,scale:1.4,transformOrigin:"50% 50%",duration:0.12,ease:"power3.out"}},{tb:.3f});')
ep.js(f'tl.set(".s04-cr",{{opacity:0}},{tb:.3f});')
ep.flash(tb, 0.9, 0.5)
ep.shake("#s04-shake", tb, 0.7, 26)
ep.cue("decompression.mp3", tb - 0.05, 1.0)
ep.cue("wind_roar.mp3", tb + 0.3, 0.8)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S05 fitted with the wrong bolts — 84 of them were too small
s, e = cut(33), cut(47)
def bolt(x, w, col, lab):
    return (f'<g filter="url(#glowS)"><rect x="{x - 50}" y="700" width="100" height="40" rx="6" fill="#1a1416" stroke="{col}" stroke-width="5"/>'
            f'<rect x="{x - w / 2:.0f}" y="740" width="{w}" height="300" fill="#1a1416" stroke="{col}" stroke-width="5"/>'
            + "".join(line(x - w / 2, 770 + k * 24, x + w / 2, 782 + k * 24, col, 3) for k in range(11)) + '</g>' + label(x, 1090, lab, 30, col))
dots = "".join(f'<circle class="{"s05-bad" if k < 84 else "s05-ok"}" cx="{150 + (k % 15) * 56}" cy="{1200 + (k // 15) * 56}" r="18" fill="#2A2426" stroke="#F2EEEA" stroke-width="4"/>' for k in range(90))
svg = bolt(330, 52, "#9FC8FF", "CORRECT") + f'<g id="s05-b2">{bolt(750, 44, "#FF6A6A", "FITTED")}</g>' + dots
html = '<div class="num" id="s05-n" style="top:1560px;font-size:90px;">0 OF 90</div>'
ep.scene("s05", s, e, svg, html, origin="50% 55%")
ep.pop("#s05-b2", W(38) - 0.1, 0.25, 0.6)
ep.js(f'tl.to(".s05-bad",{{attr:{{fill:"#FB2945",stroke:"#FFB3B0"}},duration:0.05,stagger:{(WE(46) - W(41)) / 84:.4f}}},{W(41) - 0.05:.3f});')
ep.js(f'(function(){{var el=document.getElementById("s05-n");var o={{v:0}};tl.to(o,{{v:84,duration:{WE(46) - W(41):.3f},ease:"none",onUpdate:function(){{el.textContent=Math.round(o.v)+" OF 90 TOO SMALL";}}}},{W(41) - 0.05:.3f});}})();')
ep.cue("riser.mp3", W(41), 0.4)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S06 the air rushes out of the cockpit, and takes you with it
s, e = cut(47), cut(59)
seat = '<path d="M 260 1500 L 260 1220 L 330 1220 L 330 1420 L 460 1420 L 460 1500" fill="none" stroke="#6a5a5a" stroke-width="12"/>'
cut_l = glow(N("M 40 760 L 900 760 L 1040 1000 L 1040 1560 L 40 1560 Z", fill="#06080f", sw=12, cw=4))
hole = f'<path d="M 900 760 L 1040 1000 L 980 1010 L 860 800 Z" fill="#9FC8FF" opacity="0.25" stroke="#E6EEFF" stroke-width="5"/>'
you6 = f'<g id="s06-you"><g transform="translate(390,1420)">{mascot("m6", 0, 0, 0.7, pose=dict(uarmL=130, uarmR=-130, thighL=-80, shinL=80, thighR=-80, shinR=80))}</g></g>'
svg = cut_l + hole + seat + you6
ep.scene("s06", s, e, svg, origin="60% 55%", fx=[(s, e, "ash", dict(n=60, sp=-900, color="#E6EEFF", x0=100, x1=1000, y0=780, y1=1550))])
tp = W(55) - 0.1
ep.js(f'tl.to("#s06-you",{{x:560,y:-380,rotation:-70,svgOrigin:"390 1420",duration:0.5,ease:"power3.in"}},{tp:.3f});')
ep.js(f'tl.to("#s06-you",{{opacity:0,duration:0.05}},{tp + 0.5:.3f});')
for k in range(int((tp - s) / 0.15)):
    ep.js(f'tl.set("#s06-you",{{x:{r1.uniform(0, 20):.0f},y:{r1.uniform(-14, 0):.0f}}},{s + k * 0.15:.3f});')
ep.shake("#s06-shake", s, e - s, 8)
ep.cue("wind_roar.mp3", s, 0.9)
ep.cue("whoosh-cinematic.mp3", tp, 0.9)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S07 your body is pulled through the window — only your legs stay inside
s, e = cut(59), cut(71)
svg = clouds("s07-cl", 7, 10, 1300, 1900) + nose("n7", s_m=0.55) + streaks("s07-w", 7, 40)
ring = '<ellipse id="s07-ring" cx="840" cy="1110" rx="70" ry="50" fill="none" stroke="#FFE08A" stroke-width="6" filter="url(#glowG)" opacity="0"/>'
ep.scene("s07", s, e, svg + ring + label(840, 1330, "LEGS INSIDE", 30, LAMP_CORE, extra='id="s07-l"'), origin="66% 55%", drift=0.03)
wind_anim("s07-w", s, e)
ep.js(f'tl.fromTo("#s07-cl",{{x:0}},{{x:-1400,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo("#n7-you",{{scaleX:0.2,svgOrigin:"810 1095"}},{{scaleX:1,svgOrigin:"810 1095",duration:0.5,ease:"power3.out",immediateRender:false}},{W(62) - 0.1:.3f});')
ep.js(f'gsap.set("#n7-you",{{scaleX:0.2,svgOrigin:"810 1095"}});')
ep.show("#s07-ring", W(66) - 0.05, 0.2)
ep.show("#s07-l", W(66), 0.2)
for k in range(int((e - s) / 0.12)):
    ep.rot("#n7-m-uarmL", s + k * 0.12, 0.12, 170 + r1.uniform(-25, 25), "none")
ep.shake("#s07-shake", s, e - s, 5)
ep.cue("wind_roar.mp3", s, 0.9)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S08 outside it's −17 degrees — the wind hits at over 500 km/h
s, e = cut(71), cut(87)
html = ('<div class="num" id="s08-t" style="top:580px;left:0;width:540px;font-size:120px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">15°</div><div class="lbl" style="top:720px;left:0;width:540px;font-size:30px;">AIR</div>'
        '<div class="num" id="s08-v" style="top:580px;left:540px;width:540px;font-size:120px;">0</div><div class="lbl" style="top:720px;left:540px;width:540px;font-size:30px;">KM/H WIND</div>')
svg = clouds("s08-cl", 8, 10, 1300, 1900) + nose("n8", s_m=0.55) + streaks("s08-w", 8, 50)
ep.scene("s08", s, e, svg, html, origin="66% 55%", fx=[(W(73), e, "ash", dict(n=60, sp=-1400, color="#E6EEFF", y0=900, y1=1300))])
wind_anim("s08-w", s, e, per=0.32)
ep.js(f'tl.fromTo("#s08-cl",{{x:0}},{{x:-1800,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'(function(){{var el=document.getElementById("s08-t");var o={{v:15}};tl.to(o,{{v:-17,duration:{WE(75) - W(73) + 0.3:.3f},ease:"expo.out",onUpdate:function(){{var n=Math.round(o.v);el.textContent=(n<0?"−":"")+Math.abs(n)+"°";}}}},{W(73) - 0.1:.3f});}})();')
ep.js(f'(function(){{var el=document.getElementById("s08-v");var o={{v:0}};tl.to(o,{{v:500,duration:{WE(86) - W(78) + 0.3:.3f},ease:"expo.out",onUpdate:function(){{var n=Math.round(o.v);el.textContent=n>=500?"500+":String(n);}}}},{W(78) - 0.1:.3f});}})();')
for k in range(int((e - s) / 0.1)):
    ep.rot("#n8-m-uarmL", s + k * 0.1, 0.1, 170 + r1.uniform(-30, 30), "none")
    ep.rot("#n8-m-uarmR", s + k * 0.1, 0.1, -170 + r1.uniform(-30, 30), "none")
ep.shake("#s08-shake", s, e - s, 7)
ep.cue("wind_roar.mp3", s, 1.0)
ep.cue("wind_roar.mp3", s + 4.8, 1.0)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S09 a flight attendant grabs your legs, and holds on
s, e = cut(87), cut(96)
legs = f'<g transform="translate(960,880) rotate(45)">' + "".join(f'<g transform="translate({dx},0)">' + line(0, 0, 0, 300, RED, 50) + line(0, 0, 0, 300, DARK, 38) + line(0, 20, 0, 280, CORE, 6) + f'<ellipse cx="0" cy="318" rx="34" ry="16" fill="{DARK}" stroke="{RED}" stroke-width="6"/></g>' for dx in (-30, 30)) + '</g>'
att = f'<g id="s09-att">{mascot("m9", 560, 1560, 1.0, pose=dict(uarmL=-100, farmL=-20, uarmR=-120, farmR=-10, thighL=10, thighR=-30, shinR=30))}</g>'
svg = cut_l + hole + legs + att
ep.scene("s09", s, e, svg, origin="60% 55%", fx=[(s, e, "ash", dict(n=60, sp=-900, color="#E6EEFF", x0=100, x1=1000, y0=780, y1=1550))])
ep.js(f'tl.fromTo("#s09-att",{{x:-500}},{{x:0,duration:0.5,ease:"power3.out",immediateRender:false}},{W(88) - 0.2:.3f});')
for k in range(int((e - W(93)) / 0.2)):
    ep.js(f'tl.set("#s09-att",{{x:{r1.uniform(0, 24):.0f}}},{W(93) + k * 0.2:.3f});')
ep.shake("#s09-shake", s, e - s, 6)
ep.cue("wind_roar.mp3", s, 0.8)
ep.cue("impact-bass-2.mp3", W(90), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S10 your face is blue — your eyes are open — the crew thinks you're dead
s, e = cut(96), cut(109)
head = (f'<g id="s10-face"><ellipse id="s10-skin" cx="540" cy="1130" rx="300" ry="370" fill="#2A2426" stroke="{RED}" stroke-width="18" filter="url(#glow)"/>'
        + "".join(f'<ellipse cx="{540 + sx * 120}" cy="1070" rx="80" ry="58" fill="#ECE6E5" stroke="{CORE}" stroke-width="5"/><circle cx="{540 + sx * 120}" cy="1070" r="34" fill="#6a6462"/><circle cx="{540 + sx * 120}" cy="1070" r="12" fill="#160404"/>' for sx in (-1, 1))
        + f'<path d="M 470 1310 L 610 1310" stroke="{CORE}" stroke-width="8" stroke-linecap="round"/></g>')
ep.scene("s10", s, e, head, origin="50% 55%", fx=[(s, e, "ash", dict(n=80, sp=-1300, color="#E6EEFF", y0=600, y1=1700))])
ep.js(f'tl.to("#s10-skin",{{attr:{{fill:"#1a2a6a",stroke:"#5A78FF"}},duration:0.6}},{W(99) - 0.2:.3f});')
ep.js(f'tl.to("#s10-face",{{opacity:0.75,duration:0.5}},{W(105):.3f});')
ep.shake("#s10-shake", s, e - s, 6)
ep.cue("wind_roar.mp3", s, 0.6)
ep.cue("sub.wav", W(108), 0.6)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S11 but they don't let go — for twenty minutes, until the plane lands
s, e = cut(109), cut(121)
ep.timer("s11", s, e, W(114) - 0.1, WE(116), 0, 1200, "ms", "HOLDING ON", 1.0, ring_color=LAMP)
ep.scenes[-1]["html"] += '<div class="lbl" id="s11-l" style="top:1360px;color:#FFE08A;font-size:44px;">THEY DON\'T LET GO</div>'
ep.pop("#s11-l", W(111) - 0.05, 0.2, 1.3, "power3.out")
ep.cue("impact-bass-2.mp3", W(119), 0.6)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S12 you survive, frostbite and broken bones — five months later, flying again
s, e = cut(121), cut(134)
y0, sc = 1640, 1.2
frost = f'<g id="s12-fr" opacity="0">' + "".join(f'<circle cx="{540 + sx * 84 * sc:.0f}" cy="{y0 - 218 * sc:.0f}" r="34" fill="#5A78FF" filter="url(#glowB)"/>' for sx in (-1, 1)) + '</g>'
breaks = f'<g id="s12-br" opacity="0" filter="url(#glowS)">' + line(660, y0 - 330 * sc, 700, y0 - 300 * sc, "#FFFFFF", 8) + line(380, y0 - 260 * sc, 420, y0 - 240 * sc, "#FFFFFF", 8) + '</g>'
svg = f'<g id="s12-body">{mascot("m12", 540, y0, sc, style="xray")}{frost}{breaks}</g>' + jet("j12", 540, 900, 0.9, -15)
html = '<div class="num" id="s12-n" style="top:640px;font-size:96px;color:#FFE08A;text-shadow:0 0 18px rgba(232,176,64,.8);">5 MONTHS LATER</div>'
ep.scene("s12", s, e, svg, html, origin="50% 55%")
ep.show("#s12-fr", W(124) - 0.05, 0.3)
ep.show("#s12-br", W(126) - 0.05, 0.3)
ep.js(f'gsap.set("#j12",{{opacity:0}});')
ep.js(f'tl.to("#s12-body",{{opacity:0.15,duration:0.3}},{W(128) - 0.1:.3f});')
ep.js(f'tl.fromTo("#j12",{{opacity:1,x:-700,y:300}},{{opacity:1,x:300,y:-160,duration:{e - W(128):.3f},ease:"power1.in",immediateRender:false}},{W(128) - 0.1:.3f});')
ep.pop("#s12-n", W(128) - 0.05, 0.2, 1.3, "power3.out")
ep.cue("whoosh-cinematic.mp3", W(131), 0.6)
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S13 but out there, in that wind, the world goes quiet
s, e = cut(134), cut(144)
svg = clouds("s13-cl", 13, 10, 1300, 1900) + nose("n13", s_m=0.55) + streaks("s13-w", 13, 40) + '<rect id="s13-dim" x="-100" y="-100" width="1280" height="2200" fill="#010101" opacity="0"/>'
ep.scene("s13", s, e, svg, origin="66% 55%", drift=0.04)
ep.js(f'tl.fromTo("#s13-w",{{x:0}},{{x:-900,duration:{e - s:.3f},ease:"power2.out",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s13-dim",{{opacity:0.6,duration:{e - W(140):.3f},ease:"power1.in"}},{W(140):.3f});')
ep.cue("wind_roar.mp3", s, 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(144), 147)
ep.write(red=["window", "blows", "wrong", "small", "rushes", "pulled", "legs", "seventeen", "wind", "grabs", "blue", "dead", "go", "lands", "survive", "again", "quiet"])
