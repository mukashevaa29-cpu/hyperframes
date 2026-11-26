"""Winter backgrounds for EP02 (The Whiteout), dressed to the reference channel's detail level.
Same conventions as bgs.py: 1920x1080 SVG bodies, side view, ground at y=860, dark band under it.
"""
import random

from art import moon, stars, window, house
from bgs import BG, W, H, FLOOR, _floor
import deco as D

SNOW = "#eef3fa"
SNOW_SH = "#c9d6e8"
NIGHT_SNOW = "#9fb0cc"
NIGHT_SNOW_SH = "#7f90ad"


def _band():
    return f'<rect x="0" y="{FLOOR+70}" width="{W}" height="{H-FLOOR-70}" fill="#0b0d14" opacity="0.45"/>'


def _drift(y, color, seed=1, amp=40, n=7):
    rnd = random.Random(seed)
    pts = [f"M0,{H}", f"L0,{y + rnd.uniform(-amp, amp):.0f}"]
    step = W / n
    for k in range(n):
        x1, x2 = step * k + step / 2, step * (k + 1)
        pts.append(f"Q{x1:.0f},{y + rnd.uniform(-amp, amp):.0f} {x2:.0f},{y + rnd.uniform(-amp * 0.5, amp * 0.5):.0f}")
    pts.append(f"L{W},{H} Z")
    return f'<path d="{" ".join(pts)}" fill="{color}"/>'


def snow_house(x, y, w, h, body, roof, lit, night, seed=0, buried=0.0, chimney=True):
    s, sh = (NIGHT_SNOW, NIGHT_SNOW_SH) if night else (SNOW, SNOW_SH)
    out = []
    if chimney:
        out.append(f'<rect x="{x+w*0.68}" y="{y-h-h*0.42}" width="34" height="{h*0.3}" fill="{D._sh(body, 0.75)}"/>'
                   f'<rect x="{x+w*0.68-4}" y="{y-h-h*0.42-6}" width="42" height="12" fill="{s}"/>')
        out.append(D.smoke(x + w * 0.68 + 17, y - h - h * 0.46, 0.9, "#d7dde8" if not night else "#5a6680"))
    out.append(house(x, y, w, h, body, roof, lit, seed=seed))
    # siding lines + window sills with snow + gutters
    out.append(f'<g stroke="{D._sh(body, 0.88)}" stroke-width="3">' + "".join(
        f'<line x1="{x}" y1="{yy}" x2="{x+w}" y2="{yy}"/>' for yy in range(int(y - h + 18), int(y), 22)) + '</g>')
    cols, rows = max(2, int(w // 70)), max(1, int(h // 90))
    for r in range(rows):
        for c_ in range(cols):
            wx = x + (c_ + 0.5) * w / cols - 18
            wy = y - h + 24 + r * 90
            out.append(f'<rect x="{wx-4}" y="{wy+44}" width="44" height="6" fill="{D._sh(body, 0.7)}"/><ellipse cx="{wx+18}" cy="{wy+44}" rx="24" ry="6" fill="{s}"/>')
    out.append(f'<path d="M{x-24},{y-h} L{x+w/2},{y-h-h*0.45} L{x+w+24},{y-h} L{x+w+10},{y-h+16} '
               f'Q{x+w/2},{y-h-h*0.25} {x-10},{y-h+16} Z" fill="{s}"/>')
    out.append("".join(f'<path d="M{x+k*w/7:.0f},{y-h+8} l6,{14+(k%3)*8} l6,-{14+(k%3)*8} Z" fill="#dff1ff" opacity="0.9"/>' for k in range(1, 7)))
    if buried > 0:
        top = y - h * buried
        out.append(f'<path d="M{x-60},{y+40} L{x-60},{top+30} Q{x+w*0.3},{top-20} {x+w*0.6},{top+10} '
                   f'Q{x+w*0.85},{top+30} {x+w+60},{top+40} L{x+w+60},{y+40} Z" fill="{s}"/>'
                   f'<path d="M{x-60},{top+30} Q{x+w*0.3},{top-20} {x+w*0.6},{top+10}" stroke="{sh}" stroke-width="10" fill="none"/>')
    return "".join(out)


def _hills(night, seed=4):
    c1, c2 = ("#1a2546", "#14203c") if night else ("#dfe6ef", "#d2dbe6")
    return (_drift(560, c1, seed=seed, amp=70, n=5).replace(f"M0,{H}", f"M0,{H}") +
            _drift(640, c2, seed=seed + 1, amp=50, n=6))


def town_snow(night=False, buried=0.0, lit=(True, False, True, True), seed=3):
    sky = "#0b1430" if night else "#c7d3e2"
    out = [f'<rect width="{W}" height="{H}" fill="{sky}"/>']
    if night:
        out.append(stars(40, 0, 0, W, 360, seed=seed, op=0.5) + moon(1700, 150, 34))
    else:
        out.append('<rect width="1920" height="1080" fill="#ffffff" opacity="0.18"/>')
    out.append(_hills(night, seed))
    for k, x in enumerate((40, 520, 1450)):
        out.append(D.pine(x if k != 1 else 1040, 760, 0.9 + 0.1 * (k % 2), color="#22403a" if night else "#2f5a48"))
    out.append(D.pole_wires([300, 980, 1660], top=200, ground=860, color="#3a3346" if night else "#6a6070"))
    cols = [("#2b3552", "#1b2440"), ("#33314e", "#22213a"), ("#2a3a52", "#1b2840")] if night else \
           [("#b9a58e", "#7a5a4a"), ("#a9b4a0", "#5f6f56"), ("#c4b3a2", "#6e4f45")]
    for k, x in enumerate((60, 520, 980, 1440)):
        b, r = cols[k % 3]
        out.append(snow_house(x, FLOOR, 380, 260 + (k % 2) * 40, b, r, [lit[k % len(lit)]] * 3, night, seed=k, buried=buried))
    out.append(D.fence(0, 420, FLOOR + 10, "#5a4a42" if night else "#8a7262"))
    out.append(D.mailbox(470, FLOOR + 10, "#3a6fd8"))
    out.append(D.mailbox(1400, FLOOR + 10, "#c9364a"))
    out.append(D.pine(1880, FLOOR + 40, 1.3, color="#22403a" if night else "#2f5a48"))
    out.append(_drift(FLOOR - 10 - buried * 120, NIGHT_SNOW if night else SNOW, seed=seed, amp=30))
    out.append(_band())
    return "".join(out)


def whiteout(figures=0, seed=5):
    rnd = random.Random(seed)
    out = ['<defs><linearGradient id="wo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe6ef"/>'
           '<stop offset="1" stop-color="#f4f7fb"/></linearGradient></defs>',
           f'<rect width="{W}" height="{H}" fill="url(#wo)"/>',
           '<g opacity="0.45">' + D.pole_wires([200, 900, 1600], top=260, ground=860, color="#aab4c2", wire="#b9c2ce") + '</g>',
           '<g fill="#c6cfdb" opacity="0.55">' + "".join(
               f'<path d="M{x},{FLOOR-40} L{x},{FLOOR-180} L{x+110},{FLOOR-250} L{x+220},{FLOOR-180} L{x+220},{FLOOR-40} Z"/>'
               for x in (100, 700, 1350)) + '</g>',
           '<g opacity="0.35">' + D.pine(600, 820, 0.8, color="#8a9aaa") + D.pine(1250, 830, 0.7, color="#8a9aaa") + '</g>']
    for k in range(figures):
        x = 300 + k * 420 + rnd.uniform(-60, 60)
        o = 0.35 + 0.15 * (k % 2)
        out.append(f'<g opacity="{o}" fill="#6f7a8c" transform="translate({x:.0f} {FLOOR-20}) scale({0.8 + 0.1 * (k % 3)})">'
                   '<ellipse cx="0" cy="-262" rx="44" ry="50"/><rect x="-50" y="-222" width="100" height="125" rx="26"/>'
                   '<rect x="-30" y="-110" width="24" height="110" rx="8"/><rect x="6" y="-110" width="24" height="110" rx="8"/></g>')
    out.append(_drift(FLOOR + 10, "#f7f9fc", seed=seed, amp=20))
    out.append(f'<rect x="0" y="{FLOOR+70}" width="{W}" height="{H-FLOOR-70}" fill="#1a2030" opacity="0.35"/>')
    return "".join(out)


def living_winter(fire=True, blankets=True, lit=True):
    wall = "#5e4a3c" if lit else "#3e3348"
    out = [D.wall(wall, split=600, seed=11), D.floor_planks("#4a3428" if lit else "#2e2532"),
           D.rug(1020, 900, 760, "#7a3e4e"),
           window(1380, 170, 340, 300, sky="#d9e2ee", frame="#4a3f55", inner='<rect width="340" height="300" fill="#e9eef5"/>')]
    out.append(D.curtain(1366, 150, 368, 340, "#7a4a5a") if blankets else "")
    out.append(D.frame(760, 190, 150, 190, "#9fb0c8") + D.frame(940, 230, 120, 120, "#c8a98f") + D.frame(1090, 200, 110, 150, "#a8c0a0"))
    out.append(D.shelf(760, 470, 420, seed=12))
    out.append(D.clock(1250, 230, 34))
    out.append(D.outlet(1290, 680) + D.switch(1830, 420))
    out.append(D.radiator(1420, 700, 9))
    # fireplace with bricks + mantel decor
    out.append('<rect x="240" y="420" width="420" height="440" fill="#7a5a4a"/>'
               + "".join(f'<rect x="{240 + (c * 60) + (30 if r % 2 else 0)}" y="{420 + r * 30}" width="56" height="26" fill="#8a6a58"/>'
                         for r in range(14) for c in range(7) if 240 + c * 60 + (30 if r % 2 else 0) < 640)
               + '<rect x="220" y="400" width="460" height="40" rx="6" fill="#4a3a30"/>'
               '<path d="M330,860 L330,600 Q450,520 570,600 L570,860 Z" fill="#1a1210"/>'
               '<rect x="270" y="350" width="40" height="50" rx="4" fill="#c9b27a"/><rect x="560" y="330" width="60" height="70" rx="6" fill="#6a8a9a"/>'
               '<rect x="350" y="840" width="200" height="20" fill="#3a2a20"/>')
    if fire:
        out.append('<path d="M380,860 Q370,760 420,720 Q410,780 450,770 Q450,700 500,680 Q490,760 530,790 Q540,840 520,860 Z" fill="#ff8a2a"/>'
                   '<path d="M420,860 Q420,800 450,780 Q455,820 480,810 Q495,840 490,860 Z" fill="#ffd36a"/>'
                   '<circle cx="450" cy="760" r="420" fill="#ff9a3a" opacity="0.10"/><circle cx="450" cy="760" r="220" fill="#ffb84d" opacity="0.10"/>')
    out.append('<rect x="760" y="800" width="520" height="56" rx="16" fill="#c9d2ee"/>'
               '<path d="M800,800 Q1000,770 1250,800 L1250,840 L800,840 Z" fill="#8a6fb0"/>'
               '<rect x="1180" y="770" width="90" height="40" rx="14" fill="#efe6d6"/>')
    out.append('<path d="M1780,860 L1780,560 L1920,560 L1920,860 Z" fill="#1a141e"/>')
    out.append(D.plant(700, 860, 0.9))
    out.append(D.cobweb(0, 0, 1.2))
    out.append(_band())
    return "".join(out)


def kitchen_winter(card=True, pots=True):
    out = [D.wall("#6a6478", split=540, seed=21), D.floor_tiles("#4a4656"),
           '<rect x="980" y="600" width="760" height="260" fill="#5a5d72"/><rect x="960" y="580" width="800" height="28" rx="4" fill="#7a7e96"/>',
           "".join(f'<rect x="{990+i*190}" y="620" width="170" height="220" rx="6" fill="#646880"/><rect x="{1062+i*190}" y="700" width="26" height="8" rx="4" fill="#c9cad1"/>' for i in range(4)),
           '<rect x="980" y="180" width="760" height="190" rx="6" fill="#5a5d72"/>',
           "".join(f'<rect x="{990+i*190}" y="190" width="170" height="170" rx="4" fill="#646880"/>' for i in range(4)),
           # sink + tap + window over the sink
           window(1220, 360, 260, 180, sky="#e9eef5", frame="#4a3f55", inner='<rect width="260" height="180" fill="#eef3fa"/>'),
           '<rect x="1250" y="570" width="200" height="14" rx="6" fill="#b9bdc8"/><path d="M1350,570 L1350,520 Q1350,500 1380,500 L1392,500" stroke="#9aa4ad" stroke-width="10" fill="none"/>',
           # fridge with magnets + drawings
           '<rect x="160" y="250" width="300" height="610" rx="14" fill="#dfe3ea"/><rect x="170" y="470" width="280" height="6" fill="#b9bdc8"/>'
           '<rect x="420" y="330" width="10" height="90" rx="5" fill="#9aa4ad"/><rect x="420" y="520" width="10" height="120" rx="5" fill="#9aa4ad"/>'
           '<rect x="190" y="520" width="110" height="90" fill="#fff8de" transform="rotate(5 245 565)"/><path d="M205,590 L230,555 L255,580 L285,545" stroke="#3a6fd8" stroke-width="5" fill="none"/>'
           '<circle cx="330" cy="280" r="10" fill="#3fbf7f"/><circle cx="380" cy="560" r="10" fill="#ffd43b"/>',
           D.clock(620, 230, 36), D.outlet(820, 620), D.plant(1560, 580, 0.6),
           '<rect x="560" y="430" width="240" height="14" fill="#6b4a32"/>' + "".join(
               f'<rect x="{574+k*44}" y="{378+(k%2)*8}" width="34" height="{52-(k%2)*8}" rx="6" fill="{c}"/>' for k, c in enumerate(["#c9364a", "#e8e4da", "#3a6fd8", "#ffd43b", "#8a5a9a"]))]
    if card:
        out.append('<g transform="translate(250 340) rotate(-4)"><rect x="-70" y="-90" width="140" height="180" rx="6" fill="#ffffff"/>'
                   + "".join(f'<rect x="-52" y="{-62+k*16}" width="{104 if k % 3 else 80}" height="6" rx="3" fill="#2a2a33"/>' for k in range(9))
                   + '<circle cx="0" cy="-96" r="9" fill="#ef3b4f"/></g>')
    if pots:
        out.append("".join(f'<g transform="translate({1040+k*150} 580)"><rect x="-55" y="-70" width="110" height="70" rx="10" fill="#8a8f9c"/>'
                           f'<rect x="-50" y="-66" width="100" height="14" rx="6" fill="#7fb8ff" opacity="0.8"/><rect x="-74" y="-60" width="20" height="8" rx="4" fill="#5a5f6a"/></g>' for k in range(4)))
    out.append(_band())
    return "".join(out)


def bathroom():
    out = [f'<rect width="{W}" height="{H}" fill="#cfdbe0"/>',
           '<g fill="#bfcdd4">' + "".join(f'<rect x="{x}" y="{y}" width="116" height="76"/>' for x in range(0, 1920, 120) for y in range(260, 860, 80)) + '</g>',
           D.floor_tiles("#7d8b93"),
           '<rect x="1560" y="250" width="230" height="300" rx="10" fill="#e9eef2"/><rect x="1580" y="270" width="190" height="260" fill="#b9d0dc"/>',
           '<rect x="1560" y="560" width="230" height="16" rx="6" fill="#d9e0e6"/><rect x="1590" y="520" width="20" height="40" rx="4" fill="#3fbf7f"/><rect x="1620" y="510" width="16" height="50" rx="4" fill="#ef3b4f"/>',
           '<rect x="140" y="300" width="18" height="200" fill="#9aa4ad"/><rect x="120" y="300" width="160" height="12" rx="6" fill="#9aa4ad"/>'
           '<rect x="150" y="312" width="110" height="160" rx="10" fill="#e07a5a"/><rect x="150" y="440" width="110" height="20" fill="#c9603f"/>',
           '<rect x="420" y="560" width="1080" height="300" rx="60" fill="#f4f6f8"/><rect x="420" y="760" width="1080" height="100" rx="40" fill="#e2e8ec"/>',
           '<rect x="470" y="580" width="980" height="120" rx="40" fill="#7fb8ff" opacity="0.6"/>',
           '<rect x="1380" y="440" width="24" height="120" fill="#9aa4ad"/><rect x="1300" y="430" width="110" height="24" rx="10" fill="#9aa4ad"/>',
           "".join(f'<g transform="translate({560+k*90} 560)"><rect x="-18" y="-60" width="36" height="60" rx="8" fill="{c}" opacity="0.85"/><rect x="-8" y="-74" width="16" height="16" fill="#5a5f6a"/></g>'
                   for k, c in enumerate(["#7fb8ff", "#bfe3ff", "#7fb8ff"])),
           _band()]
    return "".join(out)


def house_side(buried=0.6, night=False):
    s = NIGHT_SNOW if night else SNOW
    out = [f'<rect width="{W}" height="{H}" fill="{"#0b1430" if night else "#c7d3e2"}"/>',
           '<rect x="0" y="120" width="1920" height="760" fill="#9a8574"/>',
           '<g stroke="#8a7564" stroke-width="4">' + "".join(f'<line x1="0" y1="{y}" x2="1920" y2="{y}"/>' for y in range(160, 880, 40)) + '</g>',
           '<path d="M0,120 L1920,120 L1920,90 L0,90 Z" fill="#6e5a4c"/>' + "".join(
               f'<path d="M{x},120 l7,{18+(x//60)%3*10} l7,-{18+(x//60)%3*10} Z" fill="#dff1ff"/>' for x in range(40, 1900, 60)),
           window(300, 260, 300, 240, sky="#1a2030", frame="#e8e2d6"), D.curtain(312, 272, 276, 120, "#7a4a5a"),
           '<rect x="840" y="250" width="16" height="610" fill="#8a8f9c"/><rect x="826" y="240" width="44" height="18" rx="6" fill="#8a8f9c"/>',
           '<rect x="1100" y="560" width="160" height="60" rx="10" fill="#6a6f7a"/><rect x="1240" y="548" width="40" height="84" rx="8" fill="#5a5f6a"/>',
           '<rect x="1500" y="300" width="80" height="110" rx="6" fill="#c9cad1"/><circle cx="1540" cy="340" r="22" fill="#e8e8ee"/><rect x="1520" y="380" width="40" height="14" fill="#8a8f9c"/>',
           D.outlet(1650, 600, "#c9cad1"),
           f'<path d="M0,{H} L0,{880-buried*360} Q700,{860-buried*420} 1300,{870-buried*380} Q1700,{890-buried*360} 1920,{880-buried*370} L1920,{H} Z" fill="{s}"/>',
           _band()]
    return "".join(out)


def garage_grill():
    out = [D.wall("#4a4a56", split=520, lower="#3a3a46", seed=31), D.floor_planks("#2e2e36"),
           '<rect x="200" y="200" width="1100" height="660" fill="#2a2a32"/>',
           '<g stroke="#3a3a46" stroke-width="6">' + "".join(f'<line x1="200" y1="{y}" x2="1300" y2="{y}"/>' for y in range(240, 860, 60)) + '</g>',
           # pegboard with tools
           '<rect x="1380" y="180" width="260" height="200" fill="#8a6a4a"/>' + "".join(
               f'<circle cx="{1400+c*30}" cy="{200+r*30}" r="3" fill="#5a3f2a"/>' for c in range(8) for r in range(6))
           + '<rect x="1420" y="210" width="10" height="110" fill="#c9364a"/><rect x="1410" y="210" width="30" height="20" fill="#9aa4ad"/>'
           '<path d="M1490,220 L1520,330" stroke="#9aa4ad" stroke-width="10"/><circle cx="1580" cy="260" r="30" fill="none" stroke="#3fbf7f" stroke-width="8"/>',
           '<rect x="1340" y="700" width="140" height="160" rx="8" fill="#c9364a"/><rect x="1360" y="680" width="60" height="30" rx="6" fill="#a3182c"/>',
           '<rect x="140" y="760" width="90" height="100" rx="10" fill="#3a6fd8"/><rect x="160" y="740" width="50" height="20" fill="#2a4f9f"/>',
           '<g transform="translate(1500 860)"><rect x="-90" y="-260" width="180" height="120" rx="30" fill="#2b2f3a"/>'
           '<rect x="-12" y="-140" width="24" height="140" fill="#2b2f3a"/><rect x="-80" y="-20" width="160" height="20" rx="8" fill="#2b2f3a"/>'
           '<path d="M-40,-280 Q-30,-330 -50,-370 M0,-280 Q10,-340 -10,-390 M40,-280 Q50,-330 30,-380" stroke="#9aa4b4" stroke-width="10" fill="none" opacity="0.5"/></g>',
           '<circle cx="1500" cy="560" r="300" fill="#ff8a2a" opacity="0.06"/>',
           D.bulb(760, 0, 120, lit=True),
           '<rect x="1680" y="360" width="200" height="500" fill="#4a3b30"/><circle cx="1700" cy="620" r="8" fill="#c9b27a"/>',
           D.cobweb(1300, 0, 1.0), _band()]
    return "".join(out)


def upstairs_window():
    out = [D.wall("#3e3650", split=900, seed=41, stains=True),
           '<rect x="260" y="120" width="1400" height="740" fill="#dde4ee"/>',
           '<g opacity="0.5">' + D.pole_wires([500, 1300], top=260, ground=760, color="#9aa6b8", wire="#9aa6b8") + '</g>',
           '<g fill="#9aa6b8" opacity="0.6">' + "".join(
               f'<g transform="translate({x} 720) scale({s})"><ellipse cx="0" cy="-262" rx="44" ry="50"/>'
               '<rect x="-50" y="-222" width="100" height="125" rx="26"/><rect x="-30" y="-110" width="24" height="110" rx="8"/>'
               '<rect x="6" y="-110" width="24" height="110" rx="8"/></g>' for x, s in ((560, 0.55), (980, 0.45), (1360, 0.6))) + '</g>',
           '<g opacity="0.55">' + D.pine(420, 700, 0.6, color="#8a9aaa") + D.pine(1500, 690, 0.7, color="#8a9aaa") + '</g>',
           '<path d="M260,860 L260,640 Q700,600 1100,650 Q1400,680 1660,630 L1660,860 Z" fill="#f4f7fb"/>',
           '<rect x="240" y="100" width="1440" height="30" fill="#4a3f55"/><rect x="240" y="100" width="30" height="780" fill="#4a3f55"/>'
           '<rect x="1650" y="100" width="30" height="780" fill="#4a3f55"/><rect x="945" y="100" width="30" height="780" fill="#4a3f55"/>',
           '<path d="M270,130 Q330,300 300,520" stroke="#ffffff" stroke-opacity="0.35" stroke-width="22" fill="none"/>',
           '<path d="M1640,140 Q1600,260 1620,400" stroke="#ffffff" stroke-opacity="0.3" stroke-width="18" fill="none"/>',
           D.curtain(150, 100, 100, 760, "#6a4a6a"), D.curtain(1690, 100, 100, 760, "#6a4a6a"),
           '<rect x="200" y="860" width="1520" height="40" fill="#4a3f55"/>', _floor("#1e1a26")]
    return "".join(out)


def ceiling_cracks():
    out = [D.wall("#4e4660", y0=0, y1=860, split=620, seed=51),
           '<rect x="0" y="0" width="1920" height="300" fill="#5a5168"/>',
           '<g stroke="#2a2433" stroke-width="5" fill="none" stroke-linecap="round">'
           '<path d="M700,0 L740,60 L720,120 L780,190 L770,260"/><path d="M740,60 L820,90"/><path d="M1200,0 L1180,80 L1230,150 L1210,230"/><path d="M1180,80 L1120,110"/></g>',
           '<path d="M0,300 L1920,300" stroke="#3a3346" stroke-width="10"/>',
           '<rect x="300" y="0" width="22" height="300" fill="#463e56"/><rect x="900" y="0" width="22" height="300" fill="#463e56"/><rect x="1500" y="0" width="22" height="300" fill="#463e56"/>',
           D.bulb(960, 300, 380, lit=False), D.frame(400, 420, 160, 120, "#7a8aa0"), D.clock(1500, 460, 34),
           D.floor_planks("#2a2433"), D.rug(1020, 900, 700, "#4a3a5a"),
           '<rect x="760" y="800" width="520" height="56" rx="16" fill="#c9d2ee"/><path d="M800,800 Q1000,770 1250,800 L1250,840 L800,840 Z" fill="#6a5a8a"/>',
           D.cobweb(0, 300, 1.0), _band()]
    return "".join(out)


def car_buried(night=False):
    s = NIGHT_SNOW if night else SNOW
    out = [f'<rect width="{W}" height="{H}" fill="{"#0b1430" if night else "#c7d3e2"}"/>', _hills(night, 7),
           D.pine(1180, 760, 1.0), D.pole_wires([200, 1100], top=220, ground=860, color="#6a6070"),
           snow_house(1300, FLOOR, 500, 340, "#b9a58e", "#7a5a4a", [False, False], night, seed=9, buried=0.5),
           '<g transform="translate(300 860)"><rect x="0" y="-300" width="620" height="240" rx="30" fill="#5a7da8"/>'
           '<rect x="40" y="-270" width="180" height="90" rx="10" fill="#1d2c44"/><rect x="250" y="-270" width="180" height="90" rx="10" fill="#1d2c44"/>'
           '<rect x="0" y="-150" width="620" height="14" fill="#4a6a90"/><rect x="560" y="-200" width="40" height="24" rx="6" fill="#ffd98a"/>'
           '<circle cx="140" cy="-50" r="56" fill="#1d1f26"/><circle cx="500" cy="-50" r="56" fill="#1d1f26"/>'
           '<rect x="600" y="-110" width="50" height="20" rx="6" fill="#3a3f4f"/></g>',
           f'<path d="M150,{H} L150,700 Q400,560 700,600 Q900,620 1050,720 L1050,{H} Z" fill="{s}"/>',
           f'<path d="M0,{H} L0,860 Q600,820 1200,850 Q1600,860 1920,840 L1920,{H} Z" fill="{s}"/>',
           D.mailbox(1180, FLOOR + 20), '<rect x="1060" y="640" width="12" height="220" fill="#5a3b2a"/>', _band()]
    return "".join(out)


def shed():
    out = [f'<rect width="{W}" height="{H}" fill="#3a2e26"/>', D.floor_planks("#2a211c"),
           '<g fill="#4a3a30">' + "".join(f'<rect x="{x}" y="0" width="150" height="860"/>' for x in range(0, 1920, 170)) + '</g>',
           '<rect x="200" y="140" width="300" height="200" fill="#8a6a4a"/>' + "".join(f'<circle cx="{220+c*30}" cy="{160+r*30}" r="3" fill="#5a3f2a"/>' for c in range(9) for r in range(6)),
           '<path d="M240,180 L300,300" stroke="#9aa4ad" stroke-width="10"/><rect x="340" y="170" width="12" height="120" fill="#c9364a"/><circle cx="440" cy="230" r="34" fill="none" stroke="#3fbf7f" stroke-width="8"/>',
           '<rect x="1500" y="420" width="140" height="440" fill="#6b4a32"/>' + "".join(f'<rect x="1500" y="{440+k*100}" width="140" height="10" fill="#4f3624"/>' for k in range(4))
           + '<rect x="1520" y="480" width="50" height="58" fill="#c9364a"/><rect x="1580" y="490" width="40" height="48" fill="#3a6fd8"/><rect x="1520" y="590" width="100" height="40" fill="#c9b08a"/>',
           SLED_BG(1700, 820),
           '<rect x="360" y="560" width="1200" height="40" rx="6" fill="#6b4a32"/><rect x="400" y="600" width="30" height="260" fill="#4f3624"/><rect x="1490" y="600" width="30" height="260" fill="#4f3624"/>',
           '<rect x="800" y="440" width="320" height="120" rx="6" fill="#c9b08a"/>',
           "".join(f'<rect x="{820+k*6}" y="{420-k*4}" width="200" height="130" rx="4" fill="#ffffff" stroke="#d9d9de" stroke-width="2" transform="rotate({-3+k} 920 490)"/>' for k in range(4)),
           '<rect x="1180" y="530" width="120" height="24" rx="10" fill="#111"/><rect x="1290" y="534" width="24" height="16" rx="4" fill="#444"/>',
           '<rect x="560" y="500" width="60" height="60" rx="8" fill="#8a8f9c"/><rect x="640" y="520" width="90" height="40" rx="6" fill="#ffd43b"/>',
           D.bulb(960, 0, 160, lit=True), D.cobweb(0, 0, 1.3), D.cobweb(1920, 0, -1.3), _band()]
    return "".join(out)


def SLED_BG(x, y):
    return (f'<g transform="translate({x} {y}) rotate(-70)"><rect x="-90" y="-26" width="180" height="40" rx="18" fill="#3a6fd8"/>'
            '<path d="M-100,24 L100,24 Q120,24 116,6" stroke="#8a8f9c" stroke-width="8" fill="none"/></g>')


def spring_morning(people=True):
    out = [town_snow(night=False, buried=0.35)]
    out.append('<circle cx="1700" cy="140" r="70" fill="#fff4cf"/><circle cx="1700" cy="140" r="160" fill="#fff4cf" opacity="0.3"/>')
    out.append(''.join(f'<path d="M{x},{y} l10,26 l10,-26 Z" fill="#7fb8ff" opacity="0.7"/>' for x, y in [(140, 640), (600, 600), (1060, 620), (1520, 630)]))
    return "".join(out)


def porch_winter(open_=True):
    """Front door seen from inside the hall (winter version): coats, boots, mat, frost on the glass."""
    out = [D.wall("#3a3f58", split=560, seed=61), D.floor_planks("#2a2433"),
           '<rect x="660" y="180" width="560" height="680" fill="#c97a4a"/>',
           '<rect x="660" y="180" width="560" height="680" fill="#2a1e3a" opacity="0.55"/>',
           '<circle cx="940" cy="250" r="90" fill="#ffd98a" opacity="0.25"/>',
           '<rect x="640" y="160" width="600" height="24" fill="#4a3f55"/>',
           '<rect x="640" y="160" width="24" height="700" fill="#4a3f55"/><rect x="1216" y="160" width="24" height="700" fill="#4a3f55"/>',
           ('<path d="M1220,184 L1400,150 L1400,900 L1220,860 Z" fill="#5a3b2a"/><circle cx="1380" cy="540" r="9" fill="#c9b27a"/>' if open_
            else '<rect x="664" y="184" width="552" height="676" fill="#5a3b2a"/><rect x="700" y="220" width="480" height="260" rx="6" fill="#4a2e20"/>'
                 '<rect x="700" y="520" width="480" height="300" rx="6" fill="#4a2e20"/><circle cx="1180" cy="540" r="9" fill="#c9b27a"/><circle cx="940" cy="440" r="10" fill="#111"/>'),
           # coat hooks + coats, boots, umbrella stand, mat
           '<rect x="180" y="300" width="300" height="16" rx="6" fill="#6b4a32"/>'
           '<path d="M220,316 L200,560 L280,560 L260,316 Z" fill="#c9364a"/><path d="M320,316 L300,520 L370,520 L350,316 Z" fill="#3a6fd8"/>'
           '<path d="M410,316 L395,480 L455,480 L440,316 Z" fill="#ffd43b"/>',
           '<path d="M220,860 L220,790 L260,790 L260,840 L290,846 L290,860 Z" fill="#2a2a33"/><path d="M300,860 L300,790 L340,790 L340,840 L370,846 L370,860 Z" fill="#2a2a33"/>',
           '<rect x="1500" y="700" width="80" height="160" rx="10" fill="#4a5a6a"/><path d="M1520,700 L1560,560" stroke="#2a2a33" stroke-width="6"/>',
           D.switch(1270, 470, "#c9cad1"), D.frame(1460, 260, 160, 200, "#9fb0c8"),
           '<rect x="740" y="860" width="400" height="30" rx="8" fill="#7a5a3a"/>',
           '<path d="M664,860 L1216,860 L1400,1000 L520,1000 Z" fill="#ffb84d" opacity="0.06"/>', _band()]
    return "".join(out)


def radio_kitchen_winter():
    out = [kitchen_winter(card=True, pots=False),
           '<rect x="1180" y="470" width="300" height="110" rx="16" fill="#7a5a3a"/>',
           '<rect x="1200" y="488" width="150" height="74" rx="8" fill="#d8c9a6"/>',
           '<g stroke="#5a4a3a" stroke-width="3">' + "".join(f'<line x1="{1212+k*14}" y1="496" x2="{1212+k*14}" y2="554"/>' for k in range(10)) + '</g>',
           '<circle cx="1400" cy="510" r="18" fill="#3a2a1a"/><circle cx="1445" cy="510" r="18" fill="#3a2a1a"/>',
           '<rect x="1300" y="410" width="6" height="64" fill="#9a9384" transform="rotate(-20 1303 470)"/>',
           '<path d="M1480,560 Q1560,600 1540,700 Q1520,780 1600,800" stroke="#1d1f26" stroke-width="8" fill="none"/>']
    return "".join(out)


BG.update({"town_snow": town_snow, "whiteout": whiteout, "living_winter": living_winter, "kitchen_winter": kitchen_winter,
           "bathroom": bathroom, "house_side": house_side, "garage_grill": garage_grill, "upstairs_window": upstairs_window,
           "ceiling": ceiling_cracks, "car_buried": car_buried, "shed": shed, "spring": spring_morning,
           "porch": porch_winter, "radio_kitchen": radio_kitchen_winter})
