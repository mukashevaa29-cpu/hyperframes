"""Channel avatar (800x800) and YouTube banner (2560x1440, safe area 1546x423) in the house style.

usage: python3 kit/branding.py  -> branding/avatar.png, branding/banner.png (+ preview crops)
"""
import math, os, random, re, sys

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
from lib import N, glow, line, mascot, DARK, RED, CORE  # noqa

OUT = os.path.join(KIT, "..", "branding")
os.makedirs(OUT, exist_ok=True)
tpl = open(f"{KIT}/template.html").read()
DEFS = re.search(r"<defs>.*?</defs>", tpl, re.S).group(0)
FONTS = f"""
@font-face {{ font-family: "RC"; font-weight: 700; src: url("file://{KIT}/fonts/roboto-condensed-latin-700-normal.woff2"); }}
@font-face {{ font-family: "RC"; font-weight: 900; src: url("file://{KIT}/fonts/roboto-condensed-latin-900-normal.woff2"); }}
"""


def flames(cx, base, w, h, n=9, seed=3):
    r = random.Random(seed)
    out = ""
    for layer, (col, op, k) in enumerate([("#FF2A3A", 0.75, 1.0), ("#FF6A3D", 0.9, 0.72), ("#FFE6C8", 1.0, 0.42)]):
        for i in range(n):
            x = cx + (i / (n - 1) - 0.5) * w * 0.9
            hh = h * k * (0.55 + 0.45 * r.random()) * (1 - abs(i / (n - 1) - 0.5) * 0.9)
            wd = w / n * 1.9 * k + 10
            sway = (r.random() - 0.5) * wd * 0.6
            out += (f'<path d="M {x - wd / 2:.0f} {base} Q {x - wd * 0.65:.0f} {base - hh * 0.55:.0f} {x + sway:.0f} {base - hh:.0f} '
                    f'Q {x + wd * 0.65:.0f} {base - hh * 0.55:.0f} {x + wd / 2:.0f} {base} Z" fill="{col}" opacity="{op}"/>')
    return f'<g style="mix-blend-mode:screen" filter="url(#glowO)">{out}</g>'


def embers(w, h, n, seed=7, y0=0.35):
    r = random.Random(seed)
    s = ""
    for _ in range(n):
        x, y, rad = r.uniform(0, w), r.uniform(h * y0, h), r.uniform(2, 6)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad * 3:.1f}" fill="#FF5A2A" opacity="0.25"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}" fill="#FFB070" opacity="{r.uniform(0.5, 1):.2f}"/>'
    return s


def page(w, h, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;background:#010101}}
.t{{position:absolute;font-family:RC;font-weight:900;color:#F5F5F5;letter-spacing:4px;white-space:nowrap;text-shadow:0 4px 24px rgba(0,0,0,.9)}}
.r{{color:#F54341;text-shadow:0 0 14px rgba(255,50,60,.9),0 0 46px rgba(255,20,40,.6)}}
.s{{position:absolute;font-family:RC;font-weight:700;color:#BDB5B5;letter-spacing:10px;white-space:nowrap}}
</style></head><body>{body}</body></html>"""


# ---------------------------------------------------------------- avatar: the x-ray "you", screaming, in the fire
av_svg = (f'<svg width="800" height="800" viewBox="0 0 800 800" style="position:absolute;left:0;top:0"><defs>'
          f'<radialGradient id="fl" cx="50%" cy="100%" r="75%"><stop offset="0" stop-color="#c41c06"/><stop offset="0.45" stop-color="#5a0c03"/><stop offset="1" stop-color="#010101"/></radialGradient>'
          f'</defs>{DEFS}<rect width="800" height="800" fill="url(#fl)"/>'
          + embers(800, 800, 40, 3, 0.2)
          + mascot("av", 400, 1360, 1.55, pose=dict(uarmL=150, farmL=30, uarmR=-150, farmR=-30, head=-6), mouth_open=True)
          + flames(400, 820, 900, 330, 11, 5)
          + '<circle cx="400" cy="400" r="392" fill="none" stroke="#FB2945" stroke-width="10" opacity="0.85" filter="url(#glow)"/>'
          + '</svg>')
open(f"{OUT}/avatar.html", "w").write(page(800, 800, av_svg))

# ---------------------------------------------------------------- banner
W, H = 2560, 1440
icons = ""
# faint neon pictograms of past/future episodes around the safe area (decoration, visible on TV/desktop only)
bull = ("M 40 150 C 30 80 110 40 220 46 C 340 52 470 30 600 26 C 690 22 740 50 760 110 C 780 180 760 260 700 290 C 640 320 520 330 400 326 C 280 330 150 322 100 280 C 60 250 46 200 40 150 Z "
        "M 700 40 C 760 20 830 40 860 90 C 885 130 890 180 884 214 C 878 246 852 258 826 250 C 800 242 790 236 770 250 C 740 230 715 160 700 40 Z")
icons += f'<g transform="translate(130,780) scale(0.42)" opacity="0.55">' + glow(N(bull)) + '</g>'
chair = "M 400 780 L 680 780 L 680 1255 L 400 1255 Z M 350 1250 L 730 1250 L 730 1300 L 350 1300 Z M 372 1300 L 404 1300 L 404 1540 L 372 1540 Z M 676 1300 L 708 1300 L 708 1540 L 676 1540 Z M 270 1145 L 415 1145 L 415 1178 L 270 1178 Z M 665 1145 L 810 1145 L 810 1178 L 665 1178 Z"
icons += f'<g transform="translate(2120,300) scale(0.42)" opacity="0.55">' + glow(N(chair, fill="#46302c")) + '</g>'
guill = "M 0 0 L 40 0 L 40 900 L 0 900 Z M 360 0 L 400 0 L 400 900 L 360 900 Z M -30 -40 L 430 -40 L 430 0 L -30 0 Z M 40 180 L 360 120 L 360 260 L 40 260 Z M 60 640 L 340 640 L 340 700 L 60 700 Z"
icons += f'<g transform="translate(2390,560) scale(0.42)" opacity="0.5">' + glow(N(guill)) + '</g>'
mush = '<g transform="translate(150,330) scale(0.55)" opacity="0.5" filter="url(#glowO)">' + "".join(
    f'<circle cx="{200 + dx}" cy="{120 + dy}" r="{rr}" fill="#801F0C"/>' for dx, dy, rr in [(-120, 0, 90), (0, -30, 110), (120, 0, 90), (0, 60, 70), (0, 150, 50), (0, 230, 45), (0, 310, 45)]) + '</g>'
icons += mush
ban_svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0"><defs>'
           f'<radialGradient id="bfl" cx="50%" cy="100%" r="70%"><stop offset="0" stop-color="#b01804"/><stop offset="0.4" stop-color="#4a0901"/><stop offset="1" stop-color="#010101"/></radialGradient>'
           f'</defs>{DEFS}<rect width="{W}" height="{H}" fill="url(#bfl)"/>' + embers(W, H, 140, 11, 0.3) + icons
           # the mascot inside the safe area (x 507..2053, y 508..931), left of the title, flames at its feet
           + mascot("bn", 690, 925, 0.56, pose=dict(uarmL=150, farmL=30, uarmR=-150, farmR=-30, head=-6), mouth_open=True)
           + flames(690, 925, 330, 130, 9, 8)
           + glow(N(f"M 880 822 L 2010 822", sw=9, cw=4))
           + '</svg>')
ban_html = (ban_svg
            + '<div class="t" style="left:862px;top:634px;font-size:134px;line-height:134px">HOW DOES IT <span class="r">FEEL?</span></div>'
            + '<div class="s" style="left:868px;top:846px;font-size:38px">DARK HISTORY · SECOND BY SECOND</div>')
open(f"{OUT}/banner.html", "w").write(page(W, H, ban_html))

# ---------------------------------------------------------------- render with the preinstalled Playwright Chromium
js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  for (const [name, w, h] of [['avatar', 800, 800], ['banner', {W}, {H}]]) {{
    const p = await b.newPage({{ viewport: {{ width: w, height: h }}, deviceScaleFactor: 1 }});
    await p.goto('file://{OUT}/' + name + '.html');
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({{ path: '{OUT}/' + name + '.png' }});
  }}
  await b.close();
}})();
"""
open(f"{OUT}/render.cjs", "w").write(js)
os.system(f"cd {OUT} && node render.cjs")
print("rendered", os.listdir(OUT))
