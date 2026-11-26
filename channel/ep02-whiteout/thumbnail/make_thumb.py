"""Thumbnail 1280x720: night blizzard, open door, a clean figure with no snow on him. NO SNOW ON HIS SHOULDERS / DON'T OPEN."""
import random
import sys

sys.path.insert(0, "/home/user/hyperframes/channel/tools")
sys.path.insert(0, "/home/user/hyperframes/channel/ep02-whiteout")
import shots  # noqa: E402,F401  (applies the EP02 cast)
from art import svg_filters  # noqa: E402
from art2 import character  # noqa: E402

rnd = random.Random(7)
walker = character("w", "walker", 0, 0, 1.0, mood="creepy", arms=(6, -6))
you = character("y", "you", 0, 0, 1.0, mood="scared", arms=(10, -10))
pts = [(rnd.uniform(0, 1280), rnd.uniform(0, 720), rnd.choice([2, 3, 3, 4, 5, 7]), rnd.uniform(.35, .95)) for _ in range(320)]
flakes = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{o:.2f}"/>'
                 for x, y, r, o in pts if not (770 < x < 1080 and 130 < y < 700))
# keep the doorway figure clean: no flakes drawn over him
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Montserrat;src:url('montserrat-900.woff2') format('woff2');font-weight:100 900}}
body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#06080f;font-family:Montserrat,sans-serif}}
.t{{position:absolute;font-weight:900;letter-spacing:-.01em;line-height:.9;color:#fff;text-shadow:0 8px 0 rgba(0,0,0,.55),0 0 36px rgba(0,0,0,.7)}}
</style></head><body>
<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;inset:0"><defs>{svg_filters()}
<radialGradient id="bg" cx="70%" cy="45%" r="75%"><stop offset="0" stop-color="#22355e"/><stop offset="1" stop-color="#04060c"/></radialGradient>
<radialGradient id="porch" cx="50%" cy="0%" r="90%"><stop offset="0" stop-color="#ffd98a" stop-opacity=".95"/><stop offset=".6" stop-color="#e9a54a" stop-opacity=".55"/><stop offset="1" stop-color="#7a4a1e" stop-opacity=".2"/></radialGradient>
<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffd98a" stop-opacity=".55"/><stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>
<clipPath id="door"><rect x="760" y="120" width="330" height="560"/></clipPath></defs>
<rect width="1280" height="720" fill="url(#bg)"/>
<!-- house wall + siding -->
<rect x="640" y="60" width="640" height="660" fill="#2a2f45"/>
{''.join(f'<rect x="640" y="{60+k*34}" width="640" height="3" fill="#1d2134"/>' for k in range(20))}
<!-- open doorway, warm porch light -->
<rect x="740" y="100" width="370" height="600" fill="#3b2a20"/>
<rect x="760" y="120" width="330" height="580" fill="url(#porch)"/>
<g clip-path="url(#door)"><g transform="translate(925 790) scale(1.7)">{walker}</g></g>
<!-- door leaf swung open -->
<path d="M1090,120 L1210,90 L1210,730 L1090,700 Z" fill="#5a3a26"/><circle cx="1110" cy="420" r="9" fill="#e7c36a"/>
<!-- porch lamp -->
<circle cx="925" cy="70" r="120" fill="url(#halo)"/><rect x="905" y="52" width="40" height="40" rx="8" fill="#ffe7a6"/>
<!-- snow piled on the frame and ground -->
<path d="M730,104 Q790,80 850,100 Q925,78 1000,98 Q1060,80 1120,102 L1120,112 L730,112 Z" fill="#eef3fa"/>
<path d="M0,720 L0,640 Q160,600 330,640 Q500,680 640,650 L640,720 Z" fill="#dfe7f2"/>
<!-- the hero's face at the bottom-left, scared -->
<g transform="translate(250 1430) scale(3.4)">{you}</g>
<!-- blizzard everywhere except inside the doorway -->
<g>{flakes}</g>
<rect x="760" y="120" width="330" height="580" fill="url(#porch)" opacity=".0"/>
</svg>
<div class="t" style="left:34px;top:26px;font-size:92px">NO SNOW<br>ON HIS<br><span style="color:#7fd0ff">SHOULDERS</span></div>
<div style="position:absolute;left:770px;top:590px;white-space:nowrap;transform:rotate(-4deg);background:#ef3b4f;color:#fff;font:900 70px Montserrat;padding:6px 24px;border-radius:8px;box-shadow:0 10px 0 rgba(0,0,0,.45)">DON'T OPEN</div>
</body></html>"""
open(sys.argv[1], "w").write(html)
