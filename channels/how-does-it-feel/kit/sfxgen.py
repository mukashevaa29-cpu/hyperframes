"""Generate a sound effect with ElevenLabs.  usage: python3 kit/sfxgen.py name seconds "prompt"  -> kit/sfx/name.mp3"""
import json, sys, time, urllib.request, urllib.error, os
name, dur, text = sys.argv[1], float(sys.argv[2]), sys.argv[3]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx", name + ".mp3")
body = json.dumps(dict(text=text, duration_seconds=dur, prompt_influence=0.6)).encode()
for k in range(5):
    try:
        req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
                                     headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
        open(out, "wb").write(urllib.request.urlopen(req, timeout=120).read())
        print("ok", name)
        break
    except urllib.error.HTTPError as e:
        print("retry", name, e.code, e.read()[:200])
        time.sleep(5 * (k + 1))
