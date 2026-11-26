"""EP02 — It Snowed for 40 Days Straight. Shot list (unit indices: build/units.json)."""
import sys

sys.path.insert(0, "/home/user/hyperframes/channel/tools")
import art  # noqa: E402
from art import (phone, icon as _icon, glow, lying, receiver, moon)  # noqa: E402
from shotkit import ch, X, CHECK, RING, WAVES, panel, SIL, CURSOR, DOTS  # noqa: E402
import bgs_winter  # noqa: E402,F401  (registers the winter backgrounds)

RULES_TOTAL = 20
CHAPTER_NODES = ["DAY 1", "DAY 3", "DAY 7", "DAY 12", "DAY 20", "DAY 30", "DAY 40"]
CHAPTER_PILLS = ["INTRO", "DAY 1 · THE CARDS", "DAY 3 · THE COLD", "DAY 7 · THE WALKERS", "DAY 12 · THE ROOF",
                 "DAY 20 · THE LIGHTS", "DAY 30 · THE KNOCK", "DAY 40 · THE LAST SNOW", "FINALE"]
AUDIO = []
END_AT = None

art.CAST["you"] = dict(art.CAST["you"], outfit="hoodie")
art.CAST.update({
    "maya": dict(coat="#d9433b", coat_d="#b8352e", legs="#2b3650", hair="#7a4028", skin=art.P["skin"], hair_style="long", extra="", outfit="puffer", freckles=True),
    "dad": dict(coat="#eef1f5", coat_d="#cdd4de", legs="#2a3346", hair="#3a2a20", skin=art.P["skin"], hair_style="short", extra="glasses", outfit="scrubs"),
    "kowalski": dict(coat="#4f8a6a", coat_d="#3f7457", legs="#3a3346", hair="#e6e6ea", skin=art.P["skin"], hair_style="bun", extra="glasses", outfit="coat", scarf="#c9364a"),
    "pratt": dict(coat="#8a5a3a", coat_d="#6e472d", legs="#2a2a33", hair="#2a2422", skin=art.P["skin2"], hair_style="bald", extra="moustache", outfit="sweater"),
    "walker": dict(coat="#cfd5de", coat_d="#b4bcc8", legs="#9aa3b2", hair="#8a8f9c", skin="#e9e2da", hair_style="short", extra="", outfit="zip", blush=False),
    "walker2": dict(coat="#d8d0c8", coat_d="#bfb6ad", legs="#a3a0ad", hair="#9a8f86", skin="#ece4dc", hair_style="long", extra="", outfit="coat", blush=False),
})


# ---------------------------------------------------------------- props
def CARD(x, y, s=1.0, rot=-4, yellowed=False, hand=False):
    paper = "#efe3b8" if yellowed else "#ffffff"
    lines = "".join(f'<rect x="-52" y="{-62+k*16}" width="{104 if k % 3 else 80}" height="6" rx="3" fill="{"#2a3f8f" if hand else "#2a2a33"}" opacity="{0.8 if hand else 1}"/>'
                    for k in range(9))
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-70" y="-90" width="140" height="180" rx="6" fill="{paper}"/>'
            f'<text x="0" y="-70" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="15" fill="#ef3b4f">20 RULES</text>{lines}</g>')


def BOOTS(x, y, s=1.0):
    b = '<path d="M-20,-70 L20,-70 L20,-10 L46,-6 Q56,0 50,10 L-20,10 Z" fill="#ffd43b"/>'
    return f'<g transform="translate({x} {y}) scale({s})">{b}<g transform="translate(70 0)">{b}</g></g>'


def SLED(x, y, s=1.0, color="#ef3b4f"):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-90" y="-26" width="180" height="40" rx="18" fill="{color}"/>'
            '<path d="M-100,24 L100,24 Q120,24 116,6" stroke="#8a8f9c" stroke-width="8" fill="none"/></g>')


def RADIO(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-120" y="-70" width="240" height="140" rx="20" fill="#7a5a3a"/>'
            '<rect x="-100" y="-50" width="120" height="100" rx="10" fill="#d8c9a6"/>'
            '<circle cx="70" cy="-15" r="18" fill="#3a2a1a"/><circle cx="70" cy="35" r="12" fill="#3a2a1a"/>'
            '<rect x="-20" y="-120" width="6" height="56" fill="#9a9384" transform="rotate(-20 -17 -64)"/></g>')


def CROW(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#111"><ellipse cx="0" cy="0" rx="34" ry="20"/>'
            '<circle cx="30" cy="-16" r="14"/><path d="M42,-18 L62,-12 L42,-8 Z" fill="#333"/><path d="M-30,-4 L-62,6 L-30,10 Z"/>'
            '<rect x="-6" y="16" width="4" height="18"/><rect x="6" y="16" width="4" height="18"/></g>')


def HELI(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#2a3346"><ellipse cx="0" cy="0" rx="90" ry="40"/>'
            '<rect x="70" y="-12" width="140" height="18" rx="8"/><rect x="-140" y="-56" width="280" height="8" rx="4"/>'
            '<rect x="-4" y="-56" width="8" height="20"/><ellipse cx="-30" cy="-6" rx="34" ry="22" fill="#7fb8ff"/>'
            '<rect x="-60" y="38" width="120" height="6"/></g>')


def STEPS(x0, y0, x1, y1, n=9):
    out = []
    for k in range(n):
        t = k / max(1, n - 1)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        off = 14 if k % 2 else -14
        out.append(f'<ellipse cx="{x + off:.0f}" cy="{y:.0f}" rx="16" ry="7" fill="#8fa0bb" opacity="0.8"/>')
    return "".join(out)


def ORB(x, y, r=40):
    return (f'<g><circle cx="{x}" cy="{y}" r="{r*4}" fill="#ffd98a" opacity="0.10"/><circle cx="{x}" cy="{y}" r="{r*2}" fill="#ffd98a" opacity="0.25"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffe9b0"/></g>')


def SOCKS(x, y, s=1.0, color="#c9364a"):
    sock = f'<path d="M-18,-70 L18,-70 L18,0 Q18,24 -8,24 L-40,24 Q-54,24 -54,10 Q-54,-2 -40,-2 L-18,-2 Z" fill="{color}"/><rect x="-18" y="-70" width="36" height="14" fill="#f4f1ea"/>'
    return f'<g transform="translate({x} {y}) scale({s})">{sock}<g transform="translate(80 6)">{sock}</g></g>'


def CAN(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-34" y="-46" width="68" height="92" rx="8" fill="#c9cad1"/>'
            '<rect x="-34" y="-20" width="68" height="40" fill="#ef3b4f"/><text x="0" y="8" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="16" fill="#fff">SOUP</text></g>')


def CUTAWAY(warm_room=1):
    rooms = [(660, 360), (960, 360), (660, 560), (960, 560)]
    out = ['<path d="M600,300 L1080,140 L1560,300 Z" fill="#5a4a6e"/>']
    for k, (x, y) in enumerate([(620, 300), (980, 300), (620, 520), (980, 520)]):
        warm = k == warm_room
        out.append(f'<rect x="{x}" y="{y}" width="340" height="200" fill="{"#ff9a3a" if warm else "#3a6fd8"}" opacity="{0.85 if warm else 0.45}"/>')
    out.append('<rect x="600" y="300" width="960" height="440" fill="none" stroke="#e8e8ee" stroke-width="10"/>'
               '<line x1="960" y1="300" x2="960" y2="740" stroke="#e8e8ee" stroke-width="8"/><line x1="600" y1="520" x2="1560" y2="520" stroke="#e8e8ee" stroke-width="8"/>')
    return "".join(out)


def CAR_ICON(x, y, s=1.0, color="#5a7da8"):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-90" y="-40" width="180" height="56" rx="16" fill="{color}"/>'
            '<path d="M-50,-40 L-30,-76 L40,-76 L60,-40 Z" fill="{0}"/><circle cx="-50" cy="20" r="18" fill="#1d1f26"/><circle cx="50" cy="20" r="18" fill="#1d1f26"/></g>').replace("{0}", color)


def FLAME(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0,40 Q-34,20 -24,-14 Q-16,6 -4,-2 Q-12,-34 10,-54 Q8,-24 26,-6 Q36,22 0,40 Z" fill="#ff8a2a"/>'
            '<path d="M0,40 Q-14,26 -6,8 Q2,18 8,10 Q16,26 0,40 Z" fill="#ffd36a"/></g>')


def ROPE(x0, y0, x1, y1):
    return f'<path d="M{x0},{y0} Q{(x0+x1)/2},{max(y0, y1)+80} {x1},{y1}" stroke="#c9a46c" stroke-width="10" fill="none" stroke-linecap="round"/>'


def SNOWCOAT(x, y, s=1.0):
    """Snow flecks on a character's shoulders and head (placed over a standing character at x,y)."""
    import random
    rnd = random.Random(int(x))
    return "".join(f'<circle cx="{x + rnd.uniform(-60, 60) * s:.0f}" cy="{y + rnd.choice([-320, -230, -225, -215]) * s + rnd.uniform(-8, 8):.0f}" r="{rnd.uniform(4, 8) * s:.1f}" fill="#ffffff"/>' for _ in range(26))


W8 = dict(mood="creepy")  # walkers

SHOTS = [
    # ------------------------------------------------------------------ COLD OPEN
    dict(at=1, bg=("porch", {"open_": False}), cam=("in", 1.12),
         html=[("kk", "big", "KNOCK. KNOCK.", 560, 380, (1, "knocks"), {"anim": "slam"}),
               ("sh", "tag y", "LOOK AT THEIR SHOULDERS", 640, 640, (1, "shoulders"))],
         acts=[("shake", (1, "knocks"), 9), ("dark", ("+", 0), 0.3, 0.01)]),
    dict(at=2, bg=("porch", {"open_": True}), snow="heavy", snow_clip=(664, 184, 552, 676), cam=("in", 1.3, "50% 35%"),
         svg=[("w", ch("@w", "walker", 940, 860, 1.5, mood="creepy"))],
         html=[("ns", "tag r", "NO SNOW ON THEM?", 1080, 280, (2, "snow")),
               ("do", "stamp", "DON'T OPEN", 600, 600, (2, "open"))],
         acts=[("noblink", "@w")]),
    # ------------------------------------------------------------------ INTRO
    dict(at=3, bg=("town_snow", {"night": False}), snow="light", cam=("in", 1.05),
         svg=[("you", ch("@you", "you", 820, 900, 1.3, mood="happy")), ("maya", ch("@maya", "maya", 1060, 900, 0.95, mood="happy", arms=(40, -60)))],
         html=[("clk", "clock", "4:15 PM", 160, 160, (3, "4:15")), ("so", "tag y", "SCHOOL'S OUT EARLY", 780, 300, (4, "early")),
               ("nm", "tag g", "NOBODY MINDS", 820, 370, (5, "minds"))]),
    dict(at=6, bg=("town_snow", {"night": False}), snow="light", cam=("in", 1.35, "50% 45%"),
         svg=[("maya", ch("@maya", "maya", 960, 1060, 1.6, mood="happy"))],
         html=[("fs", "tag w", "FIRST SNOW OF THE YEAR", 1080, 260, (6, "first")), ("bf", "tag", "BIG, SLOW FLAKES", 1080, 330, (7, "flakes"))],
         acts=[("eyes", "@maya", True, (7, "eyelashes"))]),
    dict(at=8, bg=("car_buried", {"night": False}), snow="heavy", cam=("in", 1.05),
         html=[("bd", "tag y", "BY DINNER", 300, 200, (8, "dinner"))]),
    dict(at=9, bg=("town_snow", {"night": True, "lit": (True, True, True, True)}), snow="heavy", cam=("in", 1.05),
         html=[("bm", "tag y", "BY MIDNIGHT", 300, 200, (9, "midnight")), ("cs", "tag", "CAN'T SEE ACROSS THE STREET", 800, 300, (9, "see"))]),
    dict(at=10, bg=("town_snow", {"night": False, "buried": 0.7}), snow="heavy", cam=("out", 1.1),
         html=[("bm", "tag y", "BY MORNING", 300, 200, (10, "morning")), ("uw", "tag", "UP TO THE WINDOWS", 300, 270, (10, "windows")),
               ("sf", "stamp", "STILL FALLING", 640, 420, (11, "falling"))]),
    dict(at=12, bg="radio_kitchen", cam=("in", 1.15, "70% 50%"),
         svg=[("wv", WAVES(1330, 525, "#ffd43b", 1.2))],
         html=[("st", "tag", "\"IT WILL STOP TOMORROW\"", 1060, 300, (12, "tomorrow")),
               ("x1", "stamp", "IT DOESN'T", 1100, 620, (13, "doesn't")), ("x2", "tag r", "NOT THAT WEEK", 1160, 740, (14, "week"))],
         acts=[("ring", "wv", (12, "radio"), 2.0)]),
    dict(at=15, bg="stage", snow="light", cam=("in", 1.08),
         html=[("n40", "big y", "40 DAYS", 650, 380, (15, "forty"), {"anim": "slam"})]),
    dict(at=16, bg=("earth", {"lights": False}), snow="heavy", cam=("out", 1.12),
         html=[("nt", "tag", "NOT JUST YOUR TOWN", 760, 180, (16, "town")), ("wc", "tag r", "THE WHOLE COUNTRY", 760, 880, (17, "country"))]),
    dict(at=18, bg="stage", cam=("in", 1.05),
         svg=[("a", panel(560, 470, 280, 260, CAR_ICON(0, 10, 1.3, "#ffb020"), "#2a2c3c"), (18, "plows")), ("xa", X(560, 470, 0.7), (18, "plows")),
              ("b", panel(960, 470, 280, 260, _icon("paper", 0, 0, 2.2, "#c9a46c"), "#2a2c3c"), (19, "deliveries")), ("xb", X(960, 470, 0.7), (19, "deliveries")),
              ("c", panel(1360, 470, 280, 260, _icon("house", 0, 0, 2.2, "#e8e8ee"), "#2a2c3c"), (20, "way"))],
         html=[("la", "tag", "NO PLOWS", 490, 650, (18, "plows")), ("lb", "tag", "NO DELIVERIES", 860, 650, (19, "deliveries")),
               ("lc", "stamp", "NO WAY OUT", 1170, 680, (20, "out"))]),
    dict(at=21, bg=("porch", {"open_": False}), cam=("in", 1.15, "49% 45%"),
         svg=[("cd", CARD(940, 520, 1.3, -4), (21, "card"))],
         html=[("ed", "tag y", "EVERY FRONT DOOR", 1060, 300, (21, "every")), ("wp", "tag w", "WHITE PLASTIC", 1060, 370, (22, "plastic")),
               ("tr", "tag r", "20 RULES", 1060, 440, (23, "Twenty")), ("wh", "bubble", "WHO PUT THEM THERE?", 400, 300, (24, "knows"))]),
    dict(at=25, bg="stage", cam=("in", 1.06),
         svg=[("dots", DOTS(20, 470, "#3fbf7f"), (25, "followed"))],
         html=[("ss", "tag g", "THEY SAW THE SPRING", 760, 300, (25, "spring")), ("od", "tag", "ONE DAY AT A TIME", 780, 600, (27, "day")),
               ("r20", "stamp", "RULE 20 MATTERS", 680, 700, (28, "twenty"))]),
    # ------------------------------------------------------------------ DAY 1
    dict(at=29, kind="chapter"),
    dict(at=30, bg="kitchen_winter", cam=("in", 1.06, "30% 45%"),
         svg=[("dad", ch("@dad", "dad", 560, 900, 1.45, mood="happy", arms=(10, -130)))],
         html=[("ns", "tag", "NOBODY TAKES IT SERIOUSLY", 640, 220, (30, "seriously")), ("mg", "tag y", "ON THE FRIDGE", 330, 560, (31, "fridge"))],
         acts=[("talk", "@dad", (31, "laughs"), 6)]),
    dict(at=32, bg=("town_snow", {"night": True}), snow="heavy", cam=("in", 1.08),
         svg=[("car", CAR_ICON(960, 840, 1.6, "#5a7da8"))],
         html=[("ns", "tag", "NIGHT SHIFT AT THE HOSPITAL", 700, 260, (32, "hospital")), ("lt", "stamp", "THE LAST TIME FOR 40 DAYS", 480, 400, (33, "last"))],
         acts=[("move", "car", 1200, 0, (32, "drives"), 3.0, "power2.in")]),
    dict(at=34, bg=("living_winter", {"fire": True, "blankets": False, "lit": True}), cam=("in", 1.06),
         svg=[("you", ch("@you", "you", 860, 880, 1.4, mood="neutral")), ("maya", ch("@maya", "maya", 1130, 880, 0.95, mood="happy"))],
         html=[("my", "tag y", "MAYA, 7", 1080, 520, (34, "Maya")), ("po", "tag g", "POWER: ON", 300, 200, (35, "power")),
               ("tv", "tag", "\"JUST A STORM\"", 300, 270, (36, "storm"))]),
    dict(at=38, kind="rule", n="1", imp="FILL EVERYTHING WITH WATER"),
    dict(at=40, bg="bathroom", cam=("in", 1.05),
         html=[("bt", "tag b", "THE BATHTUB", 820, 460, (40, "bathtub")), ("ep", "tag b", "EVERY POT", 300, 260, (41, "pot")),
               ("eb", "tag b", "EVERY BOTTLE", 300, 330, (42, "bottle"))]),
    dict(at=43, bg="stage", cam=("in", 1.05),
         svg=[("pipe", '<rect x="360" y="440" width="1200" height="80" rx="40" fill="#8a8f9c"/><rect x="760" y="440" width="400" height="80" fill="#bfe3ff"/>'
                       '<g fill="#ffffff" opacity="0.8"><path d="M800,440 L830,470 L860,440 Z"/><path d="M1000,520 L1030,490 L1060,520 Z"/></g>', (43, "pipes")),
              ("drip", '<path d="M1560,520 Q1576,560 1560,600 Q1544,560 1560,520 Z" fill="#7fb8ff"/>', (44, "drip"))],
         html=[("pf", "tag r", "PIPES FREEZE", 820, 300, (43, "freeze")), ("oc", "tag", "OPEN THE CABINETS", 380, 640, (44, "cabinet")),
               ("dr", "tag g", "LET IT DRIP", 1420, 650, (44, "drip")), ("mv", "tag", "MOVING WATER FREEZES SLOWER", 700, 760, (45, "Moving"))]),
    dict(at=46, bg="bathroom", cam=("in", 1.06),
         svg=[("maya", ch("@maya", "maya", 660, 900, 1.1, mood="happy", arms=(30, -80))), ("bt", BOOTS(860, 860, 1.4), (47, "boots"))],
         html=[("gm", "bubble", "IT'S A GAME!", 700, 380, (46, "game")), ("rb", "tag y", "HER RAIN BOOTS", 880, 640, (47, "rain"))]),
    dict(at=49, kind="rule", n="2", imp="LIVE IN ONE ROOM"),
    dict(at=50, bg="stage", cam=("in", 1.05),
         svg=[("ct", CUTAWAY(2), (50, "Pick"))],
         html=[("or", "tag g", "ONE ROOM", 700, 780, (50, "one")), ("ch", "tag r", "CAN'T HEAT A WHOLE HOUSE", 960, 780, (51, "heat")),
               ("fp", "tag y", "THE FIREPLACE", 660, 220, (52, "fireplace"))]),
    dict(at=53, bg=("living_winter", {"fire": True, "blankets": True, "lit": True}), cam=("in", 1.06),
         html=[("tw", "tag", "TOWELS UNDER THE DOORS", 1300, 560, (53, "Towels")), ("bl", "tag", "BLANKETS OVER THE WINDOWS", 1340, 120, (54, "Blankets")),
               ("mt", "tag", "MATTRESSES ON THE FLOOR", 820, 720, (55, "Mattresses")),
               ("co", "tag w", "OTHER ROOMS: WEAR A COAT", 100, 200, (56, "coat")), ("cd", "tag g", "CLOSED DOOR = WARM ROOM", 100, 270, (57, "closed"))]),
    dict(at=59, kind="rule", n="3", imp="NEVER LET SNOW BURY THE VENTS"),
    dict(at=60, bg=("house_side", {"buried": 0.55}), snow="light", cam=("in", 1.15, "62% 62%"),
         svg=[("ar", '<path d="M1380,560 Q1460,500 1420,420" stroke="#ef3b4f" stroke-width="10" fill="none" stroke-dasharray="20 14"/><path d="M1400,420 L1420,380 L1446,416 Z" fill="#ef3b4f"/>', (63, "fumes", "fade"))],
         html=[("vn", "tag", "THE VENTS", 1080, 460, (60, "vents")), ("fd", "tag w", "FURNACE · DRYER · WATER HEATER", 900, 360, (61, "furnace")),
               ("fb", "tag r", "FUMES COME BACK INSIDE", 1240, 280, (63, "fumes"))]),
    dict(at=64, bg=("living_winter", {"fire": True, "blankets": True, "lit": False}), cam=("in", 1.06),
         svg=[("maya", lying(ch("@maya", "maya", 0, 0, 0.8), 960, 790, 90)), ("you", ch("@you", "you", 760, 880, 1.35, mood="sad"))],
         html=[("cs", "tag", "CAN'T SEE IT", 300, 200, (64, "see")), ("cm", "tag", "CAN'T SMELL IT", 300, 270, (65, "smell")),
               ("vt", "tag r", "VERY TIRED", 820, 360, (66, "tired"))],
         acts=[("eyes", "@maya", True, ("+", 0)), ("dark", (66, "tired"), 0.35, 1.0)]),
    dict(at=67, bg="stage", cam=("in", 1.05),
         html=[("h", "tag", "HEADACHE", 640, 300, (67, "headache")), ("d", "tag", "DIZZY", 820, 380, (67, "dizzy")),
               ("s", "tag", "FEELING SICK", 700, 460, (67, "sick")), ("fa", "stamp g", "GET FRESH AIR NOW", 560, 600, (67, "fresh"))]),
    dict(at=68, bg=("house_side", {"buried": 0.5}), snow="light", cam=("in", 1.06),
         svg=[("you", ch("@you", "you", 1500, 900, 1.3, mood="neutral", arms=(10, -120)))],
         html=[("td", "tag y", "TWICE A DAY", 1000, 300, (68, "Twice")), ("kp", "tag", "WITH A KITCHEN POT", 1000, 370, (68, "pot"))]),
    dict(at=69, bg="kitchen_winter", cam=("in", 1.6, "13% 32%"),
         html=[("sl", "tag", "SMALLER LETTERS", 460, 240, (69, "smaller")),
               ("cold", "tag r", "THE SNOW IS NOT THE ONLY THING THAT'S COLD", 330, 560, (70, "cold"))],
         acts=[("dark", (70, "snow"), 0.35, 0.8)]),
    # ------------------------------------------------------------------ DAY 3
    dict(at=71, kind="chapter"),
    dict(at=72, bg=("living_winter", {"fire": False, "blankets": True, "lit": False}), cam=("in", 1.06),
         svg=[("you", ch("@you", "you", 860, 880, 1.4, mood="worried")), ("maya", ch("@maya", "maya", 1130, 880, 0.95, mood="scared"))],
         html=[("po", "tag r", "POWER: OFF", 300, 200, (72, "power")), ("fs", "tag", "THE FURNACE STOPS", 300, 270, (73, "furnace")),
               ("sl", "tag w", "SILENCE", 860, 300, (74, "silence"))],
         acts=[("dark", (72, "out"), 0.3, 0.2)]),
    dict(at=75, bg="garage_grill", cam=("in", 1.06),
         svg=[("pr", ch("@pr", "pratt", 1180, 900, 1.4, mood="neutral", arms=(10, -60)))],
         html=[("mp", "tag y", "MR. PRATT", 1300, 260, (75, "Pratt")), ("gg", "tag r", "GAS GRILL IN THE GARAGE", 1060, 360, (75, "grill"))]),
    dict(at=77, kind="rule", n="4", imp="NEVER BURN FUEL INDOORS"),
    dict(at=78, bg="stage", cam=("in", 1.05),
         svg=[("a", panel(560, 470, 280, 260, '<rect x="-60" y="-50" width="120" height="70" rx="24" fill="#c9cad1"/><rect x="-8" y="20" width="16" height="70" fill="#c9cad1"/>', "#3a3c4c"), (78, "grill")),
              ("b", panel(960, 470, 280, 260, '<rect x="-70" y="-40" width="140" height="90" rx="10" fill="#ef3b4f"/><circle cx="-30" cy="60" r="16" fill="#1d1f26"/><circle cx="30" cy="60" r="16" fill="#1d1f26"/>', "#3a3c4c"), (78, "generator")),
              ("c", panel(1360, 470, 280, 260, FLAME(0, 0, 1.6), "#3a3c4c"), (78, "stove")),
              ("xa", X(560, 470, 0.7), (79, "house")), ("xb", X(960, 470, 0.7), (80, "garage")), ("xc", X(1360, 470, 0.7), (81, "open"))],
         html=[("la", "tag", "NOT IN THE HOUSE", 450, 650, (79, "house")), ("lb", "tag", "NOT IN THE GARAGE", 850, 650, (80, "garage")),
               ("lc", "tag r", "NOT EVEN WITH THE DOOR OPEN", 1180, 720, (81, "open"))]),
    dict(at=82, bg="stage", cam=("in", 1.06),
         svg=[("box", '<rect x="620" y="300" width="680" height="440" rx="20" fill="none" stroke="#c9cad1" stroke-width="12"/>', (82, "closed")),
              ("cloud", '<g fill="#8a8f9c" opacity="0.7"><circle cx="760" cy="620" r="90"/><circle cx="900" cy="580" r="120"/><circle cx="1080" cy="610" r="110"/><circle cx="1180" cy="640" r="80"/></g>', (82, "builds", "fade"))],
         html=[("co", "stamp", "CARBON MONOXIDE", 660, 160, (82, "carbon")), ("ff", "tag r", "BUILDS UP FAST", 800, 780, (82, "faster"))]),
    dict(at=83, bg=("town_snow", {"night": True, "lit": (False, True, False, False)}), snow="light", cam=("in", 1.2, "38% 70%"),
         svg=[("dg", _icon("dog", 740, 830, 1.4, "#3a2e26"), (84, "dog"))],
         html=[("gl", "tag y", "THE GARAGE LIGHT STAYS ON", 560, 300, (83, "light")), ("sc", "tag r", "NOBODY COMES", 820, 640, (84, "nobody"))]),
    dict(at=85, bg="garage_grill", cam=("in", 1.06),
         svg=[("pr", lying(ch("@pr", "pratt", 0, 0, 1.1, mood="sad"), 620, 830, 90)),
              ("you", ch("@you", "you", 420, 900, 1.35, mood="scared", arms=(-40, -70))), ("kw", ch("@kw", "kowalski", 1380, 900, 1.35, mood="worried", arms=(60, -60)))],
         html=[("mk", "tag y", "MRS. KOWALSKI", 1300, 300, (85, "Kowalski")), ("mi", "tag g", "HE MAKES IT", 820, 300, (86, "makes")),
               ("wh", "bubble", "WHO WAS IN HERE WITH ME?", 760, 470, (88, "asking"))],
         acts=[("eyes", "@pr", True, ("+", 0)), ("dark", (88, "standing"), 0.35, 0.8)]),
    dict(at=90, kind="rule", n="5", imp="STAY DRY"),
    dict(at=92, bg="stage", cam=("in", 1.05),
         svg=[("s", panel(560, 470, 280, 260, SOCKS(-30, 20, 1.1, "#7fb8ff"), "#2a2c3c"), (93, "socks")),
              ("g", panel(960, 470, 280, 260, '<path d="M-40,40 L-40,-30 Q-40,-50 -24,-50 L-24,-70 Q-10,-80 0,-66 L0,-80 Q14,-90 24,-74 L24,-60 Q40,-64 40,-44 L40,40 Z" fill="#7fb8ff"/>', "#2a2c3c"), (94, "gloves")),
              ("t", panel(1360, 470, 280, 260, '<path d="M-70,-50 L-30,-70 Q0,-50 30,-70 L70,-50 L56,-10 L40,-16 L40,70 L-40,70 L-40,-16 L-56,-10 Z" fill="#7fb8ff"/>', "#2a2c3c"), (95, "shirt"))],
         html=[("wk", "stamp", "WET KILLS FASTER", 640, 120, (92, "wet")), ("ws", "tag", "WET SOCKS", 490, 650, (93, "socks")),
               ("wg", "tag", "WET GLOVES", 880, 650, (94, "gloves")), ("sw", "tag", "SWEATY SHIRT", 1270, 650, (95, "shirt"))]),
    dict(at=96, bg=("living_winter", {"fire": False, "blankets": True, "lit": False}), cam=("in", 1.06),
         svg=[("you", ch("@you", "you", 860, 880, 1.45, mood="neutral"))],
         html=[("ly", "tag", "LAYERS", 1060, 260, (96, "layers")), ("cd", "tag", "CHANGE ANYTHING DAMP", 1060, 330, (96, "damp")),
               ("hh", "tag y", "HEAD · HANDS · FEET FIRST", 1060, 400, (97, "head")),
               ("ct", "tag r", "COTTON ✗", 400, 520, (98, "Cotton")), ("wl", "tag g", "WOOL ✓", 400, 590, (99, "Wool"))]),
    dict(at=100, bg="stage", cam=("in", 1.08),
         svg=[("sk", SOCKS(900, 560, 2.6, "#c9364a"), (100, "socks"))],
         html=[("mv", "tag y", "THE MOST VALUABLE THING IN THE HOUSE", 560, 760, (100, "valuable"))]),
    dict(at=102, kind="rule", n="6", imp="DON'T EAT THE SNOW"),
    dict(at=103, bg="stage", cam=("in", 1.05),
         svg=[("sn", '<g fill="#eef3fa"><circle cx="560" cy="520" r="90"/><circle cx="500" cy="560" r="60"/><circle cx="630" cy="560" r="70"/></g>', (103, "snow")),
              ("ar1", '<path d="M700,520 L800,520" stroke="#fff" stroke-width="8"/><path d="M800,500 L830,520 L800,540 Z" fill="#fff"/>', (106, "Melt", "fade")),
              ("pot", '<rect x="880" y="470" width="200" height="120" rx="14" fill="#8a8f9c"/>' + FLAME(980, 640, 1.0), (106, "Melt")),
              ("ar2", '<path d="M1120,520 L1220,520" stroke="#fff" stroke-width="8"/><path d="M1220,500 L1250,520 L1220,540 Z" fill="#fff"/>', (108, "boil", "fade")),
              ("cup", '<path d="M1300,450 L1420,450 L1400,590 L1320,590 Z" fill="#7fb8ff"/>', (108, "boil"))],
         html=[("hb", "tag r", "PULLS HEAT OUT OF YOU", 400, 300, (105, "heat")), ("tc", "tag y", "10 CUPS = 1 CUP", 840, 700, (107, "Ten")),
               ("bl", "tag g", "MELT · THEN BOIL", 1240, 700, (108, "boil"))]),
    dict(at=109, bg="kitchen_winter", cam=("in", 1.6, "13% 32%"),
         html=[("an", "tag", "ANOTHER REASON", 460, 240, (109, "reason")),
               ("ns", "stamp", "SOME OF THE SNOW ISN'T SNOW", 320, 520, (110, "isn't"))],
         acts=[("dark", (110, "Some"), 0.45, 0.8)]),
    # ------------------------------------------------------------------ DAY 7
    dict(at=111, kind="chapter"),
    dict(at=112, bg="upstairs_window", snow="heavy", cam=("in", 1.06),
         html=[("ab", "tag", "ABOVE THE WINDOWS", 300, 160, (112, "above")), ("ow", "tag y", "THE ONLY WAY OUT", 300, 230, (113, "way"))]),
    dict(at=114, bg=("whiteout", {"figures": 3}), snow="whiteout", cam=("in", 1.08),
         html=[("pp", "tag r", "PEOPLE", 860, 200, (116, "People")), ("ws", "tag", "WALKING SLOWLY", 820, 270, (117, "Walking")),
               ("nc", "stamp", "NO COATS", 760, 360, (118, "coats"))],
         acts=[("js", 'tl.to("$cam svg g[opacity]",{x:60,duration:6,ease:"none",stagger:0.4},0);', ("+", 0))]),
    dict(at=119, bg=("whiteout", {"figures": 0}), snow="whiteout", cam=("in", 1.1, "50% 40%"),
         svg=[("w", ch("@w", "walker", 960, 960, 1.9, **W8))],
         html=[("cc", "tag", "CLEAN CLOTHES", 1160, 300, (119, "clean")), ("dh", "tag", "DRY HAIR", 1160, 370, (120, "dry")),
               ("nl", "tag r", "THEY NEVER LOOK UP", 1100, 450, (121, "look")), ("ny", "stamp", "NOT YET", 1180, 560, (122, "yet"))],
         acts=[("noblink", "@w")]),
    dict(at=124, kind="rule", n="7", imp="FOOTPRINTS THAT ONLY COME IN"),
    dict(at=126, bg=("town_snow", {"night": False, "buried": 0.5}), snow="light", cam=("in", 1.08, "40% 70%"),
         svg=[("st", STEPS(1700, 1000, 760, 840, 11), (127, "middle", "fade"))],
         html=[("fs", "tag", "FRESH SNOW", 300, 200, (126, "fresh")), ("sd", "tag y", "STRAIGHT TO YOUR DOOR", 760, 640, (128, "Straight")),
               ("st2", "tag", "AND THEY STOP", 760, 710, (129, "stop")), ("np", "tag", "NOBODY ON THE PORCH", 300, 270, (130, "nobody")),
               ("nb", "stamp", "NO WAY BACK", 1180, 300, (131, "back"))]),
    dict(at=132, bg=("porch", {"open_": False}), cam=("in", 1.12),
         html=[("so", "tag r", "IT'S STILL OUT THERE", 300, 300, (132, "still")), ("ws", "tag g", "WAIT FOR NEW SNOW", 300, 370, (133, "covers"))],
         acts=[("dark", ("+", 0), 0.25, 0.01)]),
    dict(at=135, kind="rule", n="8", imp="CURTAINS CLOSED AFTER DARK"),
    dict(at=136, bg=("living_winter", {"fire": True, "blankets": True, "lit": False}), cam=("in", 1.1, "80% 35%"),
         html=[("cc", "tag g", "EVERY CURTAIN CLOSED", 1100, 560, (136, "curtain")), ("nc", "tag", "NOT BECAUSE OF THE COLD", 1100, 630, (137, "cold"))]),
    dict(at=138, bg=("whiteout", {"figures": 2}), snow="whiteout", cam=("in", 1.06),
         svg=[("win", '<rect x="880" y="420" width="160" height="140" fill="#ffd98a"/><circle cx="960" cy="490" r="220" fill="#ffd98a" opacity="0.25"/>', (138, "lit"))],
         html=[("ot", "tag", "THE ONLY THING YOU CAN SEE", 700, 220, (138, "only")),
               ("lk", "stamp", "NOT THE ONLY ONE LOOKING", 520, 650, (139, "looking"))]),
    dict(at=140, bg=("living_winter", {"fire": True, "blankets": True, "lit": False}), cam=("in", 1.08),
         svg=[("you", ch("@you", "you", 860, 880, 1.4, mood="worried")), ("maya", ch("@maya", "maya", 1130, 880, 0.95, mood="worried"))],
         html=[("q", "bubble", "WHY DON'T THEY GET COLD?", 1060, 360, (140, "asks")), ("na", "tag", "NO ANSWER", 640, 360, (141, "answer"))],
         acts=[("talk", "@maya", (140, "asks"), 8)]),
    dict(at=142, bg="upstairs_window", snow="heavy", cam=("in", 1.08),
         svg=[("maya", ch("@maya", "maya", 600, 980, 1.2, mood="shock"))],
         html=[("pk", "tag y", "DAY 8: MAYA PEEKS", 1100, 200, (142, "peeks")), ("js", "tag", "JUST FOR A SECOND", 1100, 270, (143, "second"))]),
    dict(at=144, bg=("town_snow", {"night": False, "buried": 0.5}), snow="light", cam=("in", 1.08),
         svg=[(f"w{k}", ch(f"@w{k}", "walker" if k % 2 else "walker2", 220 + k * 300, 900, 0.9, **W8)) for k in range(6)],
         html=[("ff", "stamp", "ALL FACING YOUR HOUSE", 560, 260, (144, "facing"))],
         acts=[("noblink", f"@w{k}") for k in range(6)] + [("shake", (144, "facing"), 7)]),
    dict(at=146, kind="rule", n="9", imp="COUNT EVERYONE EVERY HOUR"),
    dict(at=147, bg=("living_winter", {"fire": True, "blankets": True, "lit": False}), cam=("in", 1.06),
         svg=[("you", ch("@you", "you", 760, 880, 1.4, mood="neutral")), ("maya", ch("@maya", "maya", 1030, 880, 0.95, mood="neutral"))],
         html=[("ol", "tag y", "OUT LOUD", 300, 200, (147, "loud")), ("one", "big", "ONE.", 560, 300, (148, "One")),
               ("two", "big", "TWO.", 1000, 300, (149, "Two")), ("sp", "tag", "THAT'S HOW IT'S SUPPOSED TO GO", 640, 520, (150, "supposed"))]),
    dict(at=151, bg=("living_winter", {"fire": False, "blankets": True, "lit": False}), cam=("in", 1.15, "70% 50%"),
         svg=[("you", ch("@you", "you", 760, 880, 1.4, mood="neutral")), ("maya", ch("@maya", "maya", 1030, 880, 0.95, mood="neutral")),
              ("eye", '<circle cx="1830" cy="640" r="7" fill="#e8e0d8"/><circle cx="1860" cy="640" r="7" fill="#e8e0d8"/>', (152, "third", "fade"))],
         html=[("n9", "tag", "NIGHT 9", 300, 200, (151, "ninth")), ("thr", "big r", "THREE.", 1380, 420, (152, "three"), {"anim": "slam"})],
         acts=[("mood", "@you", "scared", (152, "three")), ("mood", "@maya", "scared", (152, "three")), ("dark", ("+", 0), 0.35, 0.01)]),
    dict(at=153, bg="stage", cam=("in", 1.06),
         html=[("ca", "tag", "COUNT AGAIN", 820, 300, (153, "Count")), ("ol", "tag y", "OUT LOUD", 860, 380, (154, "loud")),
               ("dl", "stamp", "DON'T LOOK AT THE CORNER", 520, 520, (155, "corner"))]),
    # ------------------------------------------------------------------ DAY 12
    dict(at=156, kind="chapter"),
    dict(at=157, bg="ceiling", cam=("in", 1.08, "40% 20%"),
         html=[("ht", "tag", "THE HOUSE STARTS TO TALK", 900, 380, (157, "talk")), ("cr", "tag y", "CRACKS", 600, 200, (158, "cracks")),
               ("gr", "tag y", "GROANS", 1200, 200, (159, "groans"))],
         acts=[("shake", (158, "cracks"), 4), ("shake", (159, "groans"), 5)]),
    dict(at=160, bg="stage", cam=("in", 1.05),
         svg=[("blk", '<rect x="560" y="360" width="360" height="200" rx="10" fill="#eef3fa"/>', (161, "foot")),
              ("eq", '<text x="1000" y="490" font-family="Montserrat" font-weight="900" font-size="90" fill="#fff">=</text>', (161, "weighs", "fade")),
              ("car", CAR_ICON(1300, 480, 1.8, "#5a7da8"), (161, "car"))],
         html=[("sh", "tag", "SNOW IS HEAVY", 820, 200, (160, "heavy")), ("ft", "tag", "1 FOOT OF WET SNOW", 600, 600, (161, "foot")),
               ("x4", "big r", "×4", 1500, 600, (162, "four"), {"anim": "slam"})]),
    dict(at=164, kind="rule", n="10", imp="LISTEN TO THE ROOF"),
    dict(at=165, bg="ceiling", cam=("in", 1.06),
         html=[("cc", "tag", "CREAKS · CRACKS", 300, 360, (166, "creaks")), ("ds", "tag", "DOORS STICKING", 300, 430, (166, "sticking")),
               ("sw", "tag g", "STRONGEST WALLS", 1300, 360, (167, "strongest")), ("nm", "tag r", "NOT IN THE MIDDLE", 1300, 430, (168, "middle"))],
         acts=[("shake", (166, "bending"), 4)]),
    dict(at=169, bg=("town_snow", {"night": True, "buried": 0.5}), snow="heavy", cam=("in", 1.1),
         html=[("lg", "tag y", "THE LEES' GARAGE · 3 AM", 600, 200, (169, "Lees")), ("bang", "big r", "BANG.", 760, 380, (170, "gunshot"), {"anim": "slam"})],
         acts=[("flash", (170, "gunshot")), ("dark", (171, "nothing"), 0.5, 0.8)]),
    dict(at=173, kind="rule", n="11", imp="NEVER SHOVEL ALONE"),
    dict(at=174, bg=("house_side", {"buried": 0.45}), snow="light", cam=("in", 1.06),
         svg=[("you", ch("@you", "you", 1500, 900, 1.3, mood="worried", arms=(10, -120))),
              ("hrt", '<path d="M0,20 L-40,-20 Q-60,-50 -30,-60 Q-10,-64 0,-40 Q10,-64 30,-60 Q60,-50 40,-20 Z" fill="#ef3b4f" transform="translate(1180 380) scale(1.4)"/>', (175, "heart"))],
         html=[("hh", "tag r", "THE HARDEST THING FOR YOUR HEART", 700, 220, (175, "hardest")),
               ("tb", "tag g", "TAKE BREAKS", 300, 520, (177, "breaks")), ("ll", "tag g", "LIFT LESS", 300, 590, (178, "Lift")),
               ("pd", "tag g", "PUSH, DON'T LIFT", 300, 660, (179, "Push")), ("sw", "tag y", "SOMEONE WATCHING", 300, 730, (180, "watching"))]),
    dict(at=181, bg=("town_snow", {"night": False, "buried": 0.45}), snow="light", cam=("in", 1.08),
         svg=[("kw", ch("@kw", "kowalski", 960, 900, 1.45, mood="happy", arms=(10, -120)))],
         html=[("mk", "tag y", "MRS. KOWALSKI", 1100, 300, (181, "Kowalski")), ("78", "tag", "AGE 78", 1100, 370, (182, "seventy")),
               ("db", "bubble", "I'VE DONE THIS BEFORE.", 1100, 450, (183, "done")), ("wn", "tag r", "WHEN?", 1100, 560, (184, "when"))],
         acts=[("talk", "@kw", (183, "tells"), 6)]),
    dict(at=185, bg="stage", cam=("in", 1.08),
         svg=[("cd", CARD(960, 470, 2.6, -3, yellowed=True, hand=True), (185, "card"))],
         html=[("yc", "tag", "YELLOW AND CRACKED", 380, 300, (186, "yellow")), ("fb", "tag y", "FEBRUARY 1978", 1240, 300, (187, "1978")),
               ("ch", "stamp", "A CHILD'S HANDWRITING", 540, 760, (188, "child's"))]),
    dict(at=190, kind="rule", n="12", imp="NEVER SLEEP IN A RUNNING CAR"),
    dict(at=191, bg=("car_buried", {"night": False}), snow="light", cam=("in", 1.15, "40% 75%"),
         svg=[("rg", RING(950, 760, 70, "#ef3b4f"), (192, "exhaust"))],
         html=[("eb", "tag r", "EXHAUST PIPE BURIED", 760, 600, (192, "exhaust")),
               ("t1", "tag g", "10 MIN AN HOUR", 1250, 200, (193, "ten")), ("t2", "tag g", "WINDOW OPEN A CRACK", 1250, 270, (193, "window")),
               ("t3", "tag g", "KEEP THE PIPE CLEAR", 1250, 340, (193, "clear"))]),
    dict(at=194, bg=("car_buried", {"night": False}), snow="light", cam=("in", 1.06),
         svg=[("kw", ch("@kw", "kowalski", 1180, 900, 1.35, mood="scared", arms=(10, -100)))],
         html=[("gc", "tag y", "THE GARCIAS", 400, 300, (194, "Garcias")), ("it", "tag g", "IN TIME", 1100, 300, (195, "time")),
               ("bl", "stamp", "BARELY", 1150, 420, (196, "Barely"))]),
    dict(at=197, bg="stage", cam=("in", 1.06),
         html=[("q", "big y", "?", 900, 120, (197, "Quick")),
               ("wq", "big", "WHICH RULE WOULD YOU FORGET?", 200, 360, (198, "Which"), {"anim": "blur"}),
               ("cm", "tag w", "TELL ME IN THE COMMENTS", 760, 560, (199, "comments")),
               ("sw", "tag", "…AND STAY WARM", 820, 660, (200, "warm"), {"anim": "fade"})]),
    # ------------------------------------------------------------------ DAY 20
    dict(at=201, kind="chapter"),
    dict(at=202, bg=("whiteout", {"figures": 3}), snow="whiteout", cam=("in", 1.06),
         svg=[("o1", ORB(400, 600, 26), (202, "lights")), ("o2", ORB(960, 560, 30), (202, "lights")), ("o3", ORB(1500, 620, 24), (202, "carrying"))],
         html=[("cl", "tag r", "THEY CARRY LIGHTS", 760, 200, (202, "lights"))]),
    dict(at=203, bg=("living_winter", {"fire": True, "blankets": True, "lit": False}), cam=("in", 1.08),
         svg=[("rd", RADIO(1150, 760, 1.1)), ("wv", WAVES(1150, 680, "#ffd43b", 1.0), (203, "radio", "fade"))],
         html=[("dv", "tag g", "DAD'S VOICE — REALLY HIS", 700, 260, (204, "voice")), ("yn", "tag y", "YOUR NAME", 760, 340, (205, "Yours")),
               ("sf", "stamp g", "SAFE. WAITING.", 680, 440, (206, "Safe"))],
         acts=[("ring", "wv", (204, "reading"), 3.0)]),
    dict(at=209, kind="rule", n="13", imp="NEVER FOLLOW A LIGHT IN THE WHITEOUT"),
    dict(at=211, bg=("whiteout", {"figures": 0}), snow="whiteout", cam=("in", 1.06),
         svg=[("orb", ORB(1300, 600, 34)), ("you", ch("@you", "you", 500, 920, 1.3, mood="worried"))],
         html=[("ud", "tag", "CAN'T TELL UP FROM DOWN", 300, 200, (211, "down")), ("ts", "tag r", "LOST 10 STEPS FROM THE DOOR", 300, 270, (212, "ten")),
               ("fr", "tag g", "FEELS LIKE RESCUE", 1180, 360, (213, "rescue")), ("af", "stamp", "ALWAYS FARTHER AWAY", 1000, 760, (216, "farther"))],
         acts=[("move", "orb", 200, -30, (214, "moves"), 1.5), ("move", "orb", 380, -40, (216, "always"), 1.5)]),
    dict(at=217, bg=("porch", {"open_": True}), snow="whiteout", snow_clip=(664, 184, 552, 676), cam=("in", 1.06),
         svg=[("rp", ROPE(1260, 520, 1700, 900), (217, "rope"))],
         html=[("tr", "tag g", "TIE A ROPE TO THE DOOR", 300, 300, (217, "tie")), ("nl", "tag", "NEVER LET GO", 300, 370, (217, "never"))]),
    dict(at=218, bg=("whiteout", {"figures": 0}), snow="whiteout", cam=("in", 1.08),
         svg=[("orb", ORB(1300, 600, 34)), ("dog", _icon("dog", 800, 830, 1.6, "#5a4636"))],
         html=[("br", "tag y", "BEAR", 760, 660, (218, "Bear")), ("cl", "tag r", "HIS COLLAR… ON THE SCHOOL ROOF", 700, 220, (219, "collar"))],
         acts=[("move", "dog", 520, -60, (218, "followed"), 2.5, "power1.in"), ("fade", "dog", (218, "twenty"), 0, 1.0)]),
    dict(at=221, kind="rule", n="14", imp="NEVER ANSWER A VOICE FROM THE ROOF"),
    dict(at=222, bg="ceiling", cam=("in", 1.1, "50% 25%"),
         html=[("ss", "tag", "SLOW STEPS", 800, 360, (224, "steps")), ("om", "tag r", "RIGHT OVER YOUR MATTRESS", 720, 430, (225, "mattress")),
               ("wh", "bubble", "kiddo… let me in…", 820, 120, (225, "whispers")), ("dv", "stamp", "DAD'S VOICE", 760, 560, (226, "voice"))],
         acts=[("dark", ("+", 0), 0.45, 0.01), ("shake", (224, "Slow"), 3)]),
    dict(at=227, bg=("living_winter", {"fire": False, "blankets": True, "lit": False}), cam=("in", 1.1),
         svg=[("you", ch("@you", "you", 860, 880, 1.4, mood="scared", arms=(-60, -30))), ("maya", ch("@maya", "maya", 1000, 880, 0.95, mood="scared"))],
         html=[("fm", "tag y", "DAD: 40 MILES AWAY", 300, 200, (227, "forty")), ("ho", "tag", "HANDS OVER HER EARS", 1100, 420, (229, "hands"))],
         acts=[("dark", ("+", 0), 0.35, 0.01)]),
    dict(at=231, kind="rule", n="15", imp="HANG SOMETHING BRIGHT ON THE DOOR"),
    dict(at=232, bg="stage", cam=("in", 1.05),
         svg=[("t", panel(560, 470, 280, 260, '<rect x="-80" y="-60" width="160" height="120" rx="8" fill="#ef3b4f"/><rect x="-80" y="30" width="160" height="10" fill="#fff" opacity="0.4"/>', "#2a2c3c"), (233, "towel")),
              ("v", panel(960, 470, 280, 260, '<path d="M-60,-70 L-20,-70 L0,-40 L20,-70 L60,-70 L60,70 L-60,70 Z" fill="#ff8a2a"/><rect x="-60" y="0" width="120" height="14" fill="#f4f1ea"/>', "#2a2c3c"), (234, "vest")),
              ("n", panel(1360, 470, 280, 260, '<rect x="-60" y="-60" width="120" height="120" rx="10" fill="#eef3fa"/>', "#2a2c3c"), (235, "snow")),
              ("xn", X(1360, 470, 0.7), (235, "snow"))],
         html=[("rs", "tag g", "SO RESCUERS CAN FIND YOU", 760, 200, (232, "rescuers")), ("lt", "tag", "RED TOWEL", 480, 650, (233, "towel")),
               ("lv", "tag", "ORANGE VEST", 870, 650, (234, "vest")), ("ln", "tag r", "NOT WHITE", 1300, 650, (235, "snow"))]),
    dict(at=236, bg=("porch", {"open_": False}), cam=("in", 1.1, "50% 60%"),
         svg=[("s1", SLED(1080, 640, 1.0)), ("s2", SLED(800, 660, 1.0, "#c9283a"), (237, "second"))],
         html=[("ms", "tag y", "MAYA'S RED SLED", 1100, 460, (236, "sled")), ("om", "tag", "BY MORNING", 300, 300, (237, "morning")),
               ("no", "stamp", "YOU DON'T OWN A SECOND ONE", 420, 820, (238, "own"))],
         acts=[("dark", (238, "own"), 0.3, 0.6)]),
    # ------------------------------------------------------------------ DAY 30
    dict(at=239, kind="chapter"),
    dict(at=240, bg=("living_winter", {"fire": True, "blankets": True, "lit": False}), cam=("in", 1.06),
         svg=[("maya", ch("@maya", "maya", 1130, 880, 0.95, mood="sad")), ("you", ch("@you", "you", 860, 880, 1.4, mood="sad"))],
         html=[("fl", "tag r", "FOOD: LOW", 300, 200, (240, "food")), ("bn", "tag", "BURNED: COFFEE TABLE · 2 CHAIRS · BOOKSHELF", 300, 270, (241, "burned")),
               ("ms", "tag", "MAYA STOPPED ASKING", 1080, 480, (242, "stopped"))]),
    dict(at=243, bg=("porch", {"open_": False}), cam=("in", 1.1),
         html=[("kk", "big", "KNOCK. KNOCK.", 560, 380, (243, "knocks"), {"anim": "slam"})],
         acts=[("shake", (243, "knocks"), 9), ("dark", ("+", 0), 0.3, 0.01)]),
    dict(at=245, kind="rule", n="16", imp="NO SNOW ON THEIR SHOULDERS? DON'T OPEN"),
    dict(at=247, bg=("porch", {"open_": True}), snow="heavy", snow_clip=(664, 184, 552, 676), cam=("in", 1.08, "50% 45%"),
         svg=[("dad", ch("@dad", "dad", 940, 860, 1.5, mood="creepy"))],
         html=[("gp", "tag", "THROUGH THE CURTAIN", 300, 200, (247, "curtain")), ("dd", "tag y", "DAD", 1080, 280, (248, "Dad")),
               ("hc", "tag", "HOSPITAL COAT · GLASSES", 1080, 350, (249, "coat")), ("fm", "tag r", "WALKED 40 MILES?", 1080, 420, (252, "forty")),
               ("ns", "stamp", "NOT A SINGLE FLAKE ON HIM", 360, 620, (253, "flake"))],
         acts=[("noblink", "@dad")]),
    dict(at=254, bg=("porch", {"open_": True}), snow="heavy", snow_clip=(664, 184, 552, 676), cam=("in", 1.25, "50% 30%"),
         svg=[("dad", ch("@dad", "dad", 940, 860, 1.5, mood="creepy", arms=(10, -100)))],
         html=[("ou", "bubble", "OPEN UP, KIDDO. IT'S COLD OUT HERE.", 1080, 220, (255, "open")),
               ("sv", "tag r", "NOT SHIVERING", 1080, 330, (256, "shivering")), ("br", "tag r", "NO BREATH", 1080, 400, (257, "breath"))],
         acts=[("noblink", "@dad"), ("talk", "@dad", (255, "says"), 10), ("shake", (254, "knocks"), 6)]),
    dict(at=258, bg=("living_winter", {"fire": False, "blankets": True, "lit": False}), cam=("in", 1.08),
         svg=[("you", ch("@you", "you", 860, 880, 1.4, mood="scared", arms=(-60, -30))), ("maya", ch("@maya", "maya", 1060, 880, 0.95, mood="sad"))],
         html=[("cc", "tag", "CLOSE THE CURTAIN", 300, 200, (258, "curtain")), ("bd", "tag", "BACK AGAINST THE DOOR", 300, 270, (259, "back")),
               ("ws", "tag g", "WAIT", 300, 340, (260, "wait")), ("ht", "tag r", "HOLD HER TIGHT", 1100, 420, (262, "tight"))],
         acts=[("dark", ("+", 0), 0.35, 0.01), ("move", "maya", 160, 0, (261, "walking"), 0.8), ("move", "maya", 0, 0, (262, "hold"), 0.4)]),
    dict(at=263, bg=("town_snow", {"night": False, "buried": 0.5}), snow="light", cam=("in", 1.08, "40% 70%"),
         svg=[("st", STEPS(760, 840, 1700, 1000, 11), (264, "Leading", "fade"))],
         html=[("la", "tag", "LEADING AWAY", 1100, 640, (264, "away")), ("ft", "stamp", "FOR THE FIRST TIME", 560, 300, (265, "first"))]),
    dict(at=267, kind="rule", n="17", imp="EAT BEFORE YOU'RE HUNGRY"),
    dict(at=268, bg="stage", cam=("in", 1.05),
         svg=[("p", _icon("person", 760, 500, 3.0, "#c9cad1")), ("fl", FLAME(760, 500, 1.4), (269, "heat"))],
         html=[("fh", "tag y", "FOOD = HEAT", 960, 300, (269, "burns")), ("sk", "tag r", "SKIPPING MEALS = COLDER", 960, 370, (270, "Skipping")),
               ("sm", "tag g", "SMALL MEALS", 960, 460, (271, "Small")), ("of", "tag g", "OFTEN", 960, 530, (272, "Often")),
               ("hd", "tag g", "HOT DRINKS", 960, 600, (273, "Hot"))]),
    dict(at=274, bg=("living_winter", {"fire": True, "blankets": True, "lit": False}), cam=("in", 1.1),
         svg=[("you", ch("@you", "you", 860, 880, 1.4, mood="sad")), ("maya", ch("@maya", "maya", 1130, 880, 0.95, mood="happy")),
              ("can", CAN(1000, 760, 1.2), (274, "soup"))],
         html=[("ls", "tag", "THE LAST CAN OF SOUP", 300, 200, (274, "last")), ("bh", "tag g", "SHE GETS THE BIGGER HALF", 1100, 460, (274, "bigger"))]),
    dict(at=276, kind="rule", n="18", imp="NEVER BURN THE CARD"),
    dict(at=278, bg="kitchen_winter", cam=("in", 1.25, "18% 40%"),
         html=[("nl", "tag r", "NOTHING LEFT TO BURN", 600, 200, (278, "nothing")), ("tc", "tag y", "THE CARD", 420, 600, (279, "card")),
               ("hw", "tag g", "YOUR HOMEWORK INSTEAD", 600, 280, (280, "homework")), ("en", "tag", "EVERY NOTEBOOK SINCE 2ND GRADE", 600, 350, (281, "notebook"))]),
    dict(at=282, bg=("town_snow", {"night": True, "buried": 0.55, "lit": (False, False, True, False)}), snow="light", cam=("in", 1.1, "30% 65%"),
         svg=[("st", STEPS(1300, 1000, 330, 820, 9), (284, "footprints", "fade"))],
         html=[("bh", "tag r", "SHE BURNED HERS", 300, 200, (282, "burned")), ("dk", "tag", "DAY 30: DARK", 300, 270, (283, "dark")),
               ("sf", "tag", "DAY 31: A SECOND SET OF FOOTPRINTS", 300, 340, (284, "second")), ("oi", "stamp", "ONLY GOING IN", 760, 500, (285, "Only"))],
         acts=[("dark", (285, "going"), 0.35, 0.8)]),
    # ------------------------------------------------------------------ DAY 40
    dict(at=286, kind="chapter"),
    dict(at=287, bg="spring", cam=("out", 1.1),
         html=[("dp", "tag", "DRIPPING", 300, 200, (288, "Dripping")), ("ss", "tag g", "THE SNOW HAS STOPPED", 300, 270, (289, "stopped")),
               ("bs", "tag", "BLUE SKY", 300, 340, (290, "blue")), ("br", "tag y", "SO BRIGHT IT HURTS", 300, 410, (291, "hurts"))]),
    dict(at=293, kind="rule", n="19", imp="WAIT FOR THE BIRDS"),
    dict(at=295, bg="spring", cam=("in", 1.06),
         svg=[(f"n{k}", ch(f"@n{k}", w, 260 + k * 330, 900, 1.05, mood="creepy", arms=(10, -150))) for k, w in enumerate(["pratt", "walker", "kowalski", "walker2", "walker"])]
             + [("dog", _icon("dog", 1720, 860, 1.4, "#5a4636"))],
         html=[("fq", "tag", "FEELS LIKE THE END", 300, 160, (295, "end")), ("al", "tag y", "ALL OF THEM", 800, 220, (297, "All")),
               ("ep", "tag", "EVEN THE PRATTS", 120, 320, (298, "Pratts")), ("ek", "tag", "EVEN MRS. KOWALSKI", 840, 320, (299, "Kowalski")),
               ("eb", "tag", "EVEN BEAR", 1600, 620, (300, "Bear")), ("nc", "stamp", "NO COATS", 760, 440, (301, "coats"))],
         acts=[("noblink", f"@n{k}") for k in range(5)]),
    dict(at=302, bg="spring", cam=("in", 1.04),
         svg=[(f"n{k}", ch(f"@n{k}", w, 260 + k * 330, 900, 1.05, mood="creepy", arms=(10, -150))) for k, w in enumerate(["pratt", "walker", "kowalski", "walker2", "walker"])],
         html=[("nb", "stamp", "NO BIRDS", 760, 260, (302, "birds")), ("ks", "tag g", "KEEP THE DOOR SHUT", 760, 400, (303, "shut")),
               ("wt", "tag", "WAIT", 900, 470, (304, "wait"))],
         acts=[("noblink", f"@n{k}") for k in range(5)]),
    dict(at=305, bg="spring", cam=("in", 1.08),
         svg=[("wire", '<path d="M0,300 Q960,360 1920,300" stroke="#2a2f3a" stroke-width="6" fill="none"/>'), ("crow", CROW(960, 316, 1.6), (305, "crow"))],
         html=[("nn", "clock", "12:00", 160, 160, (305, "noon")), ("cw", "tag y", "A CROW", 1060, 200, (305, "crow")),
               ("em", "tag", "THE STREET IS EMPTY", 760, 520, (306, "empty")), ("np", "tag", "NO PEOPLE · NO FOOTPRINTS", 720, 590, (308, "footprints")),
               ("js", "tag w", "JUST SNOW", 860, 660, (309, "snow"))],
         acts=[("flash", (305, "screams")), ("shake", (305, "screams"), 6)]),
    dict(at=310, bg=("town_snow", {"night": False, "buried": 0.4, "lit": (False, False, False, False)}), cam=("in", 1.15, "30% 70%"),
         html=[("kd", "tag", "MRS. KOWALSKI'S HOUSE: DARK", 300, 200, (310, "dark")), ("do", "stamp", "FRONT DOOR OPEN", 300, 300, (311, "open"))]),
    dict(at=313, bg="spring", cam=("in", 1.06),
         svg=[("heli", HELI(1400, 220, 1.2), (314, "helicopter")),
              ("dad", ch("@dad", "dad", 900, 900, 1.45, mood="sad", arms=(10, -140))), ("sc", SNOWCOAT(900, 900, 1.45))],
         html=[("pl", "tag", "THE PLOWS", 300, 200, (313, "plows")), ("hl", "tag", "A HELICOPTER", 1300, 360, (314, "helicopter")),
               ("cs", "tag g", "DAD — COVERED IN SNOW", 1060, 460, (315, "covered")), ("cr", "tag", "CRYING", 1060, 530, (315, "crying"))],
         acts=[("move", "heli", -300, 40, (314, "helicopter"), 4.0, "none")]),
    dict(at=316, bg="shed", cam=("in", 1.1, "50% 45%"),
         html=[("sh", "tag", "THE SHED", 300, 200, (316, "shed")), ("bx", "tag y", "A BOX", 760, 300, (317, "box")),
               ("hu", "tag", "HUNDREDS OF CARDS", 760, 680, (319, "Hundreds")), ("bl", "tag w", "BLANK", 860, 750, (320, "Blank")),
               ("mk", "tag", "A BLACK MARKER", 1160, 460, (321, "marker")), ("hf", "tag r", "HALF USED", 1160, 530, (322, "Half"))]),
    dict(at=323, bg="stage", cam=("in", 1.12),
         svg=[("cd", CARD(960, 470, 3.0, -2, hand=True))],
         html=[("lk", "tag", "LOOK CLOSELY", 380, 240, (323, "closely")), ("iy", "stamp", "IT'S YOURS", 1150, 640, (324, "yours"))],
         acts=[("shake", (324, "yours"), 8), ("dark", (324, "yours"), 0.25, 0.6)]),
    dict(at=325, kind="rule", n="20", imp="WRITE THE RULES FOR WHOEVER COMES NEXT", last=True),
    # ------------------------------------------------------------------ FINALE
    dict(at=328, bg=("town_snow", {"night": True, "buried": 0.3}), snow="light", cam=("in", 1.06),
         svg=[("c1", CARD(420, 600, 0.6, -6), (329, "door")), ("c2", CARD(960, 620, 0.6, 3), (329, "somewhere")), ("c3", CARD(1500, 600, 0.6, -2), (329, "shows"))],
         html=[("ew", "tag", "EVERY WINTER", 300, 200, (329, "winter")), ("sw", "tag y", "SOMEBODY HAS TO WRITE IT", 700, 300, (330, "write"))]),
    dict(at=331, bg="stage", cam=("in", 1.05),
         svg=[("dots", DOTS(20, 300, "#3fbf7f"), (331, "Twenty"))],
         html=[("fr", "tag g", "COULD SAVE YOUR LIFE · FOR REAL", 700, 400, (332, "save")),
               ("a", "tag w", "FILL THE BATHTUB", 820, 500, (333, "bathtub")), ("b", "tag w", "CLEAR THE VENTS", 830, 570, (334, "vents")),
               ("c", "tag w", "NEVER BURN ANYTHING INDOORS", 740, 640, (335, "burn")), ("d", "tag", "THE REST… HOPE YOU NEVER NEED", 720, 740, (336, "rest"))]),
    dict(at=337, bg=("porch", {"open_": True}), snow="heavy", snow_clip=(664, 184, 552, 676), cam=("in", 1.1, "50% 45%"),
         svg=[("fg", ch("@fg", "walker", 940, 860, 1.5, mood="creepy"))],
         html=[("ns", "tag r", "NO SNOW ON HIS SHOULDERS", 1080, 300, (337, "shoulders")), ("kn", "tag g", "YOU KNOW WHAT TO DO", 1080, 370, (337, "know"))],
         acts=[("noblink", "@fg")]),
    dict(at=338, bg="stage", snow="light", cam=("in", 1.04),
         svg=[("cur", CURSOR(1400, 1000), ("+", 0.2, "fade"))],
         html=[("wm", "wm", "THE RULE STORIES", 0, 150, ("+", 0.15), {"anim": "blur"}),
               ("q", "big", "WHAT IS RULE 21?", 370, 240, (338, "twenty")),
               ("cm", "tag w", "TELL ME IN THE COMMENTS", 730, 450, (339, "comments")),
               ("sub", "sticker", "SUBSCRIBE", 750, 560, ("+", 0.6), {"anim": "pop", "rot": 0}),
               ("subd", "sticker done", "SUBSCRIBED ✓", 615, 560, ("+", 2.25), {"anim": "fade", "rot": 0}),
               ("rd", "tag y", "I'LL BE READING THEM", 760, 760, (340, "reading"))],
         acts=[("move", "cur", -420, -360, ("+", 1.4), 0.7, "power3.inOut"),
               ("js", 'tl.to("$sub",{scale:0.9,duration:0.08,yoyo:true,repeat:1},%T%);tl.to("$sub",{opacity:0,duration:0.1},%T%+0.12);', ("+", 2.15))]),
]
_ats = [d["at"] for d in SHOTS]
assert _ats == sorted(_ats) and len(_ats) == len(set(_ats)), "shots out of order / duplicated"

SFX = [
    (1, "knocks", "knock", 0.9, None), (2, "open", "impact2", 0.8, None), (2, "door", "whoosh", 0.4, None),
    (10, "morning", "whoosh", 0.3, None), (12, "radio", "static", 0.3, 1.5), (15, "forty", "impact2", 0.7, None),
    (21, "card", "stamp", 0.5, None), (33, "last", "heartbeat", 0.4, None), (39, "water", "click", 0.3, None),
    (66, "tired", "heartbeat", 0.4, None), (72, "power", "switch", 0.7, None), (84, "dog", "dogs", 0.35, 2.0),
    (88, "standing", "riser", 0.35, None), (110, "isn't", "impact1", 0.55, None), (118, "coats", "heartbeat", 0.4, None),
    (131, "back", "heartbeat", 0.5, None), (144, "facing", "impact1", 0.6, None), (152, "three", "impact2", 0.7, None),
    (158, "cracks", "click", 0.5, None), (159, "groans", "static", 0.25, 1.5), (170, "gunshot", "impact1", 0.9, None),
    (214, "moves", "riser", 0.3, None), (224, "steps", "stamp", 0.3, None), (225, "whispers", "laugh", 0.25, 2.5),
    (238, "own", "heartbeat", 0.55, None), (243, "knocks", "stamp", 0.8, None), (254, "knocks", "stamp", 0.8, None),
    (253, "flake", "impact2", 0.5, None), (285, "Only", "impact1", 0.55, None), (305, "screams", "impact2", 0.6, None),
    (314, "helicopter", "engine", 0.4, 3.5), (324, "yours", "impact1", 0.7, None), (338, "+2.15", "click", 0.7, None),
]
MUSIC_DIPS = [(152, "three", 0.0, 1.2), (170, "gunshot", 0.0, 1.2), (253, "flake", 0.15, 1.5), (302, "birds", 0.1, 2.0),
              (324, "yours", 0.0, 1.6)]
MUSIC_ORDER = ["music_a", "music_b", "music_a", "music_c"]

CAPTION_SCRIM = True
