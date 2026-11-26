"""Set dressing: the small things that make a flat background read as a lived-in place."""
import random


def _sh(hex_, k):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)))


def wall(color, y0=0, y1=860, split=560, lower=None, seed=1, stains=True):
    """Two-tone painted wall with a dado rail, soft stains and a baseboard."""
    lower = lower or _sh(color, 0.8)
    rnd = random.Random(seed)
    out = [f'<rect x="0" y="{y0}" width="1920" height="{y1-y0}" fill="{color}"/>',
           f'<rect x="0" y="{split}" width="1920" height="{y1-split}" fill="{lower}"/>',
           f'<rect x="0" y="{split-8}" width="1920" height="12" fill="{_sh(color, 0.7)}"/>',
           f'<rect x="0" y="{y1-26}" width="1920" height="26" fill="{_sh(lower, 0.7)}"/>']
    if stains:
        for _ in range(9):
            x, y, r = rnd.uniform(0, 1920), rnd.uniform(y0 + 40, split - 40), rnd.uniform(60, 180)
            out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*0.6:.0f}" fill="{_sh(color, 0.9)}" opacity="0.35"/>')
        for _ in range(4):
            x, y = rnd.uniform(0, 1920), rnd.uniform(split + 40, y1 - 60)
            out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="120" ry="40" fill="{_sh(lower, 0.88)}" opacity="0.4"/>')
    return "".join(out)


def floor_planks(color, y=860, h=220, seed=2):
    rnd = random.Random(seed)
    out = [f'<rect x="0" y="{y}" width="1920" height="{h}" fill="{color}"/>']
    for r in range(0, h, 34):
        off = rnd.uniform(0, 300)
        for x in range(-300, 1920, 300):
            out.append(f'<rect x="{x+off:.0f}" y="{y+r}" width="4" height="34" fill="{_sh(color, 0.8)}"/>')
        out.append(f'<rect x="0" y="{y+r}" width="1920" height="3" fill="{_sh(color, 0.82)}"/>')
    return "".join(out)


def floor_tiles(color, y=860, h=220):
    out = [f'<rect x="0" y="{y}" width="1920" height="{h}" fill="{color}"/>']
    for k, x in enumerate(range(0, 1920, 96)):
        out.append(f'<rect x="{x}" y="{y}" width="96" height="48" fill="{_sh(color, 0.9 if k % 2 else 1.0)}"/>')
        out.append(f'<rect x="{x}" y="{y+48}" width="96" height="48" fill="{_sh(color, 1.0 if k % 2 else 0.9)}"/>')
    return "".join(out)


def outlet(x, y, color="#e8e4da"):
    return (f'<rect x="{x}" y="{y}" width="34" height="48" rx="5" fill="{color}"/><rect x="{x+11}" y="{y+12}" width="4" height="9" fill="#333"/>'
            f'<rect x="{x+19}" y="{y+12}" width="4" height="9" fill="#333"/><rect x="{x+11}" y="{y+28}" width="4" height="9" fill="#333"/><rect x="{x+19}" y="{y+28}" width="4" height="9" fill="#333"/>')


def switch(x, y, color="#e8e4da"):
    return f'<rect x="{x}" y="{y}" width="34" height="52" rx="5" fill="{color}"/><rect x="{x+12}" y="{y+14}" width="10" height="22" rx="3" fill="{_sh(color, 0.8)}"/>'


def frame(x, y, w, h, inner="#8aa0b8", wood="#6b4a32"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{wood}"/><rect x="{x+10}" y="{y+10}" width="{w-20}" height="{h-20}" fill="{inner}"/>'
            f'<path d="M{x+10},{y+h-10} L{x+w*0.4},{y+h*0.5} L{x+w*0.6},{y+h*0.68} L{x+w*0.75},{y+h*0.55} L{x+w-10},{y+h-10} Z" fill="{_sh(inner, 0.7)}"/>'
            f'<circle cx="{x+w*0.72}" cy="{y+h*0.32}" r="{min(w,h)*0.08}" fill="#f4e3a8"/>')


def shelf(x, y, w=360, seed=3):
    rnd = random.Random(seed)
    cols = ["#c9364a", "#3a6fd8", "#ffd43b", "#3fbf7f", "#e8e4da", "#8a5a9a", "#d9773b"]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="14" fill="#6b4a32"/><rect x="{x+10}" y="{y+14}" width="10" height="30" fill="#4f3624"/><rect x="{x+w-20}" y="{y+14}" width="10" height="30" fill="#4f3624"/>']
    bx = x + 10
    while bx < x + w - 30:
        bw, bh = rnd.randint(14, 26), rnd.randint(50, 80)
        tilt = rnd.choice([0, 0, 0, -8])
        out.append(f'<rect x="{bx}" y="{y-bh}" width="{bw}" height="{bh}" rx="2" fill="{rnd.choice(cols)}" transform="rotate({tilt} {bx} {y})"/>')
        bx += bw + rnd.randint(2, 6)
    return "".join(out)


def plant(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-36,0 L-28,-60 L28,-60 L36,0 Z" fill="#b5603a"/><rect x="-40" y="-68" width="80" height="12" rx="4" fill="#9a4f2e"/>'
            + "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="18" ry="44" fill="{c}" transform="rotate({r} {dx} {dy})"/>'
                      for dx, dy, r, c in [(-30, -110, -30, "#3f8f5a"), (0, -130, 0, "#4fa56a"), (30, -110, 30, "#3f8f5a"), (-14, -100, -12, "#5ab878"), (16, -100, 14, "#5ab878")])
            + '</g>')


def rug(x, y, w=700, color="#8a4a5a"):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="34" fill="{color}"/><ellipse cx="{x}" cy="{y}" rx="{w/2-24}" ry="22" fill="none" stroke="{_sh(color, 1.25)}" stroke-width="5"/>')


def radiator(x, y, n=8):
    return ("".join(f'<rect x="{x+k*22}" y="{y}" width="18" height="120" rx="8" fill="#d9dde6"/>' for k in range(n))
            + f'<rect x="{x-6}" y="{y+104}" width="{n*22+8}" height="10" fill="#b9bdc8"/>')


def bulb(x, y0=0, y1=170, lit=True):
    return (f'<rect x="{x-2}" y="{y0}" width="4" height="{y1-y0}" fill="#2a2a2a"/><rect x="{x-9}" y="{y1}" width="18" height="16" fill="#5a5a5a"/>'
            f'<circle cx="{x}" cy="{y1+30}" r="18" fill="{"#fff1b8" if lit else "#8a8a7a"}"/>'
            + (f'<circle cx="{x}" cy="{y1+30}" r="140" fill="#ffd98a" opacity="0.10"/>' if lit else ""))


def clock(x, y, r=38):
    return (f'<circle cx="{x}" cy="{y}" r="{r+6}" fill="#3a3346"/><circle cx="{x}" cy="{y}" r="{r}" fill="#f4f1ea"/>'
            f'<path d="M{x},{y} L{x},{y-r*0.6} M{x},{y} L{x+r*0.45},{y+r*0.2}" stroke="#2a2a33" stroke-width="5" stroke-linecap="round"/>')


def curtain(x, y, w, h, color="#7a4a5a"):
    out = [f'<rect x="{x-14}" y="{y-14}" width="{w+28}" height="10" rx="5" fill="#4a3a30"/>']
    for k in range(6):
        out.append(f'<rect x="{x + k * w / 6:.0f}" y="{y}" width="{w/6+2:.0f}" height="{h}" fill="{_sh(color, 0.88 if k % 2 else 1.0)}"/>')
    return "".join(out)


def pine(x, y, s=1.0, snow=True, color="#2f5a48"):
    sn = "#eef3fa"
    layers = []
    for k, (w, yy) in enumerate([(120, -60), (96, -130), (70, -195), (44, -250)]):
        layers.append(f'<path d="M{-w},{yy} L0,{yy-110} L{w},{yy} Z" fill="{color}"/>')
        if snow:
            layers.append(f'<path d="M{-w*0.55},{yy-50} L0,{yy-110} L{w*0.55},{yy-50} Q0,{yy-70} {-w*0.55},{yy-50} Z" fill="{sn}"/>')
    return f'<g transform="translate({x} {y}) scale({s})"><rect x="-10" y="-60" width="20" height="60" fill="#5a3b2a"/>{"".join(layers)}</g>'


def fence(x0, x1, y, color="#7a6252", snow=True):
    out = [f'<rect x="{x0}" y="{y-70}" width="{x1-x0}" height="10" fill="{color}"/><rect x="{x0}" y="{y-36}" width="{x1-x0}" height="10" fill="{color}"/>']
    for x in range(int(x0), int(x1), 40):
        out.append(f'<path d="M{x},{y} L{x},{y-90} L{x+10},{y-102} L{x+20},{y-90} L{x+20},{y} Z" fill="{_sh(color, 1.1)}"/>')
        if snow:
            out.append(f'<ellipse cx="{x+10}" cy="{y-96}" rx="14" ry="7" fill="#eef3fa"/>')
    return "".join(out)


def pole_wires(xs, top=180, ground=860, color="#3a3346", wire="#2a2433"):
    out = []
    for x in xs:
        out.append(f'<rect x="{x-7}" y="{top}" width="14" height="{ground-top}" fill="{color}"/><rect x="{x-50}" y="{top+20}" width="100" height="10" fill="{color}"/>')
    for a, b in zip(xs, xs[1:]):
        for dy in (24, 40):
            out.append(f'<path d="M{a-44},{top+dy} Q{(a+b)/2},{top+dy+60} {b-44},{top+dy}" stroke="{wire}" stroke-width="3" fill="none"/>')
            out.append(f'<path d="M{a+44},{top+dy} Q{(a+b)/2},{top+dy+60} {b+44},{top+dy}" stroke="{wire}" stroke-width="3" fill="none"/>')
    return "".join(out)


def mailbox(x, y, color="#3a6fd8"):
    return (f'<rect x="{x-6}" y="{y-110}" width="12" height="110" fill="#5a3b2a"/><path d="M{x-40},{y-110} L{x-40},{y-150} Q{x},{y-180} {x+40},{y-150} L{x+40},{y-110} Z" fill="{color}"/>'
            f'<rect x="{x+38}" y="{y-160}" width="6" height="34" fill="#ef3b4f"/><ellipse cx="{x}" cy="{y-168}" rx="40" ry="10" fill="#eef3fa"/>')


def smoke(x, y, s=1.0, color="#c9cfda"):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{color}" opacity="0.6"><circle cx="0" cy="0" r="16"/><circle cx="14" cy="-30" r="22"/>'
            '<circle cx="-6" cy="-64" r="26"/><circle cx="18" cy="-100" r="30"/></g>')


def cobweb(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="#ffffff" stroke-opacity="0.18" stroke-width="2" fill="none">'
            '<path d="M0,0 L80,0 M0,0 L0,80 M0,0 L60,60"/><path d="M20,0 Q18,18 0,20 M44,0 Q40,40 0,44 M70,0 Q62,62 0,70"/></g>')
