"""Episode 03 — How does it feel? When they execute you in the electric chair."""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kit"))
from lib import *  # noqa

ep = Episode(__file__)
W, WE, cut = ep.W, ep.WE, ep.cut
WOOD, SLAT = "#46302c", "#a3938e"
SEAT = dict(thighL="rotate(14) scale(1,0.32)", shinL="scale(1,3.125) rotate(-10)", thighR="rotate(-14) scale(1,0.32)", shinR="scale(1,3.125) rotate(10)",
            uarmL=34, farmL=-58, uarmR=-34, farmR=58)


def stage():
    cones = ('<polygon points="0,0 220,0 520,1560 160,1560" fill="url(#ec-cone)" opacity="0.9" class="ec-spot"/>'
             '<polygon points="1080,0 860,0 560,1560 920,1560" fill="url(#ec-cone)" opacity="0.9" class="ec-spot"/>'
             '<ellipse cx="540" cy="1560" rx="420" ry="60" fill="#ff6a5a" opacity="0.14" filter="url(#soft2)" class="ec-spot"/>')
    floor_lines = "".join(line(540 + (i - 6) * 40, 1540, 540 + (i - 6) * 190, 1920, "#ffffff", 1.5, 'opacity="0.07"') for i in range(13))
    return ('<defs><linearGradient id="ec-cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.13"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.03"/></linearGradient></defs>'
            + cones + floor_lines + hline(1540, sw=8, cw=3))


def chair(gid, straps=(), helmet=False, hot_straps=False):
    slats = "".join(line(x, 800, x, 1245, SLAT, 5) for x in range(445, 640, 45))
    back = glow(N("M 400 780 L 680 780 L 680 1255 L 400 1255 Z", fill=WOOD) + slats + N("M 375 750 L 705 750 L 705 795 L 375 795 Z", fill=WOOD, sw=12, cw=4), gid=f"{gid}-back")
    seat = glow(N("M 350 1250 L 730 1250 L 730 1300 L 350 1300 Z", fill=WOOD) + N("M 372 1300 L 404 1300 L 404 1540 L 372 1540 Z", fill=WOOD, sw=10, cw=4)
                + N("M 676 1300 L 708 1300 L 708 1540 L 676 1540 Z", fill=WOOD, sw=10, cw=4))
    arms = glow(N("M 270 1145 L 415 1145 L 415 1178 L 270 1178 Z", fill=WOOD, sw=12, cw=4) + N("M 665 1145 L 810 1145 L 810 1178 L 665 1178 Z", fill=WOOD, sw=12, cw=4)
                + N("M 290 1178 L 315 1178 L 315 1250 L 290 1250 Z", fill=WOOD, sw=10, cw=4) + N("M 765 1178 L 790 1178 L 790 1250 L 765 1250 Z", fill=WOOD, sw=10, cw=4))
    return back + seat + arms


def strap_svg(gid, which, hot=False):
    col = "#FF3B36" if hot else "#6b4a30"
    rects = dict(arms=[(300, 1128, 90, 26), (690, 1128, 90, 26)], legs=[(420, 1440, 90, 24), (570, 1440, 90, 24)], chest=[(440, 1120, 200, 30)])[which]
    out = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}" stroke="#F2EEEA" stroke-width="4"/><rect x="{x + w / 2 - 10}" y="{y + 3}" width="20" height="{h - 6}" fill="none" stroke="#E8B040" stroke-width="4"/>' for x, y, w, h in rects)
    return f'<g id="{gid}-{which}" filter="url(#glowS)">{out}</g>'


def helmet_svg(gid):
    cable = f'<path d="M 540 905 C 540 700 640 600 600 0" fill="none" stroke="#8a837e" stroke-width="12"/><path d="M 540 905 C 540 700 640 600 600 0" fill="none" stroke="#F2EEEA" stroke-width="3"/>'
    dome = glow(N("M 470 1000 Q 466 900 540 895 Q 614 900 610 1000 Z", fill="#4a4a52", red="#8a8aa0", core="#F2EEEA", sw=10, cw=4)
                + "".join(f'<circle cx="{482 + k * 19}" cy="990" r="4" fill="#F2EEEA"/>' for k in range(7)), f="glowS")
    sponge = f'<rect id="{gid}-sponge" x="476" y="1000" width="128" height="14" rx="6" fill="#E8C060" opacity="0.9"/>'
    return f'<g id="{gid}">{cable}{dome}{sponge}</g>'


def seated(mid, style="neon", pose_extra=None, mouth_open=False):
    p = dict(SEAT)
    p.update(pose_extra or {})
    return mascot(mid, 540, 1488, 0.85, pose=p, style=style, mouth_open=mouth_open)


def bolts_at(x0=540, y0=900, wide=True):
    b = [[x0, y0, x0 + 20, 120], [x0 - 10, y0, 380, 760], [x0 + 10, y0, 700, 760], [330, 1150, 120, 980], [750, 1150, 960, 980]]
    plasma = [[x0, y0, 120], [330, 1150, 90], [750, 1150, 90]]
    return dict(bolts=b if wide else b[:3], plasma=plasma, amp=0.35, branch=0.3)


def convulse(mid, t0, t1, amp=10, seed=1, head=True):
    r = random.Random(seed)
    for k in range(int((t1 - t0) * 30)):
        t = t0 + k * F
        ep.js(f'tl.set("#{mid}",{{x:{r.uniform(-amp, amp):.1f},y:{r.uniform(-amp * 0.6, amp * 0.3):.1f}}},{t:.3f});')
        if head and k % 2 == 0:
            ep.js(f'tl.set("#{mid}-head",{{attr:{{transform:"rotate({r.uniform(-14, 6):.0f},0,-492)"}}}},{t:.3f});')
    ep.js(f'tl.set("#{mid}",{{x:0,y:0}},{t1:.3f});')


# ---------------------------------------------------------------- S01 cold open: electrocution close-up → pull out
s, e = 0.0, cut(12)
svg = stage() + chair("c1") + seated("m1", pose_extra=dict(head=-10), mouth_open=True) + strap_svg("c1", "arms") + strap_svg("c1", "legs") + strap_svg("c1", "chest") + helmet_svg("h1")
ep.scene("s01", s, e, svg, origin="50% 50%", custom_cam=True, fx=[(s, e, "lightning", bolts_at())])
ep.js(f'tl.fromTo("#s01-cam",{{scale:2.2}},{{scale:2.3,duration:{W(4) - 0.15:.3f},ease:"none"}},0);')
ep.js(f'tl.to("#s01-cam",{{scale:1.0,duration:0.8,ease:"power2.inOut"}},{W(4) - 0.15:.3f});')
ep.js(f'tl.to("#s01-cam",{{scale:1.04,duration:{e - W(4) - 0.65:.3f},ease:"none"}},{W(4) + 0.65:.3f});')
convulse("m1", 0, e, 9, 1)
ep.floor(0, 0.7, 0.3, 0.01)
ep.cue("sfx_open_roar.mp3", 0, 0.5)
ep.cue("sizzle.wav", 0, 0.9)
ep.cue("sizzle.wav", 2.4, 0.8)
ep.cue("sub.wav", 0, 0.8)

# ---------------------------------------------------------------- S02 New York. 1890.
s, e = cut(12), cut(15)
svg = "".join(line(80 + i * 46, 560, 80 + i * 46, 1500, "#FB2945", 2, f'opacity="{0.15 + 0.25 * (i % 3) / 2:.2f}"') for i in range(21)) + line(60, 1180, 1020, 1180, "#FB2945", 3, 'opacity="0.4"')
html = ('<div class="big" id="s02-t1" style="top:760px;font-size:120px;">NEW YORK</div>'
        '<div class="num" id="s02-t2" style="top:900px;font-size:240px;">1890</div>'
        '<div class="lbl" id="s02-t3" style="top:1160px;">AUBURN PRISON</div>')
ep.scene("s02", s, e, svg, html, origin="50% 50%")
ep.pop("#s02-t1", s, 0.16, 0.85)
ep.pop("#s02-t2", W(14) - 0.05, 0.16, 0.6)
ep.pop("#s02-t3", W(14) + 0.2, 0.2, 0.5)
ep.cue("impact-bass-1.mp3", W(14) - 0.05, 0.5)
ep.floor(s, 0.6, 0.0)

# ---------------------------------------------------------------- S03 Your name is William Kemmler (mugshot)
s, e = cut(15), cut(20)
chart = "".join(line(80, y, 1000, y, "#ffffff", 2, 'opacity="0.18"') + label(70, y + 10, lab, 26, "#8a837e", "end") for y, lab in [(700, "6'"), (820, "5'6"), (940, "5'"), (1060, "4'6"), (1180, "4'")])
placard = (glow(N("M 360 1170 L 720 1170 L 720 1350 L 360 1350 Z", fill="#0a0808", sw=10, cw=4))
           + label(540, 1240, "W. KEMMLER", 46, "#F5F5F5") + label(540, 1310, "No. 1 · 1890", 40, "#FF3B36"))
svg = chart + mascot("m3", 540, 1600, 1.15, pose=dict(uarmL=-20, farmL=-120, uarmR=20, farmR=120)) + placard
ep.scene("s03", s, e, svg, origin="50% 50%", drift=0.02)
ep.flash(W(19) - 0.05, 0.75, 0.45)
ep.cue("impact-bass-1.mp3", W(19) - 0.05, 0.4)
ep.cue("pop.mp3", W(19) - 0.05, 0.6)
ep.floor(s, 0.6, 0.0)

# ---------------------------------------------------------------- S04 the first person executed with electricity
s, e = cut(20), cut(33)
bolt_icon = glow(N("M 600 640 L 470 900 L 560 900 L 500 1120 L 680 830 L 580 830 L 650 640 Z", fill="#0b1430", red="#5A78FF", core="#FFFFFF"), f="glowB", gid="s04-bolt")
html = ('<div class="num" id="s04-no" style="top:1000px;font-size:220px;">No.1</div>'
        '<div class="lbl" id="s04-sub" style="top:1235px;font-size:38px;color:#9FC8FF;">FIRST ELECTRIC EXECUTION</div>')
ep.scene("s04", s, e, bolt_icon, html, origin="50% 55%", drift=0.018, fx=[(W(30) - 0.1, e, "lightning", dict(bolts=[[200, 1250, 420, 1240], [880, 1250, 660, 1240]], plasma=[[540, 880, 90]], amp=0.4, flick=0.4))])
ep.pop("#s04-bolt", s, 0.2, 0.2)
ep.pop("#s04-no", W(26) - 0.05, 0.18, 0.3)
ep.pop("#s04-sub", W(30) - 0.05, 0.2, 0.5)
ep.cue("sizzle.wav", W(30) - 0.1, 0.6)
ep.cue("impact-bass-2.mp3", W(26) - 0.05, 0.5)
ep.floor(s, 0.55, 0.0)

# ---------------------------------------------------------------- S05 they sit you in a heavy wooden chair
s, e = cut(33), cut(41)
svg = stage() + chair("c5") + f'<g id="s05-man" opacity="0">{seated("m5")}</g>'
ep.scene("s05", s, e, svg, origin="50% 58%", drift=0.02)
for k, on in enumerate([1, 0, 1, 0, 1]):
    ep.js(f'tl.set("#s05 .ec-spot",{{opacity:{0.9 if on else 0}}},{s + 0.12 + k * 2 * F:.3f});')
    if on:
        ep.cue("click.mp3" if False else "pop.mp3", s + 0.12 + k * 2 * F, 0.25)
ep.js(f'tl.set("#s05 .ec-spot",{{opacity:0}},{s:.3f});')
ep.show("#s05-man", W(34) + 0.05)
ep.cue("impact-bass-1.mp3", W(34) + 0.05, 0.4)
ep.floor(s, 0.75, 0.0)

# ---------------------------------------------------------------- S06 straps: arms, legs, chest (punch per strap)
s, e = cut(41), cut(50)
svg = stage() + chair("c6") + seated("m6") + f'<g opacity="0" id="s06-sa">{strap_svg("c6", "arms")}</g><g opacity="0" id="s06-sl">{strap_svg("c6", "legs")}</g><g opacity="0" id="s06-sc">{strap_svg("c6", "chest")}</g>'
ep.scene("s06", s, e, svg, origin="50% 58%", custom_cam=True)
ep.js(f'tl.fromTo("#s06-cam",{{scale:0.9}},{{scale:1,duration:{5 * F:.3f},ease:"power2.out",immediateRender:false}},{s:.3f});')
for sel, wi, sc, org in [("#s06-sa", 45, 1.35, "50% 60%"), ("#s06-sl", 47, 1.45, "50% 75%"), ("#s06-sc", 49, 1.6, "50% 58%")]:
    t = W(wi) - 0.08
    ep.js(f'tl.set("#s06-cam",{{transformOrigin:"{org}"}},{t:.3f});')
    ep.js(f'tl.fromTo("#s06-cam",{{scale:{sc - 0.12:.2f}}},{{scale:{sc:.2f},duration:{5 * F:.3f},ease:"power2.out",immediateRender:false}},{t:.3f});')
    ep.pop(sel, t + 0.05, 0.14, 1.4, "power3.out")
    ep.cue("impact-bass-2.mp3", t + 0.08, 0.45)
ep.floor(s, 0.75, 0.0)

# ---------------------------------------------------------------- S07 metal helmet, wet sponge
s, e = cut(50), cut(62)
svg = stage() + chair("c7") + seated("m7") + strap_svg("c7", "arms") + strap_svg("c7", "legs") + strap_svg("c7", "chest") + helmet_svg("h7")
html = '<div class="lbl" id="s07-lab" style="top:1030px;left:620px;width:400px;text-align:left;color:#E8C060;">WET SPONGE</div>'
ep.scene("s07", s, e, svg, html, origin="50% 50%", custom_cam=True, fx=[(W(60), e, "ash", dict(n=14, sp=260, x0=480, x1=600, y0=1010, y1=1250, color="#7AA0FF"))])
ep.js(f'tl.fromTo("#s07-cam",{{scale:1.25}},{{scale:1.6,duration:{e - s:.3f},ease:"sine.inOut",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo("#h7",{{y:-700}},{{y:0,duration:0.75,ease:"power2.out",immediateRender:false}},{W(51) - 0.1:.3f});')
ep.pop("#s07-lab", W(60) - 0.05, 0.2, 0.5)
ep.cue("whoosh-cinematic.mp3", W(51) - 0.1, 0.3)
ep.cue("impact-bass-1.mp3", W(51) + 0.6, 0.5)
ep.floor(s, 0.7, 0.0)

# ---------------------------------------------------------------- S08 the water helps the current flow (close-up)
s, e = cut(62), cut(68)
arrows = "".join(f'<path class="s08-ar" d="M 540 {300 + k * 140} l -16 -26 M 540 {300 + k * 140} l 16 -26" stroke="#9FC8FF" stroke-width="6" fill="none" filter="url(#glowB)"/>' for k in range(5))
svg = stage() + chair("c8") + seated("m8") + strap_svg("c8", "chest") + helmet_svg("h8") + f'<g id="s08-arw">{arrows}</g>'
html = '<div class="lbl" id="s08-lab" style="top:1060px;left:620px;width:400px;text-align:left;color:#9FC8FF;">WATER</div>'
ep.scene("s08", s, e, svg, html, origin="50% 45%", custom_cam=True, fx=[(s, e, "ash", dict(n=18, sp=260, x0=480, x1=600, y0=1010, y1=1300, color="#7AA0FF"))])
ep.js(f'tl.fromTo("#s08-cam",{{scale:1.9}},{{scale:2.05,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.pop("#s08-lab", W(63) - 0.05, 0.2, 0.5)
ep.js(f'tl.fromTo("#s08-arw",{{y:-140}},{{y:140,duration:0.5,repeat:{int((e - W(65)) / 0.5)},ease:"none",immediateRender:false}},{W(65):.3f});')
ep.show("#s08-arw", W(65) - 0.05)
ep.floor(s, 0.6, 0.0)

# ---------------------------------------------------------------- S09 the executioner throws the switch
s, e = cut(68), cut(73)
panel = glow(N("M 240 760 L 840 760 L 840 1380 L 240 1380 Z", fill="#141416")) + label(380, 840, "OFF", 40, "#F5F5F5") + label(700, 840, "ON", 40, "#FF3B36")
contacts = glow(N("M 640 1220 L 760 1220 L 760 1260 L 640 1260 Z", fill="#6b4a30", red="#E8B040", core="#FFE08A", sw=8, cw=3), f="glowG")
lever = f'<g transform="translate(400,1240)"><g id="s09-lever" transform="rotate(-70)">' + glow(N("M -14 0 L -14 -330 L 14 -330 L 14 0 Z", fill="#2a2a30", sw=10, cw=4)
        + N("M -40 -330 L 40 -330 L 40 -390 L -40 -390 Z", fill="#0C0A0C", sw=10, cw=4)) + '</g></g>' + '<circle cx="400" cy="1240" r="26" fill="#F2EEEA"/>'
svg = panel + contacts + lever
tsw = W(72)
ep.scene("s09", s, e, svg, origin="50% 55%", drift=0.02, fx=[(tsw, e, "sparks", dict(cx=700, cy=1230, n=40, r=260, dur=0.6, color="#FFFFFF")),
                                                           (tsw, e, "lightning", dict(bolts=[[640, 1230, 520, 1000], [760, 1230, 880, 1010]], plasma=[[700, 1240, 110]], amp=0.4, flick=0.3))])
ep.rot("#s09-lever", s + 0.2, tsw - s - 0.5, -50, "power1.in")
ep.rot("#s09-lever", tsw - 0.3, 0.3, 62, "power3.in")
ep.flash(tsw, 0.6, 0.4)
ep.shake("#s09-shake", tsw, 0.4, 12)
ep.cue("sizzle.wav", tsw, 0.9)
ep.cue("impact-bass-2.mp3", tsw, 0.9)
ep.floor(s, 0.5, 0.0)
ep.floor(tsw, 0.4, 0.5, 0.1)


# ---------------------------------------------------------------- voltmeter
def voltmeter(sid, start, end, tn, val, pegged=False):
    cx, cy, R = 540, 880, 300

    def pol(v, r):
        a = math.radians(180 - v / 2000 * 180)
        return cx + r * math.cos(a), cy - r * math.sin(a)

    gt = ""
    for v in range(0, 2001, 250):
        x1, y1 = pol(v, R - 10)
        x2, y2 = pol(v, R - (52 if v % 500 == 0 else 32))
        gt += line(x1, y1, x2, y2, CORE, 6 if v % 500 == 0 else 3)
        if v % 500 == 0:
            lx, ly = pol(v, R - 96)
            gt += label(lx, ly + 10, v, 28, GREY)
    ra, rb = pol(1500, R), pol(2000, R)
    svg = (glow(N(f"M {cx - R} {cy} A {R} {R} 0 0 1 {cx + R} {cy}", fill="none") + gt)
           + f'<path d="M {ra[0]:.0f} {ra[1]:.0f} A {R} {R} 0 0 1 {rb[0]:.0f} {rb[1]:.0f}" fill="none" stroke="#FF3B36" stroke-width="30" filter="url(#glow)" opacity="0.9"/>'
           + f'<g transform="translate({cx},{cy})"><g id="{sid}-needle" transform="rotate(-90)"><g filter="url(#glow)">' + N("M -12 0 L 0 -280 L 12 0 Z", fill="#FA2335", sw=8, cw=3)
           + f'<circle r="28" fill="{DARK}" stroke="{RED}" stroke-width="10"/></g></g></g>')
    html = (f'<div class="num" id="{sid}-num" style="top:930px;font-size:170px;">0 V</div><div class="lbl" style="top:1110px;">VOLTS</div>')
    ep.scene(sid, start, end, svg, html, origin="50% 55%")
    ang = -90 + val / 2000 * 180
    ep.js(f'tl.to("#{sid}-needle",{{attr:{{transform:"rotate({ang + (8 if pegged else 6):.1f})"}},duration:0.14,ease:"power3.out"}},{tn:.3f});')
    ep.js(f'tl.to("#{sid}-needle",{{attr:{{transform:"rotate({ang:.1f})"}},duration:0.12,ease:"power2.out"}},{tn + 0.14:.3f});')
    ep.counter(f"#{sid}-num", tn, 0.26, 0, val, "v", "power3.out")
    r = random.Random(val)
    for k in range(int((end - tn - 0.3) * 15)):
        ep.js(f'tl.set("#{sid}-needle",{{attr:{{transform:"rotate({ang + r.uniform(-2.5, 2.5):.1f})"}}}},{tn + 0.3 + k * 2 * F:.3f});')
    ep.cue("riser.mp3", tn - 0.6, 0.35)
    ep.cue("impact-bass-1.mp3", tn + 0.1, 0.7)
    ep.floor(start, 0.5, 0.3)


s, e = cut(73), cut(75)
voltmeter("s10", s, e, W(73) - 0.05, 1000)

# ---------------------------------------------------------------- S11 every muscle clenches (wide electrocution)
s, e = cut(75), cut(83)
svg = stage() + chair("c11") + seated("m11", pose_extra=dict(head=-12, uarmL=48, farmL=-90, uarmR=-48, farmR=90)) + strap_svg("c11", "arms") + strap_svg("c11", "legs") + strap_svg("c11", "chest") + helmet_svg("h11")
ep.scene("s11", s, e, svg, origin="50% 55%", fx=[(s, e, "lightning", bolts_at())])
convulse("m11", s, e, 10, 11)
ep.js(f'tl.set("#s11-shake",{{y:-30}},{W(76) - 0.03:.3f});tl.set("#s11-shake",{{y:0}},{W(76) + 0.03:.3f});')
ep.cue("sizzle.wav", s, 1.0)
ep.cue("sizzle.wav", s + 2.4, 0.9)
ep.cue("sub.wav", s, 1.0)
ep.floor(s, 0.9, 0.5, 0.05)

# ---------------------------------------------------------------- S12 can't scream, jaw locked (face close-up)
s, e = cut(83), cut(94)
svg = stage() + chair("c12") + seated("m12", pose_extra=dict(head=-6)) + strap_svg("c12", "chest") + helmet_svg("h12")
ep.scene("s12", s, e, svg, origin="50% 51%", custom_cam=True, fx=[(s, e, "lightning", dict(bolts=[[540, 900, 560, 120], [500, 920, 300, 700], [580, 920, 780, 700]], plasma=[[540, 900, 140]], amp=0.35))])
ep.js(f'tl.fromTo("#s12-cam",{{scale:2.6}},{{scale:2.8,duration:{W(87) - 0.06 - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
ep.js(f'tl.set("#s12-cam",{{scale:3.4}},{W(87) - 0.05:.3f});')
ep.js(f'tl.to("#s12-cam",{{scale:3.55,duration:{e - W(87):.3f},ease:"none"}},{W(87):.3f});')
ep.js(f'gsap.set("#m12-mouth",{{attr:{{ry:3,rx:20}}}});')
convulse("m12", s, e, 5, 12)
ep.cue("sizzle.wav", s, 0.8)
ep.cue("sizzle.wav", s + 2.4, 0.8)
ep.cue("impact-bass-2.mp3", W(87) - 0.05, 0.5)
ep.floor(s, 0.8, 0.5)

# ---------------------------------------------------------------- S13 body arches, straps cut into skin
s, e = cut(94), cut(105)
svg = (stage() + chair("c13") + seated("m13", pose_extra=dict(head=-22, uarmL=50, farmL=-100, uarmR=-50, farmR=100))
       + strap_svg("c13", "arms") + strap_svg("c13", "legs") + f'<g id="s13-chest">{strap_svg("c13", "chest")}</g>' + f'<g id="s13-hot" opacity="0">{strap_svg("c13h", "arms", True)}{strap_svg("c13h", "chest", True)}{strap_svg("c13h", "legs", True)}</g>' + helmet_svg("h13"))
ep.scene("s13", s, e, svg, origin="50% 60%", fx=[(s, e, "lightning", bolts_at())])
ep.js(f'tl.fromTo("#m13",{{scaleY:1}},{{scaleY:1.06,svgOrigin:"540 1265",duration:0.4,ease:"power2.out",immediateRender:false}},{W(96) - 0.1:.3f});')
convulse("m13", s, e, 8, 13, head=False)
ep.show("#s13-hot", W(101) - 0.05, 0.3)
ep.cue("sizzle.wav", s, 1.0)
ep.cue("sizzle.wav", s + 2.4, 0.9)
ep.cue("impact-bass-1.mp3", W(101) - 0.05, 0.5)
ep.floor(s, 0.9, 0.5)

# ---------------------------------------------------------------- S14 17 seconds
s, e = cut(105), cut(107)
ep.timer("s14", s, e, s + 0.05, WE(106), 0, 17, "ms", "SECONDS", 17 / 60, ring_color="#5A78FF")
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S15 power off, doctor, declares you dead
s, e = cut(107), cut(119)
doc = mascot("doc", 1320, 1560, 0.82, hat=True, pose=dict(uarmL=-15, uarmR=15))
svg = stage() + chair("c15") + seated("m15", pose_extra=dict(head=26, uarmL=20, farmL=-20, uarmR=-20, farmR=20)) + strap_svg("c15", "arms") + strap_svg("c15", "legs") + strap_svg("c15", "chest") + helmet_svg("h15") + doc
html = '<div class="num" id="s15-dead" style="top:700px;font-size:220px;transform:rotate(-12deg);">DEAD</div>'
ep.scene("s15", s, e, svg, html, origin="50% 55%", drift=0.012, fx=[(s, e, "smoke", dict(n=8, cx=540, base=900, w=60, h=500, r0=20, r1=90, life=3, alpha=0.3))])
ep.cue("sizzle.wav", s - 0.05, 0.3)
tw = W(112) - 0.1
ep.js(f'tl.fromTo("#doc",{{x:0}},{{x:-440,duration:{W(115) - tw:.3f},ease:"power1.out",immediateRender:false}},{tw:.3f});')
n = int((W(115) - tw) / 0.2)
for k in range(n):
    a = 22 if k % 2 == 0 else -22
    ep.rot("#doc-thighL", tw + k * 0.2, 0.2, a, "sine.inOut")
    ep.rot("#doc-thighR", tw + k * 0.2, 0.2, -a, "sine.inOut")
ep.rot("#doc-thighL", tw + n * 0.2, 0.15, 0)
ep.rot("#doc-thighR", tw + n * 0.2, 0.15, 0)
tsd = W(118) - 0.05
ep.js(f'tl.fromTo("#s15-dead",{{opacity:1,scale:2.5}},{{scale:1,duration:0.14,ease:"power2.in",immediateRender:false}},{tsd:.3f});')
ep.js(f'tl.set("#s15-dead",{{opacity:0}},0);')
ep.shake("#s15-shake", tsd + 0.14, 0.25, 8)
ep.cue("impact-bass-2.mp3", tsd + 0.14, 0.8)
ep.floor(s, 0.6, 0.0)

# ---------------------------------------------------------------- S16 but you're still breathing (x-ray lungs)
s, e = cut(119), cut(123)
ep.lungs("s16", s, e, label_txt="STILL BREATHING")
n = int((e - s) / 0.8)
for k in range(n):
    ep.js(f'tl.to("#s16-lungs",{{scale:{1.07 if k % 2 == 0 else 1.0},transformOrigin:"50% 40%",duration:0.8,ease:"sine.inOut"}},{s + k * 0.8:.3f});')
ep.cue("whoosh-short.mp3", W(122), 0.35)

# ---------------------------------------------------------------- S17 witnesses scream, someone faints
s, e = cut(123), cut(127)
wit = "".join(mascot(f"w{k}", 140 + k * 200, 1560, 0.62, mouth_open=True, pose=dict(uarmL=-150 if k % 2 else 20, farmL=-20, uarmR=150 if k % 2 == 0 else -20, farmR=20)) for k in range(5))
rail = glow(N("M 40 1320 L 1040 1320 L 1040 1345 L 40 1345 Z", fill=WOOD, sw=10, cw=4)) + "".join(glow(N(f"M {x} 1345 L {x + 22} 1345 L {x + 22} 1560 L {x} 1560 Z", fill=WOOD, sw=8, cw=3)) for x in range(70, 1040, 160))
marks = "".join(f'<text class="s17-x" x="{140 + k * 200}" y="{800 + (k % 2) * 40}" fill="#FF3B36" font-family="Roboto Condensed" font-weight="900" font-size="90" text-anchor="middle" opacity="0">!</text>' for k in range(5))
svg = wit + rail + marks
ep.scene("s17", s, e, svg, origin="50% 60%", drift=0.02)
ep.js(f'tl.fromTo(".s17-x",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.15,stagger:0.07,ease:"back.out(2)",immediateRender:false}},{W(124) - 0.1:.3f});')
ep.js(f'tl.to("#w3",{{rotation:80,svgOrigin:"740 1560",duration:0.45,ease:"power2.in"}},{W(126) - 0.1:.3f});')
ep.cue("impact-bass-2.mp3", W(126) + 0.35, 0.5)
ep.floor(s, 0.6, 0.0)

# ---------------------------------------------------------------- S18 the generator needs time to charge
s, e = cut(127), cut(135)
spokes = "".join(line(0, 0, 200 * math.cos(a), 200 * math.sin(a), CORE, 6) for a in [i * math.pi / 4 for i in range(8)])
wheel = f'<g transform="translate(380,960)"><g id="s18-wheel" transform="rotate(0)">' + glow(f'<circle r="210" fill="#0C0A0C" stroke="#FB2945" stroke-width="16"/><circle r="210" fill="none" stroke="#F2EEEA" stroke-width="5"/>{spokes}<circle r="34" fill="#F2EEEA"/>') + '</g></g>'
coils = glow("".join(f'<rect x="{660 + k * 110}" y="820" width="80" height="280" rx="20" fill="#7a3a14" stroke="#E8904A" stroke-width="8"/>' + "".join(line(660 + k * 110, 850 + j * 30, 740 + k * 110, 850 + j * 30, "#FFB070", 4) for j in range(8)) for k in range(2)), f="glowO")
bar = (f'<rect x="200" y="1260" width="680" height="60" rx="30" fill="#0b1430" stroke="#5A78FF" stroke-width="6"/>'
       f'<rect id="s18-bar" x="208" y="1268" width="664" height="44" rx="22" fill="#5A78FF" filter="url(#glowB)"/>')
svg = wheel + coils + bar + label(540, 1380, "CHARGE", 30, "#9FC8FF")
html = '<div class="num" id="s18-pct" style="top:1420px;font-size:120px;color:#9FC8FF;text-shadow:0 0 18px rgba(90,120,255,.9);">0%</div>'
ep.scene("s18", s, e, svg, html, origin="50% 55%")
ep.js(f'tl.fromTo("#s18-wheel",{{attr:{{transform:"rotate(0)"}}}},{{attr:{{transform:"rotate(1440)"}},duration:{e - s:.3f},ease:"power1.in",immediateRender:false}},{s:.3f});')
ep.js(f'tl.fromTo("#s18-bar",{{scaleX:0.02,transformOrigin:"0% 50%"}},{{scaleX:0.62,duration:{e - s - 0.2:.3f},ease:"none",immediateRender:false}},{s + 0.1:.3f});')
ep.js(f'gsap.set("#s18-bar",{{scaleX:0.02,transformOrigin:"0% 50%"}});')
ep.counter("#s18-pct", s + 0.1, e - s - 0.2, 2, 62, "pct", "none")
ep.cue("riser.mp3", s, 0.35)
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S19 so you sit there... and wait (clock)
s, e = cut(135), cut(145)
ticks = "".join(line(860 + 110 * math.cos(a), 640 + 110 * math.sin(a), 860 + 128 * math.cos(a), 640 + 128 * math.sin(a), CORE, 4) for a in [i * math.pi / 6 for i in range(12)])
clock = glow(f'<circle cx="860" cy="640" r="140" fill="#0C0A0C" stroke="#FB2945" stroke-width="12"/>{ticks}' + line(860, 640, 860, 560, CORE, 8)
             + f'<g transform="translate(860,640)"><g id="s19-sec" transform="rotate(0)">' + line(0, 0, 0, -118, "#FF3B36", 4) + '</g></g>')
svg = stage() + chair("c19") + seated("m19", pose_extra=dict(head=16, uarmL=20, farmL=-20, uarmR=-20, farmR=20)) + strap_svg("c19", "arms") + strap_svg("c19", "legs") + strap_svg("c19", "chest") + helmet_svg("h19") + clock
ep.scene("s19", s, e, svg, origin="50% 55%", drift=0.02, fx=[(s, e, "smoke", dict(n=6, cx=540, base=900, w=60, h=500, r0=20, r1=80, life=3.5, alpha=0.22))])
for k in range(int(e - s) + 1):
    ep.js(f'tl.set("#s19-sec",{{attr:{{transform:"rotate({(k + 1) * 6})"}}}},{s + k:.3f});')
    ep.cue("tick.wav", s + k, 0.45)
ep.floor(s, 0.35, 0.0)
ep.js(f'tl.to("#s19 .ec-spot",{{opacity:0.45,duration:1.0}},{s:.3f});')

# ---------------------------------------------------------------- S20 the second shock: 2,000 volts
s, e = cut(145), cut(150)
voltmeter("s20", s, e, W(148) - 0.05, 2000, pegged=True)
ep.floor(W(148), 0.4, 0.9, 0.1)

# ---------------------------------------------------------------- S21 smoke rises from your head
s, e = cut(150), cut(155)
svg = stage() + chair("c21") + seated("m21", pose_extra=dict(head=-20, uarmL=50, farmL=-100, uarmR=-50, farmR=100)) + strap_svg("c21", "arms", True) + strap_svg("c21", "chest", True) + helmet_svg("h21")
ep.scene("s21", s, e, svg, origin="50% 50%", custom_cam=True, fx=[(s, e, "lightning", dict(bolts_at(), amp=0.45, branch=0.45)),
                                                                 (W(150), e, "smoke", dict(n=14, cx=540, base=880, w=90, h=700, r0=30, r1=160, life=2.5, alpha=0.45))])
ep.js(f'tl.fromTo("#s21-cam",{{scale:1.5}},{{scale:1.7,duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
convulse("m21", s, e, 14, 21)
ep.cue("sizzle.wav", s, 1.0)
ep.cue("sizzle.wav", s + 2.4, 1.0)
ep.cue("sub.wav", s, 1.0)
ep.floor(s, 0.9, 0.9, 0.05)

# ---------------------------------------------------------------- S22 the room fills with the smell (extreme wide)
s, e = cut(155), cut(164)
room = (stage() + f'<g transform="translate(540,1300) scale(0.55) translate(-540,-1300)">{chair("c22")}{seated("m22", pose_extra=dict(head=-20))}{helmet_svg("h22")}</g>'
        + "".join(mascot(f"x{k}", x, 1700, 0.45, pose=dict(uarmL=-150 if k == 1 else 10, farmL=-30)) for k, x in enumerate([120, 260, 820, 960])))
ep.scene("s22", s, e, room, origin="50% 55%", drift=0.015, fx=[(s, e, "smoke", dict(n=22, cx=540, base=1150, w=300, h=900, r0=60, r1=320, life=4, alpha=0.4, drift=0)),
                                                                (s, e, "lightning", dict(bolts=[[540, 1110, 560, 600]], plasma=[[540, 1110, 70]], amp=0.35, flick=0.3))])
ep.floor(s, 0.6, 0.3)

# ---------------------------------------------------------------- S23 over a minute
s, e = cut(164), cut(173)
ep.timer("s23", s, e, s + 0.1, WE(172) + 0.3, 17, 72, "ms", "SECONDS OF CURRENT", 72 / 90, ring_color="#5A78FF")
ep.floor(s, 0.5, 0.0)

# ---------------------------------------------------------------- S24 your heart twitches... and stops
s, e = cut(173), cut(178)
HEART = "M 540 1060 C 400 960 330 880 360 790 C 390 700 500 700 540 790 C 580 700 690 700 720 790 C 750 880 680 960 540 1060 Z"
svg = glow(N(HEART, fill="#2a0a0c"), gid="s24-heart")
ep.scene("s24", s, e, svg, origin="50% 50%", fx=[(s, e, "ecg", dict(x0=60, x1=1020, y=1300, amp=260, flat_at=W(177) - 0.1, flat_dur=0.7))])
r24 = random.Random(24)
tst = W(177) - 0.1
for k in range(int((tst - s) * 10)):
    ep.js(f'tl.set("#s24-heart",{{scale:{r24.uniform(0.94, 1.08):.2f},x:{r24.uniform(-6, 6):.0f},svgOrigin:"540 900"}},{s + k * 0.1:.3f});')
ep.js(f'tl.set("#s24-heart",{{scale:1,x:0,svgOrigin:"540 900"}},{tst:.3f});')
ep.js(f'tl.to("#s24-heart",{{opacity:0.25,duration:0.8}},{tst:.3f});')
for k in range(int((tst - s) / 0.25)):
    ep.cue("tick.wav", s + k * 0.25 + r24.uniform(0, 0.1), 0.4)
ep.floor(s, 0.4, 0.0)

# ---------------------------------------------------------------- ending
ep.ending(cut(178), 181)
ep.write(red=["chair", "kemmler", "switch", "scream", "dead", "breathing", "smoke", "heart", "electricity"])
