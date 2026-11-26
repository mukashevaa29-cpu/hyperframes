"""Vertical Shorts (1080x1920) cut from a finished episode render.

Usage: python3 shorts.py <shorts_spec.py> [short_id ...]

Each spec entry: dict(id, ep, video, u0, u1, kicker, title, offset=0.0)
  ep      episode dir (timing from build/timing_fast.json, unit indices as in build/units.json)
  video   finished render (picture + mastered audio)
  u0/u1   first/last spoken unit of the segment (u0 is normally the "Rule n." line)
  kicker  small pill above the title; title is HTML (use <y>..</y> / <r>..</r> for colour)
  offset  seconds to subtract from timing (render made before units were inserted at the start)

Layout (Shorts UI covers ~top 200 px, bottom ~380 px, right ~140 px):
  title 240-560 · picture 620-1228 (16:9, centre crop of the film without HUD or burned captions)
  big word-group captions ~1330 · end card text in the last 1.2 s (frozen last frame).
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = "/home/user/hyperframes/channel"
OUT = f"{ROOT}/shorts/out"
FONTS = f"{ROOT}/shorts/fonts"
SHOT_JS = f"{ROOT}/shorts/shot.cjs"
TAIL = 1.2
PIC_Y, PIC_H = 610, 645
COL = {"r": "&H004F3BEF&", "y": "&H003BD4FF&", "g": "&H007FBF3F&", "b": "&H00FFB07F&", None: "&H00FFFFFF&"}
WEAK = {"and", "the", "a", "an", "of", "to", "in", "on", "at", "for", "but", "or", "your", "is", "it", "that", "with", "from", "by", "his", "her", "their"}

spec_path = sys.argv[1]
_spec = importlib.util.spec_from_file_location("spec", spec_path)
spec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(spec)
only = set(sys.argv[2:])
os.makedirs(OUT, exist_ok=True)


def ts(t):
    cs = int(round(max(0, t) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def groups(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        txt = " ".join(x["w"] for x in cur)
        end_punct = re.search(r"[.,!?;:…]$", w["w"])
        if len(cur) >= 3 or len(txt) >= 16 or end_punct:
            if not end_punct and cur[-1]["w"].lower() in WEAK and len(cur) > 1:  # weak word opens the next group
                carry = cur.pop()
                out.append(cur)
                cur = [carry]
            else:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return out


def ass_file(path, words, t0, dur):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat Black,92,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H96000000&,0,0,0,0,100,100,0,0,1,7,4,5,70,70,0,1
Style: End,Montserrat Black,64,&H003BD4FF&,&H003BD4FF&,&H00000000&,&H96000000&,0,0,0,0,100,100,0,0,1,6,3,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    gs = groups(words)
    for k, g in enumerate(gs):
        a = g[0]["s"] - t0
        b = (gs[k + 1][0]["s"] - t0) if k + 1 < len(gs) else min(dur, g[-1]["e"] - t0 + 0.4)
        txt = " ".join(("{\\c" + COL[w["c"]] + "}" if w["c"] else "") + w["w"].upper() + ("{\\c" + COL[None] + "}" if w["c"] else "")
                       for w in g)
        ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\pos(540,1420)\\fscx82\\fscy82\\t(0,90,\\fscx100\\fscy100)}}{txt}")
    ev.append(f"Dialogue: 0,{ts(dur)},{ts(dur + TAIL)},End,,0,0,0,,{{\\pos(540,1420)\\fad(150,0)}}FULL STORY ON THE CHANNEL")
    open(path, "w").write(head + "\n".join(ev) + "\n")


def overlay_png(path, kicker, title, pic_y=PIC_Y, pic_h=PIC_H):
    title = re.sub(r"<y>(.*?)</y>", r'<span style="color:#ffd43b">\1</span>', title)
    title = re.sub(r"<r>(.*?)</r>", r'<span style="color:#ef3b4f">\1</span>', title)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:M;src:url('file://{ROOT}/ep01-3am-call/thumbnail/montserrat-900.woff2') format('woff2');font-weight:100 900}}
body{{margin:0;width:1080px;height:1920px;background:transparent;font-family:M,sans-serif}}
.k{{position:absolute;left:0;right:0;top:250px;text-align:center}}
.k span{{display:inline-block;background:#ef3b4f;color:#fff;font-weight:900;font-size:34px;letter-spacing:.04em;padding:8px 22px;border-radius:10px;box-shadow:0 6px 0 rgba(0,0,0,.45)}}
.t{{position:absolute;left:60px;right:60px;top:330px;height:260px;display:flex;align-items:center;justify-content:center;text-align:center;
color:#fff;font-weight:900;font-size:68px;line-height:1.02;letter-spacing:-.01em;text-shadow:0 6px 0 rgba(0,0,0,.6),0 0 30px rgba(0,0,0,.7)}}
.f{{position:absolute;left:-6px;top:{pic_y - 6}px;width:1080px;height:{pic_h}px;border:6px solid #0a0c14;box-shadow:0 18px 50px rgba(0,0,0,.7)}}
</style></head><body><div class="f"></div><div class="k"><span>{kicker}</span></div><div class="t"><div>{title}</div></div></body></html>"""
    hp = path[:-4] + ".html"
    open(hp, "w").write(html)
    subprocess.run(["node", SHOT_JS, hp, path], check=True)


for s in spec.SHORTS:
    if only and s["id"] not in only:
        continue
    ep = f"{ROOT}/{s['ep']}"
    off = s.get("offset", 0.0)
    T = {u["i"]: u for u in json.load(open(f"{ep}/build/timing_fast.json"))["units"]}
    ids = [k for k in range(s["u0"], s["u1"] + 1) if k in T]
    t0 = T[ids[0]]["start"] - 0.35 - off
    t1 = T[ids[-1]]["end"] + 0.02 - off  # the film cuts ~0.25 s after a sentence: stop before the next shot
    dur = t1 - t0
    words = [dict(w, s=w["s"] - off, e=w["e"] - off) for k in ids for w in T[k]["words"]]
    base = f"{OUT}/{s['id']}"
    ass_file(base + ".ass", words, t0, dur)
    cw = s.get("crop_w", 1440)  # wider crop for shots with tags near the edges (smaller picture)
    ph = round(1080 * 860 / cw / 2) * 2
    py = PIC_Y + (PIC_H - ph) // 2
    overlay_png(base + "_ov.png", s["kicker"], s["title"], py, ph)
    fg = f"scale=1080:{ph}"
    bg = "scale=-2:480,crop=270:480,gblur=sigma=12,scale=1080:1920,eq=brightness=-0.3:saturation=0.8"
    fc = (f"[0:v]crop={cw}:860:{(1920 - cw) // 2}:80,split[a][b];[a]{bg}[bg];[b]{fg}[fg];[bg][fg]overlay=0:{py}[v1];[v1][1:v]overlay=0:0[v2];"
          f"[v2]tpad=stop_mode=clone:stop_duration={TAIL},ass={base}.ass:fontsdir={FONTS},format=yuv420p[v];"
          f"[0:a]afade=t=in:d=0.12,afade=t=out:st={dur - 0.15:.3f}:d=0.9,apad=whole_dur={dur + TAIL:.3f}[aud]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", s["video"], "-i", base + "_ov.png",
           "-filter_complex", fc, "-map", "[v]", "-map", "[aud]", "-t", f"{dur + TAIL:.3f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
           base + ".mp4"]
    subprocess.run(cmd, check=True)
    print(s["id"], f"{t0:.2f}-{t1:.2f}", f"{dur + TAIL:.1f}s", base + ".mp4", flush=True)
