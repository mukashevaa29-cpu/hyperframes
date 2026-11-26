"""Character rig v2: the detail level of the reference channel.

Same animation contract as art.character (ids, pivots), so shot lists and build.py work unchanged:
  <cid> class="char", <cid>-armL/-armR rotate around (±46,-204), <cid>-eyes scale around y=-262,
  <cid>-browL/-browR rotate around their inner ends (∓6,-281), <cid>-m-<state> mouths.
Added: hair with volume, ears, blush, freckles, eye highlights, a darker shade side on the body and
sleeves, cuffs, soles, outfit details (puffer quilting, zipper, hood, buttons, lapels, scrubs),
hats and scarves.
"""
from art import P, BROWS, CAST

SKIN_SH = {"#e2c4a0": "#cfa983", "#c99a73": "#b4845e", "#8d5f43": "#7a4f36", "#e9e2da": "#d6cdc4", "#ece4dc": "#d9d0c6"}


def _shade(hex_, k=0.82):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * k), int(g * k), int(b * k))


def _hair_back(style, c, hw):
    if style == "long":
        return f'<path d="M{-hw-8},-300 Q{-hw-16},-240 {-hw-4},-200 L{hw+4},-200 Q{hw+16},-240 {hw+8},-300 Z" fill="{_shade(c, 0.85)}"/>'
    if style == "bun":
        return f'<circle cx="0" cy="-328" r="22" fill="{c}"/><circle cx="-6" cy="-334" r="8" fill="#ffffff" opacity="0.18"/>'
    return ""


def _hair_front(style, c, hw):
    d = _shade(c, 0.8)
    hl = '<path d="M-14,-306 Q4,-314 20,-304" stroke="#ffffff" stroke-opacity="0.22" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if style == "short":
        return (f'<path d="M{-hw-3},-258 Q{-hw-6},-320 2,-318 Q{hw+8},-318 {hw+3},-262 L{hw-4},-284 '
                f'Q{hw-14},-296 6,-292 Q-18,-300 -34,-284 L{-hw+4},-262 Z" fill="{c}"/>'
                f'<path d="M6,-292 Q-6,-280 -26,-282" stroke="{d}" stroke-width="5" fill="none"/>{hl}')
    if style == "messy":
        return (f'<path d="M{-hw-4},-256 Q{-hw-10},-322 -10,-322 L-2,-338 L8,-321 L22,-330 L22,-316 Q{hw+10},-314 {hw+4},-256 '
                f'L{hw-4},-282 L22,-292 L10,-282 L-4,-294 L-18,-282 L-30,-292 L{-hw+6},-280 Z" fill="{c}"/>{hl}')
    if style == "curly":
        bumps = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r in
                        [(-40, -290, 22), (-22, -312, 24), (4, -318, 24), (28, -310, 22), (44, -288, 20),
                         (-50, -266, 16), (52, -266, 16)])
        return bumps + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{d}" opacity="0.5"/>' for x, y in [(-26, -300), (8, -306), (32, -294)])
    if style == "long":
        return (f'<path d="M{-hw-6},-232 Q{-hw-12},-322 0,-320 Q{hw+12},-322 {hw+6},-232 L{hw-6},-236 L{hw-8},-280 '
                f'Q20,-300 -2,-286 Q-24,-300 {-hw+8},-280 L{-hw+6},-236 Z" fill="{c}"/>{hl}')
    if style == "bun":
        return (f'<path d="M{-hw-3},-252 Q{-hw-6},-316 0,-316 Q{hw+6},-316 {hw+3},-252 L{hw-6},-278 Q0,-298 {-hw+6},-278 Z" fill="{c}"/>'
                f'<path d="M-30,-300 Q0,-310 30,-300" stroke="{d}" stroke-width="4" fill="none"/>')
    if style == "side":
        return (f'<path d="M{-hw-2},-262 Q{-hw-4},-318 6,-316 Q{hw+4},-316 {hw+2},-262 L{hw-4},-286 Q-10,-302 {-hw+6},-278 Z" fill="{c}"/>{hl}')
    if style == "bald":
        return (f'<path d="M{-hw-1},-250 Q{-hw-4},-276 {-hw+8},-284 L{-hw+10},-254 Z" fill="{c}"/>'
                f'<path d="M{hw+1},-250 Q{hw+4},-276 {hw-8},-284 L{hw-10},-254 Z" fill="{c}"/>'
                '<ellipse cx="-14" cy="-302" rx="16" ry="6" fill="#ffffff" opacity="0.25"/>')
    return ""


def _hat(kind, color, hw):
    if kind == "beanie":
        d = _shade(color, 0.8)
        return (f'<path d="M{-hw-6},-276 Q{-hw-6},-336 0,-338 Q{hw+6},-336 {hw+6},-276 Z" fill="{color}"/>'
                f'<rect x="{-hw-8}" y="-286" width="{2*hw+16}" height="22" rx="10" fill="{d}"/>'
                + "".join(f'<rect x="{-hw+4+k*12}" y="-284" width="4" height="18" fill="{color}" opacity="0.5"/>' for k in range(int(2 * hw / 12)))
                + f'<circle cx="0" cy="-344" r="14" fill="{d}"/>')
    if kind == "cap":
        return (f'<path d="M{-hw-4},-282 Q{-hw},-330 0,-330 Q{hw},-330 {hw+4},-282 Z" fill="{color}"/>'
                f'<path d="M{hw-6},-284 L{hw+40},-282 Q{hw+42},-272 {hw},-272 Z" fill="{_shade(color, 0.8)}"/>')
    return ""


def _outfit(kind, c, cd, cid):
    """Body detail drawn on top of the base torso (x -52..52, y -224..-100)."""
    if kind == "puffer":
        lines = "".join(f'<path d="M-50,{y} Q0,{y+6} 50,{y}" stroke="{cd}" stroke-width="4" fill="none"/>' for y in (-196, -168, -140, -114))
        return (lines + '<rect x="-3" y="-222" width="6" height="120" fill="#d9d9de" opacity="0.8"/>'
                f'<path d="M-30,-228 L-26,-210 L26,-210 L30,-228 Z" fill="{cd}"/>')
    if kind == "hoodie":
        return (f'<path d="M-40,-224 Q0,-190 40,-224 Q30,-240 0,-238 Q-30,-240 -40,-224 Z" fill="{cd}"/>'
                '<path d="M-10,-212 L-12,-176 M10,-212 L12,-176" stroke="#f4f1ea" stroke-width="4" stroke-linecap="round"/>'
                f'<path d="M-30,-150 L30,-150 L36,-118 L-36,-118 Z" fill="{cd}"/>')
    if kind == "coat":
        return (f'<path d="M-22,-224 L0,-170 L22,-224 Z" fill="#f4f1ea" opacity="0.9"/>'
                f'<path d="M-24,-224 L-6,-176 L-30,-186 Z" fill="{cd}"/><path d="M24,-224 L6,-176 L30,-186 Z" fill="{cd}"/>'
                + "".join(f'<circle cx="0" cy="{y}" r="4.5" fill="{cd}"/>' for y in (-156, -136, -116)))
    if kind == "scrubs":
        return ('<path d="M-22,-224 L0,-188 L22,-224 Z" fill="#7fb8d9"/>'
                f'<rect x="14" y="-176" width="26" height="30" rx="4" fill="none" stroke="{cd}" stroke-width="3"/>'
                '<rect x="20" y="-186" width="4" height="22" fill="#3a6fd8"/><rect x="28" y="-188" width="4" height="24" fill="#ef3b4f"/>'
                f'<path d="M-6,-224 L-6,-100 M6,-224 L6,-100" stroke="{cd}" stroke-width="3"/>')
    if kind == "sweater":
        return (f'<path d="M-24,-224 Q0,-208 24,-224" stroke="{cd}" stroke-width="7" fill="none"/>'
                + "".join(f'<path d="M{x},-112 L{x},-100" stroke="{cd}" stroke-width="3"/>' for x in range(-44, 48, 8))
                + f'<path d="M-36,-176 L36,-176" stroke="{cd}" stroke-width="5" stroke-dasharray="6 6"/>')
    if kind == "tie":
        return ('<path d="M-18,-224 L0,-204 L18,-224 Z" fill="#f4f1ea"/><path d="M0,-212 L-9,-196 L0,-150 L9,-196 Z" fill="#c9364a"/>')
    return f'<rect x="-3" y="-220" width="6" height="116" rx="3" fill="{cd}"/>'


def character(cid, who, x, y, scale=1.0, mood="neutral", arms=(8, -8), flip=False, held="", opacity=1.0, dim=0.0):
    c = CAST[who]
    kid = who in ("leo", "kid", "kid2", "maya")
    hw = (104 if kid else 94) / 2
    hy = -262
    skin = c["skin"]
    skin_d = SKIN_SH.get(skin, _shade(skin, 0.88))
    coat, cd = c["coat"], c.get("coat_d", _shade(c["coat"], 0.82))
    outfit = c.get("outfit") or {"hoodie": "hoodie", "tie": "tie", "glasses": "sweater"}.get(c.get("extra", ""), "zip")
    sx = -scale if flip else scale
    p = ['<ellipse cx="0" cy="2" rx="66" ry="12" fill="#000" opacity="0.28"/>']
    p.append(_hair_back(c["hair_style"], c["hair"], hw))  # behind the body
    legs = c["legs"]
    # legs with an inner shade + shoes with soles
    p.append(f'<rect x="-31" y="-114" width="26" height="110" rx="7" fill="{legs}"/><rect x="5" y="-114" width="26" height="110" rx="7" fill="{legs}"/>'
             f'<rect x="21" y="-114" width="10" height="110" rx="4" fill="{_shade(legs, 0.78)}"/>'
             '<path d="M-44,-2 Q-44,-18 -24,-18 L-6,-18 L-6,2 Z" fill="#1d1d24"/><path d="M44,-2 Q44,-18 24,-18 L6,-18 L6,2 Z" fill="#1d1d24"/>'
             '<rect x="-46" y="-3" width="40" height="6" rx="3" fill="#6b6f7a"/><rect x="6" y="-3" width="40" height="6" rx="3" fill="#6b6f7a"/>')

    def arm(side, ang):
        sxp = -46 if side == "L" else 46
        hand = held if (side == "R" and held) else ""
        return (f'<g id="{cid}-arm{side}" transform="rotate({ang} {sxp} -204)">'
                f'<rect x="{sxp-13}" y="-214" width="26" height="114" rx="13" fill="{cd if side == "R" else coat}"/>'
                f'<rect x="{sxp-13}" y="-122" width="26" height="14" rx="6" fill="{_shade(coat, 0.7)}"/>'
                f'<circle cx="{sxp}" cy="-96" r="15" fill="{skin}"/><circle cx="{sxp + (8 if side == "L" else -8)}" cy="-102" r="6" fill="{skin_d}"/>'
                f'{hand}</g>')
    p.append(arm("L", arms[0]))
    p.append(arm("R", arms[1]))
    # torso with a darker shade side (clipped)
    p.append(f'<clipPath id="{cid}-bc"><rect x="-52" y="-226" width="104" height="126" rx="26"/></clipPath>'
             f'<rect x="-52" y="-226" width="104" height="126" rx="26" fill="{coat}"/>'
             f'<rect x="22" y="-230" width="40" height="140" fill="{cd}" clip-path="url(#{cid}-bc)"/>'
             f'<rect x="-52" y="-112" width="104" height="12" fill="{_shade(coat, 0.72)}" clip-path="url(#{cid}-bc)"/>')
    p.append(_outfit(outfit, coat, cd, cid))
    if c.get("scarf"):
        sc = c["scarf"]
        p.append(f'<rect x="-34" y="-236" width="68" height="22" rx="10" fill="{sc}"/>'
                 f'<rect x="10" y="-222" width="20" height="60" rx="6" fill="{sc}"/><rect x="10" y="-172" width="20" height="10" fill="{_shade(sc, 0.75)}"/>')
    # neck
    p.append(f'<rect x="-12" y="-236" width="24" height="16" fill="{skin_d}"/>')
    # head
    h = [f'<ellipse cx="{-hw-2}" cy="{hy+4}" rx="9" ry="13" fill="{skin_d}"/><ellipse cx="{hw+2}" cy="{hy+4}" rx="9" ry="13" fill="{skin_d}"/>',
         f'<rect x="{-hw}" y="{hy-54}" width="{2*hw}" height="108" rx="44" fill="{skin}"/>',
         f'<path d="M{hw-14},{hy-40} Q{hw},{hy} {hw-12},{hy+46} Q{hw},{hy+30} {hw},{hy} Q{hw},{hy-30} {hw-14},{hy-40} Z" fill="{skin_d}" opacity="0.6"/>']
    if c.get("blush", True):
        h.append(f'<ellipse cx="-28" cy="{hy+22}" rx="11" ry="7" fill="#e8786f" opacity="0.32"/><ellipse cx="28" cy="{hy+22}" rx="11" ry="7" fill="#e8786f" opacity="0.32"/>')
    if c.get("freckles"):
        h.append("".join(f'<circle cx="{fx}" cy="{hy+fy}" r="2.2" fill="#a0603a" opacity="0.7"/>' for fx, fy in
                         [(-32, 14), (-24, 18), (-36, 22), (32, 14), (24, 18), (36, 22)]))
    h.append(f'<g id="{cid}-eyes" transform="translate(0 {hy}) scale(1 1) translate(0 {-hy})">'
             f'<ellipse cx="-18" cy="{hy+2}" rx="6.5" ry="8" fill="#1a1a22"/><ellipse cx="18" cy="{hy+2}" rx="6.5" ry="8" fill="#1a1a22"/>'
             f'<circle cx="-16" cy="{hy-1}" r="2.2" fill="#ffffff"/><circle cx="20" cy="{hy-1}" r="2.2" fill="#ffffff"/></g>')
    if c.get("extra") == "glasses":
        h.append(f'<g fill="none" stroke="#2a2a33" stroke-width="3.5"><circle cx="-18" cy="{hy+2}" r="14"/>'
                 f'<circle cx="18" cy="{hy+2}" r="14"/><path d="M-4,{hy+2} L4,{hy+2}"/></g>'
                 f'<circle cx="-22" cy="{hy-4}" r="4" fill="#ffffff" opacity="0.35"/><circle cx="14" cy="{hy-4}" r="4" fill="#ffffff" opacity="0.35"/>')
    bl, br, bdy = BROWS.get(mood, (0, 0, 0))
    bc = _shade(c["hair"], 0.6) if c["hair_style"] != "bald" else "#2a1f1a"
    h.append(f'<rect id="{cid}-browL" transform="translate(0 {bdy}) rotate({bl} -6 -281)" x="-30" y="{hy-23}" width="24" height="7" rx="3.5" fill="{bc}"/>'
             f'<rect id="{cid}-browR" transform="translate(0 {bdy}) rotate({br} 6 -281)" x="6" y="{hy-23}" width="24" height="7" rx="3.5" fill="{bc}"/>')
    h.append(f'<path d="M-2,{hy+8} Q-8,{hy+22} 2,{hy+24} Q8,{hy+22} 6,{hy+18}" fill="{skin_d}"/>')
    if c.get("extra") == "moustache":
        h.append(f'<path d="M-22,{hy+32} Q-10,{hy+22} 0,{hy+28} Q10,{hy+22} 22,{hy+32} Q10,{hy+38} 0,{hy+34} Q-10,{hy+38} -22,{hy+32} Z" fill="#3a2e2a"/>')
    my = hy + 36
    mouths = {
        "line": f'<rect x="-10" y="{my-2}" width="20" height="5" rx="2.5" fill="#5a2a2a"/>',
        "open": f'<ellipse cx="0" cy="{my}" rx="10" ry="12" fill="#4a1616"/><ellipse cx="0" cy="{my+6}" rx="6" ry="4" fill="#d86a6a"/>',
        "smile": f'<path d="M-15,{my-4} Q0,{my+12} 15,{my-4} Q0,{my+4} -15,{my-4} Z" fill="#5a2a2a"/>',
        "frown": f'<path d="M-12,{my+5} Q0,{my-6} 12,{my+5}" stroke="#5a2a2a" stroke-width="5" fill="none" stroke-linecap="round"/>',
        "o": f'<ellipse cx="0" cy="{my}" rx="6" ry="7" fill="#4a1616"/>',
    }
    start = {"neutral": "line", "happy": "smile", "scared": "open", "sad": "frown", "worried": "line",
             "shock": "o", "creepy": "smile", "angry": "frown"}.get(mood, "line")
    for k, v in mouths.items():
        h.append(f'<g id="{cid}-m-{k}" opacity="{1 if k == start else 0}">{v}</g>')
    h.append(_hair_front(c["hair_style"], c["hair"], hw))
    if c.get("hat"):
        h.append(_hat(c["hat"], c.get("hat_color", "#c9364a"), hw))
    if c.get("extra") == "headset":
        h.append(f'<path d="M{-hw-2},{hy} Q{-hw-2},{hy-70} 0,{hy-68}" stroke="#222" stroke-width="6" fill="none"/>'
                 f'<rect x="{-hw-10}" y="{hy-10}" width="14" height="26" rx="6" fill="#222"/>')
    p.append(f'<g id="{cid}-head">{"".join(h)}</g>')
    body = "".join(p)
    if dim:
        body = f'<g filter="url(#dim{int(dim*100)})">{body}</g>'
    return (f'<g id="{cid}" class="char" transform="translate({x} {y}) scale({sx} {scale})" opacity="{opacity}">{body}</g>')
