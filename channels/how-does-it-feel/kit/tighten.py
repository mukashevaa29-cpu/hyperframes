"""Tighten a voiceover: shrink long pauses and shift word timings to match.

usage: python3 kit/tighten.py episodes/<ep> [pause=0.32] [dots_pause=0.55]
Reads audio/vo.mp3 + audio/words.json (from tts.py), writes them back tightened (originals kept as *_raw.*).
Pauses after a word ending in "..." keep the longer dramatic gap.
"""
import json, os, re, shutil, subprocess, sys

ep = sys.argv[1]
P = float(sys.argv[2]) if len(sys.argv) > 2 else 0.32
PD = float(sys.argv[3]) if len(sys.argv) > 3 else 0.55
A = f"{ep}/audio"
if not os.path.exists(f"{A}/vo_raw.mp3"):
    shutil.copy(f"{A}/vo.mp3", f"{A}/vo_raw.mp3")
    shutil.copy(f"{A}/words.json", f"{A}/words_raw.json")
words = json.load(open(f"{A}/words_raw.json"))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{A}/vo_raw.mp3"], capture_output=True, text=True).stdout)
log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f"{A}/vo_raw.mp3", "-af", "silencedetect=noise=-38dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
cuts = []  # (a, b) removed spans
for a, b in zip(starts, ends):
    before = [w for w in words if w["e"] <= a + 0.25]
    if not before:  # leading silence
        if b - a > 0.08:
            cuts.append((a, b - 0.05))
        continue
    target = PD if before[-1]["w"].endswith("...") else P
    if b - a > target + 0.04:
        keep_half = target / 2
        cuts.append((a + keep_half, b - keep_half))
keep, t = [], 0.0
for a, b in cuts:
    if a > t:
        keep.append((t, a))
    t = b
keep.append((t, dur))
fc = "".join(f"[0:a]atrim={s:.4f}:{e:.4f},asetpts=PTS-STARTPTS[k{i}];" for i, (s, e) in enumerate(keep))
fc += "".join(f"[k{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/vo_raw.mp3", "-filter_complex", fc, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "160k", f"{A}/vo.mp3"], check=True)


def remap(x):
    removed = 0.0
    for a, b in cuts:
        if x >= b:
            removed += b - a
        elif x > a:
            removed += x - a
    return round(x - removed, 3)


json.dump([dict(w=w["w"], s=remap(w["s"]), e=remap(w["e"])) for w in words], open(f"{A}/words.json", "w"), indent=0)
print(f"{ep}: {dur:.1f}s -> {sum(e - s for s, e in keep):.1f}s ({len(cuts)} pauses tightened)")
