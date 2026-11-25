"""Word-timed transcripts of every reference video (as they finish downloading)."""
import glob
import json
import os
import sys
import subprocess
import time

import numpy as np

from faster_whisper import WhisperModel

REF = sys.argv[1]
OUT = os.path.join(REF, "transcripts")
os.makedirs(OUT, exist_ok=True)
model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
done = set()
while len(done) < 20:
    todo = [p for p in sorted(glob.glob(os.path.join(REF, "videos", "*.mkv")))
            if ".temp" not in p and p not in done]
    if not todo:
        time.sleep(30)
        continue
    for p in todo:
        name = os.path.splitext(os.path.basename(p))[0]
        pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-vn", "-ac", "1", "-ar", "16000",
                              "-f", "f32le", "-"], capture_output=True, check=True).stdout
        audio = np.frombuffer(pcm, np.float32)
        segs, info = model.transcribe(audio, language="ru", word_timestamps=True, vad_filter=False, beam_size=1)
        out = []
        for s in segs:
            out.append({"start": s.start, "end": s.end, "text": s.text,
                        "words": [[w.start, w.end, w.word] for w in (s.words or [])]})
        json.dump({"duration": info.duration, "segments": out},
                  open(os.path.join(OUT, name + ".json"), "w"), ensure_ascii=False)
        done.add(p)
        print(name, len(out), flush=True)
print("ALL DONE", flush=True)
