"""Flat 2D art library for The Rule Stories: palette, character rig, props, backgrounds.

Everything is plain SVG markup (strings). Characters stand on their feet at (x, y); the
rig's animatable parts carry ids  <cid>-armL, -armR, -browL, -browR, -eyes, -m-<state>, -head.
Style rules (from the style bible): no outlines, flat fills, head:body ~1:3, brows carry the
emotion, soft ellipse shadow under the feet, light is additive only.
"""

# ---------------------------------------------------------------- palette
P = {
    "red": "#ef3b4f", "red_d": "#a3182c", "yellow": "#ffd43b", "green": "#3fbf7f",
    "blue": "#3a6fd8", "cyan": "#7fe3ff", "white": "#ffffff", "ink": "#16161c",
    "char": "#23232b", "char2": "#2f3039", "grey": "#8a8c96", "grey_l": "#c9cad1",
    "skin": "#e2c4a0", "skin2": "#c99a73", "skin3": "#8d5f43",
    "night": "#0a1020", "night2": "#121b31", "night3": "#1b2744", "navy": "#0d1526",
    "wall_n": "#262d42", "wall_n2": "#1f2538", "floor_n": "#1a1d2a",
    "wall_d": "#e9dcc3", "wall_d2": "#d8c7a6", "floor_d": "#a07c5a",
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- character rig
CAST = {
    # coat, coat_dark, legs, hair, skin, hair_style, extras
    "you": dict(coat="#3b6e8f", coat_d="#2f5873", legs="#1f2433", hair="#3a2a20", skin=P["skin"],
                hair_style="short", extra="hoodie"),
    "leo": dict(coat="#d9573b", coat_d="#b84528", legs="#2b3650", hair="#e0a33a", skin=P["skin"],
                hair_style="messy", extra=""),
    "grandma": dict(coat="#8a6fb0", coat_d="#735a97", legs="#3a3346", hair="#d9d9de", skin=P["skin"],
                    hair_style="bun", extra="glasses"),
    "alvarez": dict(coat="#5b7d4a", coat_d="#4a6a3b", legs="#2a2a33", hair="#2a2422", skin=P["skin2"],
                    hair_style="bald", extra="moustache"),
    "anchor": dict(coat="#2e3a5e", coat_d="#25304d", legs="#1d2233", hair="#5a3b2a", skin=P["skin"],
                   hair_style="side", extra="tie"),
    "mom": dict(coat="#c7764a", coat_d="#a9613a", legs="#2d2f3c", hair="#6b3b2a", skin=P["skin"],
                hair_style="long", extra=""),
    "kid": dict(coat="#4f9e6a", coat_d="#3f8657", legs="#2b3650", hair="#2a2422", skin=P["skin2"],
                hair_style="short", extra=""),
    "kid2": dict(coat="#c9a23a", coat_d="#ad8a2e", legs="#2b3650", hair="#7a4a2a", skin=P["skin"],
                 hair_style="messy", extra=""),
    "dispatcher": dict(coat="#3b4a6b", coat_d="#2f3c57", legs="#1d2233", hair="#1d1a1a", skin=P["skin"],
                       hair_style="long", extra="headset"),
}


def _hair(style, color, head_w):
    hw = head_w / 2
    if style == "short":
        return (f'<path d="M{-hw-2},-262 Q{-hw-4},-318 0,-318 Q{hw+4},-318 {hw+2},-262 '
                f'L{hw-6},-282 Q0,-300 {-hw+10},-284 Z" fill="{color}"/>')
    if style == "messy":
        return (f'<path d="M{-hw-3},-258 Q{-hw-8},-322 -8,-320 L0,-332 L10,-319 Q{hw+8},-318 {hw+3},-258 '
                f'L{hw-4},-280 L20,-290 L6,-282 L-8,-292 L-20,-282 L{-hw+6},-282 Z" fill="{color}"/>')
    if style == "bun":
        return (f'<circle cx="0" cy="-324" r="20" fill="{color}"/>'
                f'<path d="M{-hw-3},-250 Q{-hw-6},-316 0,-316 Q{hw+6},-316 {hw+3},-250 '
                f'L{hw-6},-276 Q0,-296 {-hw+6},-276 Z" fill="{color}"/>')
    if style == "long":
        return (f'<path d="M{-hw-6},-196 Q{-hw-10},-322 0,-320 Q{hw+10},-322 {hw+6},-196 '
                f'L{hw-6},-200 L{hw-8},-276 Q0,-296 {-hw+8},-276 L{-hw+6},-200 Z" fill="{color}"/>')
    if style == "side":
        return (f'<path d="M{-hw-2},-262 Q{-hw-4},-318 6,-316 Q{hw+4},-316 {hw+2},-262 '
                f'L{hw-4},-286 Q-10,-300 {-hw+6},-278 Z" fill="{color}"/>')
    return ""  # bald


def character(cid, who, x, y, scale=1.0, mood="neutral", arms=(8, -8), flip=False, held="",
              opacity=1.0, dim=0.0):
    """A standing character. arms = (left°, right°): 0 hangs down, -90 points right (viewer's),
    positive swings outward-left. `held` = prop markup placed in the right hand.
    `dim` 0..1 darkens the whole figure (night)."""
    c = CAST[who]
    kid = who in ("leo", "kid", "kid2")
    head_w = 100 if kid else 92
    hy = -262
    sx = -scale if flip else scale
    parts = []
    parts.append('<ellipse cx="0" cy="0" rx="62" ry="11" fill="#000" opacity="0.28"/>')
    # legs + shoes
    parts.append(f'<rect x="-30" y="-112" width="24" height="108" rx="6" fill="{c["legs"]}"/>'
                 f'<rect x="6" y="-112" width="24" height="108" rx="6" fill="{c["legs"]}"/>'
                 f'<ellipse cx="-20" cy="-4" rx="20" ry="9" fill="#111"/>'
                 f'<ellipse cx="20" cy="-4" rx="20" ry="9" fill="#111"/>')
    # arms behind body: left (viewer's left) and right
    def arm(side, ang):
        sxp = -46 if side == "L" else 46
        hand = held if (side == "R" and held) else ""
        return (f'<g id="{cid}-arm{side}" transform="rotate({ang} {sxp} -204)">'
                f'<rect x="{sxp-12}" y="-212" width="24" height="112" rx="12" fill="{c["coat_d"]}"/>'
                f'<circle cx="{sxp}" cy="-98" r="14" fill="{c["skin"]}"/>{hand}</g>')
    parts.append(arm("L", arms[0]))
    parts.append(arm("R", arms[1]))
    # body
    parts.append(f'<rect x="-50" y="-222" width="100" height="122" rx="24" fill="{c["coat"]}"/>')
    if c["extra"] == "hoodie":
        parts.append(f'<path d="M-30,-222 Q0,-196 30,-222" stroke="{c["coat_d"]}" stroke-width="8" fill="none"/>'
                     f'<rect x="-24" y="-150" width="48" height="26" rx="8" fill="{c["coat_d"]}"/>')
    elif c["extra"] == "tie":
        parts.append('<path d="M0,-218 L-9,-200 L0,-150 L9,-200 Z" fill="#c9364a"/>')
    else:
        parts.append(f'<rect x="-4" y="-218" width="8" height="112" rx="3" fill="{c["coat_d"]}"/>')
    # neck + head
    parts.append(f'<rect x="-12" y="-232" width="24" height="16" fill="{c["skin"]}"/>')
    head = [f'<rect x="{-head_w/2}" y="{hy-52}" width="{head_w}" height="104" rx="42" fill="{c["skin"]}"/>']
    head.append(_hair(c["hair_style"], c["hair"], head_w))
    # eyes (blink = scaleY on this group)
    head.append(f'<g id="{cid}-eyes" transform="translate(0 {hy}) scale(1 1) translate(0 {-hy})"><ellipse cx="-17" cy="{hy+2}" rx="5.5" ry="7" fill="#1a1a22"/>'
                f'<ellipse cx="17" cy="{hy+2}" rx="5.5" ry="7" fill="#1a1a22"/></g>')
    if c["extra"] == "glasses":
        head.append(f'<g fill="none" stroke="#2a2a33" stroke-width="3"><circle cx="-17" cy="{hy+2}" r="13"/>'
                    f'<circle cx="17" cy="{hy+2}" r="13"/><path d="M-4,{hy+2} L4,{hy+2}"/></g>')
    # brows: rotate around inner ends for emotion
    bl, br, bdy = BROWS.get(mood, (0, 0, 0))
    head.append(f'<rect id="{cid}-browL" transform="translate(0 {bdy}) rotate({bl} -6 -281)" x="-28" y="{hy-22}" width="22" height="6" rx="3" fill="#2a1f1a"/>'
                f'<rect id="{cid}-browR" transform="translate(0 {bdy}) rotate({br} 6 -281)" x="6" y="{hy-22}" width="22" height="6" rx="3" fill="#2a1f1a"/>')
    head.append(f'<rect x="-3" y="{hy+12}" width="6" height="10" rx="3" fill="{P["skin2"] if c["skin"]==P["skin"] else P["skin3"]}" opacity="0.7"/>')
    if c["extra"] == "moustache":
        head.append(f'<path d="M-20,{hy+30} Q0,{hy+20} 20,{hy+30} Q0,{hy+36} -20,{hy+30} Z" fill="#2a2422"/>')
    if c["extra"] == "headset":
        head.append(f'<path d="M{-head_w/2-2},{hy} Q{-head_w/2-2},{hy-70} 0,{hy-68}" stroke="#222" stroke-width="6" fill="none"/>'
                    f'<rect x="{-head_w/2-10}" y="{hy-10}" width="14" height="26" rx="6" fill="#222"/>'
                    f'<path d="M{-head_w/2-4},{hy+12} Q-30,{hy+40} -12,{hy+36}" stroke="#222" stroke-width="4" fill="none"/>')
    # mouths: all states drawn, one visible
    my = hy + 34
    mouths = {
        "line": f'<rect x="-10" y="{my-2}" width="20" height="5" rx="2.5" fill="#3a1f1f"/>',
        "open": f'<ellipse cx="0" cy="{my}" rx="9" ry="11" fill="#3a1414"/>',
        "smile": f'<path d="M-14,{my-4} Q0,{my+10} 14,{my-4}" stroke="#3a1f1f" stroke-width="5" fill="none" stroke-linecap="round"/>',
        "frown": f'<path d="M-12,{my+5} Q0,{my-6} 12,{my+5}" stroke="#3a1f1f" stroke-width="5" fill="none" stroke-linecap="round"/>',
        "o": f'<ellipse cx="0" cy="{my}" rx="6" ry="7" fill="#3a1414"/>',
    }
    start_mouth = {"neutral": "line", "happy": "smile", "scared": "open", "sad": "frown",
                   "worried": "line", "shock": "o", "creepy": "smile", "angry": "frown"}.get(mood, "line")
    for k, v in mouths.items():
        head.append(f'<g id="{cid}-m-{k}" opacity="{1 if k == start_mouth else 0}">{v}</g>')
    parts.append(f'<g id="{cid}-head">{"".join(head)}</g>')
    tint = f'<g opacity="{dim}"><rect x="-80" y="-345" width="160" height="350" fill="#050814"/></g>' if dim else ""
    body = "".join(parts)
    if dim:
        # darken by drawing the figure into a mask-less group with a multiply overlay clipped by the figure
        body = f'<g filter="url(#dim{int(dim*100)})">{body}</g>'
    return (f'<g id="{cid}" class="char" transform="translate({x} {y}) scale({sx} {scale})" opacity="{opacity}">'
            f'{body}</g>')


BROWS = {
    # (left rotation, right rotation, dy) — inner ends: left brow's right end, right brow's left end
    "neutral": (0, 0, 0), "happy": (-6, 6, -3), "worried": (-16, 16, -4), "scared": (-20, 20, -10),
    "angry": (18, -18, 2), "sad": (-14, 14, 0), "shock": (0, 0, -12), "creepy": (10, -10, 2),
}


def svg_filters():
    """Shared SVG filter defs (night dimming of characters, glows)."""
    out = []
    for d in (20, 35, 50, 65):
        k = 1 - d / 100
        out.append(f'<filter id="dim{d}"><feColorMatrix type="matrix" values="{k*0.9} 0 0 0 0  0 {k*0.95} 0 0 0  0 0 {k*1.15} 0 0.02  0 0 0 1 0"/></filter>')
    out.append('<filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>')
    out.append('<filter id="blur30" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="30"/></filter>')
    return "".join(out)


# ---------------------------------------------------------------- props
def phone(x, y, w=70, rot=0, screen="#0d0f14", lit=False, cid=""):
    h = w * 2
    glow = (f'<rect x="{-w/2+5}" y="{-h/2+8}" width="{w-10}" height="{h-16}" rx="8" fill="#bfe9ff" opacity="0.9"/>'
            if lit else f'<rect x="{-w/2+5}" y="{-h/2+8}" width="{w-10}" height="{h-16}" rx="8" fill="{screen}"/>')
    ident = f' id="{cid}"' if cid else ""
    return (f'<g{ident} transform="translate({x} {y}) rotate({rot})"><rect x="{-w/2}" y="{-h/2}" width="{w}" '
            f'height="{h}" rx="12" fill="#1b1d24"/>{glow}</g>')


def landline(x, y, s=1.0, color="#d8d2c4", receiver_on=True, cid="landline"):
    rec = (f'<g id="{cid}-rec"><rect x="-70" y="-62" width="140" height="30" rx="15" fill="{color}"/>'
           f'<rect x="-76" y="-70" width="34" height="40" rx="12" fill="{color}"/>'
           f'<rect x="42" y="-70" width="34" height="40" rx="12" fill="{color}"/></g>') if receiver_on else ""
    return (f'<g id="{cid}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M-80,0 L-60,-40 L60,-40 L80,0 Z" fill="{color}"/>'
            f'<rect x="-80" y="-4" width="160" height="14" rx="5" fill="#b9b2a3"/>'
            f'<g fill="#9a9384">' + "".join(f'<circle cx="{-30+i%3*30}" cy="{-28+i//3*9}" r="3"/>' for i in range(6)) + '</g>'
            f'{rec}</g>')


def tablet(x, y, w=90, rot=0, lit=True):
    h = w * 0.7
    return (f'<g transform="translate({x} {y}) rotate({rot})"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="8" fill="#1b1d24"/>'
            f'<rect x="{-w/2+5}" y="{-h/2+5}" width="{w-10}" height="{h-10}" rx="4" fill="{"#8fd3ff" if lit else "#0d0f14"}" opacity="{0.85 if lit else 1}"/></g>')


def moon(x, y, r=46):
    return (f'<circle cx="{x}" cy="{y}" r="{r*2.6}" fill="#cfe3ff" opacity="0.06"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*1.6}" fill="#cfe3ff" opacity="0.08"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#eef3ff"/>'
            f'<circle cx="{x-r*0.3}" cy="{y-r*0.2}" r="{r*0.18}" fill="#d9e2f2"/>'
            f'<circle cx="{x+r*0.25}" cy="{y+r*0.3}" r="{r*0.12}" fill="#d9e2f2"/>')


def stars(n, x0, y0, x1, y1, seed=1, op=0.7):
    import random
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        out.append(f'<circle cx="{rnd.uniform(x0,x1):.0f}" cy="{rnd.uniform(y0,y1):.0f}" r="{rnd.choice([1.2,1.6,2.2,2.8])}" '
                   f'fill="#ffffff" opacity="{rnd.uniform(op*0.4,op):.2f}"/>')
    return "".join(out)


def window(x, y, w, h, sky="#13203d", frame="#3a3f55", lit=False, inner=""):
    fill = "#ffd98a" if lit else sky
    return (f'<g transform="translate({x} {y})"><rect x="-10" y="-10" width="{w+20}" height="{h+20}" rx="4" fill="{frame}"/>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{fill}"/>'
            f'<svg x="0" y="0" width="{w}" height="{h}" overflow="hidden">{inner}</svg>'
            f'<rect x="{w/2-4}" y="0" width="8" height="{h}" fill="{frame}"/><rect x="0" y="{h/2-4}" width="{w}" height="8" fill="{frame}"/></g>')


def house(x, y, w, h, body, roof, wins_lit, seed=0, door=True):
    import random
    rnd = random.Random(seed)
    out = [f'<g transform="translate({x} {y})">',
           f'<path d="M-14,{-h} L{w/2},{-h-h*0.45} L{w+14},{-h} Z" fill="{roof}"/>',
           f'<rect x="0" y="{-h}" width="{w}" height="{h}" fill="{body}"/>']
    cols = max(2, int(w // 70))
    rows = max(1, int(h // 90))
    k = 0
    for r in range(rows):
        for c_ in range(cols):
            wx = (c_ + 0.5) * w / cols - 18
            wy = -h + 24 + r * 90
            lit = wins_lit[k % len(wins_lit)] if wins_lit else False
            out.append(f'<rect class="win" x="{wx}" y="{wy}" width="36" height="44" rx="3" fill="{"#ffd98a" if lit else "#0e1424"}"/>')
            k += 1
    if door:
        out.append(f'<rect x="{w/2-20}" y="-62" width="40" height="62" rx="3" fill="#0e1424"/>')
    out.append('</g>')
    return "".join(out)


def icon(name, x, y, s=1.0, color="#ffffff"):
    """Small flat icons for infographic stages."""
    g = {
        "phone": f'<rect x="-22" y="-42" width="44" height="84" rx="9" fill="#1b1d24"/><rect x="-18" y="-35" width="36" height="66" rx="4" fill="{color}"/>',
        "ear": f'<path d="M-10,-30 Q25,-40 25,0 Q25,22 5,30 Q0,40 -10,32" stroke="{color}" stroke-width="9" fill="none" stroke-linecap="round"/>',
        "wave": "".join(f'<rect x="{-40+i*12}" y="{-h/2}" width="7" height="{h}" rx="3.5" fill="{color}"/>' for i, h in enumerate([16, 34, 52, 30, 60, 24, 44]) ),
        "lock": f'<rect x="-26" y="-6" width="52" height="40" rx="6" fill="{color}"/><path d="M-16,-6 L-16,-20 Q-16,-38 0,-38 Q16,-38 16,-20 L16,-6" stroke="{color}" stroke-width="8" fill="none"/>',
        "key": f'<circle cx="-18" cy="0" r="16" stroke="{color}" stroke-width="8" fill="none"/><rect x="-2" y="-4" width="44" height="8" fill="{color}"/><rect x="30" y="0" width="8" height="14" fill="{color}"/>',
        "speech": f'<path d="M-40,-28 Q-40,-40 -28,-40 L28,-40 Q40,-40 40,-28 L40,8 Q40,20 28,20 L-6,20 L-22,36 L-20,20 L-28,20 Q-40,20 -40,8 Z" fill="{color}"/>',
        "tower": f'<path d="M-24,40 L0,-40 L24,40" stroke="{color}" stroke-width="7" fill="none"/><path d="M-14,10 L14,10 M-8,-12 L8,-12" stroke="{color}" stroke-width="6"/><circle cx="0" cy="-44" r="7" fill="{color}"/>',
        "globe": f'<circle cx="0" cy="0" r="38" fill="{color}"/><path d="M-20,-24 Q-4,-16 -14,0 Q-26,10 -12,26 M12,-30 Q24,-10 10,4 Q4,18 22,24" stroke="#000" stroke-opacity="0.25" stroke-width="7" fill="none"/>',
        "mic": f'<rect x="-14" y="-40" width="28" height="50" rx="14" fill="{color}"/><path d="M-26,0 Q-26,26 0,26 Q26,26 26,0 M0,26 L0,40 M-14,40 L14,40" stroke="{color}" stroke-width="6" fill="none"/>',
        "video": f'<rect x="-40" y="-26" width="58" height="52" rx="8" fill="{color}"/><path d="M22,-10 L42,-22 L42,22 L22,10 Z" fill="{color}"/>',
        "speaker": f'<rect x="-24" y="-40" width="48" height="80" rx="18" fill="{color}"/><circle cx="0" cy="12" r="14" fill="#000" opacity="0.25"/><circle cx="0" cy="-20" r="6" fill="#000" opacity="0.25"/>',
        "paper": f'<rect x="-30" y="-40" width="60" height="80" rx="4" fill="{color}"/>' + "".join(f'<rect x="-20" y="{-26+i*14}" width="{40 if i%2 else 30}" height="5" rx="2" fill="#000" opacity="0.25"/>' for i in range(5)),
        "pen": f'<rect x="-6" y="-44" width="12" height="70" rx="4" fill="{color}"/><path d="M-6,26 L0,44 L6,26 Z" fill="{color}"/>',
        "battery": f'<rect x="-34" y="-18" width="62" height="36" rx="6" stroke="{color}" stroke-width="6" fill="none"/><rect x="30" y="-8" width="7" height="16" rx="2" fill="{color}"/><rect x="-27" y="-11" width="{0.41*48:.0f}" height="22" rx="3" fill="{color}"/>',
        "dog": f'<ellipse cx="0" cy="0" rx="34" ry="18" fill="{color}"/><circle cx="34" cy="-16" r="14" fill="{color}"/><path d="M40,-30 L48,-40 L46,-24 Z" fill="{color}"/><rect x="-26" y="10" width="8" height="22" fill="{color}"/><rect x="18" y="10" width="8" height="22" fill="{color}"/><path d="M-34,-6 L-50,-20" stroke="{color}" stroke-width="7" stroke-linecap="round"/>',
        "sun": f'<circle cx="0" cy="0" r="24" fill="{color}"/>' + "".join(f'<rect x="-3" y="-44" width="6" height="12" rx="3" fill="{color}" transform="rotate({a})"/>' for a in range(0, 360, 45)),
        "cloud": f'<path d="M-40,14 Q-44,-10 -20,-12 Q-14,-34 8,-26 Q30,-38 36,-12 Q52,-8 46,14 Z" fill="{color}"/>',
        "skull": f'<path d="M-30,-6 Q-30,-40 0,-40 Q30,-40 30,-6 Q30,10 18,14 L18,28 L-18,28 L-18,14 Q-30,10 -30,-6 Z" fill="{color}"/><circle cx="-12" cy="-6" r="8" fill="#000" opacity="0.6"/><circle cx="12" cy="-6" r="8" fill="#000" opacity="0.6"/>',
        "house": f'<path d="M-38,0 L0,-34 L38,0 L38,36 L-38,36 Z" fill="{color}"/><rect x="-9" y="12" width="18" height="24" fill="#000" opacity="0.3"/>',
        "cake": f'<rect x="-36" y="-6" width="72" height="40" rx="6" fill="{color}"/><rect x="-36" y="6" width="72" height="8" fill="#000" opacity="0.2"/>' + "".join(f'<rect x="{-20+i*18}" y="-30" width="6" height="22" rx="3" fill="{color}"/><circle cx="{-17+i*18}" cy="-36" r="5" fill="#ffd43b"/>' for i in range(3)),
        "tablet": f'<rect x="-40" y="-30" width="80" height="60" rx="7" fill="#1b1d24"/><rect x="-35" y="-25" width="70" height="50" rx="3" fill="{color}"/>',
        "landline": f'<path d="M-40,30 L-30,0 L30,0 L40,30 Z" fill="{color}"/><rect x="-44" y="-22" width="88" height="18" rx="9" fill="{color}"/><rect x="-48" y="-28" width="20" height="24" rx="7" fill="{color}"/><rect x="28" y="-28" width="20" height="24" rx="7" fill="{color}"/>',
        "bell": f'<path d="M-30,20 Q-30,-30 0,-34 Q30,-30 30,20 L38,28 L-38,28 Z" fill="{color}"/><circle cx="0" cy="34" r="8" fill="{color}"/>',
        "person": f'<circle cx="0" cy="-26" r="18" fill="{color}"/><rect x="-24" y="-4" width="48" height="50" rx="16" fill="{color}"/>',
        "question": f'<text x="0" y="22" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="72" fill="{color}">?</text>',
        "calendar": f'<rect x="-36" y="-30" width="72" height="66" rx="8" fill="{color}"/><rect x="-36" y="-30" width="72" height="18" rx="6" fill="#ef3b4f"/>',
        "machine": f'<rect x="-50" y="-30" width="100" height="60" rx="8" fill="{color}"/><rect x="-34" y="-18" width="44" height="26" rx="4" fill="#000" opacity="0.35"/><circle cx="-22" cy="-5" r="7" fill="{color}"/><circle cx="-2" cy="-5" r="7" fill="{color}"/><circle cx="30" cy="-6" r="7" fill="#ef3b4f"/>',
        "trash": f'<rect x="-28" y="-26" width="56" height="62" rx="6" fill="{color}"/><rect x="-36" y="-36" width="72" height="10" rx="4" fill="{color}"/><rect x="-10" y="-44" width="20" height="10" rx="3" fill="{color}"/>',
        "tree": f'<path d="M0,-46 L34,4 L14,4 L40,36 L-40,36 L-14,4 L-34,4 Z" fill="{color}"/><rect x="-7" y="36" width="14" height="14" fill="#6b4a32"/>',
        "note": f'<rect x="-6" y="-40" width="10" height="64" fill="{color}"/><ellipse cx="-16" cy="26" rx="18" ry="13" fill="{color}"/><path d="M4,-40 Q34,-30 30,-6" stroke="{color}" stroke-width="9" fill="none"/>',
        "robot": f'<rect x="-34" y="-30" width="68" height="56" rx="12" fill="{color}"/><circle cx="-13" cy="-4" r="8" fill="#000" opacity="0.5"/><circle cx="13" cy="-4" r="8" fill="#000" opacity="0.5"/><rect x="-3" y="-46" width="6" height="16" fill="{color}"/><circle cx="0" cy="-48" r="6" fill="{color}"/>',
        "upload": f'<path d="M0,-40 L30,-8 L12,-8 L12,30 L-12,30 L-12,-8 L-30,-8 Z" fill="{color}"/>',
        "clock": f'<circle cx="0" cy="0" r="36" fill="none" stroke="{color}" stroke-width="7"/><path d="M0,0 L0,-22 M0,0 L16,8" stroke="{color}" stroke-width="6" stroke-linecap="round"/>',
    }[name]
    return f'<g transform="translate({x} {y}) scale({s})">{g}</g>'


def receiver(x, y, s=1.0, rot=0, color="#cfc8b8", cid=""):
    ident = f' id="{cid}"' if cid else ""
    return (f'<g{ident} transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-60" y="-12" width="120" height="24" rx="12" fill="{color}"/>'
            f'<rect x="-66" y="-20" width="30" height="36" rx="10" fill="{color}"/><rect x="36" y="-20" width="30" height="36" rx="10" fill="{color}"/></g>')


def cord(x1, y1, x2, y2, color="#bdb5a3"):
    """Coiled phone cord as a wavy path between two points."""
    import math
    n = 22
    pts = []
    for k in range(n + 1):
        t = k / n
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t + math.sin(t * math.pi) * 60
        off = 9 * (1 if k % 2 else -1)
        pts.append(f"{x + off:.0f},{y:.0f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="6" stroke-linejoin="round"/>'


def frame_photo(x, y, w=260, h=320, ribbon=True, inner=""):
    return (f'<g transform="translate({x} {y})"><rect x="{-w/2-16}" y="{-h/2-16}" width="{w+32}" height="{h+32}" rx="6" fill="#6b4a32"/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#cfc6b2"/>'
            f'<svg x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" overflow="hidden">{inner}</svg>'
            + (f'<path d="M{w/2-70},{-h/2-16} L{w/2+16},{-h/2+70} L{w/2+16},{-h/2+30} L{w/2-30},{-h/2-16} Z" fill="#111"/>' if ribbon else "")
            + '</g>')


def lying(markup, x, y, rot=-90):
    """Lay a standing character down (feet at x,y rotated)."""
    return f'<g transform="translate({x} {y}) rotate({rot})">{markup}</g>'


def glow(x, y, r, color="#7fd0ff", op=0.18):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="{op}" filter="url(#blur30)"/>'
