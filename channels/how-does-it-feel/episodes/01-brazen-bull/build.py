"""Episode 01 — How does it feel? When they lock you inside a bronze bull."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
BRONZE = "#C9884A"


# ---------------------------------------------------------------- the bull (local coords: body 0..900 x, -40..560 y)
def bull(gid, x=100, y=760, s=1.0, cutaway=False, door=True, mascot_inside=None, pipe=False, arcs=False, heat_fill=DARK):
    body = "M 40 150 C 30 80 110 40 220 46 C 340 52 470 30 600 26 C 690 22 740 50 760 110 C 780 180 760 260 700 290 C 640 320 520 330 400 326 C 280 330 150 322 100 280 C 60 250 46 200 40 150 Z"
    head = "M 700 40 C 760 20 830 40 860 90 C 885 130 890 180 884 214 C 878 246 852 258 826 250 C 800 242 790 236 770 250 C 740 230 715 160 700 40 Z"
    legs = ""
    for lx in (120, 230, 560, 650):
        legs += N(f"M {lx} 270 L {lx} 492 Q {lx} 502 {lx + 10} 502 L {lx + 50} 502 Q {lx + 60} 502 {lx + 60} 492 L {lx + 60} 270 Z", fill=heat_fill, cls=f"{gid}-bf")
    tail = '<path d="M 45 140 C 0 170 -10 260 10 330" fill="none" stroke="#FB2945" stroke-width="14" stroke-linecap="round"/><path d="M 45 140 C 0 170 -10 260 10 330" fill="none" stroke="#F2EEEA" stroke-width="4"/>'
    horns = ('<path d="M 760 46 C 760 0 720 -34 686 -32" fill="none" stroke="#F2EEEA" stroke-width="14" stroke-linecap="round"/>'
             '<path d="M 790 52 C 800 0 850 -32 904 -22" fill="none" stroke="#F2EEEA" stroke-width="16" stroke-linecap="round"/>')
    inner = glow(legs + tail + N(body, fill=heat_fill, cls=f"{gid}-bf") + horns + N(head, fill=heat_fill, cls=f"{gid}-bf")
                 + '<path d="M 770 70 L 728 58 L 752 96 Z" fill="#0C0A0C" stroke="#F2EEEA" stroke-width="4"/>'
                 + '<circle cx="806" cy="112" r="11" fill="#FF3B36"/><circle cx="872" cy="226" r="7" fill="#0a0505"/>'
                 + "".join(f'<circle cx="{px}" cy="{py}" r="4" fill="#F2EEEA" opacity="0.5"/>' for px, py in [(160, 110), (300, 90), (480, 80), (620, 70), (200, 280), (560, 290)]))
    door_svg = ""
    if door and not cutaway:
        door_svg = (f'<g id="{gid}-doorW"><g transform="translate(330,120)"><g id="{gid}-door">'
                    + N("M 0 0 L 120 0 L 120 130 L 0 130 Z", fill=heat_fill, sw=10, cw=4)
                    + '<circle cx="104" cy="66" r="8" fill="#F2EEEA"/></g></g></g>'
                    + f'<rect id="{gid}-hole" x="330" y="120" width="120" height="130" fill="#000" opacity="0"/>')
    cav = ""
    if cutaway:
        cav = (f'<ellipse cx="400" cy="175" rx="250" ry="105" fill="#140405" stroke="#FFB3B0" stroke-width="4" stroke-dasharray="14 10" id="{gid}-cav"/>')
    inside = mascot_inside or ""
    pipe_svg = ""
    if pipe:
        pipe_svg = (f'<path id="{gid}-pipe" d="M 560 120 C 640 70 730 90 800 140 C 840 170 860 200 878 222" fill="none" stroke="#F2EEEA" stroke-width="12" '
                    f'stroke-dasharray="420" stroke-dashoffset="420" stroke-linecap="round" filter="url(#glowS)"/>')
    arcs_svg = ""
    if arcs:
        arcs_svg = f'<g id="{gid}-arcs" filter="url(#glow)">' + "".join(
            f'<path class="{gid}-arc" d="M {900 + k * 46} {170 - k * 34} Q {930 + k * 60} 226 {900 + k * 46} {282 + k * 34}" fill="none" stroke="#FF3B36" stroke-width="{12 - k * 2}" stroke-linecap="round"/>'
            for k in range(3)) + '</g>'
    return f'<g id="{gid}"><g transform="translate({x},{y}) scale({s})">{inner}{cav}{inside}{door_svg}{pipe_svg}{arcs_svg}</g></g>'


def plinth(y=1310):
    return glow(N(f"M 40 {y} L 1040 {y} L 1040 {y + 40} L 40 {y + 40} Z", fill="#0a0808", sw=10, cw=3), f="glowS")


def arcs_pulse(gid, t0, t1, period=0.18):
    n = int((t1 - t0) / period)
    for k in range(n):
        ep.js(f'tl.set(".{gid}-arc",{{opacity:{0.45 if k % 2 else 1}}},{t0 + k * period:.3f});')


FIRE = lambda grow=0.0, amp=1.0, cx=540, base=1262, w=380, h=190: dict(cx=cx, base=base, w=w, h=h, n=10, grow=grow, amp=amp, sp=6)

# ---------------------------------------------------------------- S01 cold open: screaming bull → reveal
s, e = 0.0, cut(12)
inside = mascot("m1", 400, 270, 0.28, style="xray", pose=dict(thighL=60, shinL=-90, thighR=-20, shinR=60, uarmL=150, farmL=20, uarmR=-150, farmR=-20, head=10), mouth_open=True)
svg = bull("b1", cutaway=True, mascot_inside=inside, arcs=True, heat_fill="#5a0d0a") + plinth()
ep.scene("s01", s, e, svg, origin="84% 47%", custom_cam=True,
         fx=[(s, e, "fire", FIRE()), (s, e, "embers", dict(n=40, x0=250, x1=850, y0=500, y1=1300, sp=150)),
             (s, e, "smoke", dict(n=10, cx=980, base=900, w=60, h=500, r0=30, r1=110, sp=1, life=2.2, alpha=0.3))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.4}},{{scale:2.5,duration:{W(4) - 0.2:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.9,ease:"power2.inOut"}},{W(4) - 0.2:.3f});')
ep.js(f'tl.to("#s01-cam",{{scale:1.05,duration:{e - W(4) - 0.7:.3f},ease:"none"}},{W(4) + 0.7:.3f});')
arcs_pulse("b1", 0, e)
ep.shake("#s01-shake", 0.0, W(4), 6)
ep.floor(0, 0.3, 1.0, 0.01)
ep.cue("sfx_open_roar.mp3", 0, 0.8)
ep.cue("sub.wav", 0, 0.9)
ep.cue("roar.mp3", 0.5, 0.5)

# ---------------------------------------------------------------- S02 Sicily
s, e = cut(12), cut(17)
SIC = "M 230 960 L 300 905 L 420 900 L 540 885 L 660 872 L 780 848 L 870 828 L 850 880 L 806 960 L 784 1040 L 796 1110 L 770 1176 L 700 1150 L 616 1110 L 516 1082 L 416 1042 L 316 1004 Z"
svg = (glow(N(SIC, fill="#0e0909"), gid="s02-isle")
       + f'<g id="s02-dot"><circle cx="470" cy="1040" r="16" fill="#FF3B36" filter="url(#glow)"/><circle id="s02-ring" cx="470" cy="1040" r="16" fill="none" stroke="#FF3B36" stroke-width="5"/></g>'
       + label(470, 1100, "AKRAGAS", 30, GREY, extra='id="s02-akr"'))
html = ('<div class="num" id="s02-t1" style="top:560px;font-size:170px;">SICILY</div>'
        '<div class="lbl" id="s02-t2" style="top:1250px;font-size:44px;color:#F5F5F5;letter-spacing:8px;">6TH CENTURY BC</div>')
ep.scene("s02", s, e, svg, html, origin="50% 55%")
ep.pop("#s02-t1", s, 0.16, 0.85)
ep.pop("#s02-isle", s + 0.05, 0.25, 0.7)
ep.pop("#s02-dot", s + 0.35, 0.2, 0.0)
ep.pop("#s02-akr", s + 0.45, 0.2, 0.5)
ep.js(f'tl.fromTo("#s02-ring",{{attr:{{r:16}},opacity:1}},{{attr:{{r:70}},opacity:0,duration:0.8,ease:"power2.out",repeat:2,immediateRender:false}},{s + 0.4:.3f});')
ep.pop("#s02-t2", W(14), 0.2, 0.6)
ep.floor(s, 0.8, 0.0)

# ---------------------------------------------------------------- S03 the bull, hollow, bronze
s, e = cut(17), cut(29)
svg = (bull("b3", cutaway=False) + plinth()
       + f'<g id="s03-cavW" opacity="0"><ellipse cx="500" cy="935" rx="250" ry="105" fill="none" stroke="#FFB3B0" stroke-width="5" stroke-dasharray="16 12"/></g>'
       + f'<g id="s03-shineW" opacity="0"><defs><clipPath id="s03-clip"><path transform="translate(100,760)" d="M 40 150 C 30 80 110 40 220 46 C 340 52 470 30 600 26 C 690 22 740 50 760 110 C 780 180 760 260 700 290 C 640 320 520 330 400 326 C 280 330 150 322 100 280 C 60 250 46 200 40 150 Z"/></clipPath></defs>'
       + f'<g clip-path="url(#s03-clip)"><rect id="s03-shine" x="-200" y="600" width="70" height="900" fill="#FFD6A8" opacity="0.55" transform="rotate(14 0 1000)" filter="url(#soft2)"/></g></g>'
       + mascot("m3", 120, 1310, 0.42, pose=dict(head=-8)))
html = ('<div class="lbl" id="s03-l1" style="top:640px;font-size:40px;color:#FFB3B0;">HOLLOW</div>'
        '<div class="lbl" id="s03-l2" style="top:640px;font-size:40px;color:#E0A060;">BRONZE</div>')
ep.scene("s03", s, e, svg, html, origin="50% 55%", drift=0.02)
ep.show("#s03-cavW", W(25) - 0.05, 0.2)
ep.pop("#s03-l1", W(25) - 0.05, 0.2, 0.5)
ep.js(f'tl.to("#s03-l1",{{opacity:0,duration:0.15}},{W(28) - 0.15:.3f});')
ep.pop("#s03-l2", W(28) - 0.05, 0.2, 0.5)
ep.show("#s03-shineW", W(27))
ep.js(f'tl.fromTo("#s03-shine",{{x:0}},{{x:1300,duration:1.0,ease:"power1.inOut",immediateRender:false}},{W(27):.3f});')
ep.js(f'tl.to(".b3-bf",{{fill:"#2a1608",duration:0.8}},{W(28):.3f});')
ep.cue("riser.mp3", W(27) - 0.2, 0.25)
ep.floor(s, 0.8, 0.0)

# ---------------------------------------------------------------- S04 door opens, shoved inside (punch on the flank)
s, e = cut(29), cut(40)
svg = bull("b4", heat_fill="#2a1608") + plinth() + mascot("m4", -150, 1310, 0.42, pose=dict(uarmL=-30, uarmR=30, head=6))
ep.scene("s04", s, e, svg, origin="45% 47%", custom_cam=True)
ep.js(f'tl.fromTo("#s04-cam",{{scale:1.45}},{{scale:1.6,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
td = W(34) - 0.05
ep.js(f'tl.to("#b4-door",{{scaleX:0.12,svgOrigin:"0 0",duration:0.35,ease:"power2.out"}},{td:.3f});')
ep.show("#b4-hole", td, 0.2)
ep.cue("sfx_collapse.mp3", td, 0.25)
ts = W(37) - 0.1
ep.js(f'tl.fromTo("#m4",{{x:0,y:0,scale:1}},{{x:520,y:-250,scale:0.6,duration:0.45,ease:"power3.in",immediateRender:false}},{ts:.3f});')
ep.js(f'tl.to("#m4",{{opacity:0,duration:0.12}},{ts + 0.38:.3f});')
ep.cue("whoosh-cinematic.mp3", ts, 0.4)
ep.floor(s, 0.75, 0.0)

# ---------------------------------------------------------------- S05 door slams
s, e = cut(40), cut(44)
svg = bull("b5", heat_fill="#2a1608") + plinth()
ep.scene("s05", s, e, svg, origin="45% 47%", custom_cam=True)
ep.js(f'tl.fromTo("#s05-cam",{{scale:1.9}},{{scale:2.0,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'gsap.set("#b5-door",{{scaleX:0.12,svgOrigin:"0 0"}});')
ep.show("#b5-hole", s)
tsl = W(42) - 0.04
ep.js(f'tl.to("#b5-door",{{scaleX:1,svgOrigin:"0 0",duration:0.12,ease:"power3.in"}},{tsl:.3f});')
ep.js(f'tl.set("#b5-hole",{{opacity:0}},{tsl + 0.1:.3f});')
ep.flash(tsl + 0.12, 0.35, 0.3)
ep.shake("#s05-shake", tsl + 0.12, 0.4, 16)
ep.cue("impact-bass-2.mp3", tsl + 0.1, 0.9)
ep.cue("sub.wav", tsl + 0.1, 0.8)
ep.floor(s, 0.6, 0.0)


# ---------------------------------------------------------------- interior helper
def interior(gid, fill="#0c0606", rim=RED, inner_rings=False):
    rivets = "".join(f'<circle cx="{540 + 450 * math.cos(a):.0f}" cy="{1060 + 290 * math.sin(a):.0f}" r="6" fill="#F2EEEA" opacity="0.6"/>' for a in [i * math.pi / 9 for i in range(18)])
    rings = ""
    if inner_rings:
        rings = f'<ellipse id="{gid}-ring2" cx="540" cy="1060" rx="400" ry="250" fill="none" stroke="#FFB3B0" stroke-width="4" stroke-dasharray="14 10" opacity="0"/>'
    return glow(f'<ellipse class="{gid}-wall" cx="540" cy="1060" rx="480" ry="320" fill="{fill}" stroke="{rim}" stroke-width="18"/>'
                f'<ellipse cx="540" cy="1060" rx="480" ry="320" fill="none" stroke="#F2EEEA" stroke-width="5"/>' + rivets, gid=f"{gid}-shell") + rings


# ---------------------------------------------------------------- S06 dark, cramped, smells of metal
s, e = cut(44), cut(50)
smell = "".join(f'<path class="s06-smell" d="M {380 + k * 110} 900 q 20 -20 40 0 t 40 0 t 40 0" fill="none" stroke="#9a928c" stroke-width="6" stroke-linecap="round" opacity="0"/>' for k in range(3))
svg = interior("s06", inner_rings=True) + mascot("m6", 560, 1330, 0.55, pose=dict(thighL=50, shinL=-100, thighR=-50, shinR=100, uarmL=-45, farmL=-80, uarmR=45, farmR=80, head=14)) + smell
ep.scene("s06", s, e, svg, origin="50% 55%", drift=0.025)
ep.js(f'gsap.set("#m6",{{y:40}});')
ep.floor(s, 0.12, 0.0, 0.1)
ep.js(f'tl.fromTo("#s06-ring2",{{opacity:0,scale:1.15,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.4,ease:"power2.out",immediateRender:false}},{W(45) - 0.05:.3f});')
ep.js(f'tl.to("#s06-shell",{{scale:0.92,transformOrigin:"50% 50%",duration:0.5,ease:"power2.inOut"}},{W(45) - 0.05:.3f});')
ep.js(f'tl.fromTo(".s06-smell",{{opacity:0,y:0}},{{opacity:0.9,y:-60,duration:1.0,stagger:0.15,ease:"sine.out",immediateRender:false}},{W(47) - 0.05:.3f});')
ep.rot("#m6-head", W(47), 0.4, -6, about="0,-492")

# ---------------------------------------------------------------- S07 they light the fire (wide, cutaway)
s, e = cut(50), cut(58)
inside = mascot("m7", 400, 270, 0.28, style="xray", pose=dict(thighL=70, shinL=-110, thighR=-70, shinR=110, uarmL=-40, farmL=-70, uarmR=40, farmR=70))
svg = bull("b7", cutaway=True, mascot_inside=inside, heat_fill="#2a1608") + plinth() + glow(N("M 330 1262 L 750 1262", sw=8, cw=3), f="glowS")
tf = W(52)
ep.scene("s07", s, e, svg, origin="50% 60%", fx=[(tf, e + 0.1, "fire", FIRE(grow=1.6)), (tf + 0.8, e, "embers", dict(n=30, x0=330, x1=750, y0=900, y1=1270, sp=120))])
ep.floor(s, 0.6, 0.0)
ep.floor(tf, 0.4, 0.8, 1.6)
ep.cue("sfx_whoosh.mp3", tf - 0.1, 0.5)
ep.cue("roar.mp3", tf, 0.6)

# ---------------------------------------------------------------- S08 first minutes are just warm (timer)
s, e = cut(58), cut(64)
ep.timer("s08", s, e, W(59), WE(63) + 0.2, 0, 120, "ms", "MINUTES", 0.5)
ep.floor(s, 0.55, 0.2)

# ---------------------------------------------------------------- S09 you don't understand yet (inside, looking around)
s, e = cut(64), cut(70)
svg = interior("s09", fill="#1a0707") + mascot("m9", 540, 1330, 0.55, pose=dict(thighL=50, shinL=-100, thighR=-50, shinR=100, uarmL=-20, farmL=-30, uarmR=20, farmR=30))
ep.scene("s09", s, e, svg, origin="50% 55%", drift=0.02, fx=[(s, e, "embers", dict(n=18, x0=200, x1=880, y0=900, y1=1360, sp=80))])
ep.js(f'gsap.set("#m9",{{y:40}});')
ep.rot("#m9-head", W(65), 0.35, -16, about="0,-492")
ep.rot("#m9-head", W(67), 0.35, 16, about="0,-492")
ep.rot("#m9-head", W(69) - 0.1, 0.3, 0, about="0,-492")
ep.floor(s, 0.3, 0.3)

# ---------------------------------------------------------------- S10 bronze heats fast
s, e = cut(70), cut(74)
inside = mascot("m10", 400, 270, 0.28, style="xray", pose=dict(thighL=70, shinL=-110, thighR=-70, shinR=110, uarmL=-40, farmL=-70, uarmR=40, farmR=70))
svg = bull("b10", cutaway=True, mascot_inside=inside, heat_fill="#2a1608") + plinth()
ep.scene("s10", s, e, svg, origin="50% 60%", fx=[(s, e + 0.1, "fire", FIRE(amp=1.15)), (s, e, "embers", dict(n=40, x0=250, x1=850, y0=700, y1=1270, sp=160))])
th = W(72) - 0.05
ep.js(f'tl.to(".b10-bf",{{keyframes:[{{fill:"#450B09",duration:0.6}},{{fill:"#871712",duration:{max(0.3, e - th - 0.6):.3f}}}],ease:"power1.in"}},{th:.3f});')
ep.cue("sizzle.wav", th, 0.3)
ep.floor(s, 0.3, 1.0)

# ---------------------------------------------------------------- S11 walls scorching (thermometer)
s, e = cut(74), cut(80)
ep.thermometer("s11", s, e, W(76) - 0.1, WE(79) + 0.2, 30, 400, 400, "WALLS · CELSIUS")

# ---------------------------------------------------------------- S12 can't touch them
s, e = cut(80), cut(84)
svg = interior("s12", fill="#871712", rim="#FF6A5A") + mascot("m12", 420, 1360, 0.6, pose=dict(uarmL=-20, uarmR=-100, farmR=-20, head=-10))
ep.scene("s12", s, e, svg, origin="50% 55%", fx=[(W(82) + 0.05, e, "sparks", dict(cx=900, cy=950, n=30, r=160, dur=0.45, color="#FFF1DC"))])
tt = W(82)
ep.rot("#m12-uarmR", s + 0.1, tt - s - 0.1, -112, "power1.inOut")
ep.rot("#m12-uarmR", tt + 0.08, 0.16, -10, "power3.out")
ep.rot("#m12-farmR", tt + 0.08, 0.16, -120, "power3.out")
ep.flash(tt + 0.05, 0.3, 0.25)
ep.shake("#s12-shake", tt + 0.05, 0.25, 8)
ep.cue("sizzle.wav", tt, 0.6)
ep.cue("impact-bass-1.mp3", tt + 0.05, 0.5)
ep.floor(s, 0.3, 1.0)

# ---------------------------------------------------------------- S13 nowhere left to stand
s, e = cut(84), cut(90)
svg = interior("s13", fill="#871712", rim="#FF6A5A") + mascot("m13", 540, 1360, 0.6, pose=dict(uarmL=20, uarmR=-20))
ep.scene("s13", s, e, svg, origin="50% 60%", fx=[(s, e, "embers", dict(n=25, x0=150, x1=930, y0=850, y1=1370, sp=110))])
tfall = W(86) - 0.1
ep.js(f'tl.to("#m13",{{rotation:-84,svgOrigin:"540 1360",y:-10,duration:0.4,ease:"power2.in"}},{tfall:.3f});')
ep.cue("impact-bass-2.mp3", tfall + 0.4, 0.5)
r13 = random.Random(13)
for k in range(int((e - tfall - 0.5) / 0.14)):
    t = tfall + 0.5 + k * 0.14
    ep.rot("#m13-thighL", t, 0.12, r13.uniform(-30, 40))
    ep.rot("#m13-thighR", t, 0.12, r13.uniform(-40, 30))
    ep.rot("#m13-uarmR", t, 0.12, r13.uniform(-160, -60))
ep.floor(s, 0.3, 1.0)

# ---------------------------------------------------------------- S14 air hot like an oven
s, e = cut(90), cut(97)
waves = "".join(f'<path class="s14-w" d="M -300 {820 + k * 90} ' + " ".join(f"Q {-300 + i * 100 + 50} {820 + k * 90 + (-22 if i % 2 == 0 else 22)} {-300 + (i + 1) * 100} {820 + k * 90}" for i in range(18))
                + f'" fill="none" stroke="#FFB070" stroke-width="5" opacity="{0.35 + 0.1 * (k % 3):.2f}" filter="url(#glowO)"/>' for k in range(6))
svg = (interior("s14", fill="#5a0d0a", rim="#FF6A5A") + f'<defs><clipPath id="s14-c"><ellipse cx="540" cy="1060" rx="470" ry="310"/></clipPath></defs>'
       + f'<g clip-path="url(#s14-c)">{waves}</g>'
       + mascot("m14", 540, 1340, 0.55, pose=dict(thighL=80, shinL=-120, thighR=-80, shinR=120, uarmL=-150, farmL=-30, uarmR=150, farmR=30, head=20)))
ep.scene("s14", s, e, svg, origin="50% 55%", drift=0.02)
ep.js(f'gsap.set("#m14",{{y:40}});')
ep.js(f'tl.fromTo(".s14-w",{{x:0}},{{x:-200,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to(".s14-wall",{{fill:"#871712",duration:{e - s:.3f}}},{s:.3f});')
ep.cue("roar.mp3", s, 0.4)
ep.floor(s, 0.2, 1.0)

# ---------------------------------------------------------------- S15 every breath burns your lungs
s, e = cut(97), cut(102)
ep.lungs("s15", s, e, t_breath=W(98) - 0.1, t_flood=W(99) - 0.15, t_burn=W(99), t_burn_end=WE(101) + 0.2)
ep.cue("whoosh-short.mp3", W(98) - 0.1, 0.3)
ep.floor(s, 0.4, 0.6)

# ---------------------------------------------------------------- S16 the pipe into the head
s, e = cut(102), cut(118)
inside = mascot("m16", 360, 270, 0.28, style="xray", pose=dict(uarmL=-90, farmL=-10, uarmR=-80, farmR=-10), mouth_open=True)
svg = bull("b16", cutaway=True, mascot_inside=inside, pipe=True, heat_fill="#871712") + plinth()
ep.scene("s16", s, e, svg, origin="80% 47%", custom_cam=True, fx=[(s, e + 0.1, "fire", FIRE(amp=1.3)), (s, e, "embers", dict(n=40, x0=250, x1=850, y0=600, y1=1270, sp=180))])
ep.js(f'tl.fromTo("#s16-cam",{{scale:0.9}},{{scale:1,duration:{5 * F:.3f},ease:"power2.out",immediateRender:false}},{s:.3f});')
ep.js(f'tl.to("#s16-cam",{{scale:1.04,duration:{W(112) - s:.3f},ease:"none"}},{s + 5 * F:.3f});')
ep.js(f'gsap.set("#m16",{{rotation:-80,svgOrigin:"460 1030"}});')
tp = W(112) - 0.1
ep.js(f'tl.to("#b16-pipe",{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut"}},{tp:.3f});')
ep.js(f'tl.to("#m16",{{x:120,y:-30,duration:{e - W(113):.3f},ease:"power1.inOut"}},{W(113):.3f});')
ep.js(f'tl.to("#s16-cam",{{scale:1.9,duration:{e - W(114):.3f},ease:"power2.inOut"}},{W(114):.3f});')
ep.cue("riser.mp3", tp, 0.3)
ep.floor(s, 0.3, 1.0)

# ---------------------------------------------------------------- S17 press your face against it... and scream
s, e = cut(118), cut(126)
pipe = glow(N("M 1120 720 L 760 720 Q 700 720 700 780 L 700 820 Q 700 860 660 860 L 600 860", fill="none", sw=40, cw=8), gid="s17-pipe")
mouthpiece = glow(N("M 600 820 L 560 800 L 560 920 L 600 900 Z", fill="#2a1608", sw=10, cw=4))
face = mascot("m17", 380, 1500, 1.3, style="xray", pose=dict(head=-8, uarmR=-120, farmR=-40))
arcs = "".join(f'<path class="s17-arc" d="M {620 + k * 70} {780 - k * 30} Q {660 + k * 80} 860 {620 + k * 70} {940 + k * 30}" fill="none" stroke="#FF3B36" stroke-width="{14 - k * 3}" opacity="0"/>' for k in range(3))
svg = (f'<rect x="0" y="0" width="1080" height="1920" fill="#2a0606"/>' + pipe + mouthpiece + face + f'<g filter="url(#glow)">{arcs}</g>')
ep.scene("s17", s, e, svg, origin="50% 45%", drift=0.03)
tsc = W(125) - 0.05
ep.js(f'tl.to("#m17-mouth",{{attr:{{ry:30,rx:22}},duration:0.12,ease:"power2.out"}},{tsc:.3f});')
ep.js(f'tl.fromTo(".s17-arc",{{opacity:0,x:0}},{{opacity:1,x:120,duration:0.35,stagger:0.08,repeat:2,ease:"power1.out",immediateRender:false}},{tsc + 0.05:.3f});')
ep.shake("#s17-shake", tsc, 0.6, 14)
ep.flash(tsc, 0.25, 0.3)
ep.cue("sfx_open_roar.mp3", tsc, 0.7)
ep.cue("impact-bass-1.mp3", tsc, 0.7)
ep.floor(s, 0.2, 1.0)

# ---------------------------------------------------------------- S18 outside no one hears a scream (head close-up)
s, e = cut(126), cut(133)
svg = bull("b18", arcs=True, heat_fill="#871712", door=False) + plinth()
ep.scene("s18", s, e, svg, origin="84% 47%", custom_cam=True, fx=[(s, e, "smoke", dict(n=8, cx=1000, base=940, w=60, h=400, r0=30, r1=100, life=2.4, alpha=0.25))])
ep.js(f'tl.fromTo("#s18-cam",{{scale:2.1}},{{scale:2.25,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
arcs_pulse("b18", s, e, 0.16)
ep.cue("sfx_open_roar.mp3", s + 0.2, 0.45)
ep.floor(s, 0.3, 0.9)

# ---------------------------------------------------------------- S19 converter: scream → bellow
s, e = cut(133), cut(147)
jag_r = random.Random(4)
jag = "M 60 960 " + " ".join(f"L {60 + i * 12} {960 + jag_r.uniform(-90, 90):.0f}" for i in range(1, 22))
coil = "M 320 960 " + " ".join(f"C {320 + i * 70 + 20} 860 {320 + i * 70 + 50} 1060 {320 + (i + 1) * 70} 960" for i in range(6))
sine = "M 760 960 " + " ".join(f"Q {760 + i * 40 + 20} {960 + (-60 if i % 2 == 0 else 60)} {760 + (i + 1) * 40} 960" for i in range(7))
svg = (f'<g id="s19-jag" filter="url(#glow)"><path d="{jag}" fill="none" stroke="#FF3B36" stroke-width="7" stroke-linejoin="round"/></g>'
       + glow(N(coil, fill="none", sw=26, cw=6))
       + f'<path id="s19-pulse" d="{coil}" fill="none" stroke="#FFF1DC" stroke-width="10" stroke-dasharray="20 120" stroke-dashoffset="0" filter="url(#glowO)"/>'
       + f'<g id="s19-sineW"><g id="s19-sine" filter="url(#glow)"><path d="{sine}" fill="none" stroke="#FF3B36" stroke-width="9" stroke-linecap="round"/></g></g>'
       + label(170, 1130, "SCREAM", 34, "#F5F5F5") + label(530, 1130, "PIPES", 30, GREY) + label(900, 1130, "BELLOW", 34, "#FF3B36", extra='id="s19-bl"'))
ep.scene("s19", s, e, svg, origin="50% 50%")
ep.js(f'tl.fromTo("#s19-pulse",{{strokeDashoffset:0}},{{strokeDashoffset:-1400,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
r19 = random.Random(19)
for k in range(int((e - s) * 10)):
    ep.js(f'tl.set("#s19-jag",{{scaleY:{r19.uniform(0.6, 1.25):.2f},transformOrigin:"50% 50%"}},{s + k * 0.1:.3f});')
ep.js(f'gsap.set("#s19-sine",{{scaleY:0.3,transformOrigin:"50% 50%"}});')
ep.js(f'tl.to("#s19-sine",{{scaleY:1.6,duration:0.3,ease:"back.out(2)"}},{W(143) - 0.05:.3f});')
ep.js(f'tl.to("#s19-bl",{{attr:{{"font-size":46}},duration:0.2}},{W(143) - 0.05:.3f});')
ep.cue("impact-bass-2.mp3", W(143) - 0.05, 0.6)
ep.floor(s, 0.6, 0.2)

# ---------------------------------------------------------------- S20 the tyrant and his guests laugh
s, e = cut(147), cut(153)
throne = glow(N("M 400 1400 L 400 900 Q 540 820 680 900 L 680 1400 Z", fill="#120c06", red="#E8B040", core="#FFE08A", sw=12, cw=4), f="glowG")
king = mascot("k20", 540, 1400, 0.85, crown=True, mouth_open=True, pose=dict(thighL=-20, shinL=20, thighR=20, shinR=-20, uarmL=40, farmL=-60, uarmR=-40, farmR=60))
g1 = mascot("g20a", 200, 1460, 0.6, mouth_open=True, pose=dict(uarmR=-60, farmR=-60))
g2 = mascot("g20b", 880, 1460, 0.6, mouth_open=True, pose=dict(uarmL=60, farmL=60))
has = "".join(f'<text class="s20-ha" x="{x}" y="{y}" fill="#FF6A5A" font-family="Roboto Condensed" font-weight="900" font-size="{sz}" opacity="0" text-anchor="middle">HA</text>'
              for x, y, sz in [(300, 760, 70), (800, 720, 90), (180, 950, 56), (920, 980, 64), (560, 640, 80), (700, 900, 50)])
svg = throne + king + g1 + g2 + has + glow(N("M 0 1460 L 1080 1460", sw=10, cw=3), f="glowS")
ep.scene("s20", s, e, svg, origin="50% 60%", drift=0.02)
ep.js(f'tl.fromTo(".s20-ha",{{opacity:0,scale:0.4,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.18,stagger:0.16,ease:"back.out(2)",immediateRender:false}},{W(152) - 0.1:.3f});')
for k in range(int((e - s) / 0.18)):
    t = s + k * 0.18
    a = 8 if k % 2 else -4
    for m in ("k20", "g20a", "g20b"):
        ep.rot(f"#{m}-head", t, 0.16, a if m != "g20b" else -a, "sine.inOut", about="0,-492")
ep.floor(s, 0.6, 0.0)

# ---------------------------------------------------------------- S21 to them it's music
s, e = cut(153), cut(157)
svg = bull("b21", heat_fill="#871712", door=False, arcs=True) + plinth()
ep.scene("s21", s, e, svg, origin="60% 50%", fx=[(s, e, "notes", dict(n=9, cx=1000, cy=960, h=600, drift=-260)), (s, e + 0.1, "fire", FIRE(amp=1.2))])
arcs_pulse("b21", s, e, 0.2)
ep.floor(s, 0.35, 0.9)

# ---------------------------------------------------------------- S22 your voice breaks → rasp (scope)
s, e = cut(157), cut(165)
grid = "".join(line(80 + i * 92, 700, 80 + i * 92, 1220, "#3a1416", 2) for i in range(11)) + line(80, 960, 1000, 960, "#3a1416", 2)
wr = random.Random(22)
tall = "M 80 960 " + " ".join(f"L {80 + i * 8} {960 + math.sin(i * 0.5) * 220 * (0.7 + 0.3 * wr.random()):.0f}" for i in range(1, 116))
rasp = "M 80 960 " + " ".join(f"L {80 + i * 8} {960 + wr.uniform(-28, 28):.0f}" for i in range(1, 116))
svg = (grid + f'<g id="s22-tallW"><g id="s22-tall" filter="url(#glow)"><path d="{tall}" fill="none" stroke="#FF3B36" stroke-width="7"/></g></g>'
       + f'<g id="s22-raspW" opacity="0"><g filter="url(#glowS)"><path d="{rasp}" fill="none" stroke="#9a5a5a" stroke-width="5"/></g></g>'
       + label(90, 680, "YOUR VOICE", 30, GREY, "start"))
ep.scene("s22", s, e, svg, origin="50% 50%")
r22 = random.Random(23)
tb = W(159) - 0.05
for k in range(int((tb - s) * 15)):
    ep.js(f'tl.set("#s22-tall",{{scaleY:{r22.uniform(0.85, 1.1):.2f},transformOrigin:"50% 50%"}},{s + k * 2 * F:.3f});')
ep.js(f'tl.to("#s22-tall",{{scaleY:0.25,transformOrigin:"50% 50%",duration:{W(162) - tb:.3f},ease:"power2.in"}},{tb:.3f});')
ep.js(f'tl.to("#s22-tallW",{{opacity:0,duration:0.2}},{W(162):.3f});')
ep.show("#s22-raspW", W(162), 0.2)
for k in range(int((e - W(162)) * 15)):
    ep.js(f'tl.set("#s22-raspW",{{y:{r22.uniform(-4, 4):.1f}}},{W(162) + k * 2 * F:.3f});')
ep.cue("impact-bass-1.mp3", tb, 0.4)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S23 the bull falls silent
s, e = cut(165), cut(169)
svg = bull("b23", heat_fill="#871712", door=False, arcs=True) + plinth()
ep.scene("s23", s, e, svg, origin="60% 50%", drift=0.01, fx=[(W(167), e, "smoke", dict(n=12, cx=990, base=960, w=80, h=600, r0=30, r1=130, life=3, alpha=0.35)),
                                                            (s, e + 0.1, "fire", FIRE(amp=0.7))])
ep.js(f'tl.to(".b23-arc",{{opacity:0,duration:0.8,stagger:0.15}},{W(167) - 0.1:.3f});')
ep.js(f'tl.to(".b23-bf",{{fill:"#3a0a08",duration:{e - s:.3f}}},{s:.3f});')
ep.floor(s, 0.4, 0.4)
ep.floor(W(167), 0.25, 0.0, 1.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(169), 172)
ep.write(red=["bronze", "bull", "hollow", "fire", "scream", "music", "pipe", "tyrant", "lungs"])
