"""Shared builder for 'How does it feel?' episodes (house style: ../STYLE.md).

An episode's build.py does:
    from lib import *
    ep = Episode(__file__)
    ... ep.scene(...), ep.js(...), ep.cue(...)
    ep.write()
"""
import json, math, os, random, re, shutil

KIT = os.path.dirname(os.path.abspath(__file__))
F = 1 / 30
DARK, RED, CORE, GREY = "#0C0A0C", "#FB2945", "#F2EEEA", "#BDB5B5"


# ------------------------------------------------------------------ svg helpers
def N(d, fill=DARK, red=RED, core=CORE, sw=16, cw=5, extra="", cls=""):
    """Neon shape: red band + white core over a dark fill. Horizontal single lines get a bbox pad (SVG filters drop 0-height bboxes)."""
    m = re.fullmatch(r"M (-?\d+) (-?\d+) L (-?\d+) (-?\d+)", d.strip())
    pad = ""
    if m and m.group(2) == m.group(4):
        x0, x1, y = int(m.group(1)), int(m.group(3)), int(m.group(2))
        pad = f'<rect x="{min(x0, x1)}" y="{y - 60}" width="{abs(x1 - x0)}" height="120" fill="none"/>'
    c = f' class="{cls}"' if cls else ""
    return (pad + f'<path{c} d="{d}" fill="{fill}" stroke="{red}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'
            f'<path d="{d}" fill="none" stroke="{core}" stroke-width="{cw}" stroke-linejoin="round" stroke-linecap="round"/>')


def glow(inner, f="glow", gid="", extra=""):
    i = f' id="{gid}"' if gid else ""
    return f'<g{i} filter="url(#{f})" {extra}>{inner}</g>'


def line(x1, y1, x2, y2, c=CORE, w=4, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def label(x, y, t, size=30, c=GREY, anchor="middle", extra=""):
    size = round(size * 1.25)  # phone-readable floor (QC: labels at 28-30 px were too small)
    return (f'<text x="{x}" y="{y}" fill="{c}" font-family="Roboto Condensed" font-weight="700" font-size="{size}" '
            f'letter-spacing="3" text-anchor="{anchor}" {extra}>{t}</text>')


def hline(y, x0=-40, x1=1120, sw=12, cw=4, gid=""):
    return glow(N(f"M {x0} {y} L {x1} {y}", sw=sw, cw=cw), gid=gid)


def puffs(cx, base, top, seed, w0=60, w1=200, umbrella=True, fill="#5c160c", hi="#86280f", cls="pf", idp=""):
    rnd = random.Random(seed)
    out = []
    n = max(6, int((base - top) / 34))
    for k in range(n):
        f = k / (n - 1)
        y = base - f * (base - top)
        r = w0 + (w1 - w0) * f ** 1.4 * 0.5
        out.append((cx + rnd.uniform(-0.25, 0.25) * r, y, r))
    if umbrella:
        for k in range(9):
            out.append((cx + (k - 4) * w1 * 0.42 + rnd.uniform(-20, 20), top + rnd.uniform(-30, 40) + abs(k - 4) * 14, w1 * rnd.uniform(0.45, 0.62)))
    body = "".join(f'<circle class="{cls}"{f" id={chr(34)}{idp}{i}{chr(34)}" if idp else ""} cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{fill}"/>' for i, (x, y, r) in enumerate(out))
    hil = "".join(f'<circle cx="{x - r * 0.22:.0f}" cy="{y - r * 0.25:.0f}" r="{r * 0.55:.0f}" fill="{hi}" opacity="0.75"/>' for x, y, r in out[::2])
    lines = "".join(f'<path d="M{x - r * 0.5:.0f},{y + r * 0.1:.0f} Q{x:.0f},{y - r * 0.45:.0f} {x + r * 0.5:.0f},{y + r * 0.05:.0f}" fill="none" stroke="#F3D9C8" stroke-width="3" opacity="0.55"/>' for x, y, r in out[1::3])
    return body + hil + lines


# ------------------------------------------------------------------ mascot ("you")
def mascot(mid, x, y, s=1.0, pose=None, style="neon", crown=False, mouth_open=False, hat=False):
    """X-ray 'you'. Joints are rigged so their group's rotate() is about the joint: tween with attr transform.
    style: neon | stone | xray (red translucent, for inside objects) | dim (grey, dead)"""
    pose = pose or {}
    pal = dict(neon=(RED, DARK, CORE, "#2A2426", "glow"), stone=("#8a837e", "#6f6862", "#d8d2cc", "#7a736d", "glowStone"),
               xray=("#FF3B36", "rgba(120,10,14,0.55)", "#FFB3B0", "rgba(120,10,14,0.6)", "glow"),
               dim=("#555", "#151314", "#8a837e", "#1d1a1b", "none"),
               shadow=("#231E1B", "#231E1B", "#231E1B", "#231E1B", "none"))[style]
    rim, body, bone, head, f = pal

    def lm(length, w=40):
        return (line(0, 0, 0, length, rim, w + 12) + line(0, 0, 0, length, body, w) +
                line(0, 14, 0, length - 14, bone, 6) + f'<circle cx="0" cy="{length}" r="9" fill="none" stroke="{bone}" stroke-width="4"/>')

    def rot(name):
        a = pose.get(name, 0)
        return f'id="{mid}-{name}" transform="{a if isinstance(a, str) else f"rotate({a})"}"'

    def leg(side):
        sx = -36 if side == "L" else 36
        return (f'<g transform="translate({sx},-262)"><g {rot("thigh" + side)}>{lm(128, 44)}'
                f'<g transform="translate(0,128)"><g {rot("shin" + side)}>{lm(132, 38)}'
                f'<ellipse cx="{-10 if side == "L" else 10}" cy="138" rx="30" ry="14" fill="{body}" stroke="{rim}" stroke-width="6"/></g></g></g></g>')

    def arm(side):
        sx = -84 if side == "L" else 84
        return (f'<g transform="translate({sx},-458)"><g {rot("uarm" + side)}>{lm(118, 34)}'
                f'<g transform="translate(0,118)"><g {rot("farm" + side)}>{lm(112, 30)}'
                f'<circle cx="0" cy="122" r="25" fill="{body}" stroke="{rim}" stroke-width="7"/></g></g></g></g>')

    torso = "M -82 -478 Q -92 -400 -64 -330 L -60 -262 Q 0 -238 60 -262 L 64 -330 Q 92 -400 82 -478 Q 0 -504 -82 -478 Z"
    ribs = "".join(f'<path d="M -54 {-446 + k * 28} Q 0 {-428 + k * 28} 54 {-446 + k * 28}" fill="none" stroke="{bone}" stroke-width="5" stroke-linecap="round"/>' for k in range(4))
    spine = "".join(f'<circle cx="0" cy="{-468 + k * 19}" r="5" fill="{bone}"/>' for k in range(11))
    pelvis = f'<circle cx="-22" cy="-276" r="20" fill="none" stroke="{bone}" stroke-width="5"/><circle cx="22" cy="-276" r="20" fill="none" stroke="{bone}" stroke-width="5"/>'
    eyes = ""
    if style in ("neon", "xray"):
        eyes = (f'<g id="{mid}-eyes"><ellipse cx="-20" cy="-566" rx="11" ry="9" fill="#FF3B36"/><ellipse cx="20" cy="-566" rx="11" ry="9" fill="#FF3B36"/></g>'
                f'<path d="M -36 -588 L -8 -580 M 36 -588 L 8 -580" stroke="#FF3B36" stroke-width="6" stroke-linecap="round"/>')
    mo = 26 if mouth_open else 10
    mouth = f'<ellipse id="{mid}-mouth" cx="0" cy="-524" rx="{18 if mouth_open else 14}" ry="{mo}" fill="#0a0505" stroke="{bone}" stroke-width="3"/>'
    cracks = ('<path d="M -40 -440 L -20 -400 L -34 -360 M 30 -470 L 44 -430 L 28 -380 M -10 -590 L 6 -560 L -4 -540" stroke="#3a3532" stroke-width="4" fill="none" stroke-linecap="round"/>'
              if style == "stone" else "")
    crown_svg = ('<path d="M -50 -618 L -50 -660 L -26 -638 L 0 -676 L 26 -638 L 50 -660 L 50 -618 Z" fill="#E8B040" stroke="#FFE08A" stroke-width="5" stroke-linejoin="round"/>'
                 if crown else "")
    if hat:
        crown_svg += ('<path d="M -70 -616 L 70 -616 M -44 -616 L -44 -700 L 44 -700 L 44 -616" fill="#0C0A0C" stroke="#F2EEEA" stroke-width="7" stroke-linejoin="round"/>')
    headg = (f'<g id="{mid}-head" transform="rotate({pose.get("head", 0)},0,-492)"><ellipse cx="0" cy="-556" rx="58" ry="72" fill="{head}" stroke="{rim}" stroke-width="10"/>'
             f'<ellipse cx="0" cy="-556" rx="58" ry="72" fill="none" stroke="{bone}" stroke-width="3" opacity="0.7"/>{eyes}{mouth}{crown_svg}</g>')
    inner = (leg("L") + leg("R") + arm("L") +
             f'<path d="{torso}" fill="{body}" stroke="{rim}" stroke-width="12" stroke-linejoin="round"/>{ribs}{spine}{pelvis}' +
             headg + arm("R") + cracks)
    filt = f' filter="url(#{f})"' if f != "none" else ""
    return f'<g id="{mid}"><g transform="translate({x},{y}) scale({s})"><g{filt}>{inner}</g></g></g>'


# ------------------------------------------------------------------ Episode
class Episode:
    def __init__(self, build_file, off=0.12):
        self.dir = os.path.dirname(os.path.abspath(build_file))
        self.words = json.load(open(f"{self.dir}/audio/words.json"))
        self.off = off
        self.J, self.scenes, self.fx, self.cues = [], [], [], []
        self.shake_rnd = random.Random(77)
        self.end = None

    # timing
    def W(self, i):
        return round(self.words[i]["s"] + self.off, 3)

    def WE(self, i):
        return round(self.words[i]["e"] + self.off, 3)

    def cut(self, i):
        return round(max(0.0, self.W(i) - 2 * F), 3)

    def find(self, token, n=1):
        """index of the n-th word whose text (lowercased, stripped of punctuation) equals token."""
        k = 0
        for i, w in enumerate(self.words):
            if re.sub(r"[^\w'’,-]", "", w["w"].lower()).strip(",") == token.lower():
                k += 1
                if k == n:
                    return i
        raise KeyError(token)

    # timeline helpers
    def js(self, s):
        self.J.append(s)

    def cue(self, f, t, v=1.0):
        self.cues.append([f, round(max(0.0, t), 3), v])

    def scene(self, sid, start, end, svg, html="", origin="50% 55%", land=True, drift=0.015, custom_cam=False, fx=None, whoosh=True):
        self.scenes.append(dict(id=sid, start=round(start, 3), end=round(end, 3), svg=svg, html=html, fx=bool(fx)))
        d = end - start
        cam = f"#{sid}-cam"
        self.js(f'gsap.set("{cam}",{{transformOrigin:"{origin}"}});')
        if not custom_cam:
            if land:
                self.js(f'tl.fromTo("{cam}",{{scale:0.9}},{{scale:1,duration:{5 * F:.3f},ease:"power2.out",immediateRender:false}},{start:.3f});')
                self.js(f'tl.to("{cam}",{{scale:{1 + drift * d:.4f},duration:{max(0.05, d - 5 * F):.3f},ease:"none"}},{start + 5 * F:.3f});')
            else:
                self.js(f'tl.fromTo("{cam}",{{scale:1}},{{scale:{1 + drift * d:.4f},duration:{d:.3f},ease:"none",immediateRender:false}},{start:.3f});')
        for sysd in fx or []:
            t0, t1, typ, p = sysd
            self.fx.append([max(start, t0), min(end, t1), typ, p, f"{sid}-fx"])
        if whoosh and start > 0.5:
            self.cue("whoosh-short.mp3" if len(self.scenes) % 2 else "sfx_whoosh.mp3", start - 0.08, 0.3)

    def overlay_fx(self, t0, t1, typ, p):
        self.fx.append([t0, t1, typ, p, "fx"])

    def floor(self, t, normal, hot, dur=0.25):
        self.js(f'tl.to("#floorN",{{opacity:{normal},duration:{dur},ease:"power1.out"}},{t:.3f});')
        self.js(f'tl.to("#floorH",{{opacity:{hot},duration:{dur},ease:"power1.out"}},{t:.3f});')

    def flash(self, t, peak=0.9, dur=0.6, color=None):
        self.js(f'tl.fromTo("#flashL",{{opacity:{peak}}},{{opacity:0,duration:{dur},ease:"expo.out",immediateRender:false}},{t:.3f});')

    def shake(self, target, t, dur, amp):
        n = int(dur * 30)
        for k in range(n):
            a = amp * (1 - k / n)
            self.js(f'tl.set("{target}",{{x:{self.shake_rnd.uniform(-a, a):.1f},y:{self.shake_rnd.uniform(-a, a):.1f}}},{t + k * F:.3f});')
        self.js(f'tl.set("{target}",{{x:0,y:0}},{t + n * F:.3f});')

    def pop(self, sel, t, dur=0.18, frm=0.0, ease="back.out(2)", origin="50% 50%"):
        self.js(f'tl.fromTo("{sel}",{{scale:{frm},opacity:0,transformOrigin:"{origin}"}},{{scale:1,opacity:1,duration:{dur},ease:"{ease}",immediateRender:false}},{t:.3f});')
        self.js(f'tl.set("{sel}",{{opacity:0}},0);')

    def show(self, sel, t, dur=0.0):
        self.js(f'tl.set("{sel}",{{opacity:0}},0);')
        if dur:
            self.js(f'tl.to("{sel}",{{opacity:1,duration:{dur}}},{t:.3f});')
        else:
            self.js(f'tl.set("{sel}",{{opacity:1}},{t:.3f});')

    def counter(self, sel, t, dur, a, b, fmt="n", ease="expo.out"):
        self.js(f'(function(){{var o={{v:{a}}};var el=document.querySelector("{sel}");'
                f'tl.to(o,{{v:{b},duration:{dur:.3f},ease:"{ease}",onUpdate:function(){{el.textContent=fmtNum(o.v,"{fmt}");}}}},{t:.3f});}})();')

    def rot(self, sel, t, dur, a, ease="power2.inOut", about=""):
        tr = f"rotate({a}{',' + about if about else ''})"
        self.js(f'tl.to("{sel}",{{attr:{{transform:"{tr}"}},duration:{dur:.3f},ease:"{ease}"}},{t:.3f});')

    def flicker(self, sel, t0, t1, lo=0.82, hi=1.15, seed=1, origin="50% 100%"):
        r = random.Random(seed)
        for k in range(int((t1 - t0) * 15)):
            self.js(f'tl.set("{sel}",{{scaleY:{r.uniform(lo, hi):.2f},scaleX:{r.uniform(0.9, 1.08):.2f},transformOrigin:"{origin}"}},{t0 + k * 2 * F:.3f});')

    # ------------------------------------------------------------ reusable beats
    def ending(self, start, i_dark, sid="end"):
        """Eye → closes on 'darkness' → red flatline → fade. Returns film end time."""
        T_END = self.WE(i_dark) + 1.9
        EYE = "M 160 1000 Q 540 690 920 1000 Q 540 1310 160 1000 Z"
        ir = "".join(line(540 + 70 * math.cos(a), 1000 + 70 * math.sin(a), 540 + 145 * math.cos(a), 1000 + 145 * math.sin(a), "#8a0f12", 4) for a in [i * math.pi / 12 for i in range(24)])
        lashes = ""
        for i in range(2, 12):
            tt = i / 13
            x0 = 160 + 760 * tt
            y0 = 1000 - 4 * 155 * tt * (1 - tt) * 2
            lashes += line(x0, y0, x0 + (tt - 0.5) * 40, y0 - 46, CORE, 6)
        veins = '<path d="M 200 1000 Q 240 985 262 1005 Q 280 990 300 1000 M 880 1000 Q 840 1012 822 994 Q 800 1008 780 998" fill="none" stroke="#C2181E" stroke-width="4"/>'
        svg = (f'<defs><clipPath id="{sid}-clip"><path d="{EYE}"/></clipPath></defs>'
               f'<g id="{sid}-eye"><g filter="url(#glow)"><path d="{EYE}" fill="#ECE6E5" stroke="{RED}" stroke-width="22"/></g>'
               f'<g clip-path="url(#{sid}-clip)">{veins}<g id="{sid}-iris"><circle cx="540" cy="1000" r="150" fill="#D32620"/>{ir}'
               f'<circle cx="540" cy="1000" r="64" fill="#160404"/><circle cx="582" cy="958" r="18" fill="#FFFFFF"/></g></g>'
               f'<path d="{EYE}" fill="none" stroke="{CORE}" stroke-width="6"/>{lashes}</g>'
               f'<g id="{sid}-line" opacity="0"><g filter="url(#glow)"><rect x="0" y="940" width="1080" height="120" fill="none"/>'
               + line(0, 1000, 1080, 1000, RED, 16) + line(0, 1000, 1080, 1000, CORE, 5) + '</g></g>')
        self.scene(sid, start, T_END, svg, origin="50% 52%", drift=0.012)
        a, b = self.W(i_dark - 3) if i_dark >= 3 else start, self.W(i_dark - 1)
        self.js(f'tl.to("#{sid}-iris",{{x:-26,duration:0.12,ease:"power2.out"}},{a + 0.1:.3f});')
        self.js(f'tl.to("#{sid}-iris",{{x:14,duration:0.14,ease:"power2.out"}},{a + 0.6:.3f});')
        tcl = self.W(i_dark) + 0.01
        self.js(f'tl.to("#{sid}-eye",{{scaleY:0.8,svgOrigin:"540 1000",duration:{max(0.2, tcl - b):.3f},ease:"sine.inOut"}},{b:.3f});')
        self.js(f'tl.to("#{sid}-eye",{{scaleY:0.02,svgOrigin:"540 1000",duration:0.4,ease:"power2.in"}},{tcl:.3f});')
        self.js(f'tl.set("#{sid}-eye",{{opacity:0}},{tcl + 0.4:.3f});')
        self.js(f'tl.fromTo("#{sid}-line",{{opacity:1,scaleX:0.35,svgOrigin:"540 1000"}},{{scaleX:1,duration:{2 * F:.3f},ease:"none",immediateRender:false}},{tcl + 0.4:.3f});')
        tfade = T_END - 0.75
        self.js(f'tl.to("#{sid}-line",{{opacity:0,duration:0.4,ease:"none"}},{tfade:.3f});')
        self.js(f'tl.to("#caps",{{opacity:0,duration:0.4,ease:"none"}},{tfade:.3f});')
        self.floor(start, 0.45, 0.0)
        self.floor(b, 0.3, 0.0, max(0.1, min(0.8, tcl + 0.35 - b)))
        self.floor(tcl + 0.4, 0.0, 0.0, 0.05)
        t = start
        gap = 0.95
        while t < tcl - 0.3:
            self.cue("heart.wav", t, 0.7)
            t += gap
            gap *= 1.12
        self.cue("beep.wav", tcl + 0.4, 0.22)
        self.end = T_END
        return T_END

    def timer(self, sid, start, end, t0, t1, a, b, fmt="ms", label_txt="SECONDS", frac=1.0, ring_color="#FB2945", tick=True):
        C = 2 * math.pi * 330
        svg = (f'<circle cx="540" cy="960" r="330" fill="none" stroke="#2a0a0c" stroke-width="18"/>'
               f'<g filter="url(#glow)"><circle id="{sid}-ring" cx="540" cy="960" r="330" fill="none" stroke="{ring_color}" stroke-width="16" '
               f'stroke-dasharray="{C:.0f}" stroke-dashoffset="{C:.0f}" transform="rotate(-90 540 960)" stroke-linecap="round"/></g>')
        html = (f'<div class="num" id="{sid}-num" style="top:840px;font-size:220px;">{fmtpy(a, fmt)}</div>'
                f'<div class="lbl" id="{sid}-lbl" style="top:1085px;">{label_txt}</div>')
        self.scene(sid, start, end, svg, html, origin="50% 50%")
        self.js(f'tl.to("#{sid}-ring",{{strokeDashoffset:{C * (1 - frac):.0f},duration:{t1 - t0:.3f},ease:"power2.out"}},{t0:.3f});')
        self.counter(f"#{sid}-num", t0, t1 - t0, a, b, fmt, "power2.out")
        if tick:
            t = t0
            while t < t1:
                self.cue("tick.wav", t, 0.45)
                t += 0.08 + (t - t0) * 0.05

    def thermometer(self, sid, start, end, t0, t1, a, b, top=400, label_txt="CELSIUS", hot_floor=True):
        ty = lambda c: 1380 - c / top * 720
        tt = ""
        step = 50 if top <= 400 else 100
        for c in range(0, top + 1, step):
            tt += line(250, ty(c), 285, ty(c), CORE, 5) + label(236, ty(c) + 10, f"{c}°", 28, GREY, "end")
        waves = ""
        for k in range(5):
            y = 560 + k * 230
            d = "M -300 %d " % y + " ".join(f"Q {-300 + i * 120 + 60} {y - 26 if i % 2 == 0 else y + 26} {-300 + (i + 1) * 120} {y}" for i in range(16))
            waves += f'<path class="{sid}-w" d="{d}" fill="none" stroke="#FF3B36" stroke-width="5" opacity="{0.25 + 0.08 * k:.2f}" filter="url(#glowS)"/>'
        svg = (f'<g>{waves}</g>'
               + glow(N("M 300 660 L 300 1380 A 50 50 0 0 0 400 1380 L 400 660 A 50 50 0 0 0 300 660 Z") + f'<circle cx="350" cy="1450" r="90" fill="{DARK}" stroke="{RED}" stroke-width="16"/><circle cx="350" cy="1450" r="90" fill="none" stroke="{CORE}" stroke-width="5"/>' + tt)
               + f'<circle cx="350" cy="1450" r="64" fill="#FA2335" filter="url(#glow)"/>'
               + f'<rect id="{sid}-merc" x="326" y="{ty(b):.0f}" width="48" height="{1450 - ty(b):.0f}" rx="24" fill="#FA2335" filter="url(#glow)"/>')
        html = (f'<div class="num" id="{sid}-num" style="top:760px;left:440px;width:640px;font-size:210px;">{a}°</div>'
                f'<div class="lbl" id="{sid}-lbl" style="top:990px;left:440px;width:640px;">{label_txt}</div>')
        self.scene(sid, start, end, svg, html, origin="50% 55%")
        self.js(f'tl.fromTo("#{sid}-merc",{{scaleY:{max(0.05, a / b):.3f},transformOrigin:"50% 100%"}},{{scaleY:1,duration:{t1 - t0:.3f},ease:"expo.out",immediateRender:false}},{t0:.3f});')
        self.js(f'gsap.set("#{sid}-merc",{{scaleY:{max(0.05, a / b):.3f},transformOrigin:"50% 100%"}});')
        self.counter(f"#{sid}-num", t0, t1 - t0, a, b, "deg")
        self.js(f'tl.fromTo(".{sid}-w",{{x:0}},{{x:-240,duration:{end - start:.3f},ease:"none"}},{start:.3f});')
        self.cue("riser.mp3", t0 - 0.3, 0.35)
        self.cue("sizzle.wav", t0 + 0.2, 0.3)
        if hot_floor:
            self.floor(start, 0.4, 0.7)
            self.floor(t0, 0.3, 1.0, t1 - t0)

    def lungs(self, sid, start, end, t_breath=None, t_flood=None, t_burn=None, t_burn_end=None, flood_color="#FF8A3A", smoke=False, label_txt="LUNGS"):
        LL = "M 515 790 C 430 770 310 900 296 1150 C 284 1360 336 1440 430 1420 C 505 1404 515 1320 515 1150 Z"
        RL = "M 565 790 C 650 770 770 900 784 1150 C 796 1360 744 1440 650 1420 C 575 1404 565 1320 565 1150 Z"
        br = ('<path d="M 540 760 Q 500 820 450 880 M 470 860 L 420 940 M 450 880 L 470 980 M 540 760 Q 580 820 630 880 M 610 860 L 660 940 M 630 880 L 610 980" '
              'fill="none" stroke="#F2EEEA" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
        pr = random.Random(hash(sid) % 1000)
        parts = "".join(f'<circle id="{sid}-p{k}" cx="540" cy="440" r="{pr.uniform(6, 12):.0f}" fill="{flood_color}" opacity="0" {"" if smoke else "filter=" + chr(34) + "url(#glowO)" + chr(34)}/>' for k in range(26))
        svg = (f'<g id="{sid}-lungs"><g filter="url(#glow)">'
               f'<path id="{sid}-LL" d="{LL}" fill="{DARK}" stroke="{RED}" stroke-width="16"/><path d="{LL}" fill="none" stroke="{CORE}" stroke-width="5" class="{sid}-core"/>'
               f'<path id="{sid}-RL" d="{RL}" fill="{DARK}" stroke="{RED}" stroke-width="16"/><path d="{RL}" fill="none" stroke="{CORE}" stroke-width="5" class="{sid}-core"/>'
               + line(540, 470, 540, 770, RED, 56) + line(540, 470, 540, 770, DARK, 40) + br + '</g></g>'
               + "".join(f'<circle id="{sid}-air{k}" cx="540" cy="440" r="9" fill="#FFFFFF" opacity="0"/>' for k in range(8))
               + parts + label(500, 650, label_txt, 32, GREY, "end"))
        self.scene(sid, start, end, svg, origin="50% 50%")
        if t_breath:
            for k in range(8):
                self.js(f'tl.fromTo("#{sid}-air{k}",{{attr:{{cy:440}},opacity:0.9}},{{attr:{{cy:780}},opacity:0,duration:0.45,ease:"power1.in",immediateRender:false}},{t_breath + k * 0.07:.3f});')
            self.js(f'tl.fromTo("#{sid}-lungs",{{scale:1,transformOrigin:"50% 40%"}},{{scale:1.08,duration:0.6,ease:"power2.out",immediateRender:false}},{t_breath + 0.15:.3f});')
        if t_flood:
            for k in range(26):
                side = -1 if k % 2 == 0 else 1
                tx_, ty_ = 540 + side * pr.uniform(70, 210), pr.uniform(900, 1380)
                self.js(f'tl.fromTo("#{sid}-p{k}",{{attr:{{cx:540,cy:440}},opacity:1}},{{keyframes:[{{attr:{{cy:770}},duration:0.25,ease:"none"}},{{attr:{{cx:{tx_:.0f},cy:{ty_:.0f}}},duration:0.4,ease:"power2.out"}}],immediateRender:false}},{t_flood + k * 0.035:.3f});')
        if t_burn:
            tgt = "#3a3532" if smoke else "#871712"
            self.js(f'tl.to("#{sid}-LL, #{sid}-RL",{{fill:"{tgt}",duration:{(t_burn_end or t_burn + 1) - t_burn:.3f},ease:"power1.in"}},{t_burn:.3f});')
            if not smoke:
                self.js(f'tl.to(".{sid}-core",{{stroke:"#FFB3B0",duration:0.6}},{t_burn:.3f});')
                self.cue("sizzle.wav", t_burn, 0.4)

    # ------------------------------------------------------------ captions
    def captions(self, red=(), hard_breaks=(), max_chars=16, max_words=3):
        red = {r.lower() for r in red}
        words = [w["w"] for w in self.words]
        chunks, cur = [], []

        def flush():
            if cur:
                chunks.append(list(cur))
                cur.clear()

        for i, w in enumerate(words):
            nxt = " ".join(words[j] for j in cur + [i])
            if cur and (len(nxt) > max_chars or len(cur) >= max_words or i in hard_breaks):
                flush()
            cur.append(i)
            if re.search(r"[.,?!:…]$|\.\.\.$", w):
                # keep "HOW DOES IT FEEL?" whole
                flush()
        flush()
        # merge "How does it feel?" into one chunk
        if len(chunks) >= 2 and [words[i].lower() for i in chunks[0] + chunks[1]][:4] == ["how", "does", "it", "feel?"]:
            chunks = [chunks[0] + chunks[1]] + chunks[2:]
        caps = []
        starts = [max(0.0, self.W(c[0]) - 2 * F) for c in chunks]
        starts[0] = 0.0
        for k, c in enumerate(chunks):
            st = starts[k]
            en = starts[k + 1] if k + 1 < len(chunks) else self.end
            sent_end = re.search(r"[.?!…]$|\.\.\.$", words[c[-1]]) is not None
            html = []
            for j, i in enumerate(c):
                t = words[i].upper()
                key = re.sub(r"[^\w']", "", words[i].lower())
                is_red = key in red or bool(re.search(r"\d", t)) or (sent_end and (len(c) == 1 or j == len(c) - 1))
                if k == 0:
                    is_red = key == "feel"
                html.append(f'<span class="r">{t}</span>' if is_red else t)
            caps.append(f'<div id="c{k:02d}" class="cap clip" data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="20"><span class="ct">{" ".join(html)}</span></div>')
            self.js(f'tl.fromTo("#c{k:02d} .ct",{{scale:1.1}},{{scale:1,duration:0.1,ease:"power2.out",immediateRender:false}},{st:.3f});')
        return "".join(caps)

    # ------------------------------------------------------------ output
    def write(self, red=(), hard_breaks=()):
        assert self.end, "call ep.ending(...) last"
        D = round(self.end, 3)
        caps = self.captions(red, hard_breaks)
        scene_html = []
        for k, sc in enumerate(self.scenes):
            canvas = f'<canvas id="{sc["id"]}-fx" class="sfx" width="1080" height="1920"></canvas>' if sc["fx"] else ""
            scene_html.append(
                f'<div id="{sc["id"]}" class="scene clip" data-start="{sc["start"]:.3f}" data-duration="{sc["end"] - sc["start"]:.3f}" data-track-index="{1 + k % 2}" data-track-kind="graphics">'
                f'<div id="{sc["id"]}-shake" class="fill"><div id="{sc["id"]}-cam" class="fill">'
                f'<svg class="fill" viewBox="0 0 1080 1920" width="1080" height="1920">{sc["svg"]}</svg>{canvas}{sc["html"]}</div></div></div>')
        tpl = open(f"{KIT}/template.html").read()
        html = (tpl.replace("%%D%%", str(D)).replace("%%SCENES%%", "".join(scene_html)).replace("%%CAPS%%", caps)
                .replace("%%FX%%", json.dumps(self.fx)).replace("%%JS%%", "\n".join(self.J)))
        proj = f"{self.dir}/project"
        os.makedirs(f"{proj}/assets/fonts", exist_ok=True)
        for f in os.listdir(f"{KIT}/fonts"):
            shutil.copy(f"{KIT}/fonts/{f}", f"{proj}/assets/fonts/{f}")
        if not os.path.exists(f"{proj}/hyperframes.json"):
            json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": {"assets": "assets"}, "authoringSkill": "hyperframes"}, open(f"{proj}/hyperframes.json", "w"), indent=2)
        open(f"{proj}/index.html", "w").write(html)
        json.dump(dict(D=D, off=self.off, cues=self.cues), open(f"{self.dir}/timing.json", "w"), indent=0)
        ncap = caps.count('class="cap')
        print(f"ok {D}s, {len(self.scenes)} scenes, {len(self.J)} js, {ncap} captions, {len(self.cues)} cues")


def fmtpy(v, fmt):
    n = int(round(v))
    if fmt == "c":
        return f"{n:,}"
    if fmt == "ms":
        return f"{n // 60:02d}:{n % 60:02d}"
    if fmt == "h":
        return f"{n:02d}:00"
    if fmt == "deg":
        return f"{n}°"
    return str(n)
