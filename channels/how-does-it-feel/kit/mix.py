"""Mix VO + music bed + SFX cues for an episode into project/assets/mix.mp3 (-14 LUFS, -1.5 dBTP).

usage: python3 kit/mix.py episodes/<ep>
Music: <ep>/audio/music.mp3 if present, else a synthesized low drone.
Cues come from timing.json written by the episode's build.py (file names are relative to kit/sfx).
"""
import json, os, subprocess, sys

KIT = os.path.dirname(os.path.abspath(__file__))
ep = sys.argv[1]
tm = json.load(open(f"{ep}/timing.json"))
D, off = tm["D"], tm["off"]
music = f"{ep}/audio/music.mp3"
if not os.path.exists(music):
    music = f"{ep}/audio/drone.wav"
    expr = (f"(0.32*sin(2*PI*55*t)+0.22*sin(2*PI*82.41*t+0.3*sin(2*PI*0.07*t))+0.16*sin(2*PI*110.4*t)+0.08*sin(2*PI*164.8*t+sin(2*PI*0.11*t)))"
            f"*(0.55+0.45*sin(2*PI*0.05*t))*min(1,t/3)*(0.6+0.4*min(1,t/{D * 0.85:.1f}))*if(gt(t,{D - 4.5:.2f}),max(0,1-(t-{D - 4.5:.2f})/1.5),1)")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={D}", "-af", "aecho=0.8:0.7:180|420:0.4|0.25,lowpass=f=900", music], check=True)
ev = [(f"{ep}/audio/vo.mp3", off, 1.0), (music, 0, 0.5 if music.endswith(".wav") else 0.32)]
for f, t, v in tm["cues"]:
    ev.append((f"{KIT}/sfx/{f}", t, v))
inputs, parts = [], []
for k, (f, t, v) in enumerate(ev):
    inputs += ["-i", f]
    ms = int(t * 1000)
    parts.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={v},adelay={ms}|{ms}[a{k}]")
fc = (";".join(parts) + ";" + "".join(f"[a{k}]" for k in range(len(ev))) +
      f"amix=inputs={len(ev)}:normalize=0:dropout_transition=0,atrim=0:{D},afade=t=out:st={D - 0.5}:d=0.5,loudnorm=I=-14:TP=-1.5:LRA=9[out]")
out = f"{ep}/project/assets/mix.mp3"
os.makedirs(os.path.dirname(out), exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", out], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print(len(ev), "tracks;", " ".join(l.strip() for l in r.splitlines() if l.strip().startswith(("I:", "Peak:")))[-60:])
