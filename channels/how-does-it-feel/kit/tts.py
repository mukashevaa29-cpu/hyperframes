"""Voice an episode with ElevenLabs and keep word timings.

usage: python3 kit/tts.py episodes/<ep> [voice_id] [voice_name]
writes <ep>/audio/vo.mp3, <ep>/audio/words.json, <ep>/audio/voice.json
The API key is injected by the session's network proxy; no key is read here.
"""
import base64, json, os, sys, urllib.request

ep = sys.argv[1]
voice_id = sys.argv[2] if len(sys.argv) > 2 else "nPczCjzI2devNBz1zQrb"  # Brian (placeholder until the channel voice is chosen)
voice_name = sys.argv[3] if len(sys.argv) > 3 else "Brian"
text = " ".join(l.strip() for l in open(f"{ep}/script.txt") if l.strip())
os.makedirs(f"{ep}/audio", exist_ok=True)
body = dict(text=text, model_id="eleven_multilingual_v2",
            voice_settings=dict(stability=0.5, similarity_boost=0.8, style=0.3, use_speaker_boost=True, speed=float(os.environ.get("HDIF_SPEED", "1.05"))))
req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128",
    data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
d = json.load(urllib.request.urlopen(req, timeout=300))
open(f"{ep}/audio/vo.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
a = d["alignment"]
words, cur, s, e = [], "", None, None
for c, t0, t1 in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if c == " ":
        if cur:
            words.append(dict(w=cur, s=round(s, 3), e=round(e, 3)))
            cur = ""
        continue
    if not cur:
        s = t0
    cur += c
    e = t1
if cur:
    words.append(dict(w=cur, s=round(s, 3), e=round(e, 3)))
json.dump(words, open(f"{ep}/audio/words.json", "w"), indent=0)
json.dump(dict(voice_id=voice_id, name=voice_name, model="eleven_multilingual_v2"), open(f"{ep}/audio/voice.json", "w"))
print(f"{ep}: {len(words)} words, {words[-1]['e']:.1f}s, voice {voice_name}")
for i, w in enumerate(words):
    pass
print()
