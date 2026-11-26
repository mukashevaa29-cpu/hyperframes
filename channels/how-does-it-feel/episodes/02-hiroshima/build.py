"""Episode 02 — How does it feel? When you're in Hiroshima the moment the atomic bomb goes off."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
ORANGE = "#FF9B4F"


def city_hiro(base=1400, s=1.0, seed=3, gid=""):
    """Hiroshima skyline with the dome (Industrial Promotion Hall)."""
    rnd = random.Random(seed)
    out = []
    x = -20
    while x < 1100:
        if 330 < x < 420:
            # the dome building
            w, h = 230 * s, 150 * s
            out.append(f'<path d="M{x},{base} L{x},{base - h} L{x + w},{base - h} L{x + w},{base} Z" fill="#050404" stroke="#E8706A" stroke-width="{3 * s}"/>')
            out.append(f'<path d="M{x + w / 2 - 60 * s},{base - h} L{x + w / 2 - 60 * s},{base - h - 40 * s} L{x + w / 2 + 60 * s},{base - h - 40 * s} L{x + w / 2 + 60 * s},{base - h} Z" fill="#050404" stroke="#E8706A" stroke-width="{3 * s}"/>')
            out.append(f'<path d="M{x + w / 2 - 56 * s},{base - h - 40 * s} A{56 * s},{60 * s} 0 0 1 {x + w / 2 + 56 * s},{base - h - 40 * s}" fill="#050404" stroke="#E8706A" stroke-width="{4 * s}"/>')
            for k in range(5):
                out.append(f'<rect x="{x + 18 * s + k * 42 * s:.0f}" y="{base - h + 30 * s:.0f}" width="{16 * s:.0f}" height="{24 * s:.0f}" fill="#E0602A"/>')
            x += w + 14
            continue
        w = rnd.uniform(60, 120) * s
        h = rnd.uniform(50, 130) * s
        top = base - h
        out.append(f'<path d="M{x},{base} L{x},{top} L{x + w},{top} L{x + w},{base} Z" fill="#050404" stroke="#E8706A" stroke-width="{3 * s}"/>')
        if rnd.random() < 0.5:  # Japanese tiled roof
            out.append(f'<path d="M{x - 10 * s},{top} Q{x + w / 2},{top - 34 * s} {x + w + 10 * s},{top} Z" fill="#050404" stroke="#E8706A" stroke-width="{3 * s}"/>')
        for k in range(int(w // (30 * s))):
            if rnd.random() < 0.5:
                out.append(f'<rect x="{x + 10 * s + k * 30 * s:.0f}" y="{top + rnd.uniform(14, max(16, h - 34 * s)):.0f}" width="{11 * s:.0f}" height="{15 * s:.0f}" fill="#E0602A"/>')
        x += w + rnd.uniform(4, 14) * s
    i = f' id="{gid}"' if gid else ""
    return f'<g{i} filter="url(#glowS)">{"".join(out)}</g>'


def mushroom(gid, cx=540, base=1380, top=420, w1=300):
    stem = puffs(cx, base, top + 120, 7, 50, w1 * 0.5, umbrella=False, fill="#801F0C", hi="#B3401A")
    cap = puffs(cx, top + 160, top, 8, w1 * 0.6, w1 * 1.3, umbrella=True, fill="#801F0C", hi="#B3401A")
    core = f'<ellipse cx="{cx}" cy="{top + 40}" rx="{w1 * 0.55:.0f}" ry="{w1 * 0.25:.0f}" fill="{ORANGE}" opacity="0.85" filter="url(#soft2)"/>'
    rings = f'<ellipse cx="{cx}" cy="{top + 230}" rx="{w1 * 0.8:.0f}" ry="40" fill="none" stroke="#FFD0A0" stroke-width="5" opacity="0.6"/>'
    return f'<g id="{gid}" filter="url(#glowO)">{stem}{cap}{core}{rings}</g>'


# ---------------------------------------------------------------- S01 cold open: the mushroom cloud (frame 0 = thumbnail)
s, e = 0.0, cut(4)
svg = mushroom("s01-m", top=660) + city_hiro(1420) + hline(1420)
ep.scene("s01", s, e, svg, origin="50% 40%", custom_cam=True, fx=[(s, e, "embers", dict(n=40, x0=100, x1=980, y0=500, y1=1500, sp=180))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:1.25}},{{scale:1.12,duration:{e:.3f},ease:"power1.out"}},0);')
ep.js(f'tl.fromTo("#s01-m",{{scale:0.95,transformOrigin:"50% 100%"}},{{scale:1.05,duration:{e:.3f},ease:"none"}},0);')
ep.floor(0, 0.3, 1.0, 0.01)
ep.cue("sfx_open_roar.mp3", 0, 0.8)
ep.cue("sub.wav", 0, 0.9)

# ---------------------------------------------------------------- S02 the city, the bomb falls, detonation
s, e = cut(4), cut(15)
bomb = ('<g id="s02-bomb"><g transform="translate(560,300)">'
        + glow(N("M -26 0 Q -26 -60 0 -70 Q 26 -60 26 0 L 26 60 Q 26 90 0 96 Q -26 90 -26 60 Z", fill="#141016", sw=8, cw=3)
               + '<path d="M -26 -40 L -48 -80 L 48 -80 L 26 -40" fill="#141016" stroke="#F2EEEA" stroke-width="4"/>') + '</g></g>')
svg = (f'<g id="s02-fb" opacity="0"><circle cx="560" cy="760" r="240" fill="url(#sunGrad)" filter="url(#glowO)"/></g>'
       + f'<g id="s02-mW" opacity="0">{mushroom("s02-m", cx=560, top=430)}</g>'
       + bomb + city_hiro(1420, gid="s02-city") + hline(1420))
ep.scene("s02", s, e, svg, origin="50% 55%", drift=0.012, fx=[(W(13) + 0.1, e, "embers", dict(n=50, x0=0, x1=1080, y0=500, y1=1500, sp=260, wind=200))])
td = W(13)
ep.js(f'tl.fromTo("#s02-bomb",{{y:-200,rotation:0}},{{y:420,rotation:8,svgOrigin:"560 300",duration:{td - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.set("#s02-bomb",{{opacity:0}},{td:.3f});')
ep.js(f'tl.fromTo("#s02-fb",{{opacity:1,scale:0.05,svgOrigin:"560 760"}},{{scale:1.4,duration:0.5,ease:"expo.out",immediateRender:false}},{td:.3f});')
ep.js(f'tl.to("#s02-fb",{{opacity:0,duration:0.6}},{td + 0.5:.3f});')
ep.js(f'tl.fromTo("#s02-mW",{{opacity:0}},{{opacity:1,duration:0.3,immediateRender:false}},{td + 0.3:.3f});')
ep.js(f'tl.fromTo("#s02-m",{{scale:0.2,transformOrigin:"50% 100%"}},{{scale:1,duration:1.4,ease:"power3.out",immediateRender:false}},{td + 0.3:.3f});')
ep.js(f'tl.to("#s02-city",{{skewX:-14,transformOrigin:"50% 100%",duration:0.4,ease:"power2.out"}},{td + 0.15:.3f});')
ep.flash(td, 0.97, 1.0)
ep.shake("#s02-shake", td + 0.1, 0.9, 18)
ep.floor(s, 0.6, 0.0)
ep.floor(td, 0.3, 1.0, 0.1)
ep.cue("whoosh-cinematic.mp3", td - 1.0, 0.5)
ep.cue("sfx_open_roar.mp3", td, 1.0)
ep.cue("impact-bass-2.mp3", td, 1.0)
ep.cue("sub.wav", td, 1.0)

# ---------------------------------------------------------------- S03 500 m from ground zero (blast map)
s, e = cut(15), cut(21)
rivers = ('<path d="M -40 1500 C 200 1300 300 1100 420 980 C 520 880 700 760 1120 600" fill="none" stroke="#5A78FF" stroke-width="22" stroke-linecap="round" filter="url(#glowB)" opacity="0.85"/>'
          '<path d="M 300 1700 C 420 1400 520 1200 600 1060 C 680 920 820 860 1120 900" fill="none" stroke="#5A78FF" stroke-width="16" stroke-linecap="round" filter="url(#glowB)" opacity="0.7"/>')
rings = ""
for k, (r, lab) in enumerate([(130, "500 M"), (260, "1 KM"), (420, "2 KM")]):
    rings += (f'<g id="s03-r{k}" opacity="0"><g filter="url(#glow)"><circle cx="540" cy="1000" r="{r}" fill="none" stroke="#FB2945" stroke-width="8"/>'
              f'<circle cx="540" cy="1000" r="{r}" fill="none" stroke="#F2EEEA" stroke-width="3"/></g>' + label(540 - r * 0.72 - 10, 1000 - r * 0.72 - 10, lab, 30, "#F5F5F5", "end") + '</g>')
svg = (rivers + rings + '<circle cx="540" cy="1000" r="20" fill="#FF3B36" filter="url(#glow)"/>' + label(540, 1060, "GROUND ZERO", 28, "#FF6A5A")
       + f'<g id="s03-you" opacity="0"><circle cx="{540 - 92}" cy="{1000 + 92}" r="14" fill="#FFFFFF" filter="url(#glowB)"/>' + label(540 - 92, 1000 + 150, "YOU", 32, "#FFFFFF") + '</g>')
ep.scene("s03", s, e, svg, origin="50% 52%", drift=0.02)
for k in range(3):
    ep.js(f'tl.fromTo("#s03-r{k}",{{opacity:1,scale:0,svgOrigin:"540 1000"}},{{scale:1,duration:0.25,ease:"power3.out",immediateRender:false}},{s + 0.1 + k * 0.18:.3f});')
    ep.js(f'tl.set("#s03-r{k}",{{opacity:0}},0);')
    ep.cue("pop.mp3", s + 0.1 + k * 0.18, 0.35)
ep.pop("#s03-you", W(16) - 0.05, 0.2, 0.2)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S04 A flash.
s, e = cut(21), cut(23)
svg = mascot("m4", 540, 1560, 1.25, pose=dict(uarmL=60, farmL=50, uarmR=-60, farmR=-50, head=-6))
ep.scene("s04", s, e, svg, origin="50% 60%")
ep.flash(W(22) - 0.05, 1.0, 1.1)
ep.cue("impact-bass-1.mp3", W(22) - 0.05, 0.9)
ep.cue("riser.mp3", W(22) + 0.1, 0.25)
ep.floor(s, 0.5, 0.3)

# ---------------------------------------------------------------- S05 the light burns your retinas
s, e = cut(23), cut(39)
EYE = "M 160 1000 Q 540 690 920 1000 Q 540 1310 160 1000 Z"
ir = "".join(line(540 + 70 * math.cos(a), 1000 + 70 * math.sin(a), 540 + 145 * math.cos(a), 1000 + 145 * math.sin(a), "#8a0f12", 4) for a in [i * math.pi / 12 for i in range(24)])
lashes = ""
for i in range(2, 12):
    tt = i / 13
    x0, y0 = 160 + 760 * tt, 1000 - 4 * 155 * tt * (1 - tt) * 2
    lashes += line(x0, y0, x0 + (tt - 0.5) * 40, y0 - 46, CORE, 6)
svg = (f'<defs><clipPath id="s05-clip"><path d="{EYE}"/></clipPath></defs><g filter="url(#glow)"><path d="{EYE}" fill="#ECE6E5" stroke="{RED}" stroke-width="22"/></g>'
       f'<g clip-path="url(#s05-clip)"><g id="s05-veins" opacity="0"><path d="M 200 1000 Q 240 985 262 1005 Q 280 990 300 1000 M 880 1000 Q 840 1012 822 994 Q 800 1008 780 998 M 240 960 L 300 980 M 820 1040 L 760 1020" fill="none" stroke="#C2181E" stroke-width="5"/></g>'
       f'<circle cx="540" cy="1000" r="150" fill="#D32620"/>{ir}<circle id="s05-pupil" cx="540" cy="1000" r="60" fill="#160404"/>'
       f'<circle id="s05-burn" cx="540" cy="1000" r="10" fill="#FFF1DC" filter="url(#glowO)"/><circle cx="582" cy="958" r="18" fill="#FFFFFF"/></g>'
       f'<path d="{EYE}" fill="none" stroke="{CORE}" stroke-width="6"/>{lashes}')
ep.scene("s05", s, e, svg, origin="50% 52%", drift=0.025)
tb = W(29) - 0.1
ep.js(f'tl.to("#s05-burn",{{attr:{{r:150}},duration:{WE(31) + 0.3 - tb:.3f},ease:"power2.inOut"}},{tb:.3f});')
ep.show("#s05-veins", tb, 0.6)
ep.js(f'tl.to("#s05-burn",{{attr:{{fill:"#3a1a10"}},duration:1.2}},{WE(38) - 0.6:.3f});')
ep.cue("sizzle.wav", tb, 0.35)
ep.floor(s, 0.4, 0.1)

# ---------------------------------------------------------------- S06 then comes the heat
s, e = cut(39), cut(43)
waves = "".join(f'<path class="s06-w" d="M -200 {700 + k * 160} ' + " ".join(f"Q {-200 + i * 120 + 60} {700 + k * 160 + (-30 if i % 2 == 0 else 30)} {-200 + (i + 1) * 120} {700 + k * 160}" for i in range(13))
                + f'" fill="none" stroke="#FF6A3A" stroke-width="7" opacity="0.7" filter="url(#glowO)"/>' for k in range(5))
svg = f'<g id="s06-wv">{waves}</g>' + mascot("m6", 800, 1560, 0.9, pose=dict(uarmL=120, farmL=60, head=12))
ep.scene("s06", s, e, svg, origin="50% 55%", fx=[(s, e, "embers", dict(n=40, x0=0, x1=1080, y0=500, y1=1600, sp=240, wind=300))])
ep.js(f'tl.fromTo(".s06-w",{{x:-240}},{{x:240,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.cue("roar.mp3", s, 0.6)
ep.floor(s, 0.2, 1.0, 0.2)

# ---------------------------------------------------------------- S07 skin blisters... and bursts
s, e = cut(43), cut(48)
skin = (glow(N("M 200 960 L 880 960 L 880 1220 L 200 1220 Z", fill="#1a0a0a"))
        + f'<path d="M 200 1010 L 880 1010" stroke="#F2EEEA" stroke-width="3" opacity="0.6"/>'
        + "".join(f'<path d="M 220 {1060 + k * 40} Q 380 {1040 + k * 40} 540 {1060 + k * 40} T 860 {1060 + k * 40}" fill="none" stroke="#E87A8A" stroke-width="4" opacity="0.7"/>' for k in range(3))
        + label(540, 900, "SKIN", 30, GREY))
blis = "".join(f'<g id="s07-b{k}" opacity="0"><path d="M {250 + k * 110} 962 A 46 52 0 0 1 {342 + k * 110} 962 Z" fill="#E8A0A0" stroke="#FFF1DC" stroke-width="5" filter="url(#glowS)"/></g>' for k in range(6))
svg = skin + blis
fxs = [(W(47) + i * 0.0, W(47) + 0.6, "sparks", dict(cx=296 + i * 110, cy=930, n=10, r=110, dur=0.5, color="#FF4A4E", g=120)) for i in range(6)]
ep.scene("s07", s, e, svg, origin="50% 52%", drift=0.03, fx=fxs)
for k in range(6):
    ep.js(f'tl.fromTo("#s07-b{k}",{{opacity:1,scale:0,svgOrigin:"{296 + k * 110} 962"}},{{scale:1,duration:0.18,ease:"back.out(2)",immediateRender:false}},{W(45) - 0.05 + k * 0.1:.3f});')
    ep.js(f'tl.set("#s07-b{k}",{{opacity:0}},0);')
    ep.js(f'tl.set("#s07-b{k}",{{opacity:0}},{W(47) - 0.02:.3f});')
    ep.cue("pop.mp3", W(45) - 0.05 + k * 0.1, 0.2)
ep.cue("impact-bass-1.mp3", W(47), 0.5)
ep.floor(s, 0.5, 0.6)

# ---------------------------------------------------------------- S08 patterns burned into your body
s, e = cut(48), cut(59)
TOR = "M 380 760 Q 540 720 700 760 L 720 1000 Q 730 1200 690 1380 L 390 1380 Q 350 1200 360 1000 Z"
flowers = ""
for k, (fx, fy) in enumerate([(450, 880), (620, 940), (480, 1110), (640, 1200), (520, 1300)]):
    flowers += f'<g class="s08-fl">' + "".join(f'<circle cx="{fx + 26 * math.cos(a):.0f}" cy="{fy + 26 * math.sin(a):.0f}" r="16" fill="#F2EEEA"/>' for a in [i * 2 * math.pi / 5 for i in range(5)]) + f'<circle cx="{fx}" cy="{fy}" r="10" fill="#C2181E"/></g>'
stripes = "".join(f'<line x1="{340 + k * 60}" y1="740" x2="{240 + k * 60}" y2="1400" stroke="#F2EEEA" stroke-width="3" opacity="0.35"/>' for k in range(10))
svg = (f'<defs><clipPath id="s08-c"><path d="{TOR}"/></clipPath></defs>' + glow(N(TOR, fill="#44140E"))
       + f'<g clip-path="url(#s08-c)">{stripes}{flowers}<rect id="s08-heat" x="300" y="700" width="500" height="760" fill="#FF6A2A" opacity="0" filter="url(#soft2)"/></g>'
       + label(540, 680, "KIMONO PATTERN", 28, GREY))
ep.scene("s08", s, e, svg, origin="50% 55%", drift=0.02)
tb8 = W(54) - 0.05
ep.js(f'tl.to("#s08-heat",{{opacity:0.35,duration:0.25}},{tb8:.3f});')
ep.js(f'tl.to(".s08-fl circle",{{fill:"#3a0d08",duration:0.6,stagger:0.03}},{tb8 + 0.1:.3f});')
ep.js(f'tl.to("#s08-heat",{{opacity:0.15,duration:1.0}},{tb8 + 0.5:.3f});')
ep.cue("sizzle.wav", tb8, 0.5)
ep.floor(s, 0.5, 0.5)

# ---------------------------------------------------------------- S09 one second later
s, e = cut(59), cut(62)
ep.timer("s09", s, e, W(60) - 0.05, WE(61), 0, 1, "ms", "SECOND LATER", 1 / 60)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S10 the shock wave
s, e = cut(62), cut(65)
wave = ('<g id="s10-wave"><g filter="url(#glow)"><path d="M -60 500 Q 120 1000 -60 1500" fill="none" stroke="#FB2945" stroke-width="18"/>'
        '<path d="M -120 520 Q 40 1000 -120 1480" fill="none" stroke="#F2EEEA" stroke-width="6" opacity="0.7"/></g></g>')
svg = city_hiro(1420, gid="s10-city", seed=9) + hline(1420) + mascot("m10", 760, 1420, 0.7, pose=dict(uarmL=-30, uarmR=30)) + wave
ep.scene("s10", s, e, svg, origin="50% 60%", fx=[(W(63), e, "ash", dict(n=120, sp=0, x0=0, x1=1080, y0=500, y1=1500, color="#E8706A"))])
tw = W(63) - 0.05
ep.js(f'tl.fromTo("#s10-wave",{{x:0}},{{x:1400,duration:0.55,ease:"power2.out",immediateRender:false}},{tw:.3f});')
ep.js(f'tl.to("#s10-city",{{skewX:22,transformOrigin:"50% 100%",duration:0.35,ease:"power2.out"}},{tw + 0.15:.3f});')
ep.js(f'tl.to("#m10",{{rotation:70,svgOrigin:"760 1420",x:160,duration:0.4,ease:"power2.out"}},{tw + 0.3:.3f});')
ep.shake("#s10-shake", tw + 0.15, 0.7, 20)
ep.cue("sfx_open_roar.mp3", tw, 0.9)
ep.cue("impact-bass-2.mp3", tw + 0.15, 1.0)
ep.cue("sub.wav", tw + 0.15, 0.9)
ep.floor(s, 0.4, 0.8)

# ---------------------------------------------------------------- S11 your eardrums burst
s, e = cut(65), cut(68)
ear = (glow(N("M 560 700 C 360 690 300 880 340 1000 C 370 1080 420 1100 420 1180 C 420 1270 500 1320 580 1280 C 620 1260 640 1220 640 1180", fill="none", sw=22, cw=6))
       + glow(N("M 520 800 C 420 800 410 900 450 960 C 480 1000 520 1000 540 960", fill="none", sw=14, cw=4))
       + line(560, 980, 780, 980, CORE, 6)
       + f'<g id="s11-drum"><g filter="url(#glow)"><ellipse cx="820" cy="980" rx="22" ry="70" fill="#2a0a0c" stroke="#FB2945" stroke-width="10"/></g></g>'
       + label(700, 1110, "EARDRUM", 28, GREY))
arcs = "".join(f'<path class="s11-a" d="M {200 - k * 40} 860 Q {240 - k * 40} 980 {200 - k * 40} 1100" fill="none" stroke="#F2EEEA" stroke-width="6" opacity="0.8"/>' for k in range(3))
svg = ear + f'<g id="s11-arcs">{arcs}</g>'
ep.scene("s11", s, e, svg, origin="60% 52%", fx=[(W(67), e, "sparks", dict(cx=820, cy=980, n=24, r=120, dur=0.6, color="#FF3B36", g=200))])
ep.js(f'tl.fromTo("#s11-arcs",{{x:-100}},{{x:320,duration:{W(67) - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s11-drum",{{scaleY:0.2,svgOrigin:"820 980",duration:0.08}},{W(67) - 0.02:.3f});')
ep.flash(W(67), 0.3, 0.3)
ep.cue("impact-bass-1.mp3", W(67), 0.8)
ep.cue("beep.wav", W(67) + 0.1, 0.05)
ep.floor(s, 0.5, 0.2)

# ---------------------------------------------------------------- S12 glass tears into your skin
s, e = cut(68), cut(77)
pane = glow(N("M 140 700 L 520 700 L 520 1200 L 140 1200 Z", fill="#1a2a40", red="#5A78FF", core="#CFE0FF"), f="glowB", gid="s12-pane")
crack = '<path id="s12-crack" d="M 330 950 L 260 840 M 330 950 L 440 820 M 330 950 L 460 1060 M 330 950 L 210 1100 M 330 950 L 180 940" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="900" stroke-dashoffset="900"/>'
sr = random.Random(12)
shards = ""
for k in range(18):
    x, y = sr.uniform(160, 500), sr.uniform(720, 1180)
    pts = " ".join(f"{x + sr.uniform(-22, 22):.0f},{y + sr.uniform(-30, 30):.0f}" for _ in range(3))
    shards += f'<polygon id="s12-sh{k}" points="{pts}" fill="#9FC8FF" stroke="#FFFFFF" stroke-width="3" opacity="0" filter="url(#glowB)"/>'
blood = "".join(f'<circle class="s12-bl" cx="{800 + sr.uniform(-60, 60):.0f}" cy="{sr.uniform(1050, 1350):.0f}" r="{sr.uniform(8, 16):.0f}" fill="#C2181E" opacity="0"/>' for _ in range(9))
svg = pane + crack + shards + mascot("m12", 820, 1560, 0.75, pose=dict(uarmL=150, farmL=40)) + blood
ep.scene("s12", s, e, svg, origin="50% 55%")
tc = W(68) - 0.05
ep.js(f'tl.to("#s12-crack",{{strokeDashoffset:0,duration:0.25,ease:"power2.out"}},{tc:.3f});')
tsh = W(69) + 0.05
ep.js(f'tl.set("#s12-pane, #s12-crack",{{opacity:0}},{tsh:.3f});')
for k in range(18):
    ep.js(f'tl.fromTo("#s12-sh{k}",{{opacity:1,x:0,y:0,rotation:0}},{{x:{sr.uniform(380, 560):.0f},y:{sr.uniform(-40, 260):.0f},rotation:{sr.uniform(-300, 300):.0f},svgOrigin:"330 950",duration:{sr.uniform(0.35, 0.6):.2f},ease:"power2.out",immediateRender:false}},{tsh + k * 0.012:.3f});')
    ep.js(f'tl.set("#s12-sh{k}",{{opacity:0}},0);')
ep.js(f'tl.to(".s12-bl",{{opacity:0.9,duration:0.2,stagger:0.12}},{W(74):.3f});')
ep.flash(tsh, 0.45, 0.3)
ep.cue("sfx_collapse.mp3", tsh, 0.7)
ep.cue("impact-bass-1.mp3", tsh, 0.6)
ep.floor(s, 0.5, 0.2)

# ---------------------------------------------------------------- S13 stone wall, shadow remains
s, e = cut(77), cut(87)
bricks = ""
for row in range(14):
    y = 600 + row * 60
    off = 0 if row % 2 == 0 else 60
    for c in range(-1, 10):
        bricks += f'<rect x="{c * 120 + off}" y="{y}" width="116" height="56" fill="#716761" stroke="#5a524d" stroke-width="3"/>'
wall = f'<g>{bricks}</g><rect x="0" y="1440" width="1080" height="60" fill="#3a3330"/><rect x="0" y="1500" width="1080" height="420" fill="#272221"/><rect x="0" y="560" width="1080" height="140" fill="url(#s13-fadeG)"/>'
defs = '<defs><linearGradient id="s13-fadeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#010101"/><stop offset="1" stop-color="#010101" stop-opacity="0"/></linearGradient></defs>'
shadow = f'<g id="s13-shadow" opacity="0">{mascot("m13s", 560, 1440, 1.0, style="shadow", pose=dict(uarmR=-150, farmR=-30))}</g>'
svg = defs + wall + shadow + f'<g id="s13-manW">{mascot("m13", 520, 1500, 1.0, style="stone", pose=dict(uarmR=-150, farmR=-30))}</g>'
tsh = W(85) - 0.05
ep.scene("s13", s, e, svg, origin="50% 60%", drift=0.015, fx=[(tsh + 0.15, e, "embers", dict(n=60, x0=320, x1=760, y0=800, y1=1500, sp=160, wind=500))])
ep.js(f'gsap.set("#m13s g",{{}});')
ep.js(f'tl.to("#s13-manW",{{opacity:0,duration:0.5,ease:"power2.in"}},{tsh + 0.15:.3f});')
ep.show("#s13-shadow", tsh + 0.05, 0.3)
ep.flash(tsh, 0.95, 1.0)
ep.cue("sfx_open_roar.mp3", tsh, 0.7)
ep.cue("sub.wav", tsh, 0.9)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- S14 the shadow of who you were → the watch at 8:15
s, e = cut(87), cut(97)
watch = ('<g id="s14-watch"><g filter="url(#glowG)"><circle cx="760" cy="1440" r="70" fill="#E9E1D2" stroke="#C9A464" stroke-width="14"/>'
         + line(760, 1440, 760 + 34 * math.cos(math.radians(-90 + 8.25 * 30)), 1440 + 34 * math.sin(math.radians(-90 + 8.25 * 30)), "#141010", 8)
         + line(760, 1440, 760 + 52 * math.cos(math.radians(-90 + 15 * 6)), 1440 + 52 * math.sin(math.radians(-90 + 15 * 6)), "#141010", 6)
         + '<path d="M 720 1400 L 760 1430 L 800 1405 M 760 1430 L 750 1490" stroke="#8a837e" stroke-width="3" fill="none"/>'
         + '<circle cx="760" cy="1362" r="12" fill="none" stroke="#C9A464" stroke-width="6"/></g></g>')
svg = defs.replace("s13-fadeG", "s14-fadeG") + wall.replace("s13-fadeG", "s14-fadeG") + mascot("m14s", 560, 1440, 1.0, style="shadow", pose=dict(uarmR=-150, farmR=-30)) + watch
ep.scene("s14", s, e, svg, origin="70% 75%", custom_cam=True, fx=[(s, e, "ash", dict(n=50, sp=40, color="#9a908a"))])
ep.js(f'tl.fromTo("#s14-cam",{{scale:1.0}},{{scale:1.15,duration:{W(94) - s:.3f},ease:"sine.out",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s14-cam",{{scale:2.6,duration:0.9,ease:"power2.inOut"}},{W(94):.3f});')
t = W(94)
while t < e:
    ep.cue("tick.wav", t, 0.35)
    t += 1.0
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(97), 100)
ep.write(red=["hiroshima", "flash", "heat", "shadow", "glass", "wave"])
