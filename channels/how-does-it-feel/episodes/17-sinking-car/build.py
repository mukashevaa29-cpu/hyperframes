"""Episode 17 — How does it feel? When your car sinks into a river."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
SEA, SEA_CORE = "#5A78FF", "#E6EEFF"
LAMP, LAMP_CORE = "#E8B040", "#FFE08A"
WATER = "#0a1a44"
HAND = ("M -70 120 L -70 0 Q -70 -20 -55 -24 L -55 -150 Q -55 -170 -38 -170 Q -22 -170 -22 -150 L -22 -40 L -12 -40 L -12 -185 Q -12 -205 5 -205 Q 22 -205 22 -185 "
        "L 22 -40 L 32 -40 L 32 -165 Q 32 -185 49 -185 Q 66 -185 66 -165 L 66 -30 L 76 -30 L 76 -120 Q 76 -140 92 -140 Q 108 -140 108 -120 L 108 40 Q 108 80 90 120 Z")
CABIN = "M 150 640 L 930 640 L 1010 1480 L 70 1480 Z"


def car(gid, x, y, s=1.0, rot=0, lights=True):
    body = "M -260 40 L -260 -20 L -170 -40 L -100 -130 L 110 -130 L 180 -40 L 260 -30 L 260 40 Z"
    wins = '<path d="M -90 -115 L -10 -115 L -10 -48 L -150 -48 Z M 10 -115 L 100 -115 L 160 -48 L 10 -48 Z" fill="#1a2440" stroke="#9FC8FF" stroke-width="4"/>'
    wheels = "".join(f'<circle cx="{wx}" cy="45" r="40" fill="#0c0a0c" stroke="{CORE}" stroke-width="6"/>' for wx in (-160, 160))
    head = f'<circle id="{gid}-hl" cx="252" cy="-12" r="12" fill="{LAMP_CORE}" filter="url(#glowG)"/>' if lights else ""
    who = f'<g transform="translate(-40,-40)">{mascot(gid + "-m", 0, 0, 0.13)}</g>'
    return (f'<g id="{gid}"><g transform="translate({x},{y}) rotate({rot}) scale({s})">' + glow(N(body, fill="#0c0a0c", sw=10, cw=3)) + wins + who + wheels + head + '</g></g>')


def river(y=900, gid="", deep=True):
    i = f' id="{gid}"' if gid else ""
    grad = (f'<defs><linearGradient id="rv{y}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14306a"/><stop offset="1" stop-color="#010101"/></linearGradient></defs>'
            if deep else "")
    fill = f"url(#rv{y})" if deep else WATER
    return (f'<g{i}>{grad}<rect x="-100" y="{y}" width="1280" height="{2100 - y}" fill="{fill}" opacity="0.95"/>'
            + glow(N(f"M -100 {y} L 1180 {y}", red=SEA, core=SEA_CORE, sw=10, cw=4), f="glowB") + '</g>')


def bubbles(cls, n, seed, x0, x1, y0, y1):
    r = random.Random(seed)
    return "".join(f'<circle class="{cls}" cx="{r.uniform(x0, x1):.0f}" cy="{r.uniform(y0, y1):.0f}" r="{r.uniform(5, 14):.0f}" fill="none" stroke="#9FC8FF" stroke-width="3"/>' for _ in range(n))


def cabin(gid, water_y, mouth=False):
    """front view from the hood: windshield frame, you at the wheel, water rising (tween #gid-w y)."""
    frame = glow(N(CABIN, fill="#070a14", sw=12, cw=4))
    you = mascot(gid + "-m", 540, 1700, 1.25, mouth_open=mouth, pose=dict(uarmL=-30, farmL=-60, uarmR=30, farmR=60))
    wheel = f'<circle cx="540" cy="1330" r="150" fill="none" stroke="{CORE}" stroke-width="16"/><circle cx="540" cy="1330" r="150" fill="none" stroke="{RED}" stroke-width="5"/>' + line(390, 1330, 690, 1330, CORE, 10)
    water = (f'<clipPath id="{gid}-cp"><path d="{CABIN}"/></clipPath><g clip-path="url(#{gid}-cp)">{you}{wheel}<g id="{gid}-w" transform="translate(0,0)">'
             f'<rect x="0" y="{water_y}" width="1080" height="1400" fill="#1a3a8a" opacity="0.72"/>' + line(0, water_y, 1080, water_y, "#9FC8FF", 6) + '</g></g>')
    return frame + water + glow(N(CABIN, fill="none", sw=12, cw=4))


def bigx(gid, x, y, r=70, w=16):
    return f'<g id="{gid}" filter="url(#glow)">' + line(x - r, y - r, x + r, y + r, "#FF3B36", w) + line(x + r, y - r, x - r, y + r, "#FF3B36", w) + '</g>'


# ---------------------------------------------------------------- S01 cold open: the car sinking nose-first, close on the window → pull out
s, e = 0.0, cut(11)
svg = river(700) + car("c1", 540, 1250, 1.5, rot=35, lights=False) + bubbles("s01-b", 26, 1, 380, 720, 900, 1500)
ep.scene("s01", s, e, svg, origin="48% 62%", custom_cam=True)
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.4}},{{scale:2.5,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#c1",{{y:-80}},{{y:160,duration:{e:.3f},ease:"power1.in",immediateRender:false}},0);')
ep.js(f'tl.fromTo(".s01-b",{{y:0,opacity:0.9}},{{y:-500,opacity:0,duration:1.4,stagger:{{each:0.08,repeat:{int(e / 1.4)}}},ease:"power1.in",immediateRender:false}},0);')
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("underwater_muffle.mp3", 0, 0.9)
ep.cue("sub.wav", 0, 0.6)

# ---------------------------------------------------------------- S02 you lose control on a bridge
s, e = cut(11), cut(17)
deck = hline(1150, -100, 1180, 12, 4) + "".join(line(x, 1150, x, 1080, "#6a5a5a", 6) for x in range(0, 1081, 90)) + line(-100, 1080, 1180, 1080, "#BDB5B5", 6)
svg = river(1500) + deck + f'<g id="s02-c">{car("c2", 200, 1120, 0.75)}</g>'
ep.scene("s02", s, e, svg, origin="50% 60%", fx=[(s, e, "ash", dict(n=80, sp=900, color="#9FB4E6"))])
ep.js(f'tl.fromTo("#s02-c",{{x:-300}},{{x:450,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
for k in range(int((e - W(12)) / 0.22)):
    ep.js(f'tl.to("#c2",{{rotation:{[12, -14, 16, -10][k % 4]},svgOrigin:"200 1120",duration:0.22,ease:"sine.inOut"}},{W(12) + k * 0.22:.3f});')
ep.cue("whoosh-cinematic.mp3", W(12), 0.6)
ep.cue("rock_scrape.mp3", W(13), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S03 the car smashes through the railing
s, e = cut(17), cut(23)
svg = river(1500) + deck.replace("1080, 1180, 1080", "1080, 700, 1080") + f'<g id="s03-rail">' + line(700, 1080, 1180, 1080, "#BDB5B5", 6) + '</g>' + f'<g id="s03-c">{car("c3", 540, 1120, 0.75)}</g>'
tc = W(19) - 0.05
ep.scene("s03", s, e, svg, origin="60% 62%", fx=[(tc, tc + 0.8, "sparks", dict(cx=760, cy=1080, n=60, r=420, dur=0.8, color="#FFD27A", g=400))])
ep.js(f'tl.fromTo("#s03-c",{{x:-200}},{{x:220,duration:{tc - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s03-c",{{x:420,y:260,rotation:38,svgOrigin:"540 1120",duration:{e - tc:.3f},ease:"power2.in"}},{tc:.3f});')
ep.js(f'tl.to("#s03-rail",{{x:200,y:-120,rotation:25,svgOrigin:"760 1080",opacity:0,duration:0.7,ease:"power2.out"}},{tc:.3f});')
ep.shake("#s03-shake", tc, 0.45, 18)
ep.flash(tc, 0.4, 0.4)
ep.cue("car_crash.mp3", tc - 0.03, 1.0)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S04 you hit the water
s, e = cut(23), cut(27)
th = W(24) - 0.05
svg = river(1150) + f'<g id="s04-c">{car("c4", 540, 1150, 1.0, rot=35)}</g>'
ep.scene("s04", s, e, svg, origin="50% 60%", fx=[(th, th + 1.0, "sparks", dict(cx=540, cy=1150, n=90, r=520, dur=1.0, color="#E6EEFF", g=700))])
ep.js(f'tl.fromTo("#s04-c",{{y:-900}},{{y:0,duration:{th - s:.3f},ease:"power2.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s04-c",{{y:60,duration:0.5,ease:"power2.out"}},{th:.3f});')
ep.shake("#s04-shake", th, 0.6, 24)
ep.flash(th, 0.5, 0.5)
ep.cue("splash_big.mp3", th - 0.05, 1.0)
ep.cue("impact-bass-1.mp3", th, 0.8)

# ---------------------------------------------------------------- S05 the airbag explodes in your face
s, e = cut(27), cut(33)
ta = W(29) - 0.05
bag = f'<ellipse id="s05-bag" cx="540" cy="1150" rx="330" ry="260" fill="#ECE6E5" stroke="#FFFFFF" stroke-width="6" opacity="0.92"/>'
svg = cabin("s05c", 1700) + bag
ep.scene("s05", s, e, svg, origin="50% 58%")
ep.js(f'tl.fromTo("#s05-bag",{{scale:0,opacity:0,svgOrigin:"540 1330"}},{{scale:1,opacity:0.92,svgOrigin:"540 1330",duration:0.08,ease:"power4.out",immediateRender:false}},{ta:.3f});')
ep.js('gsap.set("#s05-bag",{opacity:0});')
ep.js(f'tl.to("#s05-bag",{{scale:0.7,opacity:0.5,svgOrigin:"540 1330",duration:{e - ta - 0.3:.3f},ease:"power1.in"}},{ta + 0.3:.3f});')
ep.flash(ta, 0.8, 0.4)
ep.shake("#s05-shake", ta, 0.4, 20)
ep.cue("airbag.mp3", ta - 0.02, 1.0)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S06 for about a minute, the car floats
s, e = cut(33), cut(40)
html = '<div class="num" id="s06-n" style="top:590px;font-size:170px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">1:00</div><div class="lbl" style="top:770px;">UNTIL IT SINKS</div>'
svg = river(1250) + f'<g id="s06-c">{car("c6", 540, 1230, 1.0)}</g>'
ep.scene("s06", s, e, svg, html, origin="50% 60%", fx=[(s, e, "ash", dict(n=60, sp=800, color="#9FB4E6"))])
ep.js(f'tl.fromTo("#s06-c",{{y:-10,rotation:-3,svgOrigin:"540 1230"}},{{y:14,rotation:3,svgOrigin:"540 1230",duration:0.9,repeat:{int((e - s) / 0.9)},yoyo:true,ease:"sine.inOut",immediateRender:false}},{s:.3f});')
ep.js(f'(function(){{var el=document.getElementById("s06-n");var o={{v:60}};tl.to(o,{{v:52,duration:{e - s:.3f},ease:"none",onUpdate:function(){{var n=Math.ceil(o.v);el.textContent=Math.floor(n/60)+":"+(n%60<10?"0":"")+(n%60);}}}},{s:.3f});}})();')
t = s
while t < e:
    ep.cue("tick.wav", t, 0.45)
    t += 1.0
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S07 water pours in around your feet — freezing, fast
s, e = cut(40), cut(49)
html = '<div class="num" id="s07-t" style="top:590px;left:640px;width:440px;font-size:110px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9);">4°C</div>'
ep.scene("s07", s, e, cabin("s07c", 1480), html, origin="50% 60%", fx=[(W(41), e, "sparks", dict(cx=540, cy=1460, n=40, r=360, dur=0.6, color="#9FC8FF", g=200))])
ep.js(f'tl.to("#s07c-w",{{y:-260,duration:{e - W(41):.3f},ease:"power1.in"}},{W(41) - 0.1:.3f});')
ep.pop("#s07-t", W(47) - 0.05, 0.2, 1.4, "power3.out")
ep.cue("water_rush.mp3", W(41) - 0.1, 0.9)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S08 you push the door — it won't move
s, e = cut(49), cut(56)
door = glow(N("M 140 700 L 760 700 L 800 1600 L 140 1600 Z", fill="#0c0f1a", sw=12, cw=4)) + f'<rect x="200" y="760" width="520" height="330" fill="#1a2440" stroke="#9FC8FF" stroke-width="5"/>' + '<rect x="250" y="1150" width="160" height="40" rx="12" fill="#3a3a44" stroke="#F2EEEA" stroke-width="4"/>'
press = "".join(f'<g class="s08-a" filter="url(#glowB)">' + N(f"M 1060 {y} L 860 {y} M 900 {y - 40} L 860 {y} L 900 {y + 40}", fill="none", red=SEA, core=SEA_CORE, sw=10, cw=3) + '</g>' for y in (850, 1100, 1350))
hand = f'<g id="s08-h"><g transform="translate(560,1180) rotate(-90) scale(1.3)">' + glow(N(HAND, fill="#2a0a0c", sw=12, cw=4)) + '</g></g>'
water = f'<rect x="-100" y="1350" width="1280" height="700" fill="#1a3a8a" opacity="0.6"/>'
svg = door + water + press + hand
ep.scene("s08", s, e, svg, origin="50% 55%")
for k in range(int((e - W(50)) / 0.28)):
    ep.js(f'tl.to("#s08-h",{{x:{30 if k % 2 == 0 else 0},duration:0.14,ease:"power2.out",yoyo:true,repeat:1}},{W(50) + k * 0.28:.3f});')
ep.js(f'tl.fromTo(".s08-a",{{x:60,opacity:0}},{{x:0,opacity:1,duration:0.3,stagger:0.08,immediateRender:false}},{W(54) - 0.1:.3f});')
ep.js('gsap.set(".s08-a",{opacity:0});')
ep.cue("lid_knock.mp3", W(50), 0.7)
ep.cue("lid_knock.mp3", W(52), 0.7)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S09 the water presses on it with the weight of a horse
s, e = cut(56), cut(68)
HORSE = ("M 300 1300 L 320 1120 Q 300 1000 360 960 L 640 950 Q 700 900 720 820 L 700 760 Q 720 720 770 740 L 840 800 Q 860 840 820 860 L 780 870 Q 760 960 730 1000 "
         "L 720 1120 L 740 1300 L 700 1300 L 680 1130 L 640 1080 L 420 1080 L 380 1130 L 360 1300 Z M 300 990 Q 240 1040 250 1140")
svg = glow(N(HORSE, fill="#140a0a", sw=10, cw=3), gid="s09-hs") + press.replace("s08-a", "s09-a")
html = '<div class="num" id="s09-n" style="top:1380px;font-size:150px;">0 KG</div><div class="lbl" style="top:1540px;">ON YOUR DOOR</div>'
ep.scene("s09", s, e, svg, html, origin="50% 55%")
ep.pop("#s09-hs", W(65) - 0.1, 0.3, 0.3)
ep.js(f'(function(){{var el=document.getElementById("s09-n");var o={{v:0}};tl.to(o,{{v:500,duration:{WE(67) - W(59) + 0.2:.3f},ease:"power2.out",onUpdate:function(){{el.textContent="~"+Math.round(o.v)+" KG";}}}},{W(59) - 0.1:.3f});}})();')
ep.cue("impact-bass-2.mp3", W(67), 0.6)
ep.cue("hull_creak.mp3", W(59), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S10 you hit the window button — nothing — the electrics are dead
s, e = cut(68), cut(78)
panel = glow(N("M 200 900 L 880 900 L 880 1360 L 200 1360 Z", fill="#14161c", sw=10, cw=3))
btn = f'<g id="s10-btn"><rect x="460" y="1020" width="160" height="220" rx="24" fill="#2a2a34" stroke="#F2EEEA" stroke-width="5"/>' + N("M 540 1060 L 500 1120 L 580 1120 Z", fill="#F2EEEA", sw=4, cw=2) + N("M 540 1200 L 500 1140 L 580 1140 Z", fill="#F2EEEA", sw=4, cw=2) + '</g>'
leds = "".join(f'<circle class="s10-led" cx="{x}" cy="960" r="12" fill="#4ACF7A" filter="url(#glowS)"/>' for x in (260, 310, 360, 720, 770, 820))
svg = panel + btn + leds + bigx("s10-x", 540, 1130, 150, 20) + f'<rect x="-100" y="1420" width="1280" height="700" fill="#1a3a8a" opacity="0.6"/>'
ep.scene("s10", s, e, svg, origin="50% 58%")
for k in range(3):
    ep.js(f'tl.fromTo("#s10-btn",{{scale:0.92,svgOrigin:"540 1130"}},{{scale:1,svgOrigin:"540 1130",duration:0.18,ease:"power2.out",immediateRender:false}},{W(69) + k * 0.3:.3f});')
ep.pop("#s10-x", W(73) - 0.05, 0.18, 1.6, "power3.out")
for k, op in enumerate((0.2, 1, 0.1, 0.8, 0)):
    ep.js(f'tl.set(".s10-led",{{opacity:{op}}},{W(76) + k * 0.08:.3f});')
ep.cue("click_dead.mp3", W(69), 0.9)
ep.cue("glitch.mp3", W(76), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S11 the water reaches your chest — then your chin
s, e = cut(78), cut(86)
ep.scene("s11", s, e, cabin("s11c", 1220, mouth=True), origin="50% 50%", fx=[(s, e, "ash", dict(n=30, sp=-80, color="#9FC8FF", y0=700))])
ep.js(f'tl.fromTo("#s11c-w",{{y:0}},{{y:-150,duration:{W(82) - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s11c-w",{{y:-330,duration:{WE(85) - W(83) + 0.2:.3f},ease:"power2.in"}},{W(83) - 0.1:.3f});')
ep.cue("water_rush.mp3", s, 0.8)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S12 the car tips forward, engine first, into the dark
s, e = cut(86), cut(95)
svg = river(700) + f'<g id="s12-c">{car("c12", 540, 980, 1.1, lights=True)}</g>' + bubbles("s12-b", 30, 12, 380, 720, 900, 1500)
ep.scene("s12", s, e, svg, origin="50% 55%", drift=0.02)
ep.js(f'tl.to("#s12-c",{{rotation:60,svgOrigin:"540 980",duration:{W(90) - s + 0.3:.3f},ease:"power2.inOut"}},{s + 0.1:.3f});')
ep.js(f'tl.to("#s12-c",{{y:900,duration:{e - W(91):.3f},ease:"power2.in"}},{W(91):.3f});')
ep.js(f'tl.to("#c12-hl",{{opacity:0.1,duration:0.4}},{W(94) - 0.2:.3f});')
ep.js(f'tl.fromTo(".s12-b",{{y:0,opacity:0.9}},{{y:-500,opacity:0,duration:1.2,stagger:0.05,ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.cue("underwater_muffle.mp3", s, 0.9)
ep.cue("hull_creak.mp3", W(88), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S13 you press your face to the roof and take one last breath
s, e = cut(95), cut(107)
roof = hline(760, -100, 1180, 14, 5)
water = '<rect id="s13-wt" x="-100" y="1030" width="1280" height="1200" fill="#1a3a8a" opacity="0.75"/>' + line(-100, 1030, 1180, 1030, "#9FC8FF", 5, 'id="s13-wl"')
svg = f'<rect x="-100" y="760" width="1280" height="1400" fill="#06102a"/>' + mascot("m13", 540, 1800, 1.6, mouth_open=True) + water + roof + bubbles("s13-b", 20, 13, 380, 700, 1100, 1500)
ep.scene("s13", s, e, svg, origin="50% 45%", drift=0.03)
ep.js(f'tl.to("#s13-wt",{{attr:{{y:978}},duration:{e - s:.3f},ease:"power1.in"}},{s:.3f});')
ep.js(f'tl.to("#s13-wl",{{attr:{{y1:978,y2:978}},duration:{e - s:.3f},ease:"power1.in"}},{s:.3f});')
ep.js(f'tl.fromTo(".s13-b",{{y:0,opacity:0.9}},{{y:-400,opacity:0,duration:1.2,stagger:{{each:0.1,repeat:{int((e - s) / 2)}}},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.cue("underwater_muffle.mp3", s, 0.6)
ep.cue("riser.mp3", W(103), 0.4)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S14 experts say: seatbelt off, window open, get out, in the first minute
s, e = cut(107), cut(123)
items = [("SEATBELT OFF", W(113)), ("WINDOW OPEN", W(115)), ("GET OUT", W(117)), ("IN THE FIRST MINUTE", W(119))]
html = '<div class="lbl" id="s14-h" style="top:600px;color:#FFE08A;font-size:42px;">THE ONLY WAY OUT</div>'
for k, (txt, t) in enumerate(items):
    html += (f'<div id="s14-i{k}" style="position:absolute;left:150px;top:{760 + k * 190}px;width:800px;font-weight:900;font-size:{64 if k < 3 else 52}px;letter-spacing:2px;'
             f'color:{"#F5F5F5" if k < 3 else "#FFE08A"};"><span style="color:#4ACF7A;margin-right:28px;">{"✓" if k < 3 else "⏱"}</span>{txt}</div>')
ep.scene("s14", s, e, "", html, origin="50% 50%")
ep.pop("#s14-h", W(108) - 0.05, 0.2, 1.3, "power3.out")
for k, (txt, t) in enumerate(items):
    ep.js(f'tl.fromTo("#s14-i{k}",{{x:-80,opacity:0}},{{x:0,opacity:1,duration:0.2,ease:"power3.out",immediateRender:false}},{t - 0.05:.3f});')
    ep.js(f'gsap.set("#s14-i{k}",{{opacity:0}});')
    ep.cue("pop.mp3", t - 0.05, 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S15 nobody ever told you
s, e = cut(123), cut(127)
svg = f'<rect x="-100" y="-100" width="1280" height="2200" fill="#06102a"/>' + f'<g id="s15-m">{mascot("m15", 540, 1500, 0.9, style="dim", pose=dict(uarmL=150, uarmR=-150, thighL=10, thighR=-10))}</g>' + bubbles("s15-b", 16, 15, 460, 620, 700, 900)
ep.scene("s15", s, e, svg, origin="50% 55%")
ep.js(f'tl.fromTo("#s15-m",{{y:-100,opacity:1}},{{y:200,opacity:0.4,duration:{e - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo(".s15-b",{{y:0,opacity:0.9}},{{y:-300,opacity:0,duration:1.0,stagger:0.12,ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.cue("underwater_muffle.mp3", s, 0.6)

# ---------------------------------------------------------------- ending
ep.ending(cut(127), 130)
ep.write(red=["sinks", "control", "railing", "water", "airbag", "floats", "freezing", "fast", "move", "horse", "nothing", "dead", "chin", "dark", "breath", "seatbelt", "window", "out", "minute", "told"])
