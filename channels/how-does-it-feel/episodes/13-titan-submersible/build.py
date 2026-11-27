"""Episode 13 — How does it feel? When you're inside the Titan submersible (June 18, 2023)."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
SEA, SEA_CORE = "#5A78FF", "#E6EEFF"
SNOW = dict(n=70, sp=-60, color="#9FB4E6", y0=300)  # marine snow drifting up past a descending sub
LAMP_CORE = "#FFE08A"
HULL = "M -260 -100 L 220 -100 A 100 100 0 0 1 220 100 L -260 100 Q -300 100 -300 0 Q -300 -100 -260 -100 Z"


def sub(gid, x, y, s=1.0, beam=False, people=0, lit=True):
    fins = N("M -300 0 L -360 -70 L -360 70 Z", fill="#0a0c14", red=SEA, core=SEA_CORE, sw=8, cw=3)
    thr = "".join(f'<rect x="-250" y="{yy}" width="90" height="26" rx="8" fill="#0a0c14" stroke="{SEA}" stroke-width="5"/>' for yy in (-134, 108))
    body = N(HULL, fill="#0a0c14", red=SEA, core=SEA_CORE, sw=12, cw=4)
    rings = "".join(line(x0, -96, x0, 96, "#2a3a6a", 4) for x0 in (-180, -60, 60, 180))
    win = f'<circle id="{gid}-win" cx="290" cy="-14" r="28" fill="{"#FFE08A" if lit else "#0a0c14"}" stroke="{SEA_CORE}" stroke-width="5"/>'
    ppl = ""
    for k in range(people):
        px = -200 + k * 95
        ppl += f'<g class="{gid}-p"><circle cx="{px}" cy="-30" r="20" fill="#2A2426" stroke="{RED}" stroke-width="5"/><path d="M {px - 30} 70 Q {px} 0 {px + 30} 70 Z" fill="#2A2426" stroke="{RED}" stroke-width="5"/></g>'
    bm = (f'<path d="M 300 -14 L 900 -260 L 900 240 Z" fill="url(#{gid}-bg)" opacity="0.7"/>'
          f'<defs><linearGradient id="{gid}-bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFF1C8" stop-opacity="0.8"/><stop offset="1" stop-color="#FFF1C8" stop-opacity="0"/></linearGradient></defs>') if beam else ""
    return (f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})">{bm}<g filter="url(#glowB)">{fins}{thr}{body}</g>{rings}{ppl}<g filter="url(#glowG)">{win}</g></g></g>')


def wreck(x, y, s=1.0, gid=""):
    d = "M -300 0 L -260 -80 L 120 -90 L 160 -150 L 200 -90 L 300 -70 L 330 0 Z"
    stacks = "".join(f'<path d="M {fx} -88 L {fx + 10} -150 L {fx + 46} -150 L {fx + 40} -88 Z" fill="#0a0c14" stroke="#6a7aa8" stroke-width="5"/>' for fx in (-170, -80))
    i = f' id="{gid}"' if gid else ""
    return f'<g{i} transform="translate({x},{y}) scale({s})">' + glow(N(d, fill="#0a0c14", red="#4a5a8a", core="#9FB4E6", sw=8, cw=3), f="glowB") + stacks + '</g>'


def water(gid, top="#0a1a3a", bottom="#010101"):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect x="-100" y="-100" width="1280" height="2200" fill="url(#{gid})"/>')


def bigx(gid, x, y, r=60, w=14):
    return f'<g id="{gid}" filter="url(#glow)">' + line(x - r, y - r, x + r, y + r, "#FF3B36", w) + line(x + r, y - r, x - r, y + r, "#FF3B36", w) + '</g>'


# ---------------------------------------------------------------- S01 cold open: the sub sinking into black water, close on the window → pull out
s, e = 0.0, cut(10)
svg = water("w1", "#06102a") + sub("t1", 520, 1080, 1.0, beam=True)
ep.scene("s01", s, e, svg, origin="73% 55%", custom_cam=True, fx=[(s, e, "ash", SNOW)])
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.6}},{{scale:2.7,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#t1",{{y:-40,rotation:4,svgOrigin:"520 1080"}},{{y:60,rotation:6,svgOrigin:"520 1080",duration:{e:.3f},ease:"sine.inOut",immediateRender:false}},0);')
r1 = random.Random(1)
for k in range(int(e / 0.2)):
    ep.js(f'tl.set("#t1-win",{{opacity:{r1.choice([1, 1, 0.5, 0.8])}}},{k * 0.2:.3f});')
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("underwater_drone.mp3", 0, 0.8)
ep.cue("sonar_ping.mp3", 0.1, 0.7)
ep.cue("hull_creak.mp3", 1.6, 0.6)

# ---------------------------------------------------------------- S02 June 18th, 2023
s, e = cut(10), cut(13)
sky = f'<rect x="-100" y="-100" width="1280" height="1050" fill="#0a0e1c"/><circle cx="820" cy="760" r="70" fill="#FFE08A" opacity="0.8" filter="url(#glowG)"/>'
ship = glow(N("M 140 940 L 560 940 L 520 1000 L 180 1000 Z", fill="#0a0c14", red=SEA, core=SEA_CORE, sw=8, cw=3) + N("M 240 940 L 240 880 L 400 880 L 400 940", fill="#0a0c14", red=SEA, core=SEA_CORE, sw=6, cw=2), f="glowB")
svg = water("w2", "#0a2050") + sky + ship + glow(N("M -100 950 L 1180 950", red=SEA, core=SEA_CORE, sw=10, cw=4), f="glowB") + sub("t2", 640, 1200, 0.5)
html = '<div class="num" id="s02-d" style="top:560px;font-size:120px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">JUNE 18, 2023</div>'
ep.scene("s02", s, e, svg, html, origin="50% 55%")
ep.pop("#s02-d", s + 0.02, 0.18, 0.8)
ep.js(f'tl.fromTo("#t2",{{y:-120}},{{y:80,duration:{e - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.cue("sonar_ping.mp3", s + 0.1, 0.4)

# ---------------------------------------------------------------- S03 one of five people inside a tube the size of a minivan
s, e = cut(13), cut(26)
van = (f'<g id="s03-van" opacity="0"><g transform="translate(0,-60)"><path d="M 200 1420 L 220 1200 Q 240 1140 320 1130 L 700 1120 Q 820 1120 860 1200 L 900 1300 L 900 1420 Z" fill="none" stroke="{LAMP_CORE}" stroke-width="6" stroke-dasharray="20 14" filter="url(#glowG)"/>'
       f'<circle cx="330" cy="1430" r="48" fill="none" stroke="{LAMP_CORE}" stroke-width="6"/><circle cx="770" cy="1430" r="48" fill="none" stroke="{LAMP_CORE}" stroke-width="6"/>' + label(540, 1560, "MINIVAN", 34, LAMP_CORE) + '</g></g>')
dims = f'<g id="s03-dim">' + line(200, 1500, 900, 1500, CORE, 4) + line(200, 1480, 200, 1520, CORE, 4) + line(900, 1480, 900, 1520, CORE, 4) + label(540, 1580, "6.7 M", 32, GREY) + '</g>'
svg = water("w3", "#06102a") + sub("t3", 560, 1260, 1.12, people=5) + van + dims
html = '<div class="num" id="s03-n" style="top:620px;font-size:200px;">0</div><div class="lbl" style="top:830px;">PEOPLE ON BOARD</div>'
ep.scene("s03", s, e, svg, html, origin="50% 60%", fx=[(s, e, "ash", SNOW)])
ep.js(f'tl.fromTo(".t3-p",{{opacity:0,scale:0,transformOrigin:"50% 100%"}},{{opacity:1,scale:1,duration:0.16,stagger:0.12,ease:"back.out(2)",immediateRender:false}},{W(16) - 0.15:.3f});')
ep.js('gsap.set(".t3-p",{opacity:0});')
ep.counter("#s03-n", W(16) - 0.15, 0.6, 0, 5, "n", "none")
ep.js(f'tl.to("#s03-van",{{opacity:1,duration:0.3}},{W(22) - 0.1:.3f});')
ep.js(f'tl.to("#s03-dim",{{opacity:0,duration:0.2}},{W(22) - 0.1:.3f});')
for k in range(5):
    ep.cue("pop.mp3", W(16) - 0.15 + k * 0.12, 0.35)
ep.cue("hull_creak.mp3", W(20), 0.4)

# ---------------------------------------------------------------- S04 no seats — one small window
s, e = cut(26), cut(31)
svg = water("w4", "#06102a") + sub("t4", 470, 1180, 1.45, people=5) + bigx("s04-x", 540, 1520, 46, 12) + label(540, 1450, "SEATS", 30, GREY)
ring = f'<circle id="s04-ring" cx="{470 + 290 * 1.45:.0f}" cy="{1180 - 14 * 1.45:.0f}" r="70" fill="none" stroke="{LAMP_CORE}" stroke-width="6" filter="url(#glowG)" opacity="0"/>'
ep.scene("s04", s, e, svg + ring + label(890, 1050, "1 WINDOW", 30, LAMP_CORE, extra='id="s04-wl"'), origin="50% 60%", fx=[(s, e, "ash", SNOW)])
ep.pop("#s04-x", W(26) + 0.05, 0.18, 1.6, "power3.out")
ep.js(f'tl.fromTo("#s04-ring",{{opacity:1,scale:2,svgOrigin:"{470 + 290 * 1.45:.0f} {1180 - 14 * 1.45:.0f}"}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out",immediateRender:false}},{W(28) - 0.05:.3f});')
ep.show("#s04-wl", W(28), 0.2)
ep.cue("impact-bass-2.mp3", W(26) + 0.05, 0.5)
ep.cue("sonar_ping.mp3", W(28), 0.4)

# ---------------------------------------------------------------- S05 the sub is steered with a game controller
s, e = cut(31), cut(39)
PAD = "M 300 1000 Q 300 900 400 900 L 680 900 Q 780 900 780 1000 L 820 1160 Q 840 1240 770 1240 Q 720 1240 690 1180 L 640 1110 L 440 1110 L 390 1180 Q 360 1240 310 1240 Q 240 1240 260 1160 Z"
btns = "".join(f'<circle class="s05-b" cx="{x}" cy="{y}" r="16" fill="{c}"/>' for x, y, c in ((680, 970, "#FB2945"), (710, 1000, "#5A78FF"), (650, 1000, "#E8B040"), (680, 1030, "#4ACF7A")))
dpad = '<path d="M 390 960 L 410 960 L 410 990 L 440 990 L 440 1010 L 410 1010 L 410 1040 L 390 1040 L 390 1010 L 360 1010 L 360 990 L 390 990 Z" fill="#F2EEEA"/>'
stick = f'<g id="s05-st"><circle cx="470" cy="1060" r="30" fill="#2A2426" stroke="{CORE}" stroke-width="5"/></g><circle cx="610" cy="1060" r="30" fill="#2A2426" stroke="{CORE}" stroke-width="5"/>'
svg = f'<g transform="translate(540,1070) scale(1.35) translate(-540,-1070)">' + glow(N(PAD, fill="#141016", red=SEA, core=SEA_CORE, sw=12, cw=4), f="glowB") + btns + dpad + stick + '</g>'
ep.scene("s05", s, e, svg, origin="50% 55%", drift=0.025)
for k in range(int((e - s) / 0.3)):
    ep.js(f'tl.to("#s05-st",{{x:{[14, -10, 6, -14][k % 4]},y:{[-8, 10, -12, 6][k % 4]},duration:0.25,ease:"sine.inOut"}},{s + k * 0.3:.3f});')
ep.js(f'tl.fromTo(".s05-b",{{scale:1.4,transformOrigin:"50% 50%"}},{{scale:1,duration:0.2,stagger:0.12,ease:"power2.out",immediateRender:false}},{W(37) - 0.1:.3f});')
ep.cue("beep.wav", W(37), 0.12)
ep.cue("underwater_drone.mp3", s, 0.5)

# ---------------------------------------------------------------- S06 diving to the wreck of the Titanic — almost four kilometers down
s, e = cut(39), cut(51)
y0, y1 = 620, 1560
my = lambda m: y0 + m / 4000 * (y1 - y0)
ruler = line(130, my(0), 130, my(4000), CORE, 5) + "".join(line(130, my(m), 166, my(m), CORE, 5) + label(182, my(m) + 10, f"{m:,} M", 26, GREY, "start") for m in range(0, 4001, 1000))
svg = water("w6", "#0a2050") + glow(ruler, f="glowS") + wreck(640, my(3800) + 20, 0.9) + f'<g id="s06-sub">{sub("t6", 640, my(0) + 20, 0.32)}</g>'
html = '<div class="num" id="s06-n" style="top:560px;left:440px;width:600px;font-size:110px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">0 M</div>'
ep.scene("s06", s, e, svg, html, origin="50% 55%", fx=[(s, e, "ash", SNOW)])
ep.js(f'tl.to("#s06-sub",{{y:{my(3800) - my(0) - 160:.0f},duration:{e - s - 0.3:.3f},ease:"power1.inOut"}},{s + 0.1:.3f});')
ep.js(f'(function(){{var el=document.getElementById("s06-n");var o={{v:0}};tl.to(o,{{v:3800,duration:{e - s - 0.3:.3f},ease:"power1.inOut",onUpdate:function(){{el.textContent=Math.round(o.v/10)*10>=1000?(Math.round(o.v/10)*10).toLocaleString("en-US")+" M":(Math.round(o.v/10)*10)+" M";}}}},{s + 0.1:.3f});}})();')
ep.cue("sonar_ping.mp3", W(44), 0.5)

# ---------------------------------------------------------------- S07 after a few hundred meters the sunlight is gone — total black
s, e = cut(51), cut(62)
rays = "".join(f'<path class="s07-r" d="M {x} -100 L {x + 60} -100 L {x + 330} 2000 L {x + 170} 2000 Z" fill="url(#s07-rg)" opacity="0.5"/>' for x in (80, 330, 600, 820))
svg = ('<defs><linearGradient id="s07-rg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FC8FF" stop-opacity="0.45"/><stop offset="1" stop-color="#9FC8FF" stop-opacity="0"/></linearGradient></defs>'
       f'<rect id="s07-bg" x="-100" y="-100" width="1280" height="2200" fill="#123a7a"/>' + rays + sub("t7", 540, 1150, 0.7, beam=False))
html = '<div class="num" id="s07-n" style="top:600px;font-size:150px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">0 M</div>'
ep.scene("s07", s, e, svg, html, origin="50% 55%", fx=[(s, e, "ash", SNOW)])
ep.js(f'(function(){{var el=document.getElementById("s07-n");var o={{v:0}};tl.to(o,{{v:1000,duration:{WE(61) - s:.3f},ease:"power1.in",onUpdate:function(){{var n=Math.round(o.v/10)*10;el.textContent=n.toLocaleString("en-US")+" M";}}}},{s + 0.05:.3f});}})();')
ep.js(f'tl.to("#s07-bg",{{attr:{{fill:"#010101"}},duration:{W(59) - s:.3f},ease:"power1.in"}},{s:.3f});')
ep.js(f'tl.to(".s07-r",{{opacity:0,duration:0.6,stagger:0.1}},{W(57) - 0.1:.3f});')
ep.js(f'tl.to("#t7, #s07-n",{{opacity:0.15,duration:0.4}},{W(60) - 0.05:.3f});')
ep.cue("sub.wav", W(60), 0.6)

# ---------------------------------------------------------------- S08 every meter, the ocean presses harder on the hull
s, e = cut(62), cut(71)
arrows = ""
for k in range(12):
    a = k * math.pi / 6
    cx, cy = 540 + 470 * math.cos(a), 1100 + 470 * math.sin(a)
    deg = math.degrees(a) + 180
    arrows += f'<g class="s08-a"><g transform="translate({cx:.0f},{cy:.0f}) rotate({deg:.0f})">' + N("M -60 0 L 60 0 M 30 -30 L 60 0 L 30 30", fill="none", red=SEA, core=SEA_CORE, sw=10, cw=3) + '</g></g>'
svg = f'<g filter="url(#glowB)">{arrows}</g>' + sub("t8", 540, 1100, 0.9)
ep.scene("s08", s, e, svg, origin="50% 57%", fx=[(s, e, "ash", SNOW)])
ep.js(f'tl.fromTo(".s08-a",{{scale:0.7,svgOrigin:"540 1100",opacity:0.4}},{{scale:0.62,opacity:1,duration:{e - s:.3f},ease:"power2.in",immediateRender:false}},{s:.3f});')
ep.js(f'gsap.set(".s08-a",{{scale:0.7,svgOrigin:"540 1100",opacity:0.4}});')
ep.js(f'tl.to("#t8",{{scaleY:0.96,svgOrigin:"540 1100",duration:{e - W(66):.3f},ease:"power2.in"}},{W(66):.3f});')
ep.cue("hull_creak.mp3", W(66), 0.8)
ep.cue("underwater_drone.mp3", s, 0.5)

# ---------------------------------------------------------------- S09 at three kilometers it's more than 300 times the surface pressure
s, e = cut(71), cut(85)
cx, cy, R = 540, 1120, 300
ticks = "".join(line(cx + (R - 10) * math.cos(a), cy + (R - 10) * math.sin(a), cx + (R - 40) * math.cos(a), cy + (R - 40) * math.sin(a), CORE, 5) for a in [math.radians(150 + i * 24) for i in range(11)])
dial = glow(f'<path d="M {cx + R * math.cos(math.radians(150)):.0f} {cy + R * math.sin(math.radians(150)):.0f} A {R} {R} 0 1 1 {cx + R * math.cos(math.radians(30)):.0f} {cy + R * math.sin(math.radians(30)):.0f}" fill="none" stroke="{SEA}" stroke-width="16"/>' + ticks, f="glowB")
needle = f'<g transform="translate({cx},{cy})"><g id="s09-nd" transform="rotate(-120)">' + line(0, 0, 0, -(R - 60), "#FF3B36", 10) + '</g><circle r="22" fill="#F2EEEA"/></g>'
html = ('<div class="num" id="s09-n" style="top:1300px;font-size:150px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">1×</div>'
        '<div class="lbl" style="top:1460px;">SURFACE PRESSURE</div><div class="num" id="s09-d" style="top:600px;font-size:90px;">3 KM</div>')
ep.scene("s09", s, e, dial + needle, html, origin="50% 55%")
ep.pop("#s09-d", W(72) - 0.05, 0.18, 1.4, "power3.out")
ep.rot("#s09-nd", W(75), WE(84) - W(75), 118, "power2.in")
ep.js(f'(function(){{var el=document.getElementById("s09-n");var o={{v:1}};tl.to(o,{{v:300,duration:{WE(79) - W(75):.3f},ease:"power2.in",onUpdate:function(){{el.textContent=Math.round(o.v)+"×";}}}},{W(75):.3f});}})();')
ep.js(f'tl.to("#s09-n",{{color:"#FF3B36",duration:0.3}},{WE(79):.3f});')
ep.shake("#s09-shake", WE(79), 0.3, 8)
ep.cue("riser.mp3", W(75), 0.5)
ep.cue("hull_creak.mp3", WE(79), 0.7)

# ---------------------------------------------------------------- S10 1 hour 45 minutes into the dive, the messages stop
s, e = cut(85), cut(96)
bars = "".join(f'<rect class="s10-bar" x="{380 + k * 80}" y="{1300 - (k + 1) * 70}" width="54" height="{(k + 1) * 70}" fill="#5A78FF" filter="url(#glowB)"/>' for k in range(5))
html = ('<div class="num" id="s10-n" style="top:620px;font-size:200px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">0:00</div><div class="lbl" style="top:840px;">INTO THE DIVE</div>'
        '<div class="num" id="s10-lost" style="top:1380px;font-size:90px;">SIGNAL LOST</div>')
ep.scene("s10", s, e, bars + hline(1300, 340, 740, 6, 2), html, origin="50% 55%",
         fx=[(s, W(95), "ecg", dict(x0=60, x1=1020, y=1560, amp=60, period=300, speed=420)), (W(95), e, "ecg", dict(x0=60, x1=1020, y=1560, amp=0.01, period=300))])
ep.js(f'(function(){{var el=document.getElementById("s10-n");var o={{v:0}};tl.to(o,{{v:105,duration:{WE(89) - W(85):.3f},ease:"power2.out",onUpdate:function(){{var n=Math.round(o.v);el.textContent=Math.floor(n/60)+":"+(n%60<10?"0":"")+(n%60);}}}},{W(85) - 0.05:.3f});}})();')
for k in range(int((W(95) - s) / 0.9)):
    ep.cue("sonar_ping.mp3", s + k * 0.9, 0.3)
ep.js(f'tl.to(".s10-bar",{{opacity:0.08,duration:0.12,stagger:{{each:0.08,from:"end"}}}},{W(94):.3f});')
ep.pop("#s10-lost", W(95) - 0.02, 0.18, 1.4, "power3.out")
ep.cue("glitch.mp3", W(95) - 0.05, 0.7)

# ---------------------------------------------------------------- S11 the carbon fiber hull gives way
s, e = cut(96), cut(102)
weave = "".join(f'<rect x="{-40 + (k % 12) * 100}" y="{600 + (k // 12) * 100}" width="96" height="96" fill="{"#15161c" if (k + k // 12) % 2 else "#1d1f28"}"/>' for k in range(12 * 11))
r11 = random.Random(11)
cracks = ""
for k in range(9):
    x, y = 540, 1100
    pts = [f"M {x} {y}"]
    a = r11.uniform(0, 2 * math.pi)
    for j in range(6):
        a += r11.uniform(-0.6, 0.6)
        x += 90 * math.cos(a)
        y += 90 * math.sin(a)
        pts.append(f"L {x:.0f} {y:.0f}")
    cracks += f'<path class="s11-c" d="{" ".join(pts)}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" stroke="#E6EEFF" stroke-width="7" filter="url(#glowB)"/>'
svg = weave + cracks + label(540, 1680, "CARBON FIBER HULL", 32, GREY)
ep.scene("s11", s, e, svg, origin="50% 57%", drift=0.04)
ep.js(f'tl.to(".s11-c",{{strokeDashoffset:0,duration:{WE(101) - W(97):.3f},stagger:0.05,ease:"power2.in"}},{W(97) - 0.1:.3f});')
ep.shake("#s11-shake", W(99), WE(101) - W(99), 10)
ep.cue("hull_creak.mp3", W(97) - 0.1, 0.9)

# ---------------------------------------------------------------- S12 the sub implodes in about one millisecond
s, e = cut(102), cut(109)
html = '<div class="num" id="s12-n" style="top:1350px;font-size:170px;color:#F5F5F5;">0.001 S</div>'
shock = '<circle id="s12-ring" cx="540" cy="1050" r="60" fill="none" stroke="#E6EEFF" stroke-width="10" filter="url(#glowB)" opacity="0"/>'
ep.scene("s12", s, e, sub("t12", 540, 1050, 1.1) + shock, html, origin="50% 55%", fx=[(W(104) - 0.02, W(104) + 0.6, "sparks", dict(cx=540, cy=1050, n=60, r=600, dur=0.6, color="#E6EEFF", g=0))])
ti = W(104) - 0.02
ep.js(f'tl.to("#t12",{{scale:0.02,svgOrigin:"540 1050",duration:{F:.3f},ease:"none"}},{ti:.3f});')
ep.js(f'tl.set("#t12",{{opacity:0}},{ti + F:.3f});')
ep.flash(ti, 1.0, 0.5)
ep.shake("#s12-shake", ti, 0.5, 26)
ep.pop("#s12-n", W(106) - 0.05, 0.18, 1.6, "power3.out")
ep.js(f'tl.fromTo("#s12-ring",{{opacity:1,scale:0.3,svgOrigin:"540 1050"}},{{opacity:0,scale:9,svgOrigin:"540 1050",duration:1.4,ease:"power2.out",immediateRender:false}},{ti + F:.3f});')
ep.cue("implosion.mp3", ti - 0.02, 1.0)
ep.cue("sub.wav", ti, 1.0)

# ---------------------------------------------------------------- S13 your brain needs a hundred times longer just to notice pain
s, e = cut(109), cut(120)
bars = (label(150, 1180, "IMPLOSION · 1 MS", 30, "#9FC8FF", "start") + f'<rect id="s13-a" x="150" y="1200" width="8" height="60" fill="#5A78FF" filter="url(#glowB)"/>'
        + label(150, 1380, "BRAIN NOTICES PAIN · ~100 MS", 30, "#FF6A6A", "start") + f'<rect id="s13-b" x="150" y="1400" width="800" height="60" fill="#FB2945" filter="url(#glow)"/>')
svg = brain(540, 840, 420, 340, gid="s13-br", seed=13) + bars
ep.scene("s13", s, e, svg, origin="50% 55%")
ep.js(f'tl.fromTo("#s13-b",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:{WE(115) - W(112):.3f},ease:"power1.inOut",immediateRender:false}},{W(112):.3f});')
ep.js('gsap.set("#s13-b",{scaleX:0,transformOrigin:"0% 50%"});')
ep.floor(s, 0.3, 0.0)

# ---------------------------------------------------------------- S14 you never feel a thing
s, e = cut(120), cut(125)
svg = water("w14", "#040814") + wreck(540, 1380, 1.2, gid="s14-w")
ep.scene("s14", s, e, svg, origin="50% 65%", drift=0.03, fx=[(s, e, "ash", dict(SNOW, sp=40, n=90))])
ep.js(f'tl.fromTo("#s14-w",{{opacity:0.9}},{{opacity:0.35,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.cue("underwater_drone.mp3", s, 0.6)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(125), 128)
ep.write(red=["titan", "five", "minivan", "seats", "window", "controller", "titanic", "black", "hull", "pressure", "stop", "implodes", "millisecond", "pain", "thing"])
