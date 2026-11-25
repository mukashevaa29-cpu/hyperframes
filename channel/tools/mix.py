"""Final audio mix: voice + ducked music bed (A -> B crossfade) + placed SFX, normalised to -14 LUFS.

Usage: python3 mix.py <episode_dir>
Reads build/vo_fast.wav, build/music_a.mp3, build/music_b.mp3, build/sfx/*.mp3, build/sfx_events.json.
Writes video/assets/audio/mix.m4a (the only audio clip the film needs).
"""
import json
import subprocess
import sys

import numpy as np
import pyloudnorm as pyln

EP = sys.argv[1]
SR = 48000


def load(path, ch=2):
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32).reshape(-1, ch).copy()


ev = json.load(open(f"{EP}/build/sfx_events.json"))
N = int(ev["duration"] * SR) + SR
out = np.zeros((N, 2), np.float32)

# ---- voice
vo = load(f"{EP}/build/vo_fast.wav")
out[:len(vo)] += vo[:N]

# ---- voice envelope for ducking (attack 40 ms, release 350 ms)
mono = np.abs(vo.mean(axis=1))
win = int(0.02 * SR)
rms = np.sqrt(np.convolve(mono ** 2, np.ones(win) / win, mode="same"))
active = (rms > 0.02).astype(np.float32)
env = np.zeros_like(active)
a_att, a_rel = 1 / (0.04 * SR), 1 / (0.35 * SR)
v = 0.0
step = 32
for i in range(0, len(active), step):  # coarse follower, then interpolate
    target = active[i]
    v += (target - v) * (min(1, a_att * step) if target > v else min(1, a_rel * step))
    env[i:i + step] = v
env = np.pad(env, (0, max(0, N - len(env))))[:N]

# ---- music: A until the switch, crossfade 4 s into B
ma, mb = load(f"{EP}/build/music_a.mp3"), load(f"{EP}/build/music_b.mp3")
sw = int(ev["music_switch"] * SR)
xf = int(4 * SR)
mus = np.zeros((N, 2), np.float32)
la = min(len(ma), sw + xf, N)
mus[:la] += ma[:la]
fade = np.linspace(1, 0, xf)[:, None]
s0 = max(0, sw)
seg = min(xf, la - s0)
if seg > 0:
    mus[s0:s0 + seg] *= fade[:seg]
lb = min(len(mb), N - s0)
bpart = mb[:lb].copy()
bpart[:xf] *= (1 - fade[:min(xf, lb)])
mus[s0:s0 + lb] += bpart
# fade the bed in at the start and out at the end
fi = int(1.5 * SR)
mus[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(3 * SR)
end = int(ev["duration"] * SR)
mus[end - fo:end] *= np.linspace(1, 0, fo)[:, None]
mus[end:] = 0
# ducking: 0.22 in the gaps, 0.11 under the voice
gain = 0.22 - 0.11 * env
# dips before payoffs (gain multiplier ramps down then back over `du`)
for t, g, du in ev["dips"]:
    a = int(t * SR)
    d = int(0.4 * SR)
    hold = int(du * SR)
    if a < 0 or a + d + hold + d > N:
        continue
    m = np.ones(N, np.float32)
    m[a:a + d] = np.linspace(1, g, d)
    m[a + d:a + d + hold] = g
    m[a + d + hold:a + 2 * d + hold] = np.linspace(g, 1, d)
    gain *= m
out += mus * gain[:, None]

# ---- sfx
cache = {}
for t, name, vol, mx in ev["events"]:
    if name not in cache:
        cache[name] = load(f"{EP}/build/sfx/{name}.mp3")
    clip = cache[name]
    if mx:
        clip = clip[:int(mx * SR)].copy()
        f = min(len(clip), int(0.25 * SR))
        clip[-f:] *= np.linspace(1, 0, f)[:, None]
    a = int(t * SR)
    b = min(N, a + len(clip))
    if a < 0 or a >= N:
        continue
    out[a:b] += clip[:b - a] * vol

# ---- loudness: -14 LUFS integrated, true peak kept under -1 dBFS
out = out[:end + int(0.5 * SR)]
meter = pyln.Meter(SR)
lufs = meter.integrated_loudness(out)
out = pyln.normalize.loudness(out, lufs, -14.0)
peak = np.abs(out).max()
lim = 10 ** (-1.2 / 20)
if peak > lim:  # soft-knee limiter on the few hottest samples
    over = np.abs(out) > lim * 0.85
    k = lim * 0.85
    x = np.abs(out[over])
    out[over] = np.sign(out[over]) * (k + (lim - k) * np.tanh((x - k) / (lim - k)))
print(f"in {lufs:.1f} LUFS -> {meter.integrated_loudness(out):.1f} LUFS, peak {20*np.log10(np.abs(out).max()):.1f} dBFS")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                "-c:a", "aac", "-b:a", "256k", f"{EP}/video/assets/audio/mix.m4a"], input=out.astype(np.float32).tobytes(),
               check=True)
print("wrote mix.m4a", f"{len(out)/SR:.1f}s")
