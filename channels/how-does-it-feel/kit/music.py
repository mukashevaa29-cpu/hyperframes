"""Score an episode with ElevenLabs Music from a composition plan tied to the story beats.

usage: python3 kit/music.py episodes/<ep>
Reads <ep>/music.json: {"global": [...], "negative": [...], "sections": [{"name", "until_word" | "until": "end", "styles": [...]}]}
Section boundaries come from word timings, so the score follows the cut. Writes <ep>/audio/music.mp3.
"""
import json, sys, urllib.request

ep = sys.argv[1]
plan = json.load(open(f"{ep}/music.json"))
words = json.load(open(f"{ep}/audio/words.json"))
tm = json.load(open(f"{ep}/timing.json"))
off, D = tm["off"], tm["D"]
secs, t0 = [], 0.0
for s in plan["sections"]:
    t1 = D if s.get("until") == "end" else words[s["until_word"]]["s"] + off
    secs.append(dict(section_name=s["name"], positive_local_styles=s["styles"], negative_local_styles=s.get("negative", []),
                     duration_ms=int(round((t1 - t0) * 1000)), lines=[]))
    t0 = t1
# the API wants every section between 3 s and 120 s: fold short ones into their neighbour
fixed = []
for s in secs:
    if fixed and s["duration_ms"] < 3000:
        fixed[-1]["duration_ms"] += s["duration_ms"]
    else:
        fixed.append(s)
if fixed[0]["duration_ms"] < 3000 and len(fixed) > 1:
    fixed[1]["duration_ms"] += fixed[0]["duration_ms"]
    fixed = fixed[1:]
body = dict(composition_plan=dict(positive_global_styles=plan["global"], negative_global_styles=plan.get("negative", []), sections=fixed), model_id="music_v1")
req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", data=json.dumps(body).encode(),
                             headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
try:
    data = urllib.request.urlopen(req, timeout=600).read()
except urllib.error.HTTPError as err:
    print(err.code, err.read()[:600])
    raise SystemExit(1)
open(f"{ep}/audio/music.mp3", "wb").write(data)
print(ep, "music", len(data) // 1024, "KB;", [(s["section_name"], s["duration_ms"]) for s in fixed])
