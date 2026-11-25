"""Stitch per-line VO into one track with edited gaps; emit word-level timing.

timing.json: {"duration", "units": [{i, kind, start, end, words:[{w,c,s,e}]}]}
Gap rules follow the style bible: near-continuous delivery (0.12 s), longer air before
rule / chapter cards so the card can build, and a few dramatic holds.
"""
import json
import re
import subprocess
import sys

import numpy as np

SR = 44100
units = json.load(open(sys.argv[1]))
vo_dir, out_wav, out_json = sys.argv[2], sys.argv[3], sys.argv[4]
HOLD_AFTER = {"Don't.": 0.55, "Hang up.": 0.9, "3:00 AM.": 1.3, "Nobody inside.": 0.9, "He didn't send it.": 0.8,
              "Your own.": 0.45, "Screen off.": 0.45, "It needs less.": 0.5, "It hurts more than you expected.": 0.8,
              "That's the first night you sleep.": 0.7, "Only a few words are different.": 0.8,
              "Because somebody just answered it.": 0.7, "Just don't write your code word.": 1.5}
RULE_LINE = re.compile(r"^(Rule \w+\.|The last rule\.)$")


def load(i):
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f"{vo_dir}/{i:03d}.mp3", "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32)


def words_from_alignment(al, text):
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, cs = [], "", None
    for ch, s, e in zip(chars, st, en):
        if ch.isspace():
            if cur:
                words.append([cur, cs, pe])
            cur, cs = "", None
            continue
        if cs is None:
            cs = s
        cur += ch
        pe = e
    if cur:
        words.append([cur, cs, pe])
    return words


spoken = [(i, u) for i, u in enumerate(units) if (u.get("text") if u["kind"] == "line" else u.get("spoken"))]
pieces, timing = [], []
t = 0.4
pieces.append(np.zeros(int(t * SR), np.float32))
for k, (i, u) in enumerate(spoken):
    meta = json.load(open(f"{vo_dir}/{i:03d}.json"))
    a = load(i)
    ws = words_from_alignment(meta["alignment"], meta["text"])
    s0 = max(0.0, ws[0][1] - 0.04)
    s1 = min(len(a) / SR, ws[-1][2] + 0.07)
    seg = a[int(s0 * SR):int(s1 * SR)].copy()
    n = len(seg)
    fade = int(0.01 * SR)
    seg[:fade] *= np.linspace(0, 1, fade)
    seg[-fade:] *= np.linspace(1, 0, fade)
    uw = u.get("words") or [{"w": w, "c": None} for w in u["spoken"].split()]
    wl = []
    for j, (w, ws_, we_) in enumerate(ws):
        c = uw[j]["c"] if j < len(uw) else None
        wl.append({"w": w, "c": c, "s": round(t + ws_ - s0, 3), "e": round(t + we_ - s0, 3)})
    timing.append({"i": i, "kind": u["kind"], "text": meta["text"], "start": round(t, 3),
                   "end": round(t + n / SR, 3), "words": wl})
    pieces.append(seg)
    t += n / SR
    # gap after this unit
    nxt = spoken[k + 1][1] if k + 1 < len(spoken) else None
    nxt_text = (nxt.get("text") or nxt.get("spoken") or "") if nxt else ""
    gap = 0.12
    if len(meta["text"].split()) <= 3:
        gap = 0.24
    if meta["text"].endswith("?"):
        gap = 0.22
    if u["kind"] == "chapter":
        gap = 0.55
    if RULE_LINE.match(meta["text"]):
        gap = 0.14
    gap = HOLD_AFTER.get(meta["text"], gap)
    # extra air before cards: a rule/chapter unit between this line and the next spoken one
    between = [x for x in units[i + 1:spoken[k + 1][0]]] if nxt else []
    if any(x["kind"] == "chapter" for x in between):
        gap = max(gap, 1.1)
    if nxt and RULE_LINE.match(nxt_text):
        gap = max(gap, 0.95)
    if nxt is None:
        gap = 1.0
    pieces.append(np.zeros(int(gap * SR), np.float32))
    t += gap

audio = np.concatenate(pieces)
peak = np.abs(audio).max()
audio = audio / peak * 0.89 if peak > 0 else audio
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-c:a", "pcm_s16le", out_wav], input=audio.astype(np.float32).tobytes(), check=True)
json.dump({"duration": round(len(audio) / SR, 3), "units": timing}, open(out_json, "w"), ensure_ascii=False)
wc = sum(len(x["words"]) for x in timing)
print(f"duration {len(audio)/SR/60:.2f} min, {wc} words, {wc/(len(audio)/SR/60):.0f} wpm")
