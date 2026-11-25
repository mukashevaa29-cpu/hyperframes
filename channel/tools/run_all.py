"""Analyse every downloaded video as soon as yt-dlp finishes merging it (3 at a time)."""
import concurrent.futures as cf
import glob
import os
import subprocess
import sys
import time

REF = sys.argv[1]
OUT = os.path.join(REF, "analysis")
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analyze.py")
TOTAL = 20
os.makedirs(OUT, exist_ok=True)


def run(path):
    name = os.path.splitext(os.path.basename(path))[0]
    r = subprocess.run([sys.executable, "-I", TOOL, path, OUT], capture_output=True, text=True)
    # loudness per 0.1s window + overall, for audio pacing
    subprocess.run(["ffmpeg", "-nostats", "-i", path, "-vn", "-af", "ebur128=metadata=1,ametadata=print:file="
                    + os.path.join(OUT, name, "loudness.txt"), "-f", "null", "-"], capture_output=True)
    return name, r.stdout.strip() + r.stderr.strip()[-500:]


started = set()
with cf.ThreadPoolExecutor(3) as ex:
    futs = []
    while len(started) < TOTAL:
        for p in sorted(glob.glob(os.path.join(REF, "videos", "*.mkv"))):
            if p not in started:
                started.add(p)
                futs.append(ex.submit(run, p))
        if len(started) < TOTAL:
            time.sleep(20)
    for f in cf.as_completed(futs):
        print(*f.result(), flush=True)
print("ALL DONE", flush=True)
