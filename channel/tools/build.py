"""Generate a HyperFrames project from SCRIPT timing + a shot list.

Usage: python3 build.py <episode_dir> <shots_module>
Writes <episode_dir>/video/index.html and compositions/{chN,captions,hud,fx}.html.

Shot spec (see ep01_shots.py):
  dict(at=<unit idx>, bg="<preset>" | ("<preset>", {kwargs}), cam=("in"|"out"|"static", amount, "x% y%"),
       svg=[ (id, markup, show) ...],            # SVG items over the background
       html=[ (id, kind, text, x, y, show, extra) ...],   # tags, stamps, clocks...
       acts=[ ("mood", cid, mood, t), ("arm", cid, "L"|"R", deg, t, dur), ("move", cid, dx, dy, t, dur),
              ("shake", t, amp), ("dark", t, to_opacity, dur), ("flash", t), ("ring", id, t, dur),
              ("fade", id, t, to, dur), ("off", sel, t, stagger) ])
  kind="rule"  -> dict(at=<'Rule n.' unit>, kind="rule", n="1", imp="...", last=False)
  kind="chapter" -> dict(at=<chapter unit>, kind="chapter")
Times `t` are word refs: (unit, word_index_or_substring) or ("+", seconds_from_shot_start).
"""
import importlib.util
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import P, svg_filters, BROWS  # noqa: E402
from bgs import BG  # noqa: E402

EP = sys.argv[1]
spec = importlib.util.spec_from_file_location("shots", sys.argv[2])
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

units = json.load(open(f"{EP}/build/units.json"))
timing = json.load(open(f"{EP}/build/timing_fast.json"))
TOTAL = timing["duration"]
T = {u["i"]: u for u in timing["units"]}
OUT = f"{EP}/video"
os.makedirs(f"{OUT}/compositions", exist_ok=True)
CUT_LAG = 0.25
SFX_EVENTS = []  # [abs_time, sound, volume, max_dur]
ORIG = json.load(open(f"{EP}/build/origins.json")) if os.path.exists(f"{EP}/build/origins.json") else {}


def origin_of(sel):
    o = ORIG.get(sel.lstrip("#").removesuffix("-r"))
    if o:
        return 'transformOrigin:"%spx %spx"' % (o[0], o[1])
    return 'transformOrigin:"50% 50%"'


# ---------------------------------------------------------------- timing helpers
def spoken_after(i):
    j = i
    while j not in T and j < len(units):
        j += 1
    return T.get(j)


def spoken_before(i):
    j = i - 1
    while j >= 0 and j not in T:
        j -= 1
    return T.get(j)


def unit_start(i):
    u = spoken_after(i)
    return u["start"] if u else TOTAL


def cut_time(i):
    """Shot boundary for a shot starting at unit i: 0.25 s after the previous line ends,
    but never after the new line starts."""
    prev = spoken_before(i)
    if prev is None:
        return 0.0
    return round(min(prev["end"] + CUT_LAG, unit_start(i) - 0.02), 3)


def word_t(ref, shot_start, shot_at):
    if ref is None:
        return shot_start
    if ref[0] == "+":
        return shot_start + ref[1]
    u, w = ref
    tu = T[u] if u in T else spoken_after(u)
    if isinstance(w, int):
        return tu["words"][w]["s"]
    for x in tu["words"]:
        if w.lower() in x["w"].lower():
            return x["s"]
    raise ValueError(f"word {w!r} not in unit {u}: {tu['text']}")


# ---------------------------------------------------------------- html pieces
CSS = """
@font-face{font-family:"Caveat";src:url("assets/fonts/caveat-600.woff2") format("woff2");font-weight:600}
.hand{font:600 48px Caveat;color:#2a3f8f;white-space:nowrap}
#root{position:absolute;inset:0;overflow:hidden;background:#0a0c14;font-family:Montserrat}
.shot{position:absolute;inset:0;overflow:hidden}
.cam{position:absolute;inset:0}
.cam>svg,.lay>svg{position:absolute;left:0;top:0;width:1920px;height:1080px}
.lay{position:absolute;left:0;top:0;width:1920px;height:1080px}
.it{position:absolute;left:0;top:0}
.tag{font:800 30px Montserrat;letter-spacing:.01em;color:#fff;background:#23232b;padding:9px 18px 8px;border-radius:5px;
  box-shadow:0 6px 0 rgba(0,0,0,.28);white-space:nowrap;display:inline-block}
.tag.y{background:#ffd43b;color:#16161c}.tag.r{background:#ef3b4f}.tag.g{background:#2fae6e}.tag.b{background:#3a6fd8}.tag.w{background:#f4f1ea;color:#16161c}
.stamp{font:900 64px Montserrat;color:#ef3b4f;border:7px solid #ef3b4f;border-radius:10px;padding:6px 24px;white-space:nowrap;display:inline-block;
  background:rgba(10,10,16,.35);text-shadow:0 3px 0 rgba(0,0,0,.3)}
.stamp.g{color:#3fbf7f;border-color:#3fbf7f}
.big{font:900 120px Montserrat;color:#fff;white-space:nowrap;letter-spacing:-.01em;text-shadow:0 8px 0 rgba(0,0,0,.35)}
.big.y{color:#ffd43b}.big.r{color:#ef3b4f}.big.g{color:#3fbf7f}
.sticker{font:900 76px Montserrat;color:#16161c;background:#f4f1ea;padding:10px 30px;border-radius:8px;white-space:nowrap;box-shadow:0 10px 0 rgba(0,0,0,.3)}
.clock{font:700 64px 'JetBrains Mono';color:#7dffc4;background:#0b0d12;padding:8px 26px;border-radius:16px;
  box-shadow:0 0 34px rgba(125,255,196,.25),0 6px 0 rgba(0,0,0,.4);white-space:nowrap}
.clock.r{color:#ff5a6e;box-shadow:0 0 34px rgba(255,90,110,.3),0 6px 0 rgba(0,0,0,.4)}
.bubble{font:800 30px Montserrat;color:#fff;background:#15151c;border:2px solid #ffd43b;border-radius:14px;padding:14px 22px;white-space:nowrap;position:relative}
.bubble:after{content:"";position:absolute;left:34px;bottom:-16px;border:9px solid transparent;border-top:12px solid #ffd43b}
.dark{position:absolute;inset:0;background:#02030a;opacity:0}
.flash{position:absolute;inset:0;background:#fff;opacity:0}
/* cards */
.rnum{position:absolute;font:400 330px 'Archivo Black';line-height:1;color:#ef3b4f;text-shadow:-10px 12px 0 #a3182c,-18px 22px 30px rgba(0,0,0,.45)}
.rnum.last{color:#ffd43b;text-shadow:-10px 12px 0 #b38f12,-18px 22px 30px rgba(0,0,0,.45)}
.rword{position:absolute;font:900 92px Montserrat;color:#fff;letter-spacing:.02em}
.rimp{position:absolute;font:900 44px Montserrat;color:#16161c;background:#ffd43b;padding:14px 26px;border-radius:6px;white-space:nowrap;box-shadow:0 8px 0 rgba(0,0,0,.35)}
.rdots{position:absolute;display:flex;gap:10px}
.rdots i{width:26px;height:26px;border-radius:50%;background:#2d2e38;display:block}
.rdots i.on{background:#ef3b4f}.rdots i.cur{background:#ef3b4f;box-shadow:0 0 0 5px rgba(239,59,79,.35)}.rdots i.lst{background:#5a4a14}
.chl{position:absolute;left:0;right:0;text-align:center;font:800 40px Montserrat;letter-spacing:.32em;color:#ffd43b}
.cht{position:absolute;left:0;right:0;text-align:center;font:900 112px Montserrat;color:#fff;letter-spacing:.005em}
.chu{position:absolute;height:10px;background:#ef3b4f;border-radius:5px}
.chline{position:absolute;display:flex;gap:0;align-items:center}
.chnode{display:flex;flex-direction:column;align-items:center;width:200px;font:800 20px Montserrat;letter-spacing:.12em;color:#5d5f6b}
.chnode b{width:22px;height:22px;border-radius:50%;background:#3a3b47;margin-bottom:14px;display:block}
.chnode.cur{color:#ffd43b}.chnode.cur b{background:#ffd43b;box-shadow:0 0 0 6px rgba(255,212,59,.25)}
.chnode.done{color:#9a9ca8}.chnode.done b{background:#9a9ca8}
"""


def tl_line(s):
    return "    " + s + "\n"


class Shot:
    def __init__(self, sid, d, start, end):
        self.id, self.d, self.start, self.end = sid, d, start, end
        self.svg, self.html, self.js = [], [], []

    def t(self, ref):
        return round(word_t(ref, self.start, self.d.get("at")) - self.start, 3)


def pop_js(sel, t, kind="pop", rot=0, svg=False):
    org = origin_of(sel) if svg else 'transformOrigin:"50% 50%"'
    if kind == "pop":
        return (f'tl.fromTo("{sel}",{{scale:0,rotation:{rot},opacity:0}},{{scale:1,rotation:{rot},opacity:1,duration:0.26,'
                f'ease:"back.out(2.6)",{org}}},{t:.3f});')
    if kind == "slam":
        return (f'tl.fromTo("{sel}",{{scale:1.9,rotation:{rot},opacity:0}},{{scale:1,rotation:{rot},opacity:1,duration:0.16,'
                f'ease:"power4.in",{org}}},{t:.3f});')
    if kind == "fade":
        return f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:0.3,ease:"power2.out"}},{t:.3f});'
    if kind == "rise":
        return (f'tl.fromTo("{sel}",{{y:40,opacity:0,rotation:{rot}}},{{y:0,opacity:1,rotation:{rot},duration:0.32,ease:"expo.out"}},{t:.3f});')
    if kind == "blur":
        return (f'tl.fromTo("{sel}",{{opacity:0,filter:"blur(10px)",rotation:{rot}}},{{opacity:1,filter:"blur(0px)",rotation:{rot},'
                f'duration:0.2,ease:"power3.out"}},{t:.3f});')
    if kind == "none":
        return ""
    raise ValueError(kind)


def shake_js(sel, t, amp=10, n=6):
    out = []
    import random
    rnd = random.Random(int(t * 1000))
    dt = 0.035
    for k in range(n):
        a = amp * (1 - k / n)
        out.append(f'tl.to("{sel}",{{x:{rnd.uniform(-a,a):.1f},y:{rnd.uniform(-a,a):.1f},duration:{dt},ease:"none"}},{t+k*dt:.3f});')
    out.append(f'tl.to("{sel}",{{x:0,y:0,duration:{dt},ease:"none"}},{t+n*dt:.3f});')
    return "".join(out)


def build_scene_shot(sh, chars_in_shot):
    d = sh.d
    sid = sh.id
    dur = sh.end - sh.start
    bg = d.get("bg", "stage")
    if isinstance(bg, tuple):
        bgsvg = BG[bg[0]](**bg[1])
    else:
        bgsvg = BG[bg]()
    dur = sh.end - sh.start
    svg_items = []
    pending = []  # [t, selector, kind, rot, is_svg]
    static_items = 0
    pre = f"{sid}-"
    for item in d.get("svg", []):
        iid, markup, show = item[0], item[1].replace("@", pre), item[2] if len(item) > 2 else None
        flt = f"<defs>{svg_filters()}</defs>" if "url(#" in markup else ""
        svg_items.append(f'<div class="lay" id="{sid}-{iid}"><div class="lay" id="{sid}-{iid}-r">'
                         f'<svg viewBox="0 0 1920 1080">{flt}<g id="{sid}-{iid}-g">{markup}</g></svg></div></div>')
        if show:
            kind = show[2] if len(show) > 2 else "pop"
            pending.append([sh.t(show[:2]), f"#{sid}-{iid}", kind, 0, True])
        else:
            static_items += 1
    for item in d.get("html", []):
        iid, kind, text, x, y = item[:5]
        show = item[5] if len(item) > 5 else None
        extra = item[6] if len(item) > 6 else {}
        rot = extra.get("rot", {"tag": -2, "stamp": -8, "sticker": 3, "clock": -2}.get(kind.split()[0], 0))
        cls = kind
        sh.html.append(f'<div class="it" style="left:{x}px;top:{y}px"><div id="{sid}-{iid}" class="{cls}">{text}</div></div>')
        anim = extra.get("anim", {"stamp": "slam", "big": "blur", "sticker": "slam"}.get(kind.split()[0], "pop"))
        t = sh.t(show) if show else 0.15
        if show is None:
            sh.js.append(f'tl.set("#{sid}-{iid}",{{rotation:{rot}}},0);')
            static_items += 1
        else:
            need = 0.5 + 0.3 * max(1, len(str(text).split())) + 0.1
            if t + need > dur:  # too close to the cut to be read: land it earlier
                t = max(0.3, dur - need)
            pending.append([t, f"#{sid}-{iid}", anim, rot, False])
        if "out" in extra:
            sh.js.append(f'tl.to("#{sid}-{iid}",{{opacity:0,scale:0.8,duration:0.15,ease:"power2.in"}},{sh.t(extra["out"]):.3f});')
    # a shot whose background is the bare stage must not sit empty: bring the first beat forward
    bare = (d.get("bg", "stage") == "stage") and static_items == 0
    if pending and bare:
        first = min(p[0] for p in pending)
        if first > 0.8:
            for p in pending:
                if p[0] == first:
                    p[0] = 0.3
    npop = 0
    for t, sel, anim, rot, is_svg in pending:
        sh.js.append(pop_js(sel, t, anim, rot, svg=is_svg))
        if anim == "slam":
            SFX_EVENTS.append([sh.start + t + 0.12, "stamp", 0.55, None])
        elif anim == "pop" and not is_svg:
            SFX_EVENTS.append([sh.start + t, "pop1" if npop % 2 else "pop2", 0.16, None])
            npop += 1
        if anim == "slam":
            sh.js.append(shake_js(f"#{sid}-cam", t + 0.16, 9))
    # camera
    cam = d.get("cam", ("in", 1.05, "50% 50%"))
    mode, amt, origin = (cam + (1.05, "50% 50%"))[:3] if isinstance(cam, tuple) else (cam, 1.05, "50% 50%")
    if mode == "in":
        sh.js.insert(0, f'tl.fromTo("#{sid}-cam",{{scale:1}},{{scale:{amt},duration:{dur:.3f},ease:"sine.inOut",transformOrigin:"{origin}"}},0);')
    elif mode == "out":
        sh.js.insert(0, f'tl.fromTo("#{sid}-cam",{{scale:{amt}}},{{scale:1,duration:{dur:.3f},ease:"sine.out",transformOrigin:"{origin}"}},0);')
    # blinks for every character in the shot (deterministic schedule)
    import re as _re
    chars_in_shot = [(c, -262) for c in _re.findall(r'id="([^"]+)" class="char"', "".join(svg_items))]
    closed = {a[1].replace("@", pre) for a in d.get("acts", []) if a[0] == "eyes" and a[2]}
    for cid, hy in chars_in_shot:
        if cid in closed:
            continue
        tb = 0.9 + (hash(cid) % 7) * 0.13
        while tb < dur - 0.3:
            sh.js.append(f'tl.to("#{cid}-eyes",{{attr:{{transform:"translate(0 {hy}) scale(1 0.12) translate(0 {-hy})"}},duration:0.06}},{tb:.3f});'
                         f'tl.to("#{cid}-eyes",{{attr:{{transform:"translate(0 {hy}) scale(1 1) translate(0 {-hy})"}},duration:0.08}},{tb+0.08:.3f});')
            tb += 3.1 + (hash(cid + str(int(tb))) % 9) * 0.21
    # actions
    for a in d.get("acts", []):
        a = tuple(x.replace("@", pre) if isinstance(x, str) else x for x in a)
        k = a[0]
        if k == "eyes":
            _, cid, closed_, ref = a
            sc = 0.12 if closed_ else 1
            sh.js.append(f'tl.set("#{cid}-eyes",{{attr:{{transform:"translate(0 -262) scale(1 {sc}) translate(0 262)"}}}},{sh.t(ref):.3f});')
            continue
        if k == "mood":
            _, cid, mood, ref = a
            t = sh.t(ref)
            lb, rb, dy = BROWS[mood]
            sh.js.append(f'tl.to("#{cid}-browL",{{attr:{{transform:"translate(0 {dy}) rotate({lb} -6 -281)"}},duration:0.14,ease:"power2.out"}},{t:.3f});'
                         f'tl.to("#{cid}-browR",{{attr:{{transform:"translate(0 {dy}) rotate({rb} 6 -281)"}},duration:0.14,ease:"power2.out"}},{t:.3f});')
            mouth = {"neutral": "line", "happy": "smile", "scared": "open", "sad": "frown", "worried": "line",
                     "shock": "o", "creepy": "smile", "angry": "frown"}[mood]
            for m in ("line", "open", "smile", "frown", "o"):
                sh.js.append(f'tl.set("#{cid}-m-{m}",{{opacity:{1 if m == mouth else 0}}},{t:.3f});')
        elif k == "talk":  # mouth flap between open/line for a stretch
            _, cid, ref, n = a
            t = sh.t(ref)
            for j in range(n):
                tt = t + j * 0.16
                sh.js.append(f'tl.set("#{cid}-m-open",{{opacity:{1 if j % 2 == 0 else 0}}},{tt:.3f});tl.set("#{cid}-m-line",{{opacity:{0 if j % 2 == 0 else 1}}},{tt:.3f});')
        elif k == "arm":
            _, cid, side, deg, ref, du = a
            sx = -46 if side == "L" else 46
            sh.js.append(f'tl.to("#{cid}-arm{side}",{{attr:{{transform:"rotate({deg} {sx} -204)"}},duration:{du},ease:"power3.out"}},{sh.t(ref):.3f});')
        elif k == "move":
            _, cid, x2, y2, ref, du = a[:6]
            ease = a[6] if len(a) > 6 else "power2.inOut"
            sh.js.append(f'tl.to("#{sid}-{cid}",{{x:{x2},y:{y2},duration:{du},ease:"{ease}"}},{sh.t(ref):.3f});')
        elif k == "shake":
            _, ref, amp = a
            sh.js.append(shake_js(f"#{sid}-cam", sh.t(ref), amp))
        elif k == "dark":
            _, ref, to, du = a
            sh.js.append(f'tl.to("#{sid}-dark",{{opacity:{to},duration:{du},ease:"power2.inOut"}},{sh.t(ref):.3f});')
        elif k == "flash":
            _, ref = a
            t = sh.t(ref)
            sh.js.append(f'tl.fromTo("#{sid}-flash",{{opacity:0.85}},{{opacity:0,duration:0.22,ease:"power2.out",immediateRender:false}},{t:.3f});')
        elif k == "ring":  # vibrate an svg item
            _, iid, ref, du = a
            t = sh.t(ref)
            n = int(du / 0.05)
            org = origin_of(f"{sid}-{iid}-r")
            sh.js.append(f'tl.fromTo("#{sid}-{iid}-r",{{rotation:-5}},{{rotation:5,duration:0.05,repeat:{n},yoyo:true,ease:"none",{org}}},{t:.3f});'
                         f'tl.to("#{sid}-{iid}-r",{{rotation:0,duration:0.05}},{t+du+0.05:.3f});')
        elif k == "fade":
            _, iid, ref, to, du = a
            sh.js.append(f'tl.to("#{sid}-{iid}",{{opacity:{to},duration:{du},ease:"power2.inOut"}},{sh.t(ref):.3f});')
        elif k == "off":  # windows/lights go dark one by one
            _, sel, ref, stag = a
            sh.js.append(f'tl.to("#{sid}-cam {sel}",{{attr:{{fill:"#0d1428"}},opacity:1,duration:0.08,stagger:{stag}}},{sh.t(ref):.3f});')
        elif k == "js":
            sh.js.append(a[1].replace("$", f"#{sid}-").replace("%T%", f"{sh.t(a[2]):.3f}"))
    svg = f'<svg viewBox="0 0 1920 1080"><defs>{svg_filters()}</defs>{bgsvg}</svg>' + "".join(svg_items)
    body = (f'<div class="cam" id="{sid}-cam">{svg}{"".join(sh.html)}</div>'
            f'<div class="dark" id="{sid}-dark" data-layout-ignore></div><div class="flash" id="{sid}-flash" data-layout-ignore></div>')
    return body


def build_rule_shot(sh, rules_total):
    d = sh.d
    sid = sh.id
    n, imp, last = d["n"], d["imp"], d.get("last", False)
    t_num = max(0.35, sh.t((d["at"], 0)) - 0.3)
    imp_unit = d["at"] + 1
    t_imp = sh.t((imp_unit, 0))
    idx = int(d.get("idx", n))
    dots = "".join(f'<i class="{"cur" if k == idx else ("on" if k < idx else ("lst" if k == rules_total else ""))}"></i>'
                   for k in range(1, rules_total + 1))
    numtxt = n
    two = len(numtxt) > 1
    nx, tx = (300, 820) if two else (440, 760)
    fs = 44 if len(imp) <= 26 else (38 if len(imp) <= 32 else 32)
    body = (f'<div class="cam" id="{sid}-cam"><svg viewBox="0 0 1920 1080">{BG["stage"](seed=int(idx) + 10)}</svg>'
            f'<div id="{sid}-num" class="rnum{" last" if last else ""}" style="left:{nx}px;top:260px">{numtxt}</div>'
            f'<div id="{sid}-word" class="rword" style="left:{tx}px;top:330px">{"LAST RULE" if last else "RULE"}</div>'
            f'<div class="it" style="left:{tx}px;top:470px"><div id="{sid}-imp" class="rimp" style="font-size:{fs}px">{imp}</div></div>'
            f'<div id="{sid}-dots" class="rdots" style="left:{960 - rules_total * 18 + 5}px;top:720px">{dots}</div>'
            f'</div><div class="flash" id="{sid}-flash" data-layout-ignore></div>')
    dur = sh.end - sh.start
    sh.js += [
        f'tl.fromTo("#{sid}-cam",{{scale:1}},{{scale:1.045,duration:{dur:.3f},ease:"sine.inOut",transformOrigin:"45% 45%"}},0);',
        f'tl.fromTo("#{sid}-num",{{scale:1.6,opacity:0,filter:"blur(14px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:0.22,ease:"power4.in",transformOrigin:"50% 60%"}},{t_num:.3f});',
        shake_js(f"#{sid}-cam", t_num + 0.22, 12),
        SFX_EVENTS.append([sh.start + t_num + 0.2, "impact1" if int(idx) % 2 else "impact2", 0.7, None]) or "",
        SFX_EVENTS.append([sh.start + t_imp, "pop2", 0.2, None]) or "",
        f'tl.fromTo("#{sid}-word",{{x:-30,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"expo.out"}},{t_num + 0.16:.3f});',
        pop_js(f"#{sid}-imp", t_imp, "pop", -2),
        f'tl.fromTo("#{sid}-dots",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,ease:"expo.out"}},{t_num + 0.3:.3f});',
    ]
    return body


CHAPTERS = None


def build_chapter_shot(sh, chapter_list, cur):
    sid = sh.id
    title = units[sh.d["at"]]["title"]
    head, _, name = title.partition("·")
    spoken = spoken_after(sh.d["at"])
    t_head = max(0.3, spoken["start"] - sh.start - 0.25)
    nodes = "".join(f'<div class="chnode{" cur" if k == cur else (" done" if k < cur else "")}"><b></b>{c}</div>'
                    for k, c in enumerate(chapter_list))
    body = (f'<div class="cam" id="{sid}-cam"><svg viewBox="0 0 1920 1080">{BG["stage"](seed=40 + cur)}</svg>'
            f'<div id="{sid}-l" class="chl" style="top:330px">{head.strip()}</div>'
            f'<div id="{sid}-t" class="cht" style="top:390px">{name.strip()}</div>'
            f'<div id="{sid}-u" class="chu" style="left:810px;width:300px;top:540px"></div>'
            f'<div id="{sid}-n" class="chline" style="left:{960 - len(chapter_list) * 100}px;top:650px">{nodes}</div>'
            f'</div>')
    dur = sh.end - sh.start
    sh.js += [
        f'tl.fromTo("#{sid}-cam",{{scale:1.04}},{{scale:1,duration:{dur:.3f},ease:"sine.out"}},0);',
        f'tl.fromTo("#{sid}-l",{{opacity:0,filter:"blur(8px)",y:-14}},{{opacity:1,filter:"blur(0px)",y:0,duration:0.4,ease:"expo.out"}},{t_head:.3f});',
        SFX_EVENTS.append([sh.start + t_head + 0.3, "whoosh", 0.45, None]) or "",
        SFX_EVENTS.append([sh.start + t_head + 0.55, "impact2", 0.5, None]) or "",
        f'tl.fromTo("#{sid}-t",{{opacity:0,filter:"blur(10px)",scale:1.08}},{{opacity:1,filter:"blur(0px)",scale:1,duration:0.28,ease:"power3.out"}},{t_head + 0.55:.3f});',
        f'tl.fromTo("#{sid}-u",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"expo.out",transformOrigin:"50% 50%"}},{t_head + 0.75:.3f});',
        f'tl.fromTo("#{sid}-n",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},{t_head + 0.9:.3f});',
    ]
    return body


# ---------------------------------------------------------------- assemble shots
shots_spec = S.SHOTS
if getattr(S, "END_AT", None):
    TOTAL = round(spoken_before(S.END_AT)["end"] + 1.2, 3)
    timing["units"] = [u for u in timing["units"] if u["start"] < TOTAL]
RULES_TOTAL = S.RULES_TOTAL
chapter_units = [i for i, u in enumerate(units) if u["kind"] == "chapter"]
chapter_names = S.CHAPTER_NODES  # labels for the chapter timeline

shots = []
for k, d in enumerate(shots_spec):
    start = 0.0 if k == 0 else cut_time(d["at"])
    if d.get("kind") == "chapter":
        prev = spoken_before(d["at"])
        start = round(prev["end"] + CUT_LAG, 3) if prev else 0.0
    shots.append([start, d])
for k in range(len(shots)):
    end = shots[k + 1][0] if k + 1 < len(shots) else TOTAL
    shots[k].append(end)

# group into chapters (one sub-composition per chapter unit)
chap_of = []
for start, d, end in shots:
    ci = max([j for j, cu in enumerate(chapter_units) if cu <= d["at"]] or [0])
    chap_of.append(ci)

hosts = []
hud_spans = []  # (start, end, chapter label, rules_done)
rule_count = 0
ch_cur = -1
for ci in sorted(set(chap_of)):
    idxs = [k for k in range(len(shots)) if chap_of[k] == ci]
    c0 = shots[idxs[0]][0]
    c1 = shots[idxs[-1]][2]
    parts, js = [], []
    for k in idxs:
        start, d, end = shots[k]
        sh = Shot(f"c{ci}s{k}", d, start, end)
        kind = d.get("kind", "scene")
        if kind == "rule":
            body = build_rule_shot(sh, RULES_TOTAL)
            rule_count = int(d.get("idx", d["n"]))
        elif kind == "chapter":
            ch_cur += 1
            body = build_chapter_shot(sh, chapter_names, ch_cur)
        else:
            chars = d.get("chars_meta", [])
            body = build_scene_shot(sh, chars)
            hud_spans.append((start, end, S.CHAPTER_PILLS[ci], rule_count))
        ls, ld = round(start - c0, 3), round(end - start, 3)
        parts.append(f'<div id="{sh.id}" class="shot clip" data-start="{ls}" data-duration="{ld}" data-track-index="0">{body}</div>')
        # shot-local times -> chapter-local
        js.append(f"  // shot {sh.id} @ {start:.2f}s\n  (function(root){{const off={ls};const tl=gsap.timeline();\n"
                  + "".join(tl_line(x) for x in sh.js if x)
                  + f"  root.add(tl,off);}})(tl);\n")
    cid = f"ch{ci}"
    html = (f'<template>\n<style>{CSS}</style>\n<div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" '
            f'data-layout-allow-overflow data-layout-allow-overlap>\n' + "\n".join(parts) +
            f'\n</div>\n<script>\n  const tl = gsap.timeline({{ paused: true }});\n' + "".join(js) +
            f'  window.__timelines["{cid}"] = tl;\n</script>\n</template>\n')
    open(f"{OUT}/compositions/{cid}.html", "w").write(html)
    hosts.append((cid, c0, c1 - c0))
    print(cid, f"{c0:.1f}-{c1:.1f}s", len(idxs), "shots")

# ---------------------------------------------------------------- captions
WEAK = {"the", "a", "an", "to", "of", "in", "on", "at", "and", "but", "or", "who", "your", "my", "his", "her", "it", "is",
        "that", "with", "for", "from", "by", "as", "if", "you", "they", "we", "he", "she", "be", "was", "are", "not", "no"}


def caption_groups():
    groups = []
    for u in timing["units"]:
        ws = u["words"]
        cur = []
        for j, w in enumerate(ws):
            cur.append(w)
            end_sent = w["w"][-1] in ".!?"
            comma = w["w"][-1] in ",;:"
            nxt_gap = ws[j + 1]["s"] - w["e"] if j + 1 < len(ws) else 9
            weak = w["w"].lower().strip(",.") in WEAK
            nxt_weak_ok = j + 1 < len(ws)
            if end_sent or (comma and len(cur) >= 2) or (nxt_gap > 0.15 and len(cur) >= 2):
                groups.append(cur)
                cur = []
            elif len(cur) >= 4 and not weak:
                groups.append(cur)
                cur = []
            elif len(cur) >= 5:
                groups.append(cur[:-1])
                cur = cur[-1:]
        if cur:
            groups.append(cur)
    return groups


cg = caption_groups()
cap_parts = []
for k, g in enumerate(cg):
    s = max(0.05, g[0]["s"] - 0.04)
    nxt = cg[k + 1][0]["s"] - 0.04 if k + 1 < len(cg) else TOTAL
    e = min(nxt, g[-1]["e"] + 0.6)
    words = []
    for w in g:
        txt = w["w"].upper().replace("&", "&amp;").replace('"', "&quot;")
        txt = txt.rstrip(".,;:") if not txt.endswith("?") and not txt.endswith("...") else txt
        cls = f' class="{w["c"]}"' if w["c"] else ""
        words.append(f"<span{cls}>{txt}</span>")
    cap_parts.append(f'<div id="cg{k}" class="cg clip" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="0">'
                     f'<div class="cgi" id="cgi{k}">{" ".join(words)}</div></div>')
cap_html = f"""<template>
<style>
#root{{position:absolute;inset:0;pointer-events:none}}
.cg{{position:absolute;left:0;right:0;top:948px;text-align:center}}
.cgi{{display:inline-block;font:900 58px Montserrat;color:#fff;letter-spacing:.01em;
  text-shadow:0 4px 0 rgba(0,0,0,.55),0 0 22px rgba(0,0,0,.6)}}
.cgi .y{{color:#ffd43b}}.cgi .r{{color:#ff4a5f}}.cgi .g{{color:#48d58f}}.cgi .b{{color:#6fa0ff}}
</style>
<div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-layout-allow-overflow>
{chr(10).join(cap_parts)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join(f'  tl.fromTo("#cgi{k}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.08,ease:"power2.out"}},{max(0.05, g[0]["s"] - 0.04):.3f});' for k, g in enumerate(cg))}
  window.__timelines["captions"] = tl;
</script>
</template>
"""
open(f"{OUT}/compositions/captions.html", "w").write(cap_html)

# ---------------------------------------------------------------- HUD (merge adjacent spans)
merged = []
for s, e, lab, rc in hud_spans:
    if merged and abs(merged[-1][1] - s) < 0.01 and merged[-1][2] == lab and merged[-1][3] == rc:
        merged[-1][1] = e
    else:
        merged.append([s, e, lab, rc])
hud_parts = []
for k, (s, e, lab, rc) in enumerate(merged):
    dots = "".join(f'<i class="{"on" if j <= rc else ("lst" if j == RULES_TOTAL else "")}">{j}</i>' for j in range(1, RULES_TOTAL + 1))
    hud_parts.append(f'<div id="h{k}" class="hs clip" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="0">'
                     f'<div class="pill">{lab}</div><div class="dots" data-layout-ignore>{dots}</div></div>')
hud_html = f"""<template>
<style>
#root{{position:absolute;inset:0;pointer-events:none}}
.hs{{position:absolute;inset:0}}
.pill{{position:absolute;left:52px;top:44px;font:800 22px Montserrat;letter-spacing:.16em;color:#ffd43b;background:rgba(10,10,16,.92);
  border:2px solid #3a3a46;border-radius:30px;padding:12px 26px 11px}}
.dots{{position:absolute;right:52px;top:46px;display:flex;gap:8px}}
.dots i{{width:34px;height:34px;border-radius:50%;background:rgba(32,33,42,.92);color:#a9abb8;font:800 14px/34px Montserrat;text-align:center;font-style:normal;display:block}}
.dots i.on{{background:#ef3b4f;color:#fff}}.dots i.lst{{background:#3a3420;color:#ffd43b}}
</style>
<div id="root" data-composition-id="hud" data-width="1920" data-height="1080">
{chr(10).join(hud_parts)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  window.__timelines["hud"] = tl;
</script>
</template>
"""
open(f"{OUT}/compositions/hud.html", "w").write(hud_html)

# ---------------------------------------------------------------- film fx: vignette, grain, dust
import random  # noqa: E402
rnd = random.Random(11)
dust = []
for k in range(36):
    x, y, r = rnd.uniform(0, 1920), rnd.uniform(0, 1080), rnd.choice([1.5, 2, 2.5, 3])
    dust.append((k, x, y, r, rnd.uniform(18, 40), rnd.uniform(-60, 60)))
fx_html = f"""<template>
<style>
#root{{position:absolute;inset:0;pointer-events:none}}
#vig{{position:absolute;inset:0;background:radial-gradient(ellipse 75% 70% at 50% 46%,rgba(0,0,0,0) 52%,rgba(0,0,0,.58) 100%)}}
#grain{{position:absolute;left:-200px;top:-200px;width:2320px;height:1480px;opacity:.09;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='4'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}}
.dust{{position:absolute;border-radius:50%;background:#fff}}
</style>
<div id="root" data-composition-id="fx" data-width="1920" data-height="1080" data-layout-ignore>
<div id="vig"></div><div id="grain"></div>
{"".join(f'<div id="d{k}" class="dust" style="left:{x:.0f}px;top:{y:.0f}px;width:{r*2}px;height:{r*2}px;opacity:{0.08 + r/30:.2f}"></div>' for k, x, y, r, _, _ in dust)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#grain",{{x:0,y:0}},{{x:-187,y:-131,duration:{TOTAL:.2f},ease:"steps({int(TOTAL * 12)})"}},0);
{chr(10).join(f'  tl.fromTo("#d{k}",{{y:0,x:0}},{{y:-{sp * TOTAL / 10:.0f},x:{dx * TOTAL / 60:.0f},duration:{TOTAL:.2f},ease:"none"}},0);' for k, x, y, r, sp, dx in dust)}
  window.__timelines["fx"] = tl;
</script>
</template>
"""
open(f"{OUT}/compositions/fx.html", "w").write(fx_html)

# ---------------------------------------------------------------- root
audio = [f'<audio id="mix" class="clip" src="assets/audio/mix.m4a" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="10" data-volume="1"></audio>']
for a in getattr(S, "AUDIO", []):
    audio.append(a)
host_html = "\n".join(
    f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s:.3f}" '
    f'data-duration="{dur:.3f}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
    for cid, s, dur in hosts)
root = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #0a0c14; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: Montserrat; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1920" data-height="1080">
{host_html}
      <div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:5"></div>
      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:6"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="3" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:7"></div>
      {chr(10).join("      " + a for a in audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(f"{OUT}/index.html", "w").write(root)
for u, w, name, vol, mx in getattr(S, "SFX", []):
    if isinstance(w, str) and w.startswith("+"):
        t = cut_time(u) + float(w[1:])
    else:
        t = word_t((u, w), 0, None)
    if t < TOTAL:
        SFX_EVENTS.append([t, name, vol, mx])
dips = []
for u, w, g, du in getattr(S, "MUSIC_DIPS", []):
    t = word_t((u, w), 0, None)
    dips.append([t - 0.6, g, du])
json.dump({"duration": TOTAL, "events": sorted(SFX_EVENTS), "dips": dips,
           "music_switch": cut_time(getattr(S, "MUSIC_SWITCH_AT", 105))}, open(f"{EP}/build/sfx_events.json", "w"))
print("total", f"{TOTAL:.1f}s", len(shots), "shots,", len(cg), "caption groups,", len(merged), "hud spans")
