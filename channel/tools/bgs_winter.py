"""Winter backgrounds for EP02 (The Whiteout). Same conventions as bgs.py: 1920x1080 SVG bodies,
side view, floor/ground at y=860, dark band under it for captions.
"""
import random

from art import moon, stars, window, house
from bgs import BG, W, H, FLOOR, _floor

SNOW = "#eef3fa"
SNOW_SH = "#c9d6e8"
NIGHT_SNOW = "#9fb0cc"
NIGHT_SNOW_SH = "#7f90ad"


def _drift(y, color, seed=1, amp=40, n=7):
    """A wavy snow drift whose top edge sits around y."""
    rnd = random.Random(seed)
    pts = [f"M0,{H}", f"L0,{y + rnd.uniform(-amp, amp):.0f}"]
    step = W / n
    for k in range(n):
        x1 = step * k + step / 2
        x2 = step * (k + 1)
        pts.append(f"Q{x1:.0f},{y + rnd.uniform(-amp, amp):.0f} {x2:.0f},{y + rnd.uniform(-amp * 0.5, amp * 0.5):.0f}")
    pts.append(f"L{W},{H} Z")
    return f'<path d="{" ".join(pts)}" fill="{color}"/>'


def snow_house(x, y, w, h, body, roof, lit, night, seed=0, buried=0.0):
    """House with a snow cap on the roof; `buried` 0..1 raises the drift up its walls."""
    s, sh = (NIGHT_SNOW, NIGHT_SNOW_SH) if night else (SNOW, SNOW_SH)
    out = [house(x, y, w, h, body, roof, lit, seed=seed)]
    out.append(f'<path d="M{x-24},{y-h} L{x+w/2},{y-h-h*0.45} L{x+w+24},{y-h} L{x+w+10},{y-h+16} '
               f'Q{x+w/2},{y-h-h*0.25} {x-10},{y-h+16} Z" fill="{s}"/>')
    if buried > 0:
        top = y - h * buried
        out.append(f'<path d="M{x-60},{y+40} L{x-60},{top+30} Q{x+w*0.3},{top-20} {x+w*0.6},{top+10} '
                   f'Q{x+w*0.85},{top+30} {x+w+60},{top+40} L{x+w+60},{y+40} Z" fill="{s}"/>'
                   f'<path d="M{x-60},{top+30} Q{x+w*0.3},{top-20} {x+w*0.6},{top+10}" stroke="{sh}" stroke-width="10" fill="none"/>')
    return "".join(out)


def town_snow(night=False, buried=0.0, lit=(True, False, True, True), seed=3):
    sky = "#0b1430" if night else "#c7d3e2"
    out = [f'<rect width="{W}" height="{H}" fill="{sky}"/>']
    if night:
        out.append(stars(40, 0, 0, W, 360, seed=seed, op=0.5))
    else:
        out.append('<rect width="1920" height="1080" fill="#ffffff" opacity="0.18"/>')
    cols = [("#2b3552", "#1b2440"), ("#33314e", "#22213a"), ("#2a3a52", "#1b2840")] if night else \
           [("#b9a58e", "#7a5a4a"), ("#a9b4a0", "#5f6f56"), ("#c4b3a2", "#6e4f45")]
    for k, x in enumerate((60, 520, 980, 1440)):
        b, r = cols[k % 3]
        out.append(snow_house(x, FLOOR, 380, 260 + (k % 2) * 40, b, r, [lit[k % len(lit)]] * 3, night, seed=k, buried=buried))
    out.append(_drift(FLOOR - 10 - buried * 120, NIGHT_SNOW if night else SNOW, seed=seed, amp=30))
    out.append(f'<rect x="0" y="{FLOOR+70}" width="{W}" height="{H-FLOOR-70}" fill="#0b0d14" opacity="0.45"/>')
    return "".join(out)


def whiteout(figures=0, seed=5):
    """Almost pure white: only the faint shapes of buried houses and walkers."""
    rnd = random.Random(seed)
    out = ['<defs><linearGradient id="wo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe6ef"/>'
           '<stop offset="1" stop-color="#f4f7fb"/></linearGradient></defs>',
           f'<rect width="{W}" height="{H}" fill="url(#wo)"/>',
           '<g fill="#c6cfdb" opacity="0.55">' + "".join(
               f'<path d="M{x},{FLOOR-40} L{x},{FLOOR-180} L{x+110},{FLOOR-250} L{x+220},{FLOOR-180} L{x+220},{FLOOR-40} Z"/>'
               for x in (100, 700, 1350)) + '</g>']
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
    wall = "#3a3047" if not lit else "#5a4636"
    out = [f'<rect width="{W}" height="{H}" fill="{wall}"/>', _floor("#2a2028")]
    # window covered by a blanket
    out.append(window(1380, 170, 340, 300, sky="#d9e2ee", frame="#4a3f55",
                      inner='<rect width="340" height="300" fill="#e9eef5"/>'))
    if blankets:
        out.append('<path d="M1360,150 L1740,150 L1730,500 Q1550,470 1370,505 Z" fill="#7a4a5a"/>'
                   '<path d="M1360,150 L1740,150 L1740,180 L1360,180 Z" fill="#5a3442"/>')
    # fireplace
    out.append('<rect x="240" y="420" width="420" height="440" fill="#6b5446"/>'
               '<rect x="220" y="400" width="460" height="40" rx="6" fill="#4a3a30"/>'
               '<path d="M330,860 L330,600 Q450,520 570,600 L570,860 Z" fill="#1a1210"/>')
    if fire:
        out.append('<g><path d="M380,860 Q370,760 420,720 Q410,780 450,770 Q450,700 500,680 Q490,760 530,790 Q540,840 520,860 Z" fill="#ff8a2a"/>'
                   '<path d="M420,860 Q420,800 450,780 Q455,820 480,810 Q495,840 490,860 Z" fill="#ffd36a"/></g>'
                   '<circle cx="450" cy="760" r="420" fill="#ff9a3a" opacity="0.10"/>'
                   '<circle cx="450" cy="760" r="220" fill="#ffb84d" opacity="0.10"/>')
    # mattresses + blankets on the floor
    out.append('<rect x="760" y="800" width="520" height="56" rx="16" fill="#c9d2ee"/>'
               '<path d="M800,800 Q1000,770 1250,800 L1250,840 L800,840 Z" fill="#8a6fb0"/>')
    # stairs corner (dark)
    out.append('<path d="M1780,860 L1780,560 L1920,560 L1920,860 Z" fill="#1a141e"/>')
    return "".join(out)


def kitchen_winter(card=True, pots=True):
    out = [f'<rect width="{W}" height="{H}" fill="#4a4a5a"/>', _floor("#2f2f3a"),
           '<rect x="980" y="600" width="760" height="260" fill="#5a5d72"/><rect x="960" y="580" width="800" height="28" rx="4" fill="#6e7290"/>',
           '<rect x="980" y="180" width="760" height="190" rx="6" fill="#5a5d72"/>',
           '<rect x="160" y="250" width="300" height="610" rx="12" fill="#d9dde6"/><rect x="170" y="470" width="280" height="6" fill="#b9bdc8"/>']
    if card:
        out.append('<g transform="translate(250 340) rotate(-4)"><rect x="-70" y="-90" width="140" height="180" rx="6" fill="#ffffff"/>'
                   + "".join(f'<rect x="-52" y="{-62+k*16}" width="{104 if k % 3 else 80}" height="6" rx="3" fill="#2a2a33"/>' for k in range(9))
                   + '<circle cx="0" cy="-96" r="9" fill="#ef3b4f"/></g>')
    if pots:
        out.append("".join(f'<g transform="translate({1040+k*150} 580)"><rect x="-55" y="-70" width="110" height="70" rx="10" fill="#8a8f9c"/>'
                           f'<rect x="-50" y="-66" width="100" height="14" rx="6" fill="#7fb8ff" opacity="0.8"/></g>' for k in range(4)))
    return "".join(out)


def bathroom():
    out = [f'<rect width="{W}" height="{H}" fill="#c9d6dc"/>',
           '<g fill="#b9c8cf">' + "".join(f'<rect x="{x}" y="{y}" width="116" height="76"/>' for x in range(0, 1920, 120) for y in range(260, 860, 80)) + '</g>',
           _floor("#7d8b93"),
           '<rect x="420" y="560" width="1080" height="300" rx="60" fill="#f4f6f8"/>',
           '<rect x="470" y="580" width="980" height="120" rx="40" fill="#7fb8ff" opacity="0.6"/>',
           '<rect x="1380" y="440" width="24" height="120" fill="#9aa4ad"/><rect x="1300" y="430" width="110" height="24" rx="10" fill="#9aa4ad"/>']
    return "".join(out)


def house_side(buried=0.6, night=False):
    """Close side view of our house wall with the vent pipe."""
    s = NIGHT_SNOW if night else SNOW
    out = [f'<rect width="{W}" height="{H}" fill="{"#0b1430" if night else "#c7d3e2"}"/>',
           '<rect x="0" y="120" width="1920" height="760" fill="#9a8574"/>',
           '<g stroke="#8a7564" stroke-width="4">' + "".join(f'<line x1="0" y1="{y}" x2="1920" y2="{y}"/>' for y in range(160, 880, 40)) + '</g>',
           window(300, 260, 300, 240, sky="#1a2030", frame="#e8e2d6"),
           # vent pipe
           '<rect x="1100" y="560" width="160" height="60" rx="10" fill="#6a6f7a"/><rect x="1240" y="548" width="40" height="84" rx="8" fill="#5a5f6a"/>',
           f'<path d="M0,{H} L0,{880-buried*360} Q700,{860-buried*420} 1300,{870-buried*380} Q1700,{890-buried*360} 1920,{880-buried*370} L1920,{H} Z" fill="{s}"/>',
           f'<rect x="0" y="{FLOOR+70}" width="{W}" height="{H-FLOOR-70}" fill="#0b0d14" opacity="0.35"/>']
    return "".join(out)


def garage_grill():
    out = [f'<rect width="{W}" height="{H}" fill="#3a3a44"/>', _floor("#2a2a30"),
           '<rect x="200" y="200" width="1100" height="660" fill="#2a2a32"/>',
           '<g stroke="#3a3a46" stroke-width="6">' + "".join(f'<line x1="200" y1="{y}" x2="1300" y2="{y}"/>' for y in range(240, 860, 60)) + '</g>',
           # grill
           '<g transform="translate(1500 860)"><rect x="-90" y="-260" width="180" height="120" rx="30" fill="#2b2f3a"/>'
           '<rect x="-12" y="-140" width="24" height="140" fill="#2b2f3a"/><rect x="-80" y="-20" width="160" height="20" rx="8" fill="#2b2f3a"/>'
           '<path d="M-40,-280 Q-30,-330 -50,-370 M0,-280 Q10,-340 -10,-390 M40,-280 Q50,-330 30,-380" stroke="#9aa4b4" stroke-width="10" fill="none" opacity="0.5"/></g>',
           '<circle cx="1500" cy="560" r="300" fill="#ff8a2a" opacity="0.06"/>',
           # side door
           '<rect x="1680" y="360" width="200" height="500" fill="#4a3b30"/><circle cx="1700" cy="620" r="8" fill="#c9b27a"/>']
    return "".join(out)


def upstairs_window():
    """Looking out of the upstairs window: the snow is level with the sill, walkers in the white."""
    out = [f'<rect width="{W}" height="{H}" fill="#2a2633"/>',
           '<rect x="260" y="120" width="1400" height="740" fill="#dde4ee"/>',
           '<g fill="#9aa6b8" opacity="0.6">' + "".join(
               f'<g transform="translate({x} 720) scale({s})"><ellipse cx="0" cy="-262" rx="44" ry="50"/>'
               '<rect x="-50" y="-222" width="100" height="125" rx="26"/><rect x="-30" y="-110" width="24" height="110" rx="8"/>'
               '<rect x="6" y="-110" width="24" height="110" rx="8"/></g>' for x, s in ((560, 0.55), (980, 0.45), (1360, 0.6))) + '</g>',
           '<path d="M260,860 L260,640 Q700,600 1100,650 Q1400,680 1660,630 L1660,860 Z" fill="#f4f7fb"/>',
           '<rect x="240" y="100" width="1440" height="30" fill="#4a3f55"/><rect x="240" y="100" width="30" height="780" fill="#4a3f55"/>'
           '<rect x="1650" y="100" width="30" height="780" fill="#4a3f55"/><rect x="945" y="100" width="30" height="780" fill="#4a3f55"/>',
           '<rect x="200" y="860" width="1520" height="40" fill="#4a3f55"/>', _floor("#1e1a26")]
    return "".join(out)


def ceiling_cracks():
    out = [f'<rect width="{W}" height="{H}" fill="#4a4258"/>',
           '<rect x="0" y="0" width="1920" height="300" fill="#5a5168"/>',
           '<g stroke="#2a2433" stroke-width="5" fill="none" stroke-linecap="round">'
           '<path d="M700,0 L740,60 L720,120 L780,190 L770,260"/><path d="M740,60 L820,90"/><path d="M1200,0 L1180,80 L1230,150"/></g>',
           '<path d="M0,300 L1920,300" stroke="#3a3346" stroke-width="10"/>',
           _floor("#2a2433"),
           '<rect x="760" y="800" width="520" height="56" rx="16" fill="#c9d2ee"/>']
    return "".join(out)


def car_buried(night=False):
    s = NIGHT_SNOW if night else SNOW
    out = [f'<rect width="{W}" height="{H}" fill="{"#0b1430" if night else "#c7d3e2"}"/>',
           snow_house(1300, FLOOR, 500, 340, "#b9a58e", "#7a5a4a", [False, False], night, seed=9, buried=0.5),
           # van
           '<g transform="translate(300 860)"><rect x="0" y="-300" width="620" height="240" rx="30" fill="#5a7da8"/>'
           '<rect x="40" y="-270" width="180" height="90" rx="10" fill="#1d2c44"/><rect x="250" y="-270" width="180" height="90" rx="10" fill="#1d2c44"/>'
           '<circle cx="140" cy="-50" r="56" fill="#1d1f26"/><circle cx="500" cy="-50" r="56" fill="#1d1f26"/>'
           '<rect x="600" y="-110" width="50" height="20" rx="6" fill="#3a3f4f"/></g>',
           f'<path d="M150,{H} L150,700 Q400,560 700,600 Q900,620 1050,720 L1050,{H} Z" fill="{s}"/>',
           f'<path d="M0,{H} L0,860 Q600,820 1200,850 Q1600,860 1920,840 L1920,{H} Z" fill="{s}"/>',
           f'<rect x="0" y="{FLOOR+70}" width="{W}" height="{H-FLOOR-70}" fill="#0b0d14" opacity="0.35"/>']
    return "".join(out)


def shed():
    out = [f'<rect width="{W}" height="{H}" fill="#3a2e26"/>', _floor("#2a211c"),
           '<g fill="#4a3a30">' + "".join(f'<rect x="{x}" y="0" width="150" height="860"/>' for x in range(0, 1920, 170)) + '</g>',
           '<rect x="360" y="560" width="1200" height="40" rx="6" fill="#6b4a32"/><rect x="400" y="600" width="30" height="260" fill="#4f3624"/><rect x="1490" y="600" width="30" height="260" fill="#4f3624"/>',
           '<rect x="800" y="440" width="320" height="120" rx="6" fill="#c9b08a"/>',
           "".join(f'<rect x="{820+k*6}" y="{420-k*4}" width="200" height="130" rx="4" fill="#ffffff" stroke="#d9d9de" stroke-width="2" transform="rotate({-3+k} 920 490)"/>' for k in range(4)),
           '<rect x="1180" y="530" width="120" height="24" rx="10" fill="#111"/><rect x="1290" y="534" width="24" height="16" rx="4" fill="#444"/>',
           '<circle cx="960" cy="200" r="16" fill="#ffd98a"/><circle cx="960" cy="200" r="260" fill="#ffd98a" opacity="0.07"/>']
    return "".join(out)


def spring_morning(people=True):
    out = [town_snow(night=False, buried=0.35)]
    out.append('<circle cx="1700" cy="140" r="70" fill="#fff4cf"/><circle cx="1700" cy="140" r="160" fill="#fff4cf" opacity="0.3"/>')
    return "".join(out)


BG.update({"town_snow": town_snow, "whiteout": whiteout, "living_winter": living_winter, "kitchen_winter": kitchen_winter,
           "bathroom": bathroom, "house_side": house_side, "garage_grill": garage_grill, "upstairs_window": upstairs_window,
           "ceiling": ceiling_cracks, "car_buried": car_buried, "shed": shed, "spring": spring_morning})
