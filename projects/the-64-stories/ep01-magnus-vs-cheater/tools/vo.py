"""Final VO: eleven_v3 take (Callum), split around the real clip, tempo x1.28 (rubberband),
voice chain, and word timings -> assets/audio/timing.json."""
import json, subprocess
TEMPO = 1.28
CHAIN = "highpass=f=70,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2.5,acompressor=threshold=-22dB:ratio=3.5:attack=4:release=90:makeup=5,alimiter=limit=0.89"
a = json.load(open("assets/audio/v2/v3_full.align.json"))
ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
words = []; cur = ""; s = None
for c, a1, b1 in zip(ch, st, en):
    if c == " ":
        if cur: words.append({"text": cur, "start": s, "end": pe}); cur = ""
        continue
    if not cur: s = a1
    cur += c; pe = b1
if cur: words.append({"text": cur, "start": s, "end": pe})
k = next(i for i, w in enumerate(words) if w["text"] == "noticed.")
cut1 = words[k]["end"] + 0.12
cut2 = words[k + 1]["start"] - 0.06
parts = [(0.0, cut1, words[:k + 1]), (cut2, words[-1]["end"] + 0.35, words[k + 1:])]
P1 = 0.15
outs = []
for i, (a0, b0, ws) in enumerate(parts):
    out = f"assets/audio/vo_final_{i + 1}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/v2/v3_full.mp3", "-af",
                    f"atrim={a0:.3f}:{b0:.3f},asetpts=PTS-STARTPTS,rubberband=tempo={TEMPO},{CHAIN},afade=t=in:d=0.01,afade=t=out:st={(b0 - a0) / TEMPO - 0.03:.3f}:d=0.03",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "128k", out], check=True)
    outs.append((out, a0, ws, (b0 - a0) / TEMPO))
CLIP_LEN = 2.25
p1_dur = outs[0][3]
clip_start = round(P1 + p1_dur + 0.05, 3)
p2_start = round(clip_start + CLIP_LEN, 3)
allw = []
for (out, a0, ws, dur), off in zip(outs, (P1, p2_start)):
    for w in ws:
        allw.append({"text": w["text"], "start": round(off + (w["start"] - a0) / TEMPO, 3), "end": round(off + (w["end"] - a0) / TEMPO, 3)})
json.dump({"p1_start": P1, "clip_start": clip_start, "p2_start": p2_start, "p1_dur": round(outs[0][3], 3), "p2_dur": round(outs[1][3], 3), "words": allw},
          open("assets/audio/timing.json", "w"), indent=0)
print("p1", round(p1_dur, 2), "clip", clip_start, "p2", p2_start, "end", allw[-1]["end"])
