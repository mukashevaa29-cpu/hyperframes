"""Build compositions/captions.html from assets/vo/words-107.json (word timings of the voiceover).
Re-run after the voiceover changes: python3 scripts/build-captions.py
"""
import json, html, re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
words = json.load(open(root / "assets/vo/words-107.json"))
END = 16.1
CAP_END = 16.1

NUM = {"two", "sixteen", "five", "2011", "2018", "twelve", "thousand", "six", "hundred", "three-zero",
       "twenty-eight", "forty-four", "point", "four", "first", "fifteen", "one", "third-highest", "december"}
MAGNUS = {"magnus", "carlsen"}
FABI = {"fabiano", "caruana", "fabi", "fabi's"}
BAD = {"never", "loses", "gone", "losses", "trouble", "couldn't", "martirosyan", "no"}
COL = {"num": "#ffc83d", "magnus": "#4fb0ff", "fabi": "#ff9a3c", "bad": "#ff5050", "base": "#8fe35a"}

def cat(w):
    k = re.sub(r"[^\w'\-]", "", w.lower())
    if k in MAGNUS: return "magnus"
    if k in FABI: return "fabi"
    if k in BAD: return "bad"
    if k in NUM or k.isdigit(): return "num"
    return "base"

groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    brk = w["text"][-1] in ".?!,:" or len(cur) == 3 or (nxt and nxt["start"] - w["end"] > 0.15)
    if brk or nxt is None:
        groups.append(cur); cur = []

out_groups, js = [], []
groups = [g for g in groups if g[0]["start"] < CAP_END - 0.1]
for gi, g in enumerate(groups):
    start = max(0.1, g[0]["start"] - 0.05)
    nstart = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else END
    end = min(nstart, g[-1]["end"] + 0.6) if gi + 1 < len(groups) else min(CAP_END, g[-1]["end"] + 0.6)
    text = " ".join(w["text"] for w in g)
    size = int(min(70, 760 / (0.62 * max(len(text), 1))))
    spans = []
    for wi, w in enumerate(g):
        spans.append(f'<span id="cw{gi}-{wi}" class="cw">{html.escape(w["text"])}</span>')
    out_groups.append(f'    <div id="cg{gi}" class="cg" style="font-size: {size}px">{" ".join(spans)}</div>')
    js.append(f'    tl.fromTo("#cg{gi}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.04 }}, {start:.3f});')
    for wi, w in enumerate(g):
        c = COL[cat(w["text"])]
        js.append(f'    tl.set("#cw{gi}-{wi}", {{ color: "{c}" }}, {w["start"]:.3f});')
        if wi + 1 < len(g):
            js.append(f'    tl.set("#cw{gi}-{wi}", {{ color: "#ffffff" }}, {g[wi + 1]["start"]:.3f});')
    js.append(f'    tl.to("#cg{gi}", {{ opacity: 0, duration: 0.06, ease: "power2.in" }}, {end - 0.06:.3f});')
    js.append(f'    tl.set("#cg{gi}", {{ opacity: 0, visibility: "hidden" }}, {end:.3f});')

doc = f"""<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      pointer-events: none;
    }}
    .cg {{
      position: absolute;
      left: 120px;
      right: 192px;
      top: 1130px;
      text-align: center;
      font-family: "Nunito", sans-serif;
      font-weight: 900;
      color: #ffffff;
      line-height: 1.1;
      opacity: 0;
      overflow: visible;
      -webkit-text-stroke: 9px rgba(0, 0, 0, 0.78);
      paint-order: stroke fill;
      text-shadow:
        0 5px 0 rgba(0, 0, 0, 0.6),
        0 0 22px rgba(0, 0, 0, 0.55);
    }}
    .cw {{
      color: #ffffff;
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(out_groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
(root / "compositions/captions.html").write_text(doc)
print(len(groups), "caption groups")
