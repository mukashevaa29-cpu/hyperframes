"""Write a YouTube .srt from build/timing_fast.json: one cue per spoken line, long lines split on word timings.

Usage: python3 srt.py <episode_dir>
"""
import json
import sys

EP = sys.argv[1]
MAXC = 42
WEAK = {"and", "the", "a", "an", "of", "to", "in", "on", "at", "for", "but", "or", "your", "you", "is", "it", "that", "with", "from", "by"}


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


cues = []
for u in json.load(open(f"{EP}/build/timing_fast.json"))["units"]:
    words = u.get("words") or []
    if not words:
        continue
    cur = []
    for w in words:
        if cur and len(" ".join(x["w"] for x in cur + [w])) > MAXC:
            carry = []
            while len(cur) > 2 and cur[-1]["w"].lower().strip(",") in WEAK:
                carry.insert(0, cur.pop())
            cues.append(cur)
            cur = carry
        cur.append(w)
    if cur:
        cues.append(cur)
out = []
for n, c in enumerate(cues, 1):
    end = c[-1]["e"]
    if n < len(cues):
        end = min(end + 0.25, cues[n][0]["s"] - 0.04)
    out.append(f"{n}\n{ts(c[0]['s'])} --> {ts(end)}\n{' '.join(x['w'] for x in c)}\n")
open(f"{EP}/captions.srt", "w").write("\n".join(out))
print(len(cues), "cues")
