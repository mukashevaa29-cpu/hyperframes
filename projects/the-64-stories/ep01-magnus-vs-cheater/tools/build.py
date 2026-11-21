"""Builds EP01 compositions from the VO word timings.

Run: python3 tools/build.py   (from the project root)
Writes index.html and compositions/*.html. Every shot is a timed .clip inside its scene;
times below are global seconds from assets/audio/timing.json, converted to scene-local.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import magnus, cheater, robot, hands  # noqa: E402

W, H = 1080, 1920
TOTAL = 66.5
TIMING = json.load(open("assets/audio/timing.json"))
WORDS = TIMING["words"]

YELLOW, LIME, RED, BLUE, TEAL = "#FFC83A", "#B8F23A", "#FF5A4F", "#5AB8FF", "#2CD3C4"

# ---------------------------------------------------------------- pieces

def piece_svg(kind, white):
    f = "#F4F2EC" if white else "#3B3F4A"
    s = "#C9C5BB" if white else "#262931"
    hl = "#FFFFFF" if white else "#5A6070"
    base = f'<path d="M18,128 L82,128 L78,114 L22,114Z" fill="{s}"/><rect x="14" y="126" width="72" height="12" rx="5" fill="{f}"/>'
    body = {
        "p": f'<circle cx="50" cy="44" r="17" fill="{f}"/><path d="M38,62 L62,62 L70,114 L30,114Z" fill="{f}"/><path d="M58,62 L62,62 L70,114 L60,114Z" fill="{s}"/>',
        "r": f'<path d="M28,30 L36,30 L36,38 L46,38 L46,30 L54,30 L54,38 L64,38 L64,30 L72,30 L72,52 L64,58 L68,114 L32,114 L36,58 L28,52Z" fill="{f}"/><path d="M60,58 L64,58 L68,114 L58,114Z" fill="{s}"/>',
        "n": f'<path d="M34,114 C30,90 40,74 46,66 C36,70 26,72 22,62 C20,52 34,40 44,30 C48,20 56,16 62,20 C76,28 80,60 72,114Z" fill="{f}"/><circle cx="46" cy="40" r="4" fill="{s}"/><path d="M64,24 C76,34 78,70 70,114 L62,114 C70,70 68,40 64,24Z" fill="{s}"/>',
        "b": f'<circle cx="50" cy="18" r="7" fill="{f}"/><path d="M50,24 C70,40 70,62 58,72 L42,72 C30,62 30,40 50,24Z" fill="{f}"/><path d="M52,38 L60,48" stroke="{s}" stroke-width="5" stroke-linecap="round"/><path d="M40,74 L60,74 L68,114 L32,114Z" fill="{f}"/><path d="M56,74 L60,74 L68,114 L58,114Z" fill="{s}"/>',
        "q": f'<path d="M24,30 L36,56 L42,24 L50,52 L58,24 L64,56 L76,30 L72,72 L28,72Z" fill="{f}"/><circle cx="24" cy="28" r="6" fill="{f}"/><circle cx="42" cy="22" r="6" fill="{f}"/><circle cx="58" cy="22" r="6" fill="{f}"/><circle cx="76" cy="28" r="6" fill="{f}"/><path d="M30,74 L70,74 L70,114 L30,114Z" fill="{f}"/><path d="M60,74 L70,74 L70,114 L62,114Z" fill="{s}"/>',
        "k": f'<rect x="46" y="4" width="8" height="26" rx="3" fill="{f}"/><rect x="38" y="12" width="24" height="8" rx="3" fill="{f}"/><path d="M30,32 C30,26 70,26 70,32 L64,72 L36,72Z" fill="{f}"/><path d="M30,74 L70,74 L70,114 L30,114Z" fill="{f}"/><path d="M60,74 L70,74 L70,114 L62,114Z" fill="{s}"/>',
    }[kind]
    gloss = f'<path d="M40,46 q4,-10 10,-12" stroke="{hl}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.6"/>'
    return f'<svg viewBox="0 0 100 140" width="100%" height="100%">{body}{base}{gloss}</svg>'


def sq_xy(sq, size):
    f = "abcdefgh".index(sq[0])
    r = int(sq[1])
    return f * size, (8 - r) * size


def board(p, position, size=880, tilt=52, theme="green", extra=""):
    """A chess.com-style board lying in 3D, pieces standing up. position: {"e4": "P", ...}."""
    sq = size / 8
    light, dark = ("#EEEED2", "#769656") if theme == "green" else ("#E9E2D0", "#3A3F4B")
    pieces = []
    for s, code in position.items():
        x, y = sq_xy(s, sq)
        white = code.isupper()
        kind = code.lower()
        pieces.append(
            f'<div id="{p}-{s}" class="pc" style="left:{x:.1f}px;top:{y:.1f}px;width:{sq:.1f}px;height:{sq:.1f}px">'
            f'<div class="pc-shadow"></div>'
            f'<div class="pc-stand" style="transform:rotateX(-{tilt}deg)">{piece_svg(kind, white)}</div></div>'
        )
    hi = (f'<div id="{p}-hi-a" class="hi" style="width:{sq:.1f}px;height:{sq:.1f}px"></div>'
          f'<div id="{p}-hi-b" class="hi" style="width:{sq:.1f}px;height:{sq:.1f}px"></div>')
    return (
        f'<div class="board-wrap" style="width:{size}px;height:{size}px;margin-left:-{size / 2:.0f}px">'
        f'<div id="{p}-board" class="board" style="width:{size}px;height:{size}px;transform:rotateX({tilt}deg);'
        f'background-color:{light};background-image:conic-gradient({dark} 0 25%,transparent 0 50%,{dark} 0 75%,transparent 0);'
        f'background-size:{sq*2:.1f}px {sq*2:.1f}px">'
        f'<div class="board-edge"></div>{hi}{"".join(pieces)}{extra}</div></div>'
    )


# ---------------------------------------------------------------- sets

def room_bg(p):
    return f'''<div class="set room">
  <div class="win"><div class="sky"></div>
    <div class="cloud" style="left:90px;top:120px"></div><div class="cloud" style="left:560px;top:60px;transform:scale(.8)"></div>
    <div class="hedge"></div><div class="lawn"></div>
    <div class="mullion v"></div><div class="mullion h"></div></div>
  <div class="curtain l"></div><div class="curtain r"></div>
  <div class="wall-shade"></div></div>'''


def stream_bg(p, hue="purple"):
    return f'''<div class="set stream {hue}"><div class="beam b1"></div><div class="beam b2"></div><div class="beam b3"></div>
  <div class="floor-glow"></div><div class="dust"></div></div>'''


def teal_bg(p):
    return '<div class="set tealw"><div class="grid-floor"></div><div class="halo"></div></div>'


def dark_bg(p):
    return '<div class="set darkhall"><div class="spot"></div><div class="crowd"></div></div>'


def desk(y=1500, color="#B9824F"):
    return f'<div class="desk" style="top:{y}px;background:linear-gradient({color},#8C5A33)"></div>'


def char(svg, x, y, w, extra=""):
    h = w * 800 / 600
    return f'<div class="char" data-layout-ignore style="left:{x - w/2:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px"><svg viewBox="0 0 600 800" width="100%" height="100%" overflow="visible">{svg}{extra}</svg></div>'


def tag(id_, text, bg=YELLOW, fg="#1B1B1B", x=540, y=300, rot=-3, size=40, row=""):
    return (f'<div class="tag-row" style="top:{y}px;{row}"><div id="{id_}" class="tag" style="background:{bg};color:{fg};'
            f'font-size:{size}px;rotate:{rot}deg">{text}</div></div>')


def stamp(id_, text, color=RED, y=760, rot=-9, size=120):
    return (f'<div class="tag-row" style="top:{y}px"><div id="{id_}" class="stamp" style="color:{color};border-color:{color};'
            f'font-size:{size}px;rotate:{rot}deg">{text}</div></div>')


def bignum(id_, text, y=230, color=YELLOW, size=210, sub=None, sub_bg=YELLOW):
    s = f'<div class="sub" style="background:{sub_bg}">{sub}</div>' if sub else ""
    return f'<div class="num-row" style="top:{y}px"><div id="{id_}" class="bignum" style="color:{color};font-size:{size}px">{text}</div>{s}</div>'


def namecard(id_, name, sub, y=210):
    return (f'<div id="{id_}" class="namecard" style="top:{y}px"><div class="nc-name">{name}</div>'
            f'<div class="nc-rule"></div><div class="nc-sub">{sub}</div></div>')


# ---------------------------------------------------------------- scene assembly

COMMON_CSS = f"""
#root {{ position:absolute; inset:0; overflow:hidden; background:#101018; font-family:Nunito, sans-serif; }}
.shot {{ position:absolute; inset:0; overflow:hidden; }}
.cam, .shake {{ position:absolute; inset:0; transform-origin:50% 45%; }}
.set {{ position:absolute; inset:-60px; }}
.room {{ background:linear-gradient(#F1E7D6,#E6D7BF); }}
.room .win {{ position:absolute; left:150px; top:170px; width:900px; height:980px; border:26px solid #FBF7EF; border-radius:6px; overflow:hidden; box-shadow:0 18px 40px rgba(80,50,20,.25); }}
.room .sky {{ position:absolute; inset:0; background:linear-gradient(#5FB4EA,#A8DBF5 70%,#D9F0FA); }}
.room .cloud {{ position:absolute; width:260px; height:90px; background:#FFFFFF; border-radius:60px; box-shadow:60px -30px 0 10px #fff,130px 0 0 0 #fff; }}
.room .hedge {{ position:absolute; left:0; right:0; top:560px; height:180px; background:radial-gradient(circle at 40px 60px,#5DBB4C 50px,transparent 52px) 0 0/90px 100px,#4EA83E; }}
.room .lawn {{ position:absolute; left:0; right:0; top:700px; bottom:0; background:linear-gradient(#7CC765,#5DAE4B); }}
.room .mullion.v {{ position:absolute; left:50%; top:0; bottom:0; width:22px; margin-left:-11px; background:#FBF7EF; }}
.room .mullion.h {{ position:absolute; top:46%; left:0; right:0; height:22px; background:#FBF7EF; }}
.room .curtain {{ position:absolute; top:120px; width:150px; height:1150px; background:repeating-linear-gradient(90deg,#2F9A55 0 34px,#277F46 34px 50px); }}
.room .curtain.l {{ left:60px; }} .room .curtain.r {{ right:-20px; }}
.room .wall-shade {{ position:absolute; inset:0; background:linear-gradient(90deg,rgba(60,30,10,.18),transparent 30%,transparent 70%,rgba(60,30,10,.22)); }}
.stream {{ background:radial-gradient(ellipse at 50% 30%,#4A2E9A,#1E1648 65%,#120E2C); }}
.stream.blue {{ background:radial-gradient(ellipse at 50% 30%,#2D58C8,#152C6E 65%,#0B1638); }}
.beam {{ position:absolute; top:-200px; width:240px; height:1700px; background:linear-gradient(rgba(190,150,255,.55),rgba(190,150,255,0) 85%); filter:blur(6px); transform-origin:50% 0; }}
.stream.blue .beam {{ background:linear-gradient(rgba(150,200,255,.5),rgba(150,200,255,0) 85%); }}
.beam.b1 {{ left:120px; rotate:14deg; }} .beam.b2 {{ left:470px; rotate:0deg; opacity:.8; }} .beam.b3 {{ left:820px; rotate:-14deg; }}
.floor-glow {{ position:absolute; left:0; right:0; bottom:0; height:700px; background:linear-gradient(transparent,rgba(10,6,30,.85)); }}
.dust {{ position:absolute; inset:0; background-image:radial-gradient(circle,rgba(255,255,255,.55) 2px,transparent 3px),radial-gradient(circle,rgba(255,220,255,.35) 3px,transparent 4px); background-size:170px 230px,260px 310px; background-position:30px 40px,110px 90px; opacity:.6; }}
.tealw {{ background:radial-gradient(ellipse at 50% 38%,#2A8F8A,#0F3E45 55%,#071C22); }}
.tealw .grid-floor {{ position:absolute; left:-400px; right:-400px; top:1150px; height:900px; background-image:linear-gradient(rgba(124,245,232,.35) 2px,transparent 2px),linear-gradient(90deg,rgba(124,245,232,.35) 2px,transparent 2px); background-size:90px 90px; transform:perspective(600px) rotateX(62deg); transform-origin:50% 0; }}
.tealw .halo {{ position:absolute; left:50%; top:560px; width:900px; height:900px; margin-left:-450px; border-radius:50%; background:radial-gradient(circle,rgba(124,245,232,.35),transparent 65%); }}
.darkhall {{ background:radial-gradient(ellipse at 50% 20%,#4A3A2A,#1C1510 60%,#0C0906); }}
.darkhall .spot {{ position:absolute; left:50%; top:-100px; width:900px; height:1500px; margin-left:-450px; background:radial-gradient(ellipse at 50% 0,rgba(255,230,180,.45),transparent 70%); }}
.desk {{ position:absolute; left:-80px; right:-80px; height:700px; box-shadow:0 -6px 0 #D69A62 inset; }}
.char {{ position:absolute; }}
.char svg {{ overflow:visible; }}
.board-wrap {{ position:absolute; left:50%; perspective:1700px; perspective-origin:50% 0%; }}
.board {{ position:relative; transform-style:preserve-3d; transform-origin:50% 100%; border-radius:6px; }}
.board-edge {{ position:absolute; inset:-18px; background:#5A3A22; border-radius:12px; transform:translateZ(-2px); box-shadow:0 40px 80px rgba(0,0,0,.45); }}
.pc {{ position:absolute; transform-style:preserve-3d; }}
.pc-stand {{ position:absolute; left:4%; width:92%; height:128%; bottom:12%; transform-origin:50% 100%; }}
.pc-shadow {{ position:absolute; left:14%; width:72%; height:40%; bottom:8%; border-radius:50%; background:rgba(0,0,0,.28); }}
.hi {{ position:absolute; left:0; top:0; background:rgba(44,211,196,.75); opacity:0; }}
.tag-row, .num-row {{ position:absolute; left:0; right:0; display:flex; flex-direction:column; align-items:center; }}
.tag {{ font-family:'Archivo Black', sans-serif; padding:10px 26px 12px; letter-spacing:.02em; text-transform:uppercase; box-shadow:0 6px 0 rgba(0,0,0,.35); opacity:0; }}
.stamp {{ font-family:'Archivo Black', sans-serif; padding:6px 30px; border:12px solid; border-radius:18px; letter-spacing:.04em; text-transform:uppercase; opacity:0; background:rgba(255,255,255,.08); text-shadow:0 4px 0 rgba(0,0,0,.25); }}
.bignum {{ font-family:'Archivo Black', sans-serif; line-height:1; text-shadow:0 10px 0 rgba(40,24,0,.55); letter-spacing:-.01em; }}
.sub {{ margin-top:12px; font-family:'Archivo Black', sans-serif; font-size:30px; color:#1B1B1B; padding:4px 16px; text-transform:uppercase; }}
.namecard {{ position:absolute; left:0; right:0; text-align:center; color:#FFFFFF; opacity:0; }}
.nc-name {{ font-family:'EB Garamond', serif; font-weight:600; font-size:76px; letter-spacing:.08em; text-transform:uppercase; text-shadow:0 4px 18px rgba(0,0,0,.6); }}
.nc-rule {{ width:120px; height:4px; background:{YELLOW}; margin:10px auto 14px; }}
.nc-sub {{ font-family:Inter, sans-serif; font-weight:700; font-size:28px; letter-spacing:.28em; text-transform:uppercase; opacity:.85; }}
.frame-card {{ position:absolute; border-radius:22px; overflow:hidden; box-shadow:0 24px 60px rgba(0,0,0,.45); }}
.live {{ font-family:Inter, sans-serif; font-weight:900; font-size:30px; color:#fff; background:#E5322D; padding:6px 16px; border-radius:8px; letter-spacing:.06em; }}
.badge {{ position:absolute; width:120px; height:120px; border-radius:50%; background:{TEAL}; color:#fff; font-family:'Archivo Black',sans-serif; font-size:64px; display:flex; align-items:center; justify-content:center; box-shadow:0 8px 0 #148A80; opacity:0; }}
.title {{ position:absolute; left:0; right:0; text-align:center; font-family:'Archivo Black', sans-serif; text-transform:uppercase; line-height:1.02; }}
.title .l1 {{ color:#FFFFFF; font-size:76px; -webkit-text-stroke:10px #1A1420; paint-order:stroke fill; text-shadow:0 8px 0 rgba(0,0,0,.45); }}
.title .l2 {{ color:{YELLOW}; font-size:80px; -webkit-text-stroke:10px #2A1A00; paint-order:stroke fill; text-shadow:0 8px 0 rgba(70,40,0,.65); }}
.clockface {{ position:absolute; width:400px; height:250px; border-radius:26px; background:#141414; border:14px solid #2B2B2B; display:flex; align-items:center; justify-content:center; font-family:'Space Mono', monospace; font-weight:700; font-size:150px; color:#8CF27A; box-shadow:inset 0 0 40px rgba(0,0,0,.8); }}
.clockname {{ position:absolute; width:400px; text-align:center; font-family:'Archivo Black',sans-serif; font-size:40px; color:#fff; }}
.spark {{ position:absolute; width:14px; height:40px; border-radius:7px; background:#FFE27A; opacity:0; }}
.confetti {{ position:absolute; width:22px; height:34px; border-radius:4px; opacity:0; }}
"""

JS_HELPERS = """
function part(tl, p, kind, name, t) {
  tl.set('[id^="' + p + '-' + kind + '-"]', { opacity: 0 }, t);
  tl.set('#' + p + '-' + kind + '-' + name, { opacity: 1 }, t);
}
function blink(tl, p, t) {
  tl.set('#' + p + '-lid-closed', { opacity: 1 }, t);
  tl.set('#' + p + '-lid-closed', { opacity: 0 }, t + 0.1);
}
function shotIn(tl, cam, t, dur, dir, push) {
  tl.fromTo(cam, { x: 170 * dir, filter: 'blur(18px)' }, { x: 0, filter: 'blur(0px)', duration: 0.2, ease: 'power3.out' }, t);
  tl.fromTo(cam, { scale: 1.0 }, { scale: 1.0 + (push || 0.07) * dur, duration: dur, ease: 'none' }, t);
}
function popIn(tl, sel, t, s) {
  tl.fromTo(sel, { opacity: 0, scale: 0.4 * (s || 1) }, { opacity: 1, scale: 1.1, duration: 0.12, ease: 'power2.out', immediateRender: false }, t);
  tl.to(sel, { scale: 1, duration: 0.1, ease: 'power2.inOut' }, t + 0.12);
}
function slam(tl, sel, shake, t) {
  tl.fromTo(sel, { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.13, ease: 'power4.in', immediateRender: false }, t);
  tl.fromTo(shake, { x: 0, y: 0 }, { keyframes: [{ x: -22, y: 12 }, { x: 18, y: -10 }, { x: -10, y: 6 }, { x: 4, y: -2 }, { x: 0, y: 0 }], duration: 0.3, ease: 'none' }, t + 0.13);
}
function move(tl, p, from, to, t, sq) {
  var f = 'abcdefgh', dx = (f.indexOf(to[0]) - f.indexOf(from[0])) * sq, dy = (parseInt(from[1]) - parseInt(to[1])) * sq;
  tl.set('#' + p + '-hi-a', { x: f.indexOf(from[0]) * sq, y: (8 - parseInt(from[1])) * sq, opacity: 0.55 }, t);
  tl.to('#' + p + '-' + from, { x: dx, y: dy, duration: 0.28, ease: 'power3.inOut' }, t);
  tl.set('#' + p + '-hi-b', { x: f.indexOf(to[0]) * sq, y: (8 - parseInt(to[1])) * sq, opacity: 0.75 }, t + 0.2);
}
"""


class Scene:
    def __init__(self, sid, start, end):
        self.sid, self.start, self.end = sid, start, end
        self.shots = []  # (html)
        self.js = []
        self.n = 0

    @property
    def dur(self):
        return round(self.end - self.start, 3)

    def loc(self, t):
        return round(t - self.start, 3)

    def shot(self, t0, t1, body, dir=1, push=0.07):
        self.n += 1
        sid = f"{self.sid}-s{self.n}"
        a, b = self.loc(t0), self.loc(t1)
        self.shots.append(
            f'<div id="{sid}" class="shot clip" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="0">'
            f'<div id="{sid}-cam" class="cam"><div id="{sid}-shake" class="shake">{body}</div></div></div>')
        self.js.append(f"shotIn(tl, '#{sid}-cam', {a}, {round(b - a, 3)}, {dir}, {push});")
        return sid

    def add(self, line):
        self.js.append(line)

    def write(self):
        html = f"""<template id="{self.sid}-template">
  <style>{COMMON_CSS}</style>
  <div id="root" data-composition-id="{self.sid}" data-width="{W}" data-height="{H}">
    {''.join(self.shots)}
  </div>
  <script>
    {JS_HELPERS}
    var tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in self.js)}
    tl.set({{}}, {{}}, {self.dur});
    window.__timelines["{self.sid}"] = tl;
  </script>
</template>
"""
        open(f"compositions/{self.sid}.html", "w").write(html)


def T(word, n=1, case=False):
    """global start time of the n-th occurrence of a word (punctuation-insensitive)"""
    k = 0
    for w in WORDS:
        a = w["text"].strip(".,?!\"")
        if (a == word) if case else (a.lower() == word.lower()):
            k += 1
            if k == n:
                return w["start"]
    raise KeyError(word)


SQ = 880 / 8
scenes = []

# ===================== S1 HOOK 0 – 5.55
s = Scene("hook", 0, 5.55)
t1 = T("But")  # 4.02
sid = s.shot(0, t1 - 0.06, room_bg("h") + desk(1430)
             + char(cheater("h1a", "smug") + hands("h1a", y=760), 540, 640, 820)
             + '<div class="title" style="top:150px"><div class="l1">STOCKFISH</div><div class="l2">COULDN\'T BEAT HIM</div></div>'
             + f'<div id="h-vs" class="frame-card" style="left:690px;top:420px;width:300px;height:330px;background:#C93A3A;border:10px solid #fff;opacity:0">'
             + f'<svg viewBox="0 60 600 640" width="100%" height="100%">{magnus("h1m", "smug")}</svg></div>'
             + tag("h-vs-tag", "VS MAGNUS", YELLOW, y=770, rot=4, size=30, row="left:600px"), dir=0)
s.add(f"popIn(tl, '#h-vs', {s.loc(T('Magnus'))});")
s.add(f"popIn(tl, '#h-vs-tag', {s.loc(T('Magnus')) + 0.15});")
s.add("blink(tl, 'h1a', 2.1);")
sid = s.shot(t1 - 0.06, s.end, room_bg("h") + desk(1500)
             + char(robot("h2r", "off"), 830, 760, 380)
             + char(cheater("h2a", "smug") + hands("h2a", y=760), 470, 560, 980)
             + tag("h2-tag", "NOT ALONE", RED, "#fff", y=300, size=56))
s.add("tl.fromTo('#h2r', { y: 260 }, { y: 0, duration: 0.45, ease: 'back.out(1.6)' }, 0.62);")
s.add(f"part(tl, 'h2r', 'eyes', 'on', {s.loc(T('alone'))});")
s.add(f"popIn(tl, '#h2-tag', {s.loc(T('alone'))});")
s.add(f"part(tl, 'h2a', 'mouth', 'flat', {s.loc(T('alone')) + 0.3});")
scenes.append(s)

# ===================== S2 RATINGS 5.55 – 13.5
s = Scene("ratings", 5.55, 13.5)
ta, tm, tw = T("Aleksandar"), T("Magnus", 2), T("World")
s.shot(ta - 0.05, tm - 0.1, stream_bg("r", "blue")
       + f'<div class="frame-card" style="left:190px;top:560px;width:700px;height:800px;background:linear-gradient(#3C7BE0,#1D4FA8);border:14px solid #fff">'
       + f'<svg viewBox="0 0 600 800" width="100%" height="100%">{cheater("r1a", "smug")}</svg></div>'
       + tag("r1-name", "ALEKSANDAR-K", BLUE, "#0B1638", y=1395, size=44, rot=-2)
       + bignum("r1-num", "0", y=250, sub="RATING", sub_bg=BLUE))
s.add(f"popIn(tl, '#r1-name', {s.loc(ta) + 0.1});")
s.add(f"tl.fromTo('#r1-num', {{ innerText: 0 }}, {{ innerText: 2118, duration: 0.7, snap: {{ innerText: 1 }}, ease: 'power2.out' }}, {s.loc(T('twenty-one'))});")
s.add(f"blink(tl, 'r1a', {s.loc(ta) + 1.6});")
s.shot(tm - 0.1, tw - 0.08, stream_bg("r", "purple")
       + f'<div class="frame-card" style="left:190px;top:560px;width:700px;height:800px;background:linear-gradient(#E0503C,#A82A1D);border:14px solid #fff">'
       + f'<svg viewBox="0 0 600 800" width="100%" height="100%">{magnus("r2m", "smug")}</svg></div>'
       + tag("r2-name", "MAGNUS CARLSEN", RED, "#fff", y=1395, size=44, rot=2)
       + bignum("r2-num", "0", y=250, sub="RATING", sub_bg=YELLOW), dir=-1)
s.add(f"popIn(tl, '#r2-name', {s.loc(tm)});")
s.add(f"tl.fromTo('#r2-num', {{ innerText: 0 }}, {{ innerText: 2892, duration: 0.7, snap: {{ innerText: 1 }}, ease: 'power2.out' }}, {s.loc(T('twenty-eight'))});")
s.shot(tw - 0.08, s.end, stream_bg("r", "purple")
       + char(magnus("r3m", "smug") + hands("r3m", y=760), 540, 520, 1060)
       + '<svg id="r3-crown" viewBox="0 0 200 120" style="position:absolute;left:400px;top:330px;width:280px;opacity:0"><path d="M10,110 L20,30 L60,70 L100,10 L140,70 L180,30 L190,110Z" fill="#FFC83A" stroke="#B07A10" stroke-width="8" stroke-linejoin="round"/><circle cx="100" cy="10" r="10" fill="#FFE27A"/></svg>'
       + tag("r3-tag", "WORLD CHAMPION", YELLOW, y=230, size=60))
s.add(f"popIn(tl, '#r3-tag', {s.loc(tw)});")
s.add(f"tl.fromTo('#r3-crown', {{ opacity: 0, y: -200 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: 'bounce.out' }}, {s.loc(T('champion'))});")
scenes.append(s)

# ===================== S3 BOARD 13.5 – 21.3
POS_A = {"a8": "r", "c8": "b", "d8": "q", "f8": "r", "g8": "k", "a7": "p", "b7": "p", "e7": "b", "g7": "p", "h7": "p",
         "c6": "p", "e6": "p", "f6": "n", "d7": "n", "d5": "p", "f5": "p",
         "c4": "P", "d4": "P", "e3": "P", "f3": "N", "c3": "N", "a2": "P", "b2": "P", "g2": "P", "h2": "P", "f2": "P",
         "a1": "R", "c1": "B", "d1": "Q", "f1": "R", "g1": "K", "d3": "B"}
s = Scene("board", 13.5, 21.3)
tb, tnot, tperf = T("But", 2), T("Not"), T("Perfect")
s.shot(s.start, tb - 0.06, stream_bg("b", "blue") + char(magnus("b1m", "smug") + hands("b1m", y=760), 540, 300, 900) + f'<div style="position:absolute;left:0;right:0;top:820px">{board("b1", POS_A)}</div>'
       + tag("b1-tag", "OVER IN 20 MOVES?", YELLOW, y=330, size=58), push=0.05)
s.add(f"popIn(tl, '#b1-tag', {s.loc(T('over'))});")
s.shot(tb - 0.06, tnot - 0.06, stream_bg("b", "blue") + char(cheater("b2a", "smug") + hands("b2a", y=760), 540, 280, 900) + f'<div style="position:absolute;left:0;right:0;top:820px">{board("b2", POS_A)}</div>'
       + '<div id="b2-bang" class="badge" style="left:800px;top:700px">!!</div>'
       + tag("b2-tag", "BEST MOVE", TEAL, "#062A27", y=330, size=58), dir=-1)
for i, (fr, to, w) in enumerate([("f6", "e4", T("move", 1)), ("e7", "d6", T("move", 2)), ("d8", "e7", T("Aleksandar", 2)), ("d7", "f6", T("plays"))]):
    lt = s.loc(w) - s.loc(tb - 0.06)
    s.add(f"move(tl, 'b2', '{fr}', '{to}', {s.loc(w)}, {SQ});")
    s.add(f"popIn(tl, '#b2-bang', {s.loc(w) + 0.22});")
    s.add(f"tl.to('#b2-bang', {{ opacity: 0, duration: 0.1 }}, {s.loc(w) + 0.5});")
s.add(f"popIn(tl, '#b2-tag', {s.loc(T('perfectly'))});")
s.shot(tnot - 0.06, tperf - 0.06, room_bg("b") + desk(1450) + char(cheater("b3a", "smug") + hands("b3a", y=760), 540, 520, 1000)
       + tag("b3-tag", "GOOD", "#FFFFFF", "#1B1B1B", y=280, size=80)
       + '<div class="tag-row" style="top:300px"><div id="b3-strike" style="width:320px;height:16px;background:#FF5A4F;rotate:-8deg;margin-top:46px;opacity:0"></div></div>')
s.add(f"popIn(tl, '#b3-tag', {s.loc(T('good'))});")
s.add(f"tl.fromTo('#b3-strike', {{ opacity: 1, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.15, ease: 'power2.out' }}, {s.loc(T('good')) + 0.3});")
sid = s.shot(tperf - 0.06, s.end, stream_bg("b", "blue") + char(cheater("b4a", "smug") + hands("b4a", y=760), 540, 300, 900) + f'<div style="position:absolute;left:0;right:0;top:820px">{board("b4", POS_A)}</div>'
             + stamp("b4-stamp", "PERFECT", "#2CD3C4", y=520, size=150), dir=-1)
s.add(f"slam(tl, '#b4-stamp', '#{sid}-shake', {s.loc(tperf)});")
scenes.append(s)

# ===================== S4 WHISPER 21.3 – 28.7
s = Scene("whisper", 21.3, 28.7)
tsf, teven = T("Stockfish"), T("Even")
s.shot(s.start, tsf - 0.06, room_bg("w")
       + char(cheater("w1a", "neutral", look=(-10, 0)), 380, 300, 1250)
       + char(robot("w1r", "whisper"), 900, 420, 520)
       + '<svg id="w1-waves" viewBox="0 0 200 200" style="position:absolute;left:560px;top:620px;width:200px;opacity:0">'
       + '<path d="M150,40 Q110,100 150,160" stroke="#2CD3C4" stroke-width="12" fill="none" stroke-linecap="round"/>'
       + '<path d="M110,60 Q80,100 110,140" stroke="#2CD3C4" stroke-width="12" fill="none" stroke-linecap="round"/>'
       + '<path d="M70,80 Q55,100 70,120" stroke="#2CD3C4" stroke-width="12" fill="none" stroke-linecap="round"/></svg>', push=0.05)
s.add(f"tl.fromTo('#w1r', {{ x: 120 }}, {{ x: 0, duration: 0.5, ease: 'power3.out' }}, {s.loc(T('someone'))});")
for k in range(5):
    s.add(f"tl.fromTo('#w1-waves', {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.15, immediateRender: false }}, {s.loc(T('whispering')) + k * 0.36});")
    s.add(f"tl.set('#w1r-mouth-talk', {{ opacity: {k % 2} }}, {s.loc(T('whispering')) + k * 0.18});")
s.add(f"tl.to('#w1-waves', {{ opacity: 0, duration: 0.1 }}, {s.loc(tsf) - 0.2});")
s.shot(tsf - 0.06, teven - 0.06, teal_bg("w") + char(robot("w2r", "on"), 540, 520, 980)
       + namecard("w2-name", "STOCKFISH", "CHESS ENGINE", y=200)
       + tag("w2-tag", "STRONGEST ON EARTH", TEAL, "#062A27", y=1340, size=54))
s.add(f"tl.fromTo('#w2-name', {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }}, {s.loc(tsf) + 0.05});")
s.add(f"popIn(tl, '#w2-tag', {s.loc(T('strongest'))});")
s.add(f"tl.fromTo('#w2r-bulb', {{ fill: '#1FB5A8' }}, {{ fill: '#7CF5E8', duration: 0.2, repeat: 5, yoyo: true }}, {s.loc(tsf) + 0.3});")
s.shot(teven - 0.06, s.end, stream_bg("w", "purple") + char(magnus("w3m", "focus", look=(12, 2)) + hands("w3m", y=760), 540, 560, 1000)
       + '<div style="position:absolute;left:60px;top:220px" class="live">● LIVE</div>'
       + '<div id="w3-q" class="bignum" style="position:absolute;left:760px;top:420px;font-size:200px;color:#FFC83A;opacity:0">?</div>', dir=-1)
s.add(f"popIn(tl, '#w3-q', {s.loc(T('noticed'))});")
scenes.append(s)

# ===================== S5 REAL CLIP 28.7 – 30.95
s = Scene("clip", 28.7, 30.95)
s.shot(s.start, s.end, stream_bg("c", "purple")
       + namecard("c-name", "MAGNUS CARLSEN", "WORLD CHAMPION · LIVE ON CHESS24", y=250)
       + '<div class="frame-card" style="left:40px;top:520px;width:1000px;height:700px;background:#fff"></div>', dir=0, push=0)
s.shots.append('<video id="c-cam" class="clip" src="assets/video/magnus_cam.mp4" data-start="0.15" data-duration="2.1" data-track-index="1" '
               'data-has-audio="true" playsinline style="position:absolute;left:52px;top:532px;width:976px;height:676px;object-fit:cover;z-index:5;border-radius:12px"></video>'
               '<div style="position:absolute;left:74px;top:554px;z-index:6" class="live">● LIVE</div>')
s.add("tl.fromTo('#c-name', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }, 0.1);")
scenes.append(s)

# ===================== S6 ENDGAME 30.95 – 38.4
POS_E1 = {"a8": "r", "d8": "q", "g8": "k", "a7": "p", "b7": "p", "c7": "p", "g7": "p", "h6": "p", "e5": "p", "c6": "n",
          "a2": "P", "b2": "P", "c2": "P", "g2": "P", "h2": "P", "f3": "P", "c3": "N", "e3": "B", "c1": "K", "d1": "Q", "a1": "R", "h8": "r", "h1": "R"}
POS_E2 = {"d8": "r", "h8": "r", "e7": "k", "a7": "p", "b7": "p", "c7": "p", "g7": "p", "h6": "p", "e5": "p", "c6": "n", "b4": "b",
          "a2": "P", "b2": "P", "c2": "P", "g2": "P", "h2": "P", "f3": "P", "c3": "N", "e3": "B", "d3": "R", "e1": "R", "c1": "K"}
s = Scene("endgame", 30.95, 38.4)
the, tand = T("He", case=True), T("And", case=True)
s.shot(s.start, the - 0.06, stream_bg("e", "purple") + char(magnus("e1m", "focus") + hands("e1m", y=760), 540, 380, 900)
       + f'<div style="position:absolute;left:0;right:0;top:1060px">{board("e1", POS_E1, size=820)}</div>'
       + tag("e1-tag", "NO MORE ATTACKS", YELLOW, y=230, size=56))
s.add(f"popIn(tl, '#e1-tag', {s.loc(T('attacking'))});")
s.add(f"part(tl, 'e1m', 'mouth', 'smirk', {s.loc(T('attacking'))});")
s.shot(the - 0.06, tand - 0.06, stream_bg("e", "blue") + char(magnus("e2m", "smug") + hands("e2m", y=760), 540, 300, 900) + f'<div style="position:absolute;left:0;right:0;top:820px">{board("e2", POS_E1)}</div>'
       + tag("e2-tag", "QUEENS TRADED", "#FFFFFF", "#1B1B1B", y=300, size=56)
       + tag("e2-tag2", "ROOKS TRADED", "#FFFFFF", "#1B1B1B", y=400, size=56), dir=-1)
for sq_ in ("d1", "d8"):
    s.add(f"tl.to('#e2-{sq_}', {{ y: -900, opacity: 0, duration: 0.45, ease: 'power3.in' }}, {s.loc(T('queens'))});")
for sq_ in ("a1", "a8", "h8", "h1"):
    s.add(f"tl.to('#e2-{sq_}', {{ y: -900, opacity: 0, duration: 0.45, ease: 'power3.in' }}, {s.loc(T('rooks'))});")
s.add(f"popIn(tl, '#e2-tag', {s.loc(T('queens'))});")
s.add(f"popIn(tl, '#e2-tag2', {s.loc(T('rooks'))});")
s.shot(tand - 0.06, s.end, dark_bg("e") + char(magnus("e3m", "focus") + hands("e3m", y=760), 300, 360, 640) + char(cheater("e3a", "nervous") + hands("e3a", y=760), 790, 380, 620) + f'<div style="position:absolute;left:0;right:0;top:820px">{board("e3", POS_E2, theme="green")}</div>'
       + tag("e3-tag", "LONG. SLOW. ENDGAME.", "#FFFFFF", "#1B1B1B", y=320, size=54), push=0.03)
s.add(f"popIn(tl, '#e3-tag', {s.loc(T('endgame'))});")
scenes.append(s)

# ===================== S7 HUMAN 38.4 – 44.6
s = Scene("human", 38.4, 44.6)
ta2, tcopy = T("A", case=True), T("copying")
s.shot(s.start, ta2 - 0.06, teal_bg("u") + char(robot("u1r", "whisper"), 540, 470, 760)
       + f'<div style="position:absolute;left:0;right:0;top:1180px;transform:scale(.7);transform-origin:50% 0">{board("u1", POS_E2)}</div>'
       + tag("u1-tag", "NO HANDS", RED, "#fff", y=250, size=60))
s.add(f"popIn(tl, '#u1-tag', {s.loc(T('pieces'))});")
s.add(f"tl.fromTo('#u1r', {{ rotation: 0, transformOrigin: '50% 80%' }}, {{ keyframes: [{{ rotation: -6 }}, {{ rotation: 6 }}, {{ rotation: 0 }}], duration: 0.8, ease: 'sine.inOut' }}, {s.loc(T('pieces')) - 0.3});")
s.shot(ta2 - 0.06, tcopy - 0.25, room_bg("u") + char(cheater("u2a", "neutral", look=(0, 14)), 540, 220, 760)
       + f'<div style="position:absolute;left:0;right:0;top:860px">{board("u2", POS_E2)}</div>'
       + f'<div id="u2-hand" style="position:absolute;left:330px;top:1110px;width:120px;height:120px;border-radius:50%;background:#F3CBA6;box-shadow:inset -10px -10px 0 #E2AE87"></div>'
       + tag("u2-tag", "HUMAN", YELLOW, y=230, size=64), dir=-1)
s.add(f"popIn(tl, '#u2-tag', {s.loc(T('human'))});")
s.add(f"tl.to('#u2-hand', {{ x: 140, y: -70, duration: 0.6, ease: 'power2.inOut' }}, {s.loc(T('human')) - 0.2});")
s.add(f"tl.to('#u2-c6', {{ x: {SQ}, y: {SQ}, duration: 0.6, ease: 'power2.inOut' }}, {s.loc(T('does')) - 0.1});")
s.add(f"tl.to('#u2-hand', {{ x: 260, y: 30, duration: 0.6, ease: 'power2.inOut', overwrite: 'auto' }}, {s.loc(T('does')) - 0.1});")
s.shot(tcopy - 0.25, s.end, room_bg("u") + desk(1420) + char(cheater("u3a", "nervous", look=(-12, 0)) + hands("u3a", y=760), 540, 520, 980)
       + '<div class="frame-card" style="left:70px;top:230px;width:330px;height:200px;background:#141414;border:10px solid #2B2B2B;display:flex;align-items:center;justify-content:center">'
       + '<div id="u3-clock" style="font-family:\'Space Mono\',monospace;font-weight:700;font-size:96px;color:#FF5A4F">0:41</div></div>'
       + tag("u3-tag", "COPY... PASTE...", "#FFFFFF", "#1B1B1B", y=300, size=44, row="left:420px"))
s.add(f"popIn(tl, '#u3-tag', {s.loc(T('every'))});")
s.add(f"tl.fromTo('#u3-clock', {{ innerText: 41 }}, {{ innerText: 19, duration: 2.0, ease: 'none', snap: {{ innerText: 1 }}, modifiers: {{ innerText: function (v) {{ return '0:' + String(Math.round(v)).padStart(2, '0'); }} }} }}, {s.loc(tcopy)});")
for k in range(4):
    s.add(f"tl.to('#u3a-iris-l, #u3a-iris-r', {{ x: {12 if k % 2 == 0 else -12}, duration: 0.12 }}, {s.loc(tcopy) + 0.5 * k});")
scenes.append(s)

# ===================== S8 CLOCK 44.6 – 53.1
s = Scene("clock", 44.6, 53.1)
tten, tzero, ttime, tmw = T("Ten"), T("Zero"), T("Time's"), T("Magnus", 6)
CL = ('<div style="position:absolute;left:50px;top:560px;width:980px;height:640px;border-radius:40px;background:linear-gradient(#7A4A28,#4E2E18);box-shadow:0 40px 80px rgba(0,0,0,.6)"></div>'
      '<div style="position:absolute;left:250px;top:500px;width:110px;height:70px;border-radius:14px;background:#C9C2B5"></div>'
      '<div style="position:absolute;left:720px;top:520px;width:110px;height:50px;border-radius:14px;background:#C9C2B5"></div>'
      '<div id="{p}-cm" class="clockface" style="left:90px;top:640px;width:440px;height:300px;font-size:160px">1:31</div>'
      '<div id="{p}-ca" class="clockface" style="left:550px;top:640px;width:440px;height:300px;font-size:160px;color:#FF5A4F">0:12</div>'
      '<div class="clockname" style="left:90px;top:965px;width:440px">MAGNUS</div><div class="clockname" style="left:550px;top:965px;width:440px">ALEKSANDAR</div>'
      '<div class="frame-card" style="left:170px;top:180px;width:280px;height:280px;border-radius:50%;background:linear-gradient(#E0503C,#A82A1D);border:10px solid #fff">'
      f'<svg viewBox="100 60 400 400" width="100%" height="100%">{magnus("{p}m", "smug").replace("{{", "{{{{").replace("}}", "}}}}")}</svg></div>'
      '<div class="frame-card" style="left:630px;top:180px;width:280px;height:280px;border-radius:50%;background:linear-gradient(#3C7BE0,#1D4FA8);border:10px solid #fff">'
      f'<svg viewBox="100 60 400 400" width="100%" height="100%">{cheater("{p}a", "nervous").replace("{{", "{{{{").replace("}}", "}}}}")}</svg></div>')
s.shot(s.start, tten - 0.06, dark_bg("k") + CL.format(p="k1")
       + tag("k1-tag", "OVER A MINUTE", LIME, "#0E2A00", y=1060, size=44, row="right:500px")
       + tag("k1-tag2", "SECONDS", RED, "#fff", y=1060, size=44, row="left:500px"), push=0.04)
s.add(f"popIn(tl, '#k1-tag', {s.loc(T('minute'))});")
s.add(f"popIn(tl, '#k1-tag2', {s.loc(T('seconds'))});")
s.add(f"tl.fromTo('#k1-ca', {{ scale: 1 }}, {{ scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }}, {s.loc(T('seconds'))});")
sid = s.shot(tten - 0.06, ttime - 0.06, dark_bg("k")
             + '<div id="k2-face" class="clockface" style="left:90px;top:620px;width:900px;height:520px;font-size:340px;color:#FF5A4F;border-width:24px">0:10</div>'
             + '<div class="clockname" style="left:340px;top:540px">ALEKSANDAR</div>'
             + '<div class="frame-card" style="left:400px;top:200px;width:280px;height:280px;border-radius:50%;background:linear-gradient(#3C7BE0,#1D4FA8);border:10px solid #fff">'
             + f'<svg viewBox="100 60 400 400" width="100%" height="100%">{cheater("k2a", "nervous")}</svg></div>'
             + '<div id="k2-red" style="position:absolute;inset:0;background:#FF2A1F;opacity:0;mix-blend-mode:screen"></div>', dir=-1, push=0.06)
s.add(f"tl.set('#k2-face', {{ innerText: '0:05' }}, {s.loc(T('Five'))});")
s.add(f"tl.set('#k2-face', {{ innerText: '0:00' }}, {s.loc(tzero)});")
s.add(f"tl.fromTo('#k2-red', {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.5 }}, {s.loc(tzero)});")
s.add(f"slam(tl, '#k2-face', '#{sid}-shake', {s.loc(tzero) - 0.13});")
sid = s.shot(ttime - 0.06, tmw - 0.06, dark_bg("k") + CL.format(p="k3") + stamp("k3-stamp", "TIME'S UP", RED, y=330, size=130))
s.add(f"tl.set('#k3-ca', {{ innerText: '0:00' }}, 0);")
s.add(f"slam(tl, '#k3-stamp', '#{sid}-shake', {s.loc(ttime)});")
confetti = "".join(f'<div id="cf{i}" class="confetti" style="left:{60 + (i * 97) % 960}px;top:{-60 - (i * 53) % 300}px;background:{[YELLOW, TEAL, RED, BLUE, LIME][i % 5]}"></div>' for i in range(22))
s.shot(tmw - 0.06, s.end, stream_bg("k", "purple") + char(magnus("k4m", "smug") + hands("k4m", y=760), 540, 560, 1000)
       + bignum("k4-score", "1 – 0", y=200, color="#FFFFFF", size=190, sub="MAGNUS WINS", sub_bg=LIME) + confetti, dir=-1)
s.add(f"popIn(tl, '#k4-score', {s.loc(tmw)});")
s.add(f"part(tl, 'k4m', 'mouth', 'smile', {s.loc(T('wins'))});")
for i in range(22):
    s.add(f"tl.fromTo('#cf{i}', {{ opacity: 1, y: 0, rotation: {i * 37 % 180} }}, {{ y: {1300 + (i * 71) % 500}, rotation: {360 + i * 53}, duration: 1.6, ease: 'none' }}, {s.loc(T('wins')) + (i % 6) * 0.05});")
scenes.append(s)

# ===================== S9 VERDICT 53.1 – 60.95
s = Scene("verdict", 53.1, 60.95)
twh, tsav = T("Which"), T("Savage")
sid = s.shot(s.start, twh - 0.06, room_bg("v") + desk(1450) + char(robot("v1r", "off"), 850, 700, 360)
             + char(cheater("v1a", "nervous") + hands("v1a", y=760), 480, 520, 980)
             + stamp("v1-stamp", "ACCUSED", RED, y=300, size=140))
s.add(f"slam(tl, '#v1-stamp', '#{sid}-shake', {s.loc(T('accused'))});")
s.add(f"part(tl, 'v1r', 'eyes', 'whisper', {s.loc(T('Stockfish', 3))});")
s.add(f"tl.to('#v1r', {{ y: 120, duration: 0.4, ease: 'power2.in' }}, {s.loc(T('Stockfish', 3)) + 0.3});")
sparks = "".join(f'<div id="sp{i}" class="spark" style="left:{420 + (i * 61) % 260}px;top:{560 + (i * 43) % 200}px;rotate:{i * 47}deg"></div>' for i in range(10))
s.shot(twh - 0.06, tsav - 0.06, teal_bg("v") + char(robot("v2r", "on"), 540, 520, 980) + sparks
       + tag("v2-tag", "LOST TO A HUMAN", RED, "#fff", y=260, size=60), dir=-1)
s.add(f"part(tl, 'v2r', 'eyes', 'panic', {s.loc(T('lost'))});")
s.add(f"part(tl, 'v2r', 'mouth', 'talk', {s.loc(T('lost'))});")
s.add(f"popIn(tl, '#v2-tag', {s.loc(T('lost'))});")
s.add(f"tl.to('#v2r', {{ rotation: 8, y: 60, transformOrigin: '50% 90%', duration: 0.6, ease: 'power2.in' }}, {s.loc(T('Magnus', 7)) - 0.1});")
s.add(f"tl.to('#v2r', {{ filter: 'grayscale(1) brightness(0.7)', duration: 0.5 }}, {s.loc(T('Magnus', 7))});")
for i in range(10):
    s.add(f"tl.fromTo('#sp{i}', {{ opacity: 1, x: 0, y: 0 }}, {{ opacity: 0, x: {(i - 5) * 50}, y: {-120 - (i * 31) % 160}, duration: 0.5, ease: 'power2.out' }}, {s.loc(T('lost')) + (i % 4) * 0.05});")
s.shot(tsav - 0.06, s.end, stream_bg("v", "purple") + char(magnus("v3m", "smug") + hands("v3m", y=760), 540, 440, 1160), push=0.09)
s.add(f"blink(tl, 'v3m', {s.loc(tsav) + 0.5});")
scenes.append(s)

# ===================== S10 CTA 60.95 – 66.5
s = Scene("cta", 60.95, TOTAL)
s.shot(s.start, TOTAL - 0.25, stream_bg("z", "blue")
       + f'<div class="frame-card" style="left:50px;top:660px;width:470px;height:580px;background:linear-gradient(#E0503C,#A82A1D);border:12px solid #fff">'
       + f'<svg viewBox="0 0 600 800" width="100%" height="100%">{magnus("z1m", "smug")}</svg></div>'
       + f'<div class="frame-card" style="left:560px;top:660px;width:470px;height:580px;background:linear-gradient(#2A8F8A,#0F3E45);border:12px solid #fff">'
       + f'<svg viewBox="0 0 600 800" width="100%" height="100%">{robot("z1r", "on")}</svg></div>'
       + '<div class="bignum" style="position:absolute;left:0;right:0;top:880px;text-align:center;font-size:120px;color:#fff">VS</div>'
       + tag("z-q", "HOW MANY MOVES VS STOCKFISH?", YELLOW, y=330, size=44)
       + tag("z-c", "COMMENT A NUMBER", TEAL, "#062A27", y=430, size=40)
       + tag("z-f", "FOLLOW THE 64 STORIES", "#FFFFFF", "#1B1B1B", y=520, size=32), push=0.03)
s.add("popIn(tl, '#z-q', 0.1);")
s.add(f"popIn(tl, '#z-c', {s.loc(T('Comment'))});")
s.add(f"popIn(tl, '#z-f', {s.loc(T('number')) + 0.2});")
s.shot(TOTAL - 0.25, TOTAL, '<div style="position:absolute;inset:0;background:#000"></div><div id="z-streak" style="position:absolute;left:340px;top:958px;width:400px;height:4px;border-radius:2px;background:linear-gradient(90deg,transparent,#fff,transparent)"></div>', dir=0, push=0)
scenes.append(s)

os.makedirs("compositions", exist_ok=True)
for sc in scenes:
    sc.write()

# ===================== captions
KEY = {"magnus": BLUE, "carlsen": BLUE, "aleksandar": BLUE, "stockfish": TEAL, "alone": RED, "perfect": LIME, "perfectly": LIME,
       "zero": RED, "up": RED, "wins": LIME, "accused": RED, "lost": RED, "savage": YELLOW, "minute": LIME, "seconds": RED,
       "eighteen": YELLOW, "ninety-two": YELLOW, "champion": YELLOW, "endgame": YELLOW, "human": YELLOW, "time": RED, "number": YELLOW}
groups = []
cur = []
for i, w in enumerate(WORDS):
    cur.append(w)
    end_punct = w["text"][-1] in ".?!,"
    if len(cur) >= 3 or end_punct:
        groups.append(cur)
        cur = []
if cur:
    groups.append(cur)
# the real clip quote, from the source transcript (227.95 = media start)
quote = [("\"Yeah,", 228.38, 228.48), ("this", 228.50, 228.62), ("guy's", 228.66, 228.94), ("playing", 228.96, 229.18), ("really", 229.30, 229.48), ("well.\"", 229.52, 229.68)]
qw = [{"text": t, "start": round(TIMING["clip_start"] + a - 227.95, 3), "end": round(TIMING["clip_start"] + b - 227.95, 3)} for t, a, b in quote]
groups.append(qw[:3])
groups.append(qw[3:])
groups.sort(key=lambda g: g[0]["start"])

cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    gs = max(0.1, g[0]["start"] - 0.05)
    nxt = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else TOTAL - 0.3
    ge = min(max(g[-1]["end"] + 0.25, gs + 0.4), nxt)
    spans = []
    for wi, w in enumerate(g):
        spans.append(f'<span id="cw{gi}-{wi}" class="cw">{w["text"]}</span>')
        key = w["text"].strip(".,?!\"").lower()
        col = KEY.get(key, LIME)
        cap_js.append(f"tl.set('#cw{gi}-{wi}', {{ color: '{col}' }}, {round(w['start'], 3)});")
        if wi + 1 < len(g):
            cap_js.append(f"tl.set('#cw{gi}-{wi}', {{ color: '#FFFFFF' }}, {round(g[wi + 1]['start'], 3)});")
    cap_html.append(f'<div id="cg{gi}" class="cg">{" ".join(spans)}</div>')
    cap_js.append(f"tl.fromTo('#cg{gi}', {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.08, ease: 'power2.out' }}, {round(gs, 3)});")
    cap_js.append(f"tl.set('#cg{gi}', {{ opacity: 0, visibility: 'hidden' }}, {round(ge, 3)});")

open("compositions/captions.html", "w").write(f"""<template id="captions-template">
  <style>
    #root {{ position:absolute; inset:0; pointer-events:none; }}
    .cg {{ position:absolute; left:40px; right:40px; top:1165px; text-align:center; font-family:Nunito, sans-serif; font-weight:900;
          font-size:66px; line-height:1.1; color:#FFFFFF; -webkit-text-stroke:12px #15121A; paint-order:stroke fill;
          text-shadow:0 6px 0 rgba(0,0,0,.35); opacity:0; overflow:visible; }}
    .cw {{ display:inline-block; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
    {''.join(cap_html)}
  </div>
  <script>
    var tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in cap_js)}
    tl.set({{}}, {{}}, {TOTAL});
    window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ===================== fx overlay: flashes, grain, vignette, watermark
FLASH = [T("Stockfish"), T("Even") - 0.06, TIMING["clip_start"], T("Savage") - 0.06, T("Time's") - 0.06]
fx_js = []
for t in FLASH:
    fx_js.append(f"tl.fromTo('#fx-flash', {{ opacity: 0.95 }}, {{ opacity: 0, duration: 0.2, ease: 'power2.out', immediateRender: false }}, {round(t, 3)});")
fx_js.append(f"tl.set('#fx-wm', {{ opacity: 0 }}, {TOTAL - 0.25});")
fx_js.append(f"tl.fromTo('#fx-grain', {{ x: 0, y: 0 }}, {{ x: -320, y: -260, duration: {TOTAL}, ease: 'steps({int(TOTAL * 12)})' }}, 0);")
open("compositions/fx.html", "w").write(f"""<template id="fx-template">
  <style>
    #root {{ position:absolute; inset:0; pointer-events:none; overflow:hidden; }}
    #fx-vig {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.42) 100%); }}
    #fx-grain {{ position:absolute; left:0; top:0; width:1500px; height:2300px; opacity:.07; mix-blend-mode:overlay; }}
    #fx-flash {{ position:absolute; inset:0; background:#FFF6E6; opacity:0; }}
    #fx-wm {{ position:absolute; left:0; right:0; top:1262px; text-align:center; color:#fff; opacity:.18; font-family:Inter,sans-serif; font-weight:800; }}
    #fx-wm b {{ display:block; font-size:34px; }} #fx-wm span {{ font-size:18px; letter-spacing:.06em; }}
  </style>
  <div id="root" data-composition-id="fx" data-width="{W}" data-height="{H}">
    <svg id="fx-grain" viewBox="0 0 1500 2300"><filter id="fx-n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/></filter><rect width="1500" height="2300" filter="url(#fx-n)"/></svg>
    <div id="fx-vig"></div>
    <div id="fx-wm" data-layout-ignore><b>@the64stories</b><span>IF YOU SEE THIS ON YOUTUBE, IT'S STOLEN</span></div>
    <div id="fx-flash"></div>
  </div>
  <script>
    var tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + l for l in fx_js)}
    tl.set({{}}, {{}}, {TOTAL});
    window.__timelines["fx"] = tl;
  </script>
</template>
""")

# ===================== root
hosts = []
for i, sc in enumerate(scenes):
    hosts.append(f'<div id="{sc.sid}" data-composition-id="{sc.sid}" data-composition-src="compositions/{sc.sid}.html" data-start="{sc.start}" '
                 f'data-duration="{sc.dur}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
hosts.append(f'<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" '
             f'data-track-index="1" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:20"></div>')
hosts.append(f'<div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" '
             f'data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:30"></div>')

# audio: VO, music, sfx (peaks one frame after picture)
SFX = []
def sfx(name, t, vol=0.8):
    SFX.append((name, round(t, 3), vol))

whooshes = ["whoosh_a", "whoosh_b", "whoosh_c"]
cuts = sorted({round(sc.start + float(x.split('data-start="')[1].split('"')[0]), 3) for sc in scenes for x in sc.shots})
for k, c in enumerate(cuts):
    if 0.5 < c < TOTAL - 1:
        sfx(whooshes[k % 3], c - 0.05, 0.45)
for w in ("move",):
    pass
for t in (T("move", 1), T("move", 2), T("Aleksandar", 2), T("plays")):
    sfx("piece", t + 0.25, 0.7)
    sfx("pop", t + 0.24, 0.5)
sfx("robot", T("alone") - 0.1, 0.6)
sfx("robot", T("whispering") - 0.1, 0.6)
sfx("stamp", T("Perfect") + 0.1, 0.8)
sfx("stamp", T("Time's") + 0.1, 0.8)
sfx("stamp", T("accused") + 0.1, 0.8)
sfx("ticks", T("seconds") - 0.2, 0.55)
sfx("flag", T("Zero") + 0.03, 0.7)
sfx("impact", T("Zero") - 1.6, 0.8)
sfx("powerdown", T("lost"), 0.7)
sfx("pop", T("Comment"), 0.5)

import subprocess
def adur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
lanes_end = []
sfx_tags = []
for i, (n, t, v) in enumerate(sorted(SFX, key=lambda x: x[1])):
    d = round(min(adur(f"assets/audio/sfx/{n}.mp3"), TOTAL - t), 3)
    lane = next((k for k, e in enumerate(lanes_end) if e <= t), None)
    if lane is None:
        lanes_end.append(0); lane = len(lanes_end) - 1
    lanes_end[lane] = t + d
    sfx_tags.append(f'<audio id="sfx{i}" src="assets/audio/sfx/{n}.mp3" data-start="{t}" data-duration="{d}" data-track-index="{5 + lane}" data-volume="{v}"></audio>')
audio = [f'<audio id="vo1" src="assets/audio/vo_part1_tight.mp3" data-start="{TIMING["p1_start"]}" data-duration="{round(adur('assets/audio/vo_part1_tight.mp3'), 3)}" data-track-index="3" data-volume="1"></audio>',
         f'<audio id="vo2" src="assets/audio/vo_part2_tight.mp3" data-start="{TIMING["p2_start"]}" data-duration="{round(min(adur('assets/audio/vo_part2_tight.mp3'), TOTAL - TIMING["p2_start"]), 3)}" data-track-index="3" data-volume="1"></audio>',
         f'<audio id="music" src="assets/audio/music.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="0.32"></audio>']
audio += sfx_tags

open("index.html", "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#101018; }}
      #root {{ position:relative; width:100%; height:100%; background:#101018; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
      {chr(10).join('      ' + h for h in hosts)}
      {chr(10).join('      ' + a for a in audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("scenes:", len(scenes), "shots:", sum(len(s.shots) for s in scenes), "caption groups:", len(groups), "sfx:", len(SFX))
