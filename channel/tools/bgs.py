"""Backgrounds (1920x1080 SVG bodies, no outer <svg>). Side view, 2-4 flat layers.
Floor line sits at y=860; the band under it stays dark for captions.
"""
from art import P, moon, stars, window, house, landline, phone, icon

W, H = 1920, 1080
FLOOR = 860


def _floor(color, band="#0b0d14"):
    return (f'<rect x="0" y="{FLOOR}" width="{W}" height="{H-FLOOR}" fill="{color}"/>'
            f'<rect x="0" y="{FLOOR+70}" width="{W}" height="{H-FLOOR-70}" fill="{band}" opacity="0.55"/>')


def stage(tint="#141420", rays=True, seed=3):
    """Abstract dark stage for cards and infographics: soft diagonal light streaks + dust."""
    out = [f'<defs><radialGradient id="stg{seed}" cx="50%" cy="42%" r="70%"><stop offset="0" stop-color="#262636"/>'
           f'<stop offset="1" stop-color="{tint}"/></radialGradient></defs>',
           f'<rect width="{W}" height="{H}" fill="url(#stg{seed})"/>']
    if rays:
        for k, (x, w, o) in enumerate([(380, 140, 0.05), (820, 220, 0.04), (1300, 160, 0.05), (1640, 90, 0.035)]):
            out.append(f'<path d="M{x},-40 L{x+w},-40 L{x+w-520},{H+40} L{x-520},{H+40} Z" fill="#ffffff" opacity="{o}"/>')
    out.append(stars(60, 0, 0, W, H, seed=seed, op=0.18))
    return "".join(out)


def bedroom(lamp=False, moonlit=True):
    wall = "#2a3150" if not lamp else "#cdb99a"
    out = [f'<rect width="{W}" height="{H}" fill="{wall}"/>',
           f'<rect x="0" y="{FLOOR-30}" width="{W}" height="30" fill="#20263d"/>',
           _floor("#1a1f33"),
           # window with night sky
           window(1180, 170, 420, 340, sky="#0e1a36", frame="#3b4366",
                  inner=moon(330, 90, 34) + stars(30, 0, 0, 420, 340, seed=7, op=0.9)
                  + '<g fill="#0a1226">' + "".join(f'<rect x="{x}" y="{340-h}" width="{w}" height="{h}"/>' for x, w, h in [(0, 70, 120), (66, 50, 160), (112, 90, 100), (196, 60, 190), (250, 110, 130), (356, 64, 170)]) + '</g>'),
           # moonlight patch on the floor/wall
           '<path d="M1170,520 L1620,520 L1760,860 L1040,860 Z" fill="#9fb7ff" opacity="0.06"/>' if moonlit else "",
           # bed
           '<rect x="260" y="640" width="760" height="140" rx="18" fill="#3e4a78"/>'
           '<rect x="250" y="560" width="40" height="300" rx="10" fill="#2b3252"/>'
           '<rect x="980" y="640" width="40" height="220" rx="10" fill="#2b3252"/>'
           '<rect x="300" y="610" width="200" height="70" rx="30" fill="#c9d2ee"/>'
           '<path d="M470,640 Q620,600 980,640 L980,720 L470,720 Z" fill="#5868a3"/>'
           '<rect x="270" y="780" width="740" height="16" fill="#232947"/>',
           # nightstand + lamp
           '<rect x="40" y="680" width="190" height="180" rx="8" fill="#3a3045"/>'
           '<rect x="56" y="740" width="158" height="8" fill="#2a2333"/>'
           '<rect x="120" y="600" width="12" height="80" fill="#5b5466"/>'
           f'<path d="M80,600 L172,600 L150,540 L102,540 Z" fill="{"#ffd98a" if lamp else "#6b6480"}"/>',
           ]
    return "".join(out)


def hallway(door_light=True):
    out = [f'<rect width="{W}" height="{H}" fill="#262c45"/>',
           '<rect x="0" y="560" width="1920" height="300" fill="#222840"/>',
           '<rect x="0" y="552" width="1920" height="10" fill="#323a5a"/>',
           _floor("#191d2e"),
           # family photos
           '<g fill="#3a4266">' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>' for x, y, w, h in [(180, 300, 120, 90), (340, 280, 90, 120), (1500, 300, 140, 100)]) + '</g>',
           # kid's door ajar with tablet light spilling
           '<rect x="760" y="300" width="300" height="560" fill="#141829"/>',
           '<rect x="760" y="300" width="300" height="560" fill="#7fd0ff" opacity="0.16"/>' if door_light else "",
           '<path d="M1060,300 L1180,330 L1180,880 L1060,860 Z" fill="#4a3a33"/>',
           '<circle cx="1160" cy="600" r="7" fill="#c9b27a"/>',
           '<path d="M760,860 L1060,860 L1240,1000 L620,1000 Z" fill="#7fd0ff" opacity="0.07"/>' if door_light else "",
           # stair rail going down on the right
           '<g fill="#3a3045">' + "".join(f'<rect x="{1380+i*60}" y="{560+i*40}" width="12" height="{300-i*40}"/>' for i in range(8)) + '</g>'
           '<path d="M1370,560 L1880,880" stroke="#4a3d55" stroke-width="16"/>',
           ]
    return "".join(out)


def kids_room():
    out = [f'<rect width="{W}" height="{H}" fill="#273455"/>',
           _floor("#1b2238"),
           window(220, 190, 300, 260, sky="#0e1a36", frame="#3b4a72", inner=stars(20, 0, 0, 300, 260, seed=9, op=0.9) + moon(240, 60, 22)),
           # posters
           '<rect x="680" y="220" width="160" height="210" rx="6" fill="#3d4f7d"/><circle cx="760" cy="310" r="40" fill="#d9573b" opacity="0.8"/>'
           '<rect x="880" y="260" width="120" height="150" rx="6" fill="#4a3f6b"/>',
           # bed (low)
           '<rect x="620" y="690" width="900" height="110" rx="16" fill="#e07a3b"/>'
           '<rect x="600" y="620" width="36" height="240" rx="10" fill="#7a4a2a"/>'
           '<rect x="1500" y="690" width="36" height="170" rx="10" fill="#7a4a2a"/>'
           '<rect x="650" y="650" width="180" height="60" rx="26" fill="#f2e6d0"/>',
           ]
    return "".join(out)


def kitchen(night=True, doorway=True):
    wall = "#2b2f40" if night else "#e9dcc3"
    out = [f'<rect width="{W}" height="{H}" fill="{wall}"/>',
           f'<rect x="0" y="{FLOOR-12}" width="{W}" height="12" fill="#1f2230"/>' if night else f'<rect x="0" y="{FLOOR-12}" width="{W}" height="12" fill="#b89f7c"/>',
           _floor("#1b1d28" if night else "#a07c5a"),
           # cabinets + counter
           f'<rect x="980" y="180" width="760" height="190" rx="6" fill="{"#363b52" if night else "#c9b08a"}"/>',
           "".join(f'<rect x="{990+i*190}" y="190" width="170" height="170" rx="4" fill="{"#3e445e" if night else "#d6bf98"}"/>' for i in range(4)),
           f'<rect x="980" y="600" width="760" height="260" fill="{"#363b52" if night else "#c9b08a"}"/>',
           f'<rect x="960" y="580" width="800" height="28" rx="4" fill="{"#4a5170" if night else "#e7d3ae"}"/>',
           # fridge
           f'<rect x="1770" y="300" width="160" height="560" rx="10" fill="{"#5a6078" if night else "#eceff2"}"/>',
           # wall landline with coiled cord
           '<rect x="560" y="330" width="120" height="170" rx="12" fill="#cfc8b8"/>',
           '<rect x="575" y="345" width="90" height="140" rx="10" fill="#bdb5a3"/>',
           # doorway to the hall
           '<rect x="120" y="300" width="300" height="560" fill="#141724"/>' if doorway else "",
           '<rect x="108" y="290" width="324" height="14" fill="#3a3f55"/>' if doorway else "",
           ]
    return "".join(out)


def kitchen_table(lamp=True):
    out = [f'<rect width="{W}" height="{H}" fill="#2a2a3a"/>',
           _floor("#1c1c28"),
           # hanging lamp + warm pool of light
           '<rect x="956" y="0" width="8" height="250" fill="#444"/>',
           '<path d="M880,250 L1040,250 L1000,200 L920,200 Z" fill="#ffd98a"/>' if lamp else '<path d="M880,250 L1040,250 L1000,200 L920,200 Z" fill="#5a5466"/>',
           '<path d="M890,250 L1030,250 L1500,860 L420,860 Z" fill="#ffd98a" opacity="0.10"/>' if lamp else "",
           '<ellipse cx="960" cy="740" rx="560" ry="140" fill="#ffd98a" opacity="0.08"/>' if lamp else "",
           # table
           '<rect x="520" y="690" width="880" height="26" rx="6" fill="#6b4a32"/>'
           '<rect x="560" y="716" width="24" height="144" fill="#4f3624"/><rect x="1336" y="716" width="24" height="144" fill="#4f3624"/>',
           '<rect x="880" y="664" width="64" height="30" rx="6" fill="#d9d2c0"/>'  # mug
           ]
    return "".join(out)


def street_night(lit=(True, False, True, True, False, True), seed=4, dogs=False):
    out = [f'<rect width="{W}" height="{H}" fill="#0b1430"/>',
           stars(80, 0, 0, W, 420, seed=seed, op=0.85), moon(1650, 150, 40),
           # far skyline
           '<g fill="#111b3a">' + "".join(f'<rect x="{x}" y="{560-h}" width="{w}" height="{h}"/>' for x, w, h in [(0, 120, 200), (110, 90, 260), (190, 140, 170), (320, 80, 300), (390, 160, 210), (540, 110, 240), (640, 150, 190), (780, 90, 280), (860, 170, 220), (1020, 120, 260), (1130, 140, 180), (1260, 100, 300), (1350, 180, 230), (1520, 120, 270), (1630, 150, 200), (1770, 150, 250)]) + '</g>',
           ]
    xs = [40, 360, 680, 1000, 1320, 1640]
    for k, x in enumerate(xs):
        out.append(house(x, FLOOR, 260, 240 + (k % 3) * 30, ["#26304f", "#2d2f4a", "#2a3550"][k % 3],
                         ["#1a2038", "#21223a", "#1b2440"][k % 3], [lit[k % len(lit)], not lit[k % len(lit)], lit[k % len(lit)]], seed=k))
    # street lamps
    for x in (300, 960, 1600):
        out.append(f'<rect x="{x}" y="560" width="10" height="300" fill="#2a2f44"/><rect x="{x-30}" y="552" width="60" height="12" rx="6" fill="#2a2f44"/>')
    out.append(_floor("#151a2a"))
    out.append('<rect x="0" y="880" width="1920" height="10" fill="#2a3048"/>')
    return "".join(out)


def city_night(lit_ratio=0.6, seed=5):
    import random
    rnd = random.Random(seed)
    out = [f'<rect width="{W}" height="{H}" fill="#0a1128"/>', stars(120, 0, 0, W, 500, seed=seed, op=0.8)]
    x = 0
    while x < W:
        w = rnd.randint(110, 220)
        h = rnd.randint(280, 640)
        out.append(f'<rect x="{x}" y="{FLOOR-h}" width="{w}" height="{h}" fill="{rnd.choice(["#141d3c", "#18213f", "#121a35"])}"/>')
        for r in range(int(h // 46)):
            for c in range(int((w - 20) // 34)):
                lit = rnd.random() < lit_ratio
                out.append(f'<rect class="cw" x="{x+14+c*34}" y="{FLOOR-h+16+r*46}" width="18" height="24" fill="{"#ffd98a" if lit else "#0d142b"}" opacity="{0.9 if lit else 1}"/>')
        x += w + rnd.randint(4, 16)
    out.append(_floor("#0d1222"))
    return "".join(out)


def earth(lights=True, seed=8):
    import random
    rnd = random.Random(seed)
    out = [f'<rect width="{W}" height="{H}" fill="#04070f"/>', stars(220, 0, 0, W, H, seed=seed, op=0.9),
           '<circle cx="960" cy="520" r="430" fill="#3a6fd8" opacity="0.10"/>',
           '<circle cx="960" cy="520" r="380" fill="#16326b"/>',
           '<g fill="#1f4a3a">'
           '<path d="M700,330 Q760,250 880,290 Q930,360 860,420 Q800,470 760,560 Q700,520 690,440 Z"/>'
           '<path d="M980,300 Q1120,260 1200,340 Q1230,420 1150,450 Q1080,430 1020,470 Q960,420 980,300 Z"/>'
           '<path d="M1040,520 Q1120,520 1150,600 Q1120,700 1060,760 Q1020,680 1030,600 Z"/>'
           '<path d="M780,620 Q860,610 880,680 Q850,760 800,780 Q760,720 780,620 Z"/>'
           '<path d="M1210,620 Q1270,640 1260,700 Q1220,720 1200,680 Z"/></g>',
           '<circle cx="960" cy="520" r="380" fill="none" stroke="#7fb0ff" stroke-opacity="0.35" stroke-width="10"/>']
    if lights:
        pts = []
        for _ in range(260):
            a, r = rnd.uniform(0, 6.283), rnd.uniform(0, 360) ** 0.5 * 19
            x, y = 960 + r * __import__("math").cos(a), 520 + r * __import__("math").sin(a)
            pts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.6,2.2,2.8])}"/>')
        out.append('<g class="earth-lights" fill="#ffe08a" opacity="0.85">' + "".join(pts) + '</g>')
    out.append('<path d="M960,140 A380,380 0 0 1 960,900 A300,380 0 0 0 960,140 Z" fill="#000" opacity="0.35"/>')
    return "".join(out)


def phone_close(caller="MY NUMBER", number="+1 (415) 555-0142", ringing=True, hand=True):
    """Phone held in a hand, incoming-call screen. Phone box 760x... centred at x=960, y 110..890."""
    out = [f'<rect width="{W}" height="{H}" fill="#0c0f1c"/>',
           '<circle cx="960" cy="480" r="520" fill="#7fd0ff" opacity="0.05"/>',
           '<circle cx="960" cy="480" r="340" fill="#7fd0ff" opacity="0.06"/>']
    if hand:
        out.append('<path d="M760,1080 L770,860 Q780,800 840,790 L1080,790 Q1140,800 1150,860 L1160,1080 Z" fill="#c99a73"/>'
                   '<rect x="735" y="560" width="70" height="200" rx="35" fill="#c99a73"/>'
                   '<rect x="738" y="420" width="62" height="150" rx="31" fill="#c99a73"/>')
    out += ['<rect x="770" y="110" width="380" height="780" rx="52" fill="#15171e"/>',
            '<rect x="786" y="126" width="348" height="748" rx="40" fill="#0f1a33"/>',
            '<rect x="910" y="140" width="100" height="20" rx="10" fill="#15171e"/>',
            '<text x="960" y="230" text-anchor="middle" font-family="Montserrat" font-weight="600" font-size="30" fill="#9fb3d9">incoming call</text>',
            f'<text x="960" y="320" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#ffffff">{caller}</text>',
            f'<text x="960" y="368" text-anchor="middle" font-family="Montserrat" font-weight="600" font-size="30" fill="#cfd8ee">{number}</text>',
            '<circle cx="960" cy="520" r="78" fill="#2a3a66"/><circle cx="960" cy="500" r="28" fill="#8ea3cf"/><path d="M912,570 Q960,520 1008,570 Z" fill="#8ea3cf"/>',
            '<circle cx="868" cy="760" r="48" fill="#ef3b4f"/><rect x="846" y="754" width="44" height="12" rx="6" fill="#fff"/>',
            '<circle cx="1052" cy="760" r="48" fill="#3fbf7f"/>'
            '<path d="M1034,750 Q1032,741 1039,739 L1047,737 Q1052,746 1049,755 Q1056,768 1067,773 Q1076,769 1080,777 L1078,784 Q1074,790 1065,788 Q1039,779 1034,750 Z" fill="#fff"/>']
    if hand:
        out.append('<rect x="1100" y="700" width="70" height="230" rx="35" fill="#b88a64" transform="rotate(32 1135 815)"/>'
                   '<rect x="1140" y="520" width="56" height="170" rx="28" fill="#c99a73"/><rect x="1140" y="380" width="52" height="150" rx="26" fill="#c99a73"/>')
    return "".join(out)


def phone_screen(lines, header="Messages", accent="#3a6fd8"):
    """Phone filling the frame with a list UI (messages, notes, voicemail). lines = [(text, side)]"""
    out = [f'<rect width="{W}" height="{H}" fill="#0c0f1c"/>',
           '<rect x="700" y="40" width="520" height="860" rx="60" fill="#15171e"/>',
           '<rect x="718" y="58" width="484" height="824" rx="46" fill="#f3f4f7"/>',
           f'<text x="960" y="150" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#16161c">{header}</text>',
           '<rect x="718" y="180" width="484" height="2" fill="#d9dbe2"/>']
    y = 230
    for text, side in lines:
        if side == "in":
            out.append(f'<rect x="750" y="{y}" width="330" height="70" rx="22" fill="#e3e5ec"/>'
                       f'<text x="772" y="{y+45}" font-family="Montserrat" font-weight="700" font-size="26" fill="#16161c">{text}</text>')
        else:
            out.append(f'<rect x="840" y="{y}" width="330" height="70" rx="22" fill="{accent}"/>'
                       f'<text x="862" y="{y+45}" font-family="Montserrat" font-weight="700" font-size="26" fill="#fff">{text}</text>')
        y += 96
    return "".join(out)


def doorway_grandma():
    """Kitchen doorway seen from the hall; warm kitchen light behind, dark hall in front."""
    out = [f'<rect width="{W}" height="{H}" fill="#1c2033"/>',
           '<rect x="660" y="160" width="600" height="700" fill="#e8c98e"/>',
           '<rect x="660" y="160" width="600" height="700" fill="#ffb84d" opacity="0.25"/>',
           '<rect x="700" y="420" width="520" height="30" fill="#c9a46c"/>',  # counter in kitchen
           '<rect x="1110" y="250" width="110" height="170" rx="10" fill="#cfc8b8"/>',  # wall phone base inside
           '<rect x="640" y="140" width="640" height="24" fill="#2a2f45"/>',
           '<rect x="640" y="140" width="24" height="720" fill="#2a2f45"/><rect x="1256" y="140" width="24" height="720" fill="#2a2f45"/>',
           '<path d="M660,860 L1260,860 L1500,1080 L420,1080 Z" fill="#ffcf7a" opacity="0.10"/>',
           _floor("#151827"),
           ]
    return "".join(out)


BG = {
    "stage": stage, "bedroom": bedroom, "hallway": hallway, "kids_room": kids_room, "kitchen": kitchen,
    "kitchen_table": kitchen_table, "street_night": street_night, "city_night": city_night, "earth": earth,
    "phone_close": phone_close, "phone_screen": phone_screen, "doorway": doorway_grandma,
}


def living_room(lights=False, tv_on=False):
    wall = "#2a2f45" if not lights else "#d9c9a8"
    out = [f'<rect width="{W}" height="{H}" fill="{wall}"/>',
           _floor("#1b1e2c" if not lights else "#8a6a4c"),
           window(1460, 170, 300, 280, sky="#0e1a36", frame="#3b4366", inner=stars(16, 0, 0, 300, 280, seed=12, op=0.8)),
           # TV on a low stand (left)
           '<rect x="120" y="700" width="420" height="160" rx="8" fill="#3a3045"/>',
           '<rect x="150" y="400" width="360" height="230" rx="10" fill="#111319"/>',
           f'<rect x="164" y="414" width="332" height="202" rx="4" fill="{"#7fb2ff" if tv_on else "#0b0d12"}" opacity="{0.8 if tv_on else 1}"/>',
           '<rect x="310" y="630" width="40" height="70" fill="#222"/>',
           # couch (right)
           '<rect x="820" y="560" width="640" height="120" rx="40" fill="#5a4a6e"/>',
           '<rect x="800" y="660" width="680" height="140" rx="30" fill="#6a5a80"/>',
           '<rect x="780" y="620" width="90" height="200" rx="34" fill="#5a4a6e"/><rect x="1410" y="620" width="90" height="200" rx="34" fill="#5a4a6e"/>',
           '<rect x="840" y="800" width="24" height="60" fill="#2a2333"/><rect x="1420" y="800" width="24" height="60" fill="#2a2333"/>',
           # coffee table
           '<rect x="600" y="760" width="200" height="20" rx="6" fill="#6b4a32"/><rect x="620" y="780" width="14" height="80" fill="#4f3624"/><rect x="766" y="780" width="14" height="80" fill="#4f3624"/>',
           ]
    return "".join(out)


def tv_news(text="SOLAR STORM?", color="#ef3b4f"):
    """A TV filling most of the frame, showing a news set. The anchor is placed by the shot."""
    out = [f'<rect width="{W}" height="{H}" fill="#14161f"/>',
           '<rect x="260" y="70" width="1400" height="800" rx="26" fill="#0b0c10"/>',
           '<rect x="290" y="100" width="1340" height="740" rx="8" fill="#1d3466"/>',
           '<rect x="290" y="100" width="1340" height="740" rx="8" fill="url(#newsg)"/>',
           '<defs><linearGradient id="newsg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a4c8f"/><stop offset="1" stop-color="#101b38"/></linearGradient></defs>',
           '<g fill="#ffffff" opacity="0.06">' + "".join(f'<rect x="{330+k*130}" y="130" width="90" height="380" rx="6"/>' for k in range(10)) + '</g>',
           '<rect x="420" y="560" width="1080" height="120" rx="10" fill="#0f1730"/>',
           f'<rect x="290" y="700" width="1340" height="90" fill="{color}"/>',
           f'<text x="330" y="762" font-family="Montserrat" font-weight="900" font-size="52" fill="#fff">{text}</text>',
           '<rect x="290" y="790" width="1340" height="50" fill="#0b0c10"/>',
           '<text x="330" y="825" font-family="Montserrat" font-weight="700" font-size="26" fill="#cfd6e8">BREAKING NEWS · LIVE</text>',
           '<rect x="900" y="870" width="120" height="40" fill="#0b0c10"/>',
           ]
    return "".join(out)


def classroom():
    out = [f'<rect width="{W}" height="{H}" fill="#cfe0d0"/>',
           '<rect x="0" y="560" width="1920" height="300" fill="#b9cdb9"/>',
           _floor("#8a6a4c"),
           '<rect x="560" y="140" width="800" height="330" rx="8" fill="#2f4a3a"/>',
           '<rect x="540" y="470" width="840" height="16" fill="#7a5a3a"/>',
           '<text x="600" y="230" font-family="Montserrat" font-weight="700" font-size="40" fill="#e8f0e8" opacity="0.85">TUESDAY</text>',
           window(140, 180, 260, 260, sky="#9fd0ff", frame="#7a8a7a"),
           window(1520, 180, 260, 260, sky="#9fd0ff", frame="#7a8a7a"),
           ]
    for r, y in enumerate((700, 800)):
        for c in range(6):
            x = 200 + c * 270 + (r * 40)
            out.append(f'<rect x="{x}" y="{y-70}" width="170" height="18" rx="4" fill="#a8774a"/>'
                       f'<rect x="{x+10}" y="{y-52}" width="10" height="70" fill="#6b4a32"/><rect x="{x+150}" y="{y-52}" width="10" height="70" fill="#6b4a32"/>')
    return "".join(out)


def microwave(door_open=False, glow_on=False):
    out = [f'<rect width="{W}" height="{H}" fill="#2b2f40"/>',
           '<rect x="0" y="640" width="1920" height="40" rx="4" fill="#4a5170"/>',
           '<rect x="0" y="680" width="1920" height="400" fill="#363b52"/>',
           # microwave
           '<rect x="560" y="250" width="800" height="400" rx="26" fill="#cfd3de"/>',
           '<rect x="600" y="290" width="540" height="320" rx="16" fill="#1a1d26"/>',
           f'<rect x="620" y="310" width="500" height="280" rx="10" fill="{"#ffd98a" if glow_on else "#0e1016"}" opacity="{0.6 if glow_on else 1}"/>',
           '<g fill="#000" opacity="0.25">' + "".join(f'<circle cx="{640+i*24}" cy="{330+j*24}" r="4"/>' for i in range(20) for j in range(11)) + '</g>',
           '<rect x="1170" y="290" width="150" height="320" rx="12" fill="#b9bdc8"/>',
           '<rect x="1195" y="320" width="100" height="40" rx="6" fill="#0d1220"/>',
           '<text x="1245" y="350" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="26" fill="#3a4258">--:--</text>',
           '<g fill="#8a8f9c">' + "".join(f'<rect x="{1195+(k%3)*36}" y="{390+(k//3)*36}" width="26" height="26" rx="5"/>' for k in range(9)) + '</g>',
           # unplugged cord
           '<path d="M1360,560 Q1460,600 1440,700 Q1420,760 1500,760" stroke="#1d1f26" stroke-width="12" fill="none"/>',
           '<rect x="1490" y="742" width="40" height="34" rx="6" fill="#1d1f26"/><rect x="1530" y="750" width="16" height="6" fill="#aaa"/><rect x="1530" y="762" width="16" height="6" fill="#aaa"/>',
           ]
    return "".join(out)


def ambulance_street(day=True):
    sky = "#9fc4e8" if day else "#0b1430"
    out = [f'<rect width="{W}" height="{H}" fill="{sky}"/>',
           house(520, FLOOR, 520, 360, "#c9a98a" if day else "#2a3550", "#8a5a4a" if day else "#1b2440", [False, False, False], seed=3),
           house(1180, FLOOR, 360, 300, "#b8b0a0" if day else "#26304f", "#6a6a7a" if day else "#1a2038", [False, False], seed=5),
           _floor("#6a6f7a" if day else "#151a2a"),
           '<rect x="0" y="870" width="1920" height="10" fill="#e8e8ee" opacity="0.4"/>',
           # ambulance
           '<g transform="translate(140 860)">'
           '<rect x="0" y="-260" width="430" height="220" rx="14" fill="#f4f4f6"/>'
           '<path d="M430,-200 L540,-200 L590,-120 L590,-40 L430,-40 Z" fill="#f4f4f6"/>'
           '<path d="M446,-188 L530,-188 L566,-126 L446,-126 Z" fill="#1d2c44"/>'
           '<rect x="0" y="-150" width="590" height="24" fill="#ef3b4f"/>'
           '<rect x="170" y="-236" width="24" height="70" fill="#ef3b4f"/><rect x="147" y="-213" width="70" height="24" fill="#ef3b4f"/>'
           '<rect x="40" y="-284" width="80" height="24" rx="6" fill="#3a6fd8"/><rect x="140" y="-284" width="60" height="24" rx="6" fill="#ef3b4f"/>'
           '<circle cx="110" cy="-36" r="46" fill="#1d1f26"/><circle cx="110" cy="-36" r="18" fill="#8a8f9c"/>'
           '<circle cx="470" cy="-36" r="46" fill="#1d1f26"/><circle cx="470" cy="-36" r="18" fill="#8a8f9c"/>'
           '</g>',
           # exhaust puffs
           '<g fill="#d9dce4" opacity="0.7"><circle cx="110" cy="800" r="18"/><circle cx="80" cy="780" r="24"/><circle cx="46" cy="752" r="30"/></g>',
           ]
    return "".join(out)


def notebook(lines=(), date="", page="#e9d9a6", ink="#2a3f8f"):
    out = [f'<rect width="{W}" height="{H}" fill="#2a2420"/>',
           '<rect x="380" y="60" width="1160" height="900" rx="10" fill="#1b1714"/>',
           f'<rect x="420" y="80" width="1080" height="860" rx="6" fill="{page}"/>',
           '<g fill="none" stroke="#b9a56f" stroke-width="2">' + "".join(f'<line x1="440" y1="{170+k*54}" x2="1480" y2="{170+k*54}"/>' for k in range(14)) + '</g>',
           '<line x1="540" y1="80" x2="540" y2="940" stroke="#c9504a" stroke-width="3" opacity="0.7"/>',
           f'<text x="1440" y="140" text-anchor="end" font-family="Caveat" font-size="44" fill="{ink}">{date}</text>' if date else "",
           ]
    for k, ln in enumerate(lines):
        out.append(f'<text id="nbl{k}" x="570" y="{214+k*54}" font-family="Caveat" font-size="42" fill="{ink}">{ln}</text>')
    return "".join(out)


def bedroom_grandma():
    out = [f'<rect width="{W}" height="{H}" fill="#2b2a3c"/>',
           _floor("#1c1b28"),
           '<g fill="#3d3b52">' + "".join(f'<rect x="{x}" y="0" width="40" height="860"/>' for x in range(60, 1900, 120)) + '</g>',
           window(1300, 180, 320, 300, sky="#0e1a36", frame="#4a4660", inner=moon(250, 70, 26) + stars(14, 0, 0, 320, 300, seed=21, op=0.8)),
           # old bed
           '<rect x="200" y="600" width="80" height="260" rx="10" fill="#5a3b2a"/>',
           '<rect x="260" y="660" width="620" height="120" rx="16" fill="#8a7aa0"/>',
           '<rect x="290" y="630" width="160" height="60" rx="26" fill="#efe6d6"/>',
           # nightstand with open drawer
           '<rect x="940" y="640" width="260" height="220" rx="8" fill="#6b4a32"/>',
           '<rect x="955" y="690" width="230" height="60" rx="6" fill="#4f3624"/>',
           '<rect x="955" y="760" width="230" height="60" rx="6" fill="#5a3f2a"/>',
           '<rect x="1040" y="560" width="14" height="80" fill="#8a8292"/><path d="M1000,560 L1094,560 L1074,505 L1020,505 Z" fill="#e7c98f"/>',
           '<circle cx="1047" cy="560" r="130" fill="#ffd98a" opacity="0.08"/>',
           ]
    return "".join(out)


BG.update({"living_room": living_room, "tv_news": tv_news, "classroom": classroom, "microwave": microwave,
           "ambulance": ambulance_street, "notebook": notebook, "bedroom_grandma": bedroom_grandma})


def gas_station():
    out = [f'<rect width="{W}" height="{H}" fill="#e4e9ef"/>',
           '<rect x="0" y="0" width="1920" height="70" fill="#c9d2dc"/>',
           "".join(f'<rect x="{x}" y="20" width="160" height="24" rx="6" fill="#fff8de"/>' for x in range(120, 1900, 320)),
           _floor("#b9bfc8"),
           # shelves
           "".join(f'<g transform="translate({x} 380)"><rect width="300" height="480" fill="#9aa4b2"/>'
                   + "".join(f'<rect x="10" y="{20+r*118}" width="280" height="10" fill="#7d8796"/>'
                             + "".join(f'<rect x="{16+c*46}" y="{-30+r*118+20}" width="38" height="48" rx="4" fill="{col}"/>'
                                       for c, col in enumerate(["#ef3b4f", "#ffd43b", "#3a6fd8", "#3fbf7f", "#f4f1ea", "#d9573b"]))
                             for r in range(4)) + '</g>' for x in (120, 470)),
           # counter + register
           '<rect x="1060" y="600" width="780" height="260" fill="#6b7686"/>',
           '<rect x="1040" y="580" width="820" height="30" rx="6" fill="#8a95a5"/>',
           '<rect x="1560" y="500" width="160" height="90" rx="10" fill="#2f3542"/><rect x="1580" y="515" width="120" height="40" rx="4" fill="#7fe3a0"/>',
           # door with chime
           '<rect x="860" y="300" width="160" height="560" fill="#bfe0f5" opacity="0.7"/><rect x="852" y="292" width="176" height="12" fill="#7d8796"/>',
           ]
    return "".join(out)


def payphone(x, y, s=1.0, cid=""):
    ident = f' id="{cid}"' if cid else ""
    return (f'<g{ident} transform="translate({x} {y}) scale({s})">'
            '<rect x="-12" y="-300" width="24" height="300" fill="#5a6070"/>'
            '<rect x="-70" y="-470" width="140" height="190" rx="10" fill="#3a6fd8"/>'
            '<rect x="-56" y="-455" width="112" height="40" rx="4" fill="#cfe0ff"/>'
            '<text x="0" y="-428" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#16233f">PHONE</text>'
            '<rect x="-50" y="-400" width="60" height="100" rx="6" fill="#2a2f3a"/>'
            '<g fill="#c9cad1">' + "".join(f'<rect x="{18+(k%3)*12}" y="{-396+(k//3)*14}" width="9" height="10" rx="2"/>' for k in range(12)) + '</g>'
            '<rect x="-64" y="-405" width="16" height="70" rx="8" fill="#1d1f26"/></g>')


def street_day(n_phones=3):
    out = [f'<rect width="{W}" height="{H}" fill="#b8d4ea"/>',
           '<circle cx="1760" cy="120" r="70" fill="#fff4cf"/><circle cx="1760" cy="120" r="140" fill="#fff4cf" opacity="0.25"/>',
           house(40, FLOOR, 420, 300, "#d9c4a8", "#8a5a4a", [False, False, False], seed=1),
           house(560, FLOOR, 360, 260, "#c9d2c0", "#6a7a5a", [False, False], seed=2),
           house(1020, FLOOR, 420, 320, "#e0cdb8", "#7a4a3a", [False, False, False], seed=3),
           house(1540, FLOOR, 340, 280, "#cbbfd8", "#5a4a6e", [False, False], seed=4),
           _floor("#8a8f9a"),
           '<rect x="0" y="880" width="1920" height="8" fill="#e8e8ee" opacity="0.5"/>']
    return "".join(out)


def porch_door(open_=True):
    """Front door seen from inside the hall: open door, dusk porch light outside."""
    out = [f'<rect width="{W}" height="{H}" fill="#2a2f45"/>',
           '<rect x="660" y="180" width="560" height="680" fill="#c97a4a"/>',
           '<rect x="660" y="180" width="560" height="680" fill="#2a1e3a" opacity="0.55"/>',
           '<circle cx="940" cy="250" r="90" fill="#ffd98a" opacity="0.25"/>',
           '<rect x="640" y="160" width="600" height="24" fill="#3a3f55"/>',
           '<rect x="640" y="160" width="24" height="700" fill="#3a3f55"/><rect x="1216" y="160" width="24" height="700" fill="#3a3f55"/>',
           ('<path d="M1220,184 L1400,150 L1400,900 L1220,860 Z" fill="#5a3b2a"/><circle cx="1380" cy="540" r="9" fill="#c9b27a"/>' if open_
            else '<rect x="664" y="184" width="552" height="676" fill="#5a3b2a"/><circle cx="1180" cy="540" r="9" fill="#c9b27a"/><circle cx="940" cy="440" r="10" fill="#111"/>'),
           _floor("#1b1e2c"),
           '<path d="M664,860 L1216,860 L1400,1000 L520,1000 Z" fill="#ffb84d" opacity="0.06"/>']
    return "".join(out)


def radio_kitchen():
    out = [kitchen(night=True, doorway=False),
           '<rect x="1180" y="470" width="300" height="110" rx="16" fill="#7a5a3a"/>',
           '<rect x="1200" y="488" width="150" height="74" rx="8" fill="#d8c9a6"/>',
           '<g stroke="#5a4a3a" stroke-width="3">' + "".join(f'<line x1="{1212+k*14}" y1="496" x2="{1212+k*14}" y2="554"/>' for k in range(10)) + '</g>',
           '<circle cx="1400" cy="510" r="18" fill="#3a2a1a"/><circle cx="1445" cy="510" r="18" fill="#3a2a1a"/>',
           '<rect x="1300" y="410" width="6" height="64" fill="#9a9384" transform="rotate(-20 1303 470)"/>',
           '<path d="M1480,560 Q1560,600 1540,700 Q1520,780 1600,800" stroke="#1d1f26" stroke-width="8" fill="none"/>']
    return "".join(out)


def closet():
    out = [f'<rect width="{W}" height="{H}" fill="#2b2a3c"/>', _floor("#1c1b28"),
           '<rect x="560" y="120" width="800" height="740" fill="#4a3b2e"/>',
           '<rect x="590" y="150" width="740" height="690" fill="#1c1712"/>',
           '<rect x="590" y="360" width="740" height="16" fill="#4a3b2e"/>',
           '<g fill="#3a4266">' + "".join(f'<rect x="{620+k*90}" y="180" width="70" height="170" rx="8"/>' for k in range(7)) + '</g>',
           '<rect x="760" y="560" width="400" height="240" rx="6" fill="#c9b08a"/><rect x="760" y="560" width="400" height="40" fill="#b39a74"/>',
           '<text x="960" y="700" text-anchor="middle" font-family="Caveat" font-size="46" fill="#5a3b2a">DON\'T OPEN</text>']
    return "".join(out)


BG.update({"gas_station": gas_station, "street_day": street_day, "porch": porch_door, "radio_kitchen": radio_kitchen,
           "closet": closet})
