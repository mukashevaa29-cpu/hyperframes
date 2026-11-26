"""Episode 04 — How does it feel? When they burn you alive at the stake."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut


def stake(mid, chained=True, logs=True, screaming=False, pose=None, chains_id=None):
    post = glow(N("M 515 420 L 565 420 L 565 1560 L 515 1560 Z", fill="#1a0f0a", sw=12, cw=4))
    p = dict(uarmL=20, farmL=-10, uarmR=-20, farmR=10, head=0)
    p.update(pose or {})
    man = mascot(mid, 540, 1460, 1.15, pose=p, mouth_open=screaming)
    chains = ""
    if chained:
        cid = chains_id or f"{mid}-ch"
        chains = (f'<g id="{cid}a">' + "".join(f'<ellipse cx="{430 + k * 36}" cy="1010" rx="20" ry="12" fill="none" stroke="#F2EEEA" stroke-width="7" filter="url(#glowS)"/>' for k in range(7)) + '</g>'
                  + f'<g id="{cid}b">' + "".join(f'<ellipse cx="{450 + k * 36}" cy="1240" rx="20" ry="12" fill="none" stroke="#F2EEEA" stroke-width="7" filter="url(#glowS)"/>' for k in range(6)) + '</g>')
    pile = ""
    if logs:
        lr = random.Random(4)
        pile = "".join(f'<g class="{mid}-log" id="{mid}-log{i}">' + glow(N(f"M {cx - 150} {cy - 18} L {cx + 150} {cy - 18} L {cx + 150} {cy + 18} L {cx - 150} {cy + 18} Z", fill="#1a0f0a", sw=10, cw=4,
                                                         extra=f'transform="rotate({ang} {cx} {cy})"'), f="glowS") + '</g>'
                       for i, (cx, cy, ang) in enumerate([(420, 1560, 12), (660, 1560, -12), (540, 1600, 0), (360, 1610, -6), (720, 1610, 6), (540, 1540, 4)]))
    return post + man + chains + pile


def fire(h=420, w=640, amp=1.0, grow=0.0, base=1600):
    return dict(cx=540, base=base, w=w, h=h, n=12, grow=grow, amp=amp, sp=7, nofade=True)


def thrash(mid, t0, t1, seed=1, step=0.1):
    r = random.Random(seed)
    for k in range(int((t1 - t0) / step)):
        t = t0 + k * step
        ep.rot(f"#{mid}-head", t, step, r.uniform(-25, 25), "sine.inOut", about="0,-492")
        ep.rot(f"#{mid}-farmL", t, step, r.uniform(-60, 20), "sine.inOut")
        ep.rot(f"#{mid}-farmR", t, step, r.uniform(-20, 60), "sine.inOut")


# ---------------------------------------------------------------- S01 cold open: burning at the stake → pull out
s, e = 0.0, cut(12)
svg = stake("m1", screaming=True, pose=dict(head=-12))
ep.scene("s01", s, e, svg, origin="50% 45%", custom_cam=True,
         fx=[(s, e, "fire", fire(h=760, w=700)), (s, e, "embers", dict(n=60, x0=150, x1=930, y0=400, y1=1650, sp=200)),
             (s, e, "smoke", dict(n=10, cx=540, base=700, w=300, h=700, r0=60, r1=220, life=3, alpha=0.3))])
ep.js(f'tl.fromTo("#s01-cam",{{scale:1.6}},{{scale:1.65,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.7,ease:"power2.out"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.to("#s01-cam",{{scale:1.04,duration:{e - W(4) - 0.55:.3f},ease:"none"}},{W(4) + 0.55:.3f});')
thrash("m1", 0, e, 1)
ep.floor(0, 0.3, 1.0, 0.01)
ep.cue("sfx_open_roar.mp3", 0, 0.7)
ep.cue("roar.mp3", 0, 0.8)
ep.cue("sub.wav", 0, 0.8)

# ---------------------------------------------------------------- S02 chained to a post
s, e = cut(12), cut(18)
svg = stake("m2", logs=False, pose=dict(head=4))
ep.scene("s02", s, e, svg, origin="50% 50%", drift=0.02)
ep.js(f'tl.fromTo("#m2-cha",{{x:-700}},{{x:0,duration:0.22,ease:"power3.out",immediateRender:false}},{W(13) - 0.05:.3f});')
ep.js(f'gsap.set("#m2-cha",{{x:-700}});gsap.set("#m2-chb",{{x:700}});')
ep.js(f'tl.fromTo("#m2-chb",{{x:700}},{{x:0,duration:0.22,ease:"power3.out",immediateRender:false}},{W(16) - 0.05:.3f});')
ep.cue("impact-bass-2.mp3", W(13) + 0.15, 0.5)
ep.cue("impact-bass-2.mp3", W(16) + 0.15, 0.5)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S03 brushwood at your feet (logs fly in)
s, e = cut(18), cut(22)
svg = stake("m3", pose=dict(head=10))
ep.scene("s03", s, e, svg, origin="50% 70%", drift=0.02)
lr = random.Random(3)
for k in range(6):
    side = -1 if k % 2 == 0 else 1
    ep.js(f'tl.fromTo("#m3-log{k}",{{x:{side * 800},rotation:{side * 40}}},{{x:0,rotation:0,duration:0.22,ease:"power3.out",immediateRender:false}},{W(18) - 0.05 + k * 0.08:.3f});')
ep.js('gsap.set("#s03 .m3-log",{x:900});')
for k in range(6):
    ep.cue("impact-bass-1.mp3", W(18) + 0.15 + k * 0.08, 0.15)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S04 the executioner brings the torch
s, e = cut(22), cut(27)
torch = ('<g id="s04-torch"><g transform="translate(860,1300) rotate(-35)">' + glow(N("M -14 0 L 14 0 L 10 260 L -10 260 Z", fill="#3a2010", sw=8, cw=3), f="glowS")
         + '<path d="M -24 0 Q -30 -60 0 -110 Q 30 -60 24 0 Z" fill="#FFE2B8" stroke="#FF8A3A" stroke-width="6" filter="url(#glowO)"/></g></g>')
svg = stake("m4", pose=dict(head=16)) + torch
ti = W(26)
ep.scene("s04", s, e, svg, origin="50% 70%", drift=0.02, fx=[(ti, e + 0.1, "fire", fire(h=260, w=520, grow=0.8))])
ep.js('gsap.set("#s04-torch",{x:500,y:300});')
ep.js(f'tl.fromTo("#s04-torch",{{x:500,y:300}},{{x:0,y:0,duration:0.5,ease:"power2.out",immediateRender:false}},{W(24) - 0.1:.3f});')
ep.js(f'tl.to("#s04-torch",{{x:-120,y:120,duration:0.3,ease:"power2.in"}},{ti - 0.25:.3f});')
ep.cue("whoosh-cinematic.mp3", W(24) - 0.1, 0.35)
ep.cue("sfx_whoosh.mp3", ti, 0.6)
ep.cue("roar.mp3", ti, 0.5)
ep.floor(s, 0.5, 0.0)
ep.floor(ti, 0.4, 0.6, 0.8)

# ---------------------------------------------------------------- S05 first few seconds, only warmth
s, e = cut(27), cut(35)
ep.timer("s05", s, e, W(28), WE(34), 0, 5, "ms", "SECONDS", 5 / 60)
ep.floor(s, 0.5, 0.25)

# ---------------------------------------------------------------- S06 you don't even realize (the eye)
s, e = cut(35), cut(41)
EYE = "M 160 1000 Q 540 690 920 1000 Q 540 1310 160 1000 Z"
ir = "".join(line(540 + 70 * math.cos(a), 1000 + 70 * math.sin(a), 540 + 145 * math.cos(a), 1000 + 145 * math.sin(a), "#8a0f12", 4) for a in [i * math.pi / 12 for i in range(24)])
svg = (f'<defs><clipPath id="s06-c"><path d="{EYE}"/></clipPath></defs><g id="s06-eye"><g filter="url(#glow)"><path d="{EYE}" fill="#ECE6E5" stroke="{RED}" stroke-width="22"/></g>'
       f'<g clip-path="url(#s06-c)"><g id="s06-iris"><circle cx="540" cy="1000" r="150" fill="#D32620"/>{ir}<circle cx="540" cy="1000" r="64" fill="#160404"/><circle cx="582" cy="958" r="18" fill="#FFF"/></g></g>'
       f'<path d="{EYE}" fill="none" stroke="{CORE}" stroke-width="6"/></g>')
ep.scene("s06", s, e, svg, origin="50% 52%", drift=0.02)
for k, (t, x) in enumerate([(W(36), -40), (W(37) + 0.1, 30), (W(39), -10)]):
    ep.js(f'tl.to("#s06-iris",{{x:{x},duration:0.1,ease:"power2.out"}},{t:.3f});')
tb = W(38)
ep.js(f'tl.to("#s06-eye",{{scaleY:0.05,svgOrigin:"540 1000",duration:0.07,ease:"power2.in"}},{tb:.3f});')
ep.js(f'tl.to("#s06-eye",{{scaleY:1,svgOrigin:"540 1000",duration:0.1,ease:"power2.out"}},{tb + 0.07:.3f});')
ep.floor(s, 0.45, 0.2)

# ---------------------------------------------------------------- S07 20 seconds in
s, e = cut(41), cut(44)
ep.timer("s07", s, e, s + 0.05, WE(43), 15, 20, "ms", "SECONDS", 20 / 60)
ep.floor(s, 0.5, 0.3)

# ---------------------------------------------------------------- S08 the fire reaches your feet
s, e = cut(44), cut(49)
FOOT = "M 380 700 L 520 700 L 540 1180 Q 560 1260 660 1280 L 820 1300 Q 880 1310 880 1360 L 880 1400 L 380 1400 Z"
svg = glow(N(FOOT)) + line(440, 760, 470, 1340, CORE, 5) + label(300, 900, "FOOT", 30, GREY, "end")
tf = W(45) - 0.05
ep.scene("s08", s, e, svg, origin="50% 60%", drift=0.025, fx=[(tf, e + 0.1, "fire", dict(cx=630, base=1440, w=620, h=300, n=9, grow=0.7, amp=1.0, sp=7))])
ep.cue("sfx_whoosh.mp3", tf, 0.5)
ep.floor(s, 0.4, 0.4)
ep.floor(tf, 0.3, 0.9, 0.6)

# ---------------------------------------------------------------- S09 600 degrees
s, e = cut(49), cut(51)
ep.thermometer("s09", s, e, s + 0.05, WE(50), 20, 600, 700, "CELSIUS")

# ---------------------------------------------------------------- S10 skin blisters, bursts... and blackens
s, e = cut(51), cut(57)
skin = glow(N("M 180 960 L 900 960 L 900 1260 L 180 1260 Z", fill="#1a0a0a"), gid="s10-skin") + "".join(
    f'<path d="M 200 {1030 + k * 60} Q 380 {1000 + k * 60} 540 {1030 + k * 60} T 880 {1030 + k * 60}" fill="none" stroke="#E87A8A" stroke-width="4" opacity="0.7"/>' for k in range(3))
blis = "".join(f'<g id="s10-b{k}" opacity="0"><path d="M {230 + k * 120} 962 A 50 56 0 0 1 {330 + k * 120} 962 Z" fill="#E8A0A0" stroke="#FFF1DC" stroke-width="5" filter="url(#glowS)"/></g>' for k in range(6))
char = f'<g id="s10-char" opacity="0"><rect x="180" y="940" width="720" height="40" fill="#0a0606"/><path d="M 220 950 L 300 1010 L 360 980 L 460 1060 M 560 950 L 620 1030 L 720 990 L 800 1080" stroke="#FF3B36" stroke-width="5" fill="none" filter="url(#glowS)"/></g>'
svg = skin + blis + char + label(540, 900, "SKIN", 30, GREY)
fxs = [(W(54), W(54) + 0.6, "sparks", dict(cx=280 + i * 120, cy=930, n=10, r=120, dur=0.5, color="#FF4A4E", g=120)) for i in range(6)]
ep.scene("s10", s, e, svg, origin="50% 52%", drift=0.025, fx=fxs)
for k in range(6):
    ep.js(f'tl.fromTo("#s10-b{k}",{{opacity:1,scale:0,svgOrigin:"{280 + k * 120} 962"}},{{scale:1,duration:0.16,ease:"back.out(2)",immediateRender:false}},{W(53) - 0.05 + k * 0.07:.3f});')
    ep.js(f'tl.set("#s10-b{k}",{{opacity:0}},0);tl.set("#s10-b{k}",{{opacity:0}},{W(54) - 0.02:.3f});')
ep.js(f'tl.to("#s10-skin path",{{fill:"#060404",duration:{W(56) - W(54) + 0.2:.3f},ease:"power1.in"}},{W(54) + 0.1:.3f});')
ep.show("#s10-char", W(56) - 0.05, 0.3)
ep.cue("impact-bass-1.mp3", W(54), 0.5)
ep.cue("sizzle.wav", W(55), 0.5)
ep.floor(s, 0.4, 0.7)

# ---------------------------------------------------------------- S11 pain signal up the spine
s, e = cut(57), cut(65)
vert = "".join(glow(N(f"M 500 {1500 - k * 54} L 580 {1500 - k * 54} L 580 {1500 - k * 54 - 38} L 500 {1500 - k * 54 - 38} Z", fill="#1a0a0c", sw=8, cw=3), f="glowS") for k in range(16))
pulses = "".join(f'<circle class="s11-pl" id="s11-pl{i}" cx="540" cy="1500" r="26" fill="#FF3B36" filter="url(#glow)" opacity="0"/>' for i in range(5))
svg = vert + pulses + label(640, 700, "TO THE BRAIN", 30, GREY, "start") + '<path d="M 540 640 L 540 560 M 520 590 L 540 560 L 560 590" stroke="#F2EEEA" stroke-width="5" fill="none"/>'
ep.scene("s11", s, e, svg, origin="50% 55%", drift=0.02)
n = int((e - s - 0.2) / 0.3)
for k in range(n):
    sel = f"#s11-pl{k % 5}"
    ep.js(f'tl.fromTo("{sel}",{{attr:{{cy:1500}},opacity:1}},{{attr:{{cy:640}},opacity:0.3,duration:0.5,ease:"power1.in",immediateRender:false}},{s + 0.1 + k * 0.3:.3f});')
ep.js('tl.set("#s11 .s11-pl",{opacity:0},0);')
ep.cue("sizzle.wav", s, 0.3)
ep.floor(s, 0.45, 0.3)

# ---------------------------------------------------------------- S12 brain alarm: can't think of anything else
s, e = cut(65), cut(71)
gyri = "".join(f'<path d="M {360 + k * 52} 820 Q {380 + k * 52} 900 {360 + k * 52} 980 Q {340 + k * 52} 1060 {360 + k * 52} 1140" fill="none" stroke="#F2EEEA" stroke-width="4" opacity="0.6"/>' for k in range(8))
brain = glow(N("M 540 780 C 380 760 300 860 310 980 C 320 1120 420 1200 540 1190 C 660 1200 760 1120 770 980 C 780 860 700 760 540 780 Z", fill="#3a0a0c") + gyri + line(540, 790, 540, 1190, CORE, 5), gid="s12-brain")
rings = "".join(f'<ellipse class="s12-rg" cx="540" cy="990" rx="{300 + k * 70}" ry="{110 + k * 26}" fill="none" stroke="#FF3B36" stroke-width="6" opacity="0.6" filter="url(#glow)"/>' for k in range(3))
badges = "".join(f'<g class="s12-bd"><circle cx="{540 + 360 * math.cos(a):.0f}" cy="{990 + 170 * math.sin(a):.0f}" r="34" fill="#FF3B36" filter="url(#glow)"/><text x="{540 + 360 * math.cos(a):.0f}" y="{1004 + 170 * math.sin(a):.0f}" fill="#fff" font-family="Roboto Condensed" font-weight="900" font-size="44" text-anchor="middle">!</text></g>'
                 for a in [i * math.pi / 3 for i in range(6)])
svg = rings + brain + badges
ep.scene("s12", s, e, svg, origin="50% 52%")
ep.shake("#s12-shake", s, e - s, 6)
ep.js(f'tl.fromTo(".s12-rg",{{opacity:0.2}},{{opacity:1,duration:0.2,repeat:{int((e - s) / 0.2)},yoyo:true,ease:"sine.inOut",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo(".s12-bd",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:0.15,stagger:0.06,ease:"back.out(2)",immediateRender:false}},{s + 0.1:.3f});')
for k in range(int((e - s) / 0.33)):
    ep.cue("tick.wav", s + k * 0.33, 0.5)
ep.floor(s, 0.6, 0.6)

# ---------------------------------------------------------------- S13 you try to break free (thrashing in the fire)
s, e = cut(71), cut(76)
svg = stake("m13", screaming=True)
ep.scene("s13", s, e, svg, origin="50% 55%", fx=[(s, e, "fire", fire(h=520, w=680)), (s, e, "embers", dict(n=50, x0=150, x1=930, y0=500, y1=1650, sp=200))])
thrash("m13", s, e, 13, 0.08)
ep.js(f'tl.fromTo("#m13",{{x:-14}},{{x:14,duration:0.1,repeat:{int((e - s) / 0.1)},yoyo:true,ease:"none",immediateRender:false}},{s:.3f});')
ep.cue("roar.mp3", s, 0.6)
ep.floor(s, 0.3, 1.0)

# ---------------------------------------------------------------- S14 but the chain holds
s, e = cut(76), cut(80)
links = "".join(f'<ellipse cx="{60 + k * 76}" cy="900" rx="46" ry="26" fill="none" stroke="#F2EEEA" stroke-width="12"/>' for k in range(14))
lock = ('<g transform="translate(540,1010)">' + '<path d="M -50 -40 L -50 -90 A 50 50 0 0 1 50 -90 L 50 -40" fill="none" stroke="#F2EEEA" stroke-width="16"/>'
        + N("M -80 -40 L 80 -40 L 80 90 L -80 90 Z", fill="#1a1416") + '<circle cx="0" cy="20" r="14" fill="#F2EEEA"/></g>')
svg = f'<g id="s14-chain"><g filter="url(#glow)">{links}</g>{glow(lock)}</g>'
ep.scene("s14", s, e, svg, origin="50% 50%")
tj = W(78) - 0.05
for k, dx in enumerate([10, -8, 6, -4, 0]):
    ep.js(f'tl.set("#s14-chain",{{y:{dx}}},{tj + k * 2 * F:.3f});')
ep.cue("impact-bass-2.mp3", tj, 0.7)
ep.floor(s, 0.45, 0.3)

# ---------------------------------------------------------------- S15 after a minute, something strange
s, e = cut(80), cut(86)
ep.timer("s15", s, e, s + 0.1, WE(82), 55, 60, "ms", "MINUTE", 1.0)
ep.shake("#s15-shake", W(84), 0.35, 12)
ep.js(f'tl.to("#s15-ring",{{attr:{{stroke:"#8a837e"}},duration:0.4}},{W(84):.3f});')
ep.js(f'tl.to("#s15-num",{{color:"#BDB5B5",textShadow:"0 0 0 rgba(0,0,0,0)",duration:0.4}},{W(84):.3f});')
ep.cue("impact-bass-1.mp3", W(84), 0.5)
ep.floor(s, 0.5, 0.3)

# ---------------------------------------------------------------- S16 the fire burns through the nerve endings
s, e = cut(86), cut(93)
trunk = '<path d="M 540 700 L 540 1100" stroke="#FF3B36" stroke-width="12" filter="url(#glow)"/>'
ends = ""
for k in range(6):
    x = 240 + k * 120
    ends += (f'<g id="s16-n{k}"><path d="M 540 1100 Q {(540 + x) / 2:.0f} 1180 {x} 1300" fill="none" stroke="#FF3B36" stroke-width="7" filter="url(#glow)"/>'
             f'<circle cx="{x}" cy="1300" r="18" fill="#FF3B36" filter="url(#glow)"/></g>')
svg = trunk + ends + label(565, 720, "TO THE BRAIN", 30, GREY, "start") + label(260, 1060, "NERVE ENDINGS", 30, GREY)
ep.scene("s16", s, e, svg, origin="50% 55%", drift=0.02, fx=[(s, e, "fire", dict(cx=540, base=1620, w=860, h=170, n=12, amp=0.9, sp=7))])
for k in range(6):
    t = W(88) + k * (W(92) - W(88)) / 6
    ep.js(f'tl.to("#s16-n{k} path, #s16-n{k} circle",{{attr:{{stroke:"#555",fill:"#555"}},duration:0.15}},{t:.3f});')
    ep.js(f'tl.to("#s16-n{k}",{{opacity:0.6,duration:0.15}},{t:.3f});')
    ep.cue("tick.wav", t, 0.4)
ep.floor(s, 0.4, 0.6)

# ---------------------------------------------------------------- S17 your legs stop hurting
s, e = cut(93), cut(98)
LEG = "M 440 600 L 620 600 L 610 1100 L 600 1420 L 700 1440 L 700 1490 L 470 1490 L 480 1100 Z"
dashes = "".join(f'<path class="s17-d" d="M {700 + (k % 2) * 30} {760 + k * 140} l 60 -20" stroke="#FF3B36" stroke-width="10" stroke-linecap="round" filter="url(#glow)"/>' for k in range(4))
xmark = ('<path id="s17-x1" d="M 300 800 L 780 1300" stroke="#FF3B36" stroke-width="20" stroke-linecap="round" stroke-dasharray="700" stroke-dashoffset="700" filter="url(#glow)"/>'
         '<path id="s17-x2" d="M 780 800 L 300 1300" stroke="#FF3B36" stroke-width="20" stroke-linecap="round" stroke-dasharray="700" stroke-dashoffset="700" filter="url(#glow)"/>')
svg = f'<g id="s17-leg">{glow(N(LEG))}</g><g id="s17-legdead" opacity="0">{N(LEG, red="#555", core="#777", fill="#0c0c0c", sw=6, cw=2)}</g>' + dashes + xmark
ep.scene("s17", s, e, svg, origin="50% 55%")
r17 = random.Random(17)
td = W(96) - 0.05
for k in range(int((td - s) * 10)):
    ep.js(f'tl.set(".s17-d",{{opacity:{r17.choice([0.3, 1, 1])}}},{s + k * 0.1:.3f});')
ep.js(f'tl.set(".s17-d",{{opacity:0}},{td:.3f});')
ep.js(f'tl.set("#s17-leg",{{opacity:0}},{td:.3f});')
ep.show("#s17-legdead", td)
ep.js(f'tl.to("#s17-x1",{{strokeDashoffset:0,duration:0.14,ease:"power2.out"}},{td + 0.1:.3f});')
ep.js(f'tl.to("#s17-x2",{{strokeDashoffset:0,duration:0.14,ease:"power2.out"}},{td + 0.26:.3f});')
ep.cue("sfx_whoosh.mp3", td + 0.1, 0.4)
ep.cue("sfx_whoosh.mp3", td + 0.26, 0.4)
ep.floor(s, 0.45, 0.2)

# ---------------------------------------------------------------- S18 you simply can't feel them (signal flatlines)
s, e = cut(98), cut(104)
grid = "".join(line(80 + i * 92, 760, 80 + i * 92, 1180, "#3a1416", 2) for i in range(11))
ep.scene("s18", s, e, grid + label(90, 740, "PAIN SIGNAL", 30, GREY, "start"), origin="50% 50%",
         fx=[(s, e, "ecg", dict(x0=80, x1=1000, y=970, amp=300, flat_at=W(101) - 0.1, flat_dur=0.8))])
ep.cue("beep.wav", W(101) + 0.6, 0.12)
ep.floor(s, 0.45, 0.2)

# ---------------------------------------------------------------- S19 the flames climb higher
s, e = cut(104), cut(108)
svg = stake("m19", screaming=True, pose=dict(head=-18))
ep.scene("s19", s, e, svg, origin="50% 50%", fx=[(s, e, "fire", dict(fire(h=900, w=720), grow=1.6)), (s, e, "embers", dict(n=70, x0=150, x1=930, y0=300, y1=1650, sp=260))])
ep.js(f'tl.fromTo("#s19-cam",{{y:0}},{{y:120,duration:{e - s:.3f},ease:"power1.inOut",immediateRender:false}},{s:.3f});')
ep.cue("roar.mp3", s, 0.8)
ep.floor(s, 0.3, 1.0)

# ---------------------------------------------------------------- S20 hot air scorches your throat
s, e = cut(108), cut(122)
HEAD = "M 640 520 C 470 500 380 610 380 760 C 380 830 395 870 410 900 L 380 960 L 420 978 L 412 1030 C 430 1080 500 1090 540 1076 L 560 1400 L 720 1400 L 720 1020 C 790 950 810 850 790 740 C 770 600 730 530 640 520 Z"
airway = '<path id="s20-air" d="M 400 970 C 480 980 560 990 610 1030 C 630 1100 635 1250 635 1400" fill="none" stroke="#F2EEEA" stroke-width="26" stroke-linecap="round" opacity="0.85"/>'
dots = "".join(f'<circle class="s20-dot" id="s20-d{i}" cx="300" cy="970" r="10" fill="#FFFFFF" opacity="0"/>' for i in range(10))
svg = glow(N(HEAD)) + airway + dots + label(740, 1200, "AIRWAY", 30, GREY, "start")
ep.scene("s20", s, e, svg, origin="50% 50%", drift=0.018)
for k in range(10):
    t = W(110) - 0.1 + k * 0.12
    sel = f"#s20-d{k}"
    ep.js(f'tl.fromTo("{sel}",{{attr:{{cx:300,cy:970}},opacity:1}},{{keyframes:[{{attr:{{cx:610,cy:1030}},duration:0.35,ease:"none"}},{{attr:{{cx:635,cy:1400}},duration:0.4,ease:"none"}}],immediateRender:false}},{t:.3f});')
ep.js('tl.set("#s20 .s20-dot",{opacity:0},0);')
th = W(114) - 0.05
ep.js(f'tl.to("#s20 .s20-dot",{{attr:{{fill:"#FF3B36"}},duration:0.2}},{th:.3f});')
ep.js(f'tl.to("#s20-air",{{attr:{{stroke:"#FF3B36"}},duration:0.4}},{W(116) - 0.05:.3f});')
for k in range(10):
    t = th + 0.3 + k * 0.12
    sel = f"#s20-d{k}"
    ep.js(f'tl.fromTo("{sel}",{{attr:{{cx:300,cy:970}},opacity:1}},{{keyframes:[{{attr:{{cx:610,cy:1030}},duration:0.35,ease:"none"}},{{attr:{{cx:635,cy:1400}},duration:0.4,ease:"none"}}],immediateRender:false}},{t:.3f});')
ep.cue("whoosh-short.mp3", W(110), 0.35)
ep.cue("sizzle.wav", W(116), 0.5)
ep.floor(s, 0.45, 0.5)

# ---------------------------------------------------------------- S21 it starts to swell (airway cross-section)
s, e = cut(122), cut(126)
svg = (glow(N("M 540 700 C 760 700 820 860 820 980 C 820 1100 760 1260 540 1260 C 320 1260 260 1100 260 980 C 260 860 320 700 540 700 Z", fill="#3a0a0c"))
       + f'<ellipse id="s21-open" cx="540" cy="980" rx="170" ry="150" fill="#010101" stroke="#F2EEEA" stroke-width="6"/>' + label(540, 640, "AIRWAY", 30, GREY))
ep.scene("s21", s, e, svg, origin="50% 52%")
ep.js(f'tl.to("#s21-open",{{attr:{{rx:46,ry:28}},duration:{e - W(124):.3f},ease:"power1.in"}},{W(124) - 0.1:.3f});')
ep.floor(s, 0.45, 0.4)

# ---------------------------------------------------------------- S22 every breath smaller than the last (bars)
s, e = cut(126), cut(133)
bars = ""
for k, h in enumerate([520, 400, 300, 210, 130]):
    bars += f'<rect id="s22-b{k}" x="{180 + k * 150}" y="{1400 - h}" width="100" height="{h}" rx="10" fill="#FB2945" filter="url(#glow)" opacity="0"/>'
svg = bars + hline(1400, 120, 960) + label(540, 1480, "BREATH VOLUME", 30, GREY)
ep.scene("s22", s, e, svg, origin="50% 55%")
for k in range(5):
    t = s + 0.1 + k * (e - s - 0.6) / 5
    ep.js(f'tl.fromTo("#s22-b{k}",{{opacity:1,scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:0.2,ease:"back.out(1.6)",immediateRender:false}},{t:.3f});')
    ep.js(f'tl.set("#s22-b{k}",{{opacity:0}},0);')
    ep.cue("whoosh-short.mp3", t, 0.2 - k * 0.03)
ep.floor(s, 0.45, 0.3)

# ---------------------------------------------------------------- S23 smoke fills your lungs
s, e = cut(133), cut(137)
ep.lungs("s23", s, e, t_flood=W(133), t_burn=W(134), t_burn_end=WE(136) + 0.3, flood_color="#8a837e", smoke=True)
ep.cue("sizzle.wav", W(133), 0.3)
ep.floor(s, 0.4, 0.3)

# ---------------------------------------------------------------- S24 carbon monoxide pushes the oxygen out
s, e = cut(137), cut(146)
cells = ""
for k in range(6):
    x, y = 260 + (k % 3) * 280, 860 + (k // 3) * 320
    cells += (f'<g id="s24-c{k}">' + glow(f'<ellipse cx="{x}" cy="{y}" rx="110" ry="80" fill="#9a1a1c" stroke="#FB2945" stroke-width="10"/><ellipse cx="{x}" cy="{y}" rx="50" ry="30" fill="#6a0f12"/>')
              + f'<g id="s24-o{k}"><circle cx="{x + 80}" cy="{y - 70}" r="34" fill="#5A78FF" filter="url(#glowB)"/>' + label(x + 80, y - 58, "O₂", 30, "#FFFFFF") + '</g>'
              + f'<g id="s24-co{k}" opacity="0"><circle cx="{x + 80}" cy="{y - 70}" r="34" fill="#555"/>' + label(x + 80, y - 58, "CO", 30, "#FFFFFF") + '</g></g>')
svg = cells + label(540, 1380, "RED BLOOD CELLS", 30, GREY)
ep.scene("s24", s, e, svg, origin="50% 55%", drift=0.02)
for k in range(6):
    t = W(139) + k * (W(143) - W(139)) / 6
    ep.js(f'tl.to("#s24-o{k}",{{y:-260,x:{(k % 3 - 1) * 120},opacity:0,duration:0.4,ease:"power2.in"}},{t:.3f});')
    ep.show(f"#s24-co{k}", t + 0.05, 0.1)
    ep.js(f'tl.to("#s24-c{k} ellipse",{{attr:{{fill:"#3a0a0c"}},duration:0.4}},{t:.3f});')
    ep.cue("pop.mp3", t, 0.2)
ep.floor(s, 0.45, 0.2)

# ---------------------------------------------------------------- S25 heart beats faster, trying to save your brain
s, e = cut(146), cut(157)
HEART = "M 540 1020 C 400 920 330 840 360 750 C 390 660 500 660 540 750 C 580 660 690 660 720 750 C 750 840 680 920 540 1020 Z"
svg = f'<g transform="translate(0,-60)">' + glow(N(HEART, fill="#2a0a0c"), gid="s25-heart") + '</g>'
html = '<div class="num" id="s25-bpm" style="top:1010px;font-size:140px;">90</div><div class="lbl" style="top:1160px;">BEATS PER MINUTE</div>'
ep.scene("s25", s, e, svg, html, origin="50% 50%", fx=[(s, e, "ecg", dict(x0=60, x1=1020, y=1450, amp=140, period=420, period1=190, dur=e - s, speed=380))])
ep.counter("#s25-bpm", s + 0.1, e - s - 0.3, 90, 190, "n", "power1.in")
t, gap = s, 0.66
while t < e - 0.1:
    ep.js(f'tl.fromTo("#s25-heart",{{scale:1.1,svgOrigin:"540 860"}},{{scale:1,duration:{min(0.25, gap * 0.6):.2f},ease:"power2.out",immediateRender:false}},{t:.3f});')
    ep.cue("heart.wav", t, 0.5)
    t += gap
    gap = max(0.3, gap * 0.93)
ep.floor(s, 0.45, 0.3)

# ---------------------------------------------------------------- S26 the crowd's noise turns muffled
s, e = cut(157), cut(162)
wr = random.Random(26)
wave = "M 80 960 " + " ".join(f"L {80 + i * 10} {960 + wr.uniform(-200, 200) * abs(math.sin(i * 0.15)):.0f}" for i in range(1, 93))
svg = f'<g id="s26-w"><g filter="url(#glow)"><path id="s26-p" d="{wave}" fill="none" stroke="#FF3B36" stroke-width="6"/></g></g>' + label(90, 700, "SOUND", 30, GREY, "start")
ep.scene("s26", s, e, svg, origin="50% 50%")
ep.js(f'tl.to("#s26-w",{{scaleY:0.15,svgOrigin:"540 960",duration:{e - W(160):.3f},ease:"power1.in"}},{W(160) - 0.1:.3f});')
ep.js(f'tl.to("#s26-p",{{attr:{{stroke:"#7a5a5a"}},duration:{e - W(160):.3f}}},{W(160) - 0.1:.3f});')
ep.floor(s, 0.4, 0.2)

# ---------------------------------------------------------------- S27 the firelight blurs
s, e = cut(162), cut(165)
ep.scene("s27", s, e, "", origin="50% 60%", fx=[(s, e + 0.1, "fire", dict(cx=540, base=1500, w=900, h=900, n=12, amp=1.0, sp=6))])
ep.js(f'tl.fromTo("#s27-cam",{{filter:"blur(0px)"}},{{filter:"blur(18px)",duration:0.45,ease:"power1.in",immediateRender:false}},{W(164) - 0.05:.3f});')
ep.floor(s, 0.3, 0.7)

# ---------------------------------------------------------------- S28 you're still conscious (dim, slumped)
s, e = cut(165), cut(168)
svg = stake("m28", pose=dict(head=24))
ep.scene("s28", s, e, svg, origin="50% 40%", drift=0.03, fx=[(s, e, "fire", fire(h=700, w=700, amp=0.75)), (s, e, "smoke", dict(n=14, cx=540, base=900, w=400, h=900, r0=80, r1=300, life=3, alpha=0.45))])
ep.floor(s, 0.25, 0.5)

# ---------------------------------------------------------------- S29 a few more seconds (countdown)
s, e = cut(168), cut(172)
C = 2 * math.pi * 330
svg = (f'<g filter="url(#glow)"><circle id="s29-ring" cx="540" cy="960" r="330" fill="none" stroke="#FB2945" stroke-width="16" stroke-dasharray="{C:.0f}" stroke-dashoffset="0" transform="rotate(-90 540 960)"/></g>')
html = '<div class="num" id="s29-n" style="top:840px;font-size:240px;">3</div>'
ep.scene("s29", s, e, svg, html, origin="50% 50%")
ep.js(f'tl.to("#s29-ring",{{strokeDashoffset:{C:.0f},duration:{e - s:.3f},ease:"none"}},{s:.3f});')
ep.counter("#s29-n", s, e - s, 3.49, 0.51, "n", "none")
for k in range(3):
    ep.cue("tick.wav", s + k * (e - s) / 3, 0.6)
ep.floor(s, 0.25, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(172), 175)
ep.write(red=["stake", "torch", "fire", "chain", "strange", "smoke", "heart", "conscious", "flames"])
