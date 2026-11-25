"""Thumbnail 1280x720: face lit by the phone, caller ID = your own number, 3:00 AM, DON'T ANSWER."""
import sys
sys.path.insert(0, "/home/user/hyperframes/channel/tools")
from art import character, svg_filters, phone, glow, moon, stars  # noqa: E402

face = character("t", "you", 0, 0, 1.0, mood="scared", arms=(10, -10))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Montserrat;src:url('montserrat-900.woff2') format('woff2');font-weight:100 900}}
body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#06080f;font-family:Montserrat,'Archivo Black',sans-serif}}
.t{{position:absolute;font-weight:900;letter-spacing:-.01em;line-height:.92}}
</style></head><body>
<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;inset:0"><defs>{svg_filters()}
<radialGradient id="bg" cx="38%" cy="55%" r="70%"><stop offset="0" stop-color="#1b2a52"/><stop offset="1" stop-color="#05070d"/></radialGradient>
<radialGradient id="lit" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#9fe0ff" stop-opacity=".32"/><stop offset="1" stop-color="#9fe0ff" stop-opacity="0"/></radialGradient></defs>
<rect width="1280" height="720" fill="url(#bg)"/>{stars(40,0,0,1280,300,seed=3,op=.5)}
<!-- huge face, lit from below by the phone -->
<g transform="translate(300 1390) scale(3.6)">{face}</g>
<ellipse cx="330" cy="520" rx="330" ry="260" fill="url(#lit)"/>
<!-- phone -->
<g transform="translate(860 360) rotate(8)">
 <rect x="-170" y="-330" width="340" height="660" rx="44" fill="#121419"/>
 <rect x="-156" y="-316" width="312" height="632" rx="34" fill="#0f1a33"/>
 <text x="0" y="-215" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="26" fill="#9fb3d9">incoming call</text>
 <text x="0" y="-150" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="46" fill="#fff">YOUR NUMBER</text>
 <text x="0" y="-105" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="28" fill="#cfd8ee">+1 ••• ••• ••42</text>
 <circle cx="-78" cy="220" r="46" fill="#ef3b4f"/><rect x="-100" y="214" width="44" height="12" rx="6" fill="#fff"/>
 <circle cx="78" cy="220" r="46" fill="#3fbf7f"/>
 <g transform="translate(78 220)"><rect x="-56" y="-10" width="112" height="20" rx="8" fill="#ef3b4f" transform="rotate(45)"/><rect x="-56" y="-10" width="112" height="20" rx="8" fill="#ef3b4f" transform="rotate(-45)"/></g>
</g>
<g fill="none" stroke="#ffd43b" stroke-width="10" stroke-linecap="round" transform="translate(860 360)">
 <path d="M-230,-60 Q-262,0 -230,60"/><path d="M-272,-96 Q-318,0 -272,96"/><path d="M240,-60 Q272,0 240,60"/><path d="M282,-96 Q328,0 282,96"/></g>
</svg>
<div class="t" style="left:40px;top:28px;font-size:150px;color:#ffd43b;text-shadow:0 10px 0 rgba(0,0,0,.5),0 0 40px rgba(0,0,0,.6)">3:00 AM</div>
<div style="position:absolute;left:46px;top:196px;transform:rotate(-4deg);background:#ef3b4f;color:#fff;font:900 64px Montserrat;padding:6px 22px;border-radius:8px;box-shadow:0 10px 0 rgba(0,0,0,.45)">DON'T ANSWER</div>
</body></html>"""
open(sys.argv[1], "w").write(html)
