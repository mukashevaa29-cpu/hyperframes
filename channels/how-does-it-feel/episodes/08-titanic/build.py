"""Episode 08 — How does it feel? When you're on the Titanic as it sinks."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
SEA, SEA_CORE = "#5A78FF", "#E6EEFF"


def stars(seed=1, n=90, ymax=1100):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(380, ymax):.0f}" r="{r.choice([1.5, 2, 2.5])}" fill="#F2EEEA" opacity="{r.uniform(0.3, 0.9):.2f}"/>' for _ in range(n))


def sea(y=1250, gid=""):
    i = f' id="{gid}"' if gid else ""
    return (f'<g{i}><rect x="-200" y="{y}" width="1480" height="1200" fill="#050a1c" opacity="0.94"/>'
            + glow(N(f"M -200 {y} L 1280 {y}", red=SEA, core=SEA_CORE, sw=10, cw=4), f="glowB") + '</g>')


def half(gid, x0, x1, bow=False, stern=False):
    """one half of the hull with its funnels and lit portholes, in ship-local coords (keel y=1100)."""
    hull = f"M {x0} 990 L {x1} 990 L {x1 - (40 if bow else 0)} 1100 L {x0 + (40 if stern else 0)} 1100 Z"
    sup = f"M {max(x0, 200)} 940 L {min(x1, 880)} 940 L {min(x1, 880)} 990 L {max(x0, 200)} 990 Z" if x1 > 200 and x0 < 880 else ""
    funnels = "".join(f'<path d="M {fx} 940 L {fx + 6} 830 L {fx + 56} 830 L {fx + 50} 940 Z" fill="#1a1416" stroke="#E8B040" stroke-width="6"/>' for fx in (330, 450, 570, 690) if x0 <= fx < x1)
    holes = "".join(f'<circle class="{gid}-lt" cx="{x}" cy="1030" r="7" fill="#FFD27A"/>' for x in range(x0 + 30, x1 - 20, 34))
    return f'<g id="{gid}">' + glow(N(hull, fill="#0c0a0c") + (N(sup, fill="#0c0a0c", sw=8, cw=3) if sup else "") + funnels) + holes + '</g>'


def ship(gid):
    return f'<g id="{gid}">' + half(f"{gid}-f", 560, 1040, bow=True) + half(f"{gid}-r", 40, 560, stern=True) + '</g>'


# ---------------------------------------------------------------- S01 cold open: the stern standing up in the night → pull out
s, e = 0.0, cut(12)
svg = stars(1) + f'<g transform="rotate(-62 540 1180)">{ship("t1")}</g>' + sea(1250)
ep.scene("s01", s, e, svg, origin="50% 50%", custom_cam=True, fx=[(s, e, "sparks", dict(cx=540, cy=1240, n=30, r=200, dur=5, color="#E6EEFF", g=0))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:1.6}},{{scale:1.65,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.fromTo("#t1",{{y:0}},{{y:160,duration:{e:.3f},ease:"power1.in"}},0);')
r1 = random.Random(1)
for k in range(int(e / 0.15)):
    ep.js(f'tl.set(".t1-f-lt, .t1-r-lt",{{opacity:{r1.choice([1, 1, 0.3, 0.6])}}},{k * 0.15:.3f});')
ep.floor(0, 0.0, 0.0, 0.01)
ep.cue("roar.mp3", 0, 0.5)
ep.cue("sub.wav", 0, 0.7)

# ---------------------------------------------------------------- S02 April 15th, 1912 — 2:20 in the morning
s, e = cut(12), cut(19)
cx, cy = 540, 1150
ticks = "".join(line(cx + 190 * math.cos(a), cy + 190 * math.sin(a), cx + 215 * math.cos(a), cy + 215 * math.sin(a), CORE, 5) for a in [i * math.pi / 6 for i in range(12)])
clock = glow(f'<circle cx="{cx}" cy="{cy}" r="230" fill="#0C0A0C" stroke="#FB2945" stroke-width="14"/>{ticks}')
hands = (f'<g transform="translate({cx},{cy})"><g id="s02-hh" transform="rotate(0)">' + line(0, 0, 0, -110, CORE, 12) + '</g>'
         f'<g id="s02-mh" transform="rotate(0)">' + line(0, 0, 0, -170, "#FF3B36", 7) + '</g><circle r="14" fill="#F2EEEA"/></g>')
html = '<div class="num" id="s02-d" style="top:600px;font-size:110px;">APRIL 15, 1912</div>'
ep.scene("s02", s, e, clock + hands, html, origin="50% 55%")
ep.pop("#s02-d", s + 0.02, 0.16, 0.8)
ep.js(f'tl.to("#s02-hh",{{attr:{{transform:"rotate(70)"}},duration:{WE(18) - s - 0.2:.3f},ease:"power2.inOut"}},{s + 0.15:.3f});')
ep.js(f'tl.to("#s02-mh",{{attr:{{transform:"rotate(840)"}},duration:{WE(18) - s - 0.2:.3f},ease:"power2.inOut"}},{s + 0.15:.3f});')
ep.cue("tick.wav", W(15), 0.5)
ep.floor(s, 0.4, 0.0)

# ---------------------------------------------------------------- S03 the deck tilts beneath your feet
s, e = cut(19), cut(25)
svg = stars(3) + f'<g transform="translate(540,1100) scale(0.88) translate(-540,-1100)"><g id="s03-tilt">{ship("t3")}</g></g>' + sea(1180)
ep.scene("s03", s, e, svg, origin="50% 55%")
ep.js(f'tl.fromTo("#s03-tilt",{{rotation:0,svgOrigin:"540 1100"}},{{rotation:10,svgOrigin:"540 1100",y:40,duration:{e - s:.3f},ease:"power2.out",immediateRender:false}},{s + 0.05:.3f});')
ep.cue("sfx_collapse.mp3", W(21), 0.3)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S04 lifeboats for barely half — and most are already gone
s, e = cut(25), cut(42)
boats = "".join(f'<g class="s04-b"><g transform="translate({140 + (k % 5) * 180},{760 + (k // 5) * 120})"><path d="M -60 0 L 60 0 L 40 40 L -40 40 Z" fill="#0c0a0c" stroke="#E6EEFF" stroke-width="5"/></g></g>' for k in range(20))
bars = (f'<rect x="140" y="1360" width="800" height="50" fill="#1a1416" stroke="#F2EEEA" stroke-width="3"/>'
        f'<rect id="s04-bar" x="140" y="1360" width="{800 * 1178 / 2224:.0f}" height="50" fill="#5A78FF" filter="url(#glowB)"/>'
        + label(140, 1340, "SEATS: 1,178", 30, "#9FC8FF", "start") + label(940, 1340, "ON BOARD: 2,224", 30, "#F5F5F5", "end"))
ep.scene("s04", s, e, f'<g filter="url(#glowB)">{boats}</g>' + bars, origin="50% 55%")
ep.js(f'tl.fromTo(".s04-b",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.15,stagger:0.05,immediateRender:false}},{s + 0.05:.3f});')
ep.js(f'tl.fromTo("#s04-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.6,ease:"power2.out",immediateRender:false}},{W(29) - 0.1:.3f});')
ep.js(f'tl.to(".s04-b",{{x:"+=1400",opacity:0,duration:0.5,stagger:{{each:0.04,from:"random"}},ease:"power2.in"}},{W(36):.3f});')
ep.js('gsap.set("#s04-bar",{scaleX:0,transformOrigin:"0% 50%"});')
ep.cue("whoosh-cinematic.mp3", W(36), 0.4)
ep.floor(s, 0.35, 0.0)

# ---------------------------------------------------------------- S05 the stern rises, then the ship breaks in two
s, e = cut(42), cut(55)
svg = stars(5) + ship("t5") + sea(1180)
ep.scene("s05", s, e, svg, origin="50% 55%", fx=[(W(52), e, "sparks", dict(cx=560, cy=1040, n=40, r=260, dur=0.8, color="#FFD27A", g=200))])
ep.js(f'tl.to("#t5",{{rotation:-28,svgOrigin:"760 1180",y:80,duration:{W(49) - s:.3f},ease:"power1.out"}},{s:.3f});')
tb = W(52) - 0.05
ep.js(f'tl.to("#t5-r",{{rotation:-30,svgOrigin:"560 1100",y:-40,duration:0.6,ease:"power2.out"}},{tb:.3f});')
ep.js(f'tl.to("#t5-f",{{rotation:18,svgOrigin:"560 1100",y:220,duration:1.0,ease:"power2.in"}},{tb:.3f});')
ep.shake("#s05-shake", tb, 0.6, 14)
ep.cue("sfx_collapse.mp3", tb, 0.9)
ep.cue("sub.wav", tb, 0.9)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S06 you jump
s, e = cut(55), cut(57)
svg = stars(6) + sea(1300) + mascot("m6", 540, 900, 0.7, pose=dict(uarmL=150, farmL=20, uarmR=-150, farmR=-20))
ep.scene("s06", s, e, svg, origin="50% 55%", fx=[(e - 0.25, e, "sparks", dict(cx=540, cy=1300, n=30, r=220, dur=0.5, color="#E6EEFF", g=300))])
ep.js(f'tl.fromTo("#m6",{{y:180}},{{y:640,duration:{e - s:.3f},ease:"power2.in",immediateRender:false}},{s:.3f});')
ep.cue("whoosh-cinematic.mp3", s, 0.6)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S07 the water is minus two degrees Celsius
s, e = cut(57), cut(64)
waves = "".join(f'<path class="s07-w" d="M -300 {900 + k * 160} ' + " ".join(f"Q {-300 + i * 120 + 60} {900 + k * 160 + (-24 if i % 2 == 0 else 24)} {-300 + (i + 1) * 120} {900 + k * 160}" for i in range(16)) + f'" fill="none" stroke="#5A78FF" stroke-width="6" opacity="0.6" filter="url(#glowB)"/>' for k in range(5))
html = '<div class="num" id="s07-n" style="top:560px;font-size:240px;color:#9FC8FF;text-shadow:0 0 20px rgba(90,120,255,.9),0 0 60px rgba(60,90,255,.6);">10°C</div><div class="lbl" style="top:820px;color:#9FC8FF;">WATER TEMPERATURE</div>'
ep.scene("s07", s, e, waves, html, origin="50% 50%")
ep.js(f'(function(){{var o={{v:10}};var el=document.getElementById("s07-n");tl.to(o,{{v:-2,duration:{WE(63) - W(60):.3f},ease:"expo.out",onUpdate:function(){{var n=Math.round(o.v);el.textContent=(n<0?"−":"")+Math.abs(n)+"°C";}}}},{W(60) - 0.05:.3f});}})();')
ep.js(f'tl.fromTo(".s07-w",{{x:0}},{{x:-240,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S08 the cold hits like a thousand knives
s, e = cut(64), cut(71)
r8 = random.Random(8)
knives = ""
for k in range(24):
    a = r8.uniform(0, 2 * math.pi)
    x, y = 540 + 560 * math.cos(a), 1050 + 560 * math.sin(a)
    knives += f'<g class="s08-k" transform="translate({x:.0f},{y:.0f}) rotate({math.degrees(a) + 90:.0f})"><path d="M 0 -50 L 12 30 L 0 50 L -12 30 Z" fill="#E6EEFF" stroke="#9FC8FF" stroke-width="3"/></g>'
svg = sea(1150) + mascot("m8", 540, 1420, 0.7, mouth_open=True, pose=dict(uarmL=120, farmL=40, uarmR=-120, farmR=-40)) + f'<g id="s08-ks" filter="url(#glowB)">{knives}</g>'
ep.scene("s08", s, e, svg, origin="50% 55%")
ep.js(f'tl.fromTo("#s08-ks",{{scale:1.6,svgOrigin:"540 1050",opacity:0}},{{scale:0.55,opacity:1,duration:{W(70) - W(66) + 0.1:.3f},ease:"power3.in",immediateRender:false}},{W(66) - 0.1:.3f});')
ep.js('gsap.set("#s08-ks",{opacity:0});')
ep.shake("#s08-shake", W(70), 0.45, 12)
ep.cue("impact-bass-1.mp3", W(70), 0.7)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S09 you gasp, swallow seawater, can't control your breathing
s, e = cut(71), cut(81)
ep.lungs("s09", s, e, t_flood=W(74) - 0.1, t_burn=W(74), t_burn_end=W(80), flood_color="#5A78FF", burn_color="#14204a", label_txt="GASP REFLEX")
for k in range(int((e - W(76)) / 0.3)):
    ep.js(f'tl.to("#s09-lungs",{{scale:{1.1 if k % 2 == 0 else 0.95},transformOrigin:"50% 40%",duration:0.3,ease:"sine.inOut"}},{W(76) + k * 0.3:.3f});')
ep.cue("whoosh-short.mp3", W(72), 0.5)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S10 your life jacket keeps you afloat, but not warm
s, e = cut(81), cut(93)
vest = '<path d="M 488 1222 L 592 1222 L 604 1352 L 476 1352 Z" fill="#ECE6E5" stroke="#F2EEEA" stroke-width="5" opacity="0.85"/><path d="M 540 1222 L 540 1352" stroke="#9a928c" stroke-width="4"/>'
svg = sea(1250) + f'<g id="s10-f">{mascot("m10", 540, 1520, 0.62, pose=dict(uarmL=60, farmL=-30, uarmR=-60, farmR=30))}{vest}</g>'
html = '<div class="num" id="s10-n" style="top:560px;font-size:180px;">37°</div><div class="lbl" style="top:760px;">BODY TEMPERATURE</div>'
ep.scene("s10", s, e, svg, html, origin="50% 55%")
ep.js(f'tl.fromTo("#s10-f",{{y:-10}},{{y:12,duration:0.9,repeat:{int((e - s) / 0.9)},yoyo:true,ease:"sine.inOut",immediateRender:false}},{s:.3f});')
ep.counter("#s10-n", W(88), e - W(88), 37, 31, "deg", "power1.out")
ep.js(f'tl.to("#s10-n",{{color:"#9FC8FF",duration:1.0}},{W(88):.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S11 your arms stop working, then your legs
s, e = cut(93), cut(100)
svg = sea(1250) + mascot("m11", 540, 1520, 0.62, pose=dict(uarmL=60, farmL=-30, uarmR=-60, farmR=30, thighL=20, thighR=-20)) + vest
ep.scene("s11", s, e, svg, origin="50% 55%")
ep.rot("#m11-uarmL", W(95) - 0.1, 0.6, 5)
ep.rot("#m11-uarmR", W(95) - 0.1, 0.6, -5)
ep.rot("#m11-farmL", W(95) - 0.1, 0.6, 0)
ep.rot("#m11-farmR", W(95) - 0.1, 0.6, 0)
ep.rot("#m11-thighL", W(98), 0.6, 0)
ep.rot("#m11-thighR", W(98), 0.6, 0)
ep.js(f'tl.to("#m11 line, #m11 path, #m11 ellipse, #m11 circle",{{attr:{{stroke:"#7a8aa8"}},duration:1.0}},{W(98):.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S12 fifteen hundred people screaming in the dark
s, e = cut(100), cut(110)
r12 = random.Random(12)
people = "".join(f'<circle class="s12-p" cx="{r12.uniform(40, 1040):.0f}" cy="{r12.uniform(1280, 1800):.0f}" r="{r12.uniform(4, 9):.1f}" fill="#ECE6E5" opacity="0.9"/>' for _ in range(220))
html = '<div class="num" id="s12-n" style="top:600px;font-size:200px;">0</div><div class="lbl" style="top:820px;">PEOPLE IN THE WATER</div>'
ep.scene("s12", s, e, stars(12) + sea(1250) + people, html, origin="50% 60%")
ep.counter("#s12-n", W(102) - 0.1, WE(104) - W(102) + 0.3, 0, 1500, "c")
ep.js(f'tl.fromTo(".s12-p",{{opacity:0}},{{opacity:0.9,duration:0.05,stagger:{{each:{(WE(104) - W(102) + 0.3) / 220:.4f},from:"random"}},immediateRender:false}},{W(102) - 0.1:.3f});')
ep.js('gsap.set(".s12-p",{opacity:0});')
for k in range(int((e - WE(104) - 0.3) / 0.12)):
    ep.js(f'tl.set(".s12-p",{{opacity:{r12.choice([0.9, 0.6, 1.0])}}},{WE(104) + 0.3 + k * 0.12:.3f});')
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- S13 within twenty minutes, it goes quiet
s, e = cut(110), cut(116)
ep.timer("s13", s, e, W(111) - 0.1, WE(112), 0, 1200, "ms", "MINUTES", 1.0, ring_color=SEA)
ep.floor(s, 0.0, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(116), 119)
ep.write(red=["titanic", "lifeboats", "jump", "cold", "knives", "breathing", "warm", "screaming", "quiet"])
