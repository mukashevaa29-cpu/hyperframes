"""Voice every spoken unit with ElevenLabs (with character timestamps), one request per line.

Writes build/vo/NNN.mp3 + NNN.json (alignment). Skips units already done, so it can be re-run.
The proxy injects the API key; the header value here is a placeholder.
"""
import base64
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.request

VOICE = "TbEd6wZh117FdOyTGS3q"  # Brody
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": True}

units = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
spoken = []
for i, u in enumerate(units):
    t = u.get("text") if u["kind"] == "line" else u.get("spoken")
    if t:
        spoken.append((i, t))


def job(k):
    i, text = spoken[k]
    mp3 = os.path.join(out, f"{i:03d}.mp3")
    if os.path.exists(mp3):
        return i, "skip"
    body = {
        "text": text, "model_id": MODEL, "voice_settings": SETTINGS,
        "previous_text": " ".join(t for _, t in spoken[max(0, k - 3):k]),
        "next_text": " ".join(t for _, t in spoken[k + 1:k + 3]),
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": "placeholder", "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
            break
        except Exception as e:  # rate limits / transient errors
            if attempt == 4:
                return i, f"FAIL {e}"
            time.sleep(3 * (attempt + 1))
    open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump({"text": text, "alignment": d.get("alignment")}, open(mp3[:-4] + ".json", "w"))
    return i, "ok"


with cf.ThreadPoolExecutor(3) as ex:
    for i, s in ex.map(job, range(len(spoken))):
        if s != "skip":
            print(i, s, flush=True)
print("DONE", len(spoken))
