"""Flat 2D character rigs for The 64 Stories, emitted as inline SVG.

Each character is a <g> in a 600x800 box. Expression parts are separate groups
(`{p}-brow-*`, `{p}-lid-*`, `{p}-mouth-*`) so a scene timeline can switch them with
opacity. `expr` picks which ones are visible at frame 0.
"""

SKIN = "#F3CBA6"
SKIN_SH = "#E2AE87"
SKIN_DEEP = "#C98E68"
BLUSH = "#F39A93"
INK = "#2B2220"


def _vis(on):
    return "1" if on else "0"


def _eyes(p, iris="#5B3A22", lids=None, look=(0, 0)):
    """Eyes + eyelid variants. lids: name of the visible lid group."""
    lx, ly = look
    out = []
    for side, cx in (("l", 238), ("r", 362)):
        out.append(
            f'<g id="{p}-eye-{side}">'
            f'<ellipse cx="{cx}" cy="318" rx="37" ry="33" fill="#FFFFFF"/>'
            f'<g id="{p}-iris-{side}" transform="translate({lx} {ly})">'
            f'<circle cx="{cx}" cy="320" r="17" fill="{iris}"/>'
            f'<circle cx="{cx}" cy="320" r="9" fill="#1A1210"/>'
            f'<circle cx="{cx + 6}" cy="313" r="5" fill="#FFFFFF"/>'
            f"</g></g>"
        )
    # lid variants cover the top of the eye in skin + a thick lash line
    lid_defs = {
        "open": (lambda cx: f'<path d="M{cx-38},304 Q{cx},278 {cx+38},304" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'),
        "smug": (lambda cx: f'<path d="M{cx-40},290 L{cx+40},290 L{cx+40},317 Q{cx},309 {cx-40},317 Z" fill="{SKIN}"/>'
                 f'<path d="M{cx-38},317 Q{cx},307 {cx+38},317" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'),
        "wide": (lambda cx: f'<path d="M{cx-36},300 Q{cx},270 {cx+36},300" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'),
        "closed": (lambda cx: f'<path d="M{cx-40},286 L{cx+40},286 L{cx+40},352 L{cx-40},352 Z" fill="{SKIN}"/>'
                   f'<path d="M{cx-34},322 Q{cx},334 {cx+34},322" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'),
    }
    for name, fn in lid_defs.items():
        out.append(f'<g id="{p}-lid-{name}" opacity="{_vis(lids == name)}">{fn(238)}{fn(362)}</g>')
    return "".join(out)


def _brows(p, color, which):
    shapes = {
        "flat": ((238, 262, 0), (362, 262, 0)),
        "smug": ((238, 268, 8), (362, 256, -12)),
        "worried": ((238, 258, -16), (362, 258, 16)),
        "angry": ((238, 266, 18), (362, 266, -18)),
        "up": ((238, 244, -4), (362, 244, 4)),
    }
    out = []
    for name, ((x1, y1, a1), (x2, y2, a2)) in shapes.items():
        out.append(
            f'<g id="{p}-brow-{name}" opacity="{_vis(which == name)}" fill="{color}">'
            f'<rect x="{x1-38}" y="{y1-10}" width="76" height="20" rx="10" transform="rotate({a1} {x1} {y1})"/>'
            f'<rect x="{x2-38}" y="{y2-10}" width="76" height="20" rx="10" transform="rotate({a2} {x2} {y2})"/>'
            f"</g>"
        )
    return "".join(out)


def _mouths(p, which, lip="#8E3B33"):
    m = {
        "flat": f'<path d="M268,420 Q300,424 332,420" fill="none" stroke="{lip}" stroke-width="8" stroke-linecap="round"/>',
        "smirk": f'<path d="M262,418 Q300,428 330,414 Q340,408 346,398" fill="none" stroke="{lip}" stroke-width="8" stroke-linecap="round"/>',
        "smile": f'<path d="M258,408 Q300,452 342,408 Z" fill="#7A2A25"/><path d="M270,412 Q300,424 330,412 L330,416 Q300,428 270,416Z" fill="#FFF"/>',
        "o": f'<ellipse cx="300" cy="424" rx="20" ry="26" fill="#6B2420"/><ellipse cx="300" cy="436" rx="11" ry="8" fill="#E06A6A"/>',
        "grit": f'<rect x="254" y="402" width="92" height="34" rx="14" fill="#FFFFFF" stroke="{lip}" stroke-width="6"/>'
        + "".join(f'<line x1="{x}" y1="404" x2="{x}" y2="434" stroke="#C9B9B2" stroke-width="3"/>' for x in range(270, 340, 13))
        + f'<line x1="256" y1="419" x2="344" y2="419" stroke="#C9B9B2" stroke-width="3"/>',
        "worry": f'<path d="M266,428 Q300,408 334,428" fill="none" stroke="{lip}" stroke-width="8" stroke-linecap="round"/>',
    }
    return "".join(f'<g id="{p}-mouth-{k}" opacity="{_vis(which == k)}">{v}</g>' for k, v in m.items())


def _head(p, extra_back="", extra_front="", beard=""):
    return (
        extra_back
        # ears
        + f'<ellipse cx="150" cy="330" rx="30" ry="40" fill="{SKIN}"/><path d="M146,312 Q160,330 148,350" stroke="{SKIN_SH}" stroke-width="7" fill="none" stroke-linecap="round"/>'
        + f'<ellipse cx="450" cy="330" rx="30" ry="40" fill="{SKIN}"/><path d="M454,312 Q440,330 452,350" stroke="{SKIN_SH}" stroke-width="7" fill="none" stroke-linecap="round"/>'
        # skull: egg, slightly wider at the cheeks
        + f'<path d="M300,146 C398,146 450,214 450,312 C450,436 388,512 300,512 C212,512 150,436 150,312 C150,214 202,146 300,146 Z" fill="url(#skinGrad)"/>'
        # soft form shadow on the right side + under hair
        + f'<path d="M420,220 C452,262 458,330 446,392 C430,452 380,494 318,500 C392,470 432,400 432,318 C432,280 428,248 420,220Z" fill="{SKIN_SH}" opacity="0.55"/>'
        # blush
        + f'<ellipse cx="206" cy="382" rx="30" ry="16" fill="{BLUSH}" opacity="0.55"/><ellipse cx="394" cy="382" rx="30" ry="16" fill="{BLUSH}" opacity="0.55"/>'
        # nose
        + f'<path d="M298,340 Q286,372 300,384 Q312,388 318,380" fill="none" stroke="{SKIN_DEEP}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        + beard
        + extra_front
    )


def magnus(p="mag", expr="smug", look=(0, 0)):
    hair = "#8B5A32"
    curl = "#6A4122"
    hl = "#B07A48"
    # curly hair: a cloud of circles with darker curl strokes
    import math

    blobs = []
    pts = [(300, 132, 74), (222, 150, 66), (378, 150, 66), (168, 206, 58), (432, 206, 58), (150, 270, 46), (450, 270, 46),
           (262, 104, 56), (338, 104, 56), (190, 116, 46), (410, 116, 46)]
    for x, y, r in pts:
        blobs.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{hair}"/>')
    curls = []
    for i, (x, y, r) in enumerate(pts):
        rr = r * 0.42
        a0 = 0.6 + i * 1.3
        sx, sy = x + math.cos(a0) * rr, y + math.sin(a0) * rr
        ex, ey = x + math.cos(a0 + 4.2) * rr, y + math.sin(a0 + 4.2) * rr
        curls.append(f'<path d="M{sx:.0f},{sy:.0f} A{rr:.0f},{rr:.0f} 0 1 0 {ex:.0f},{ey:.0f}" fill="none" stroke="{curl}" stroke-width="7" stroke-linecap="round"/>')
    highlights = "".join(f'<path d="M{x-r*0.5:.0f},{y-r*0.5:.0f} q{r*0.4:.0f},-{r*0.3:.0f} {r*0.8:.0f},-{r*0.05:.0f}" fill="none" stroke="{hl}" stroke-width="7" stroke-linecap="round" opacity="0.75"/>' for x, y, r in pts[:5])
    back = f'<g id="{p}-hair-back">{"".join(blobs)}</g>'
    fringe = (f'<g id="{p}-hair-front">'
              f'<path d="M164,246 C166,176 226,150 300,150 C374,150 434,176 436,246 C420,226 398,214 372,222 C356,200 330,196 300,210 C270,196 244,200 228,222 C202,214 180,226 164,246Z" fill="{hair}"/>'
              f'<circle cx="236" cy="214" r="30" fill="{hair}"/><circle cx="300" cy="200" r="32" fill="{hair}"/><circle cx="364" cy="214" r="30" fill="{hair}"/>'
              f'<path d="M222,212 a14,14 0 1 1 22,10" fill="none" stroke="{curl}" stroke-width="7" stroke-linecap="round"/>'
              f'<path d="M290,196 a15,15 0 1 0 22,12" fill="none" stroke="{curl}" stroke-width="7" stroke-linecap="round"/>'
              f'<path d="M352,210 a14,14 0 1 1 22,8" fill="none" stroke="{curl}" stroke-width="7" stroke-linecap="round"/>'
              + "".join(curls) + highlights + "</g>")
    beard = (f'<g id="{p}-beard">'
             f'<path d="M152,352 C156,446 204,528 300,532 C396,528 444,446 448,352 C438,398 418,420 392,428 C368,410 336,404 300,406 C264,404 232,410 208,428 C182,420 162,398 152,352Z" fill="#7B4E2A"/>'
             f'<path d="M240,404 Q270,386 300,394 Q330,386 360,404 Q336,416 300,412 Q264,416 240,404Z" fill="#6E4424"/>'
             + "".join(f'<path d="M{x},{y} l6,10" stroke="#5E3A1E" stroke-width="5" stroke-linecap="round"/>' for x, y in
                       [(196, 452), (226, 476), (258, 494), (296, 502), (334, 494), (366, 476), (396, 452), (180, 420), (414, 420), (276, 462), (318, 462)])
             + "</g>")
    expr_map = {"smug": ("smug", "smug", "smirk"), "neutral": ("open", "flat", "flat"), "worried": ("wide", "worried", "worry"),
                "focus": ("smug", "angry", "flat"), "shock": ("wide", "up", "o")}
    lid, brow, mouth = expr_map[expr]
    face = _eyes(p, iris="#3D6E8F", lids=lid, look=look) + _brows(p, "#5A361C", brow) + _mouths(p, mouth, lip="#6A2A22")
    return (f'<g id="{p}">'
            + _body(p, "#F4F1EC", "#D9D4CC", collar="#CFC8BE")
            + f'<g id="{p}-head">{back}{_head(p, beard=beard)}{face}{fringe}</g></g>')


def cheater(p="alx", expr="neutral", look=(0, 0)):
    hair = "#3A2A22"
    cap = "#1F8A84"
    back = ""
    front = (f'<g id="{p}-hair">'
             f'<path d="M156,268 C150,190 214,150 300,150 C386,150 450,190 444,268 C420,232 380,222 340,234 C320,220 280,220 260,234 C220,222 180,232 156,268Z" fill="{hair}"/>'
             f"</g>"
             # backwards cap
             f'<g id="{p}-cap">'
             f'<path d="M150,236 C150,150 220,108 300,108 C380,108 450,150 450,236 C380,214 220,214 150,236Z" fill="{cap}"/>'
             f'<path d="M150,236 C220,214 380,214 450,236 L452,250 C380,230 220,230 148,250Z" fill="#14625E"/>'
             f'<rect x="270" y="98" width="60" height="18" rx="9" fill="#14625E"/>'
             f'<path d="M330,128 Q380,140 412,176" stroke="#2BB3AB" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.7"/>'
             f"</g>")
    stubble = f'<path d="M210,440 Q300,500 390,440 Q380,488 300,500 Q220,488 210,440Z" fill="#B8957B" opacity="0.35"/>'
    expr_map = {"neutral": ("open", "flat", "flat"), "smug": ("smug", "smug", "smirk"), "nervous": ("wide", "worried", "grit"),
                "shock": ("wide", "up", "o"), "sweat": ("open", "worried", "worry")}
    lid, brow, mouth = expr_map[expr]
    face = _eyes(p, iris="#4A3526", lids=lid, look=look) + _brows(p, "#2A1E18", brow) + _mouths(p, mouth)
    sweat = (f'<g id="{p}-sweat" opacity="{_vis(expr in ("nervous", "sweat"))}">'
             f'<path d="M448,214 C470,250 476,272 460,284 C444,294 428,280 434,260 C438,246 444,234 448,214Z" fill="#7FD4F5"/>'
             f'<ellipse cx="452" cy="268" rx="5" ry="8" fill="#FFFFFF" opacity="0.8"/></g>')
    return (f'<g id="{p}">'
            + _body(p, "#4B4E5C", "#3A3C48", hood=True)
            + f'<g id="{p}-head">{back}{_head(p, beard=stubble)}{face}{front}{sweat}</g></g>')


def _body(p, cloth, cloth_sh, collar=None, hood=False):
    # torso as a soft trapezoid; hands are separate balls (house style: no arms)
    out = [f'<g id="{p}-body">',
           f'<defs><radialGradient id="skinGrad" cx="42%" cy="38%" r="70%"><stop offset="0" stop-color="#F8D6B6"/><stop offset="0.7" stop-color="{SKIN}"/><stop offset="1" stop-color="#E8B691"/></radialGradient></defs>',
           f'<path d="M258,480 L342,480 L346,560 Q300,574 254,560Z" fill="{SKIN_SH}"/>',
           f'<path d="M254,540 Q300,560 346,540 L346,560 Q300,574 254,560Z" fill="#B97F5C" opacity="0.5"/>',
           f'<path d="M110,800 C110,640 150,560 300,548 C450,560 490,640 490,800Z" fill="{cloth}"/>',
           f'<path d="M420,590 C470,630 490,700 490,800 L430,800 C440,700 430,640 420,590Z" fill="{cloth_sh}"/>']
    if collar:
        out.append(f'<path d="M232,556 L300,640 L368,556 Q300,580 232,556Z" fill="{collar}"/>')
    if hood:
        out.append(f'<path d="M190,566 C220,620 380,620 410,566 C380,592 220,592 190,566Z" fill="#3A3C48"/>')
        out.append('<path d="M272,600 L266,690 M328,600 L334,690" stroke="#D8D8E0" stroke-width="6" stroke-linecap="round"/>')
        out.append('<circle cx="266" cy="694" r="7" fill="#D8D8E0"/><circle cx="334" cy="694" r="7" fill="#D8D8E0"/>')
    out.append("</g>")
    return "".join(out)


def hands(p, y=760, spread=170, skin=SKIN):
    return (f'<g id="{p}-hands"><circle id="{p}-hand-l" cx="{300 - spread}" cy="{y}" r="46" fill="{skin}"/>'
            f'<circle id="{p}-hand-r" cx="{300 + spread}" cy="{y}" r="46" fill="{skin}"/>'
            f'<path d="M{300-spread-24},{y-16} q20,-16 40,-4" stroke="#FFFFFF" stroke-width="7" fill="none" opacity="0.45" stroke-linecap="round"/>'
            f'<path d="M{300+spread-24},{y-16} q20,-16 40,-4" stroke="#FFFFFF" stroke-width="7" fill="none" opacity="0.45" stroke-linecap="round"/></g>')


def robot(p="sf", expr="whisper"):
    """Stockfish: a small teal robot with fish fins for ears and a screen face."""
    body = "#E9F4F3"
    body_sh = "#BFD9D7"
    teal = "#1FB5A8"
    glow = "#7CF5E8"
    eyes = {
        "whisper": f'<rect x="232" y="300" width="44" height="16" rx="8" fill="{glow}"/><rect x="324" y="300" width="44" height="16" rx="8" fill="{glow}"/>',
        "on": f'<circle cx="254" cy="308" r="24" fill="{glow}"/><circle cx="346" cy="308" r="24" fill="{glow}"/><circle cx="262" cy="300" r="7" fill="#FFF"/><circle cx="354" cy="300" r="7" fill="#FFF"/>',
        "panic": f'<path d="M232,292 l44,32 M276,292 l-44,32 M324,292 l44,32 M368,292 l-44,32" stroke="#FF6B6B" stroke-width="10" stroke-linecap="round"/>',
        "off": f'<rect x="236" y="306" width="36" height="6" rx="3" fill="#3B5A57"/><rect x="328" y="306" width="36" height="6" rx="3" fill="#3B5A57"/>',
    }
    eye_g = "".join(f'<g id="{p}-eyes-{k}" opacity="{_vis(expr == k)}">{v}</g>' for k, v in eyes.items())
    return (f'<g id="{p}">'
            # antenna
            + f'<line x1="300" y1="150" x2="300" y2="96" stroke="{body_sh}" stroke-width="10" stroke-linecap="round"/>'
            + f'<circle id="{p}-bulb" cx="300" cy="88" r="20" fill="{teal}"/><circle cx="294" cy="82" r="6" fill="#FFF" opacity="0.7"/>'
            # fish-fin ears
            + f'<path d="M146,240 C110,220 78,226 64,236 C86,262 92,300 70,336 C100,344 130,336 146,320Z" fill="{teal}"/><path d="M150,276 L110,250 M150,300 L104,292 M150,324 L112,330" stroke="#168C82" stroke-width="6" stroke-linecap="round"/>'
            + f'<path d="M454,240 C490,220 522,226 536,236 C514,262 508,300 530,336 C500,344 470,336 454,320Z" fill="{teal}"/><path d="M450,276 L490,250 M450,300 L496,292 M450,324 L488,330" stroke="#168C82" stroke-width="6" stroke-linecap="round"/>'
            # head shell
            + f'<rect x="140" y="150" width="320" height="300" rx="110" fill="{body}"/>'
            + f'<path d="M420,190 C452,240 458,330 440,392 C424,430 392,448 360,450 L380,450 C440,440 460,390 460,300 C460,250 446,214 420,190Z" fill="{body_sh}"/>'
            + f'<path d="M190,190 q40,-28 100,-26" stroke="#FFFFFF" stroke-width="14" fill="none" stroke-linecap="round" opacity="0.9"/>'
            # screen face
            + f'<rect x="186" y="232" width="228" height="164" rx="70" fill="#123B3A"/>'
            + f'<rect x="196" y="240" width="208" height="40" rx="20" fill="#1C5452" opacity="0.6"/>'
            + eye_g
            + f'<g id="{p}-mouth-talk" opacity="{_vis(expr == "whisper")}"><rect x="276" y="350" width="48" height="12" rx="6" fill="{glow}"/></g>'
            + f'<g id="{p}-mouth-smile" opacity="{_vis(expr == "on")}"><path d="M268,346 Q300,372 332,346" stroke="{glow}" stroke-width="10" fill="none" stroke-linecap="round"/></g>'
            # tiny body
            + f'<rect x="216" y="452" width="168" height="150" rx="56" fill="{body}"/>'
            + f'<rect x="250" y="490" width="100" height="56" rx="20" fill="#123B3A"/>'
            + f'<text x="300" y="528" text-anchor="middle" font-family="Space Mono, monospace" font-weight="700" font-size="26" fill="{glow}">SF</text>'
            + "</g>")


def sheet_html():
    cards = [
        ("Magnus — smug", magnus("m1", "smug") + hands("m1")),
        ("Magnus — worried", magnus("m2", "worried", look=(6, 4)) + hands("m2")),
        ("Aleksandar — smug", cheater("a1", "smug") + hands("a1")),
        ("Aleksandar — nervous", cheater("a2", "nervous", look=(-6, 0)) + hands("a2")),
        ("Stockfish — whisper", robot("s1", "whisper")),
        ("Stockfish — panic", robot("s2", "panic")),
    ]
    cells = "".join(
        f'<div class="cell"><svg viewBox="0 0 600 800">{svg}</svg><div class="lab">{lab}</div></div>' for lab, svg in cards
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#1d2340;font-family:Nunito,sans-serif}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;padding:24px;width:1032px}}
.cell{{background:radial-gradient(circle at 50% 35%,#5b4bb0,#2a2160 70%);border-radius:18px;overflow:hidden;position:relative}}
.cell:nth-child(n+3){{background:linear-gradient(#bfe3f7,#e9f6fb 55%,#7cc26a 56%,#5aa94b)}}
.cell:nth-child(n+5){{background:radial-gradient(circle at 50% 40%,#2b6f74,#0d2b33 75%)}}
svg{{display:block;width:100%}}
.lab{{position:absolute;bottom:10px;width:100%;text-align:center;color:#fff;font-weight:900;font-size:24px;text-shadow:0 2px 4px #000}}
</style></head><body><div class="grid">{cells}</div></body></html>"""


if __name__ == "__main__":
    import sys

    open(sys.argv[1], "w").write(sheet_html())
