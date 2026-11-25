"""Turn frames.npz of one analysed video into shots.json + summary.json + review sheets.

shots.json  per shot: timing, camera move (cumulative zoom / pan / shake), light, colour,
            pop-in count, light events, transition type into the shot
summary.json  video-level aggregates
sheets/     every-3-seconds contact sheets with timestamps, transition-strip sheets
"""
import glob
import json
import os
import re
import subprocess
import sys

import cv2
import numpy as np
from sklearn.cluster import KMeans

FPS = 30.0


def rising(mask, gap):
    idx = np.where(mask[1:] & ~mask[:-1])[0] + 1
    out = []
    for i in idx:
        if not out or i - out[-1] > gap:
            out.append(int(i))
    return out


def palette(paths, k=8):
    px = []
    for p in paths:
        im = cv2.imread(p)
        if im is None:
            continue
        im = cv2.resize(im, (96, 54), interpolation=cv2.INTER_AREA)
        px.append(im.reshape(-1, 3))
    if not px:
        return []
    px = np.vstack(px).astype(np.float32)
    km = KMeans(k, n_init=3, random_state=0).fit(px)
    share = np.bincount(km.labels_, minlength=k) / len(px)
    order = np.argsort(-share)
    return [{"hex": "#%02x%02x%02x" % tuple(int(v) for v in km.cluster_centers_[i][::-1]),
             "share": round(float(share[i]), 3)} for i in order]


def main(video, adir):
    name = os.path.splitext(os.path.basename(video))[0]
    od = os.path.join(adir, name)
    d = np.load(os.path.join(od, "frames.npz"))
    a, cols = d["data"], list(d["cols"])
    C = lambda k: a[:, cols.index(k)]  # noqa: E731
    n = len(a)
    luma, cut = C("luma"), C("cut") > 0
    logs = np.log(np.clip(C("scale"), 0.9, 1.1))
    dx, dy = C("dx"), C("dy")
    reliable = C("inlier") > 0.5
    logs[~reliable] = 0
    dx[~reliable] = 0
    dy[~reliable] = 0
    cuts = list(np.where(cut)[0])
    bounds = cuts + [n]
    pop = (C("chg_top") > 0.004) & (C("chg_top") < 0.35)
    cap = C("chg_cap") > 0.015
    shots = []
    for si in range(len(cuts)):
        s, e = int(bounds[si]), int(bounds[si + 1])
        sl = slice(s + 1, e)
        zoom = float(np.exp(logs[sl].sum()))
        panx, pany = float(dx[sl].sum()), float(dy[sl].sum())
        # shake = high-frequency jitter of translation
        jit = 0.0
        if e - s > 10:
            hx = dx[sl] - np.convolve(dx[sl], np.ones(9) / 9, mode="same")
            hy = dy[sl] - np.convolve(dy[sl], np.ones(9) / 9, mode="same")
            jit = float(np.sqrt((hx ** 2 + hy ** 2).mean()))
        moves = []
        if zoom > 1.03:
            moves.append("push-in")
        if zoom < 0.97:
            moves.append("pull-out")
        if abs(panx) > 24:
            moves.append("pan-" + ("left" if panx > 0 else "right"))  # content moves right => camera pans left
        if abs(pany) > 24:
            moves.append("tilt-" + ("up" if pany > 0 else "down"))
        if jit > 0.6:
            moves.append("shake")
        # where in the shot the move happens and how fast
        zf = np.abs(logs[sl]) > 0.0003
        pf = np.hypot(dx[sl], dy[sl]) > 0.25
        mv = zf | pf
        move_frac = float(mv.mean()) if e - s > 1 else 0.0
        lum = luma[s:e]
        lights = []
        if e - s > 6:
            sm = np.convolve(lum, np.ones(5) / 5, mode="same")
            for j in range(3, len(sm) - 6):
                if sm[j + 5] - sm[j] < -25 and (not lights or j - lights[-1][0] > 15):
                    lights.append((j, "darken"))
                if sm[j + 5] - sm[j] > 25 and (not lights or j - lights[-1][0] > 15):
                    lights.append((j, "brighten"))
            spikes = np.where((lum[1:-1] - np.minimum(lum[:-2], lum[2:])) > 35)[0]
            for j in spikes:
                lights.append((int(j) + 1, "flash"))
        # transition into this shot
        trans = "start" if si == 0 else "cut"
        if si > 0:
            w0, w1 = max(0, s - 10), min(n, s + 10)
            win = luma[w0:w1]
            before, after = luma[max(0, s - 20):max(1, s - 10)].mean(), luma[min(n - 1, s + 10):min(n, s + 20)].mean()
            if win.min() < 8 and before > 15 and after > 15:
                trans = "dip-to-black"
            elif win.max() > max(before, after) + 50:
                trans = "white-flash"
            elif np.abs(dx[max(0, s - 6):s]).mean() > 6:
                trans = "whip"
            elif C("mad")[max(0, s - 8):s].mean() > 6:
                trans = "animated/dissolve"
        pops = [p for p in rising(pop[s:e], 8) if p > 3]
        shots.append({
            "i": si, "start": round(s / FPS, 2), "dur": round((e - s) / FPS, 2), "into": trans,
            "camera": moves or ["static"], "zoom": round(zoom, 3), "pan_px480": [round(panx, 1), round(pany, 1)],
            "shake": round(jit, 2), "move_frac": round(move_frac, 2),
            "luma": round(float(lum.mean()), 1), "contrast": round(float(C("contrast")[s:e].mean()), 1),
            "sat": round(float(C("sat")[s:e].mean()), 1), "warm": round(float(C("warm")[s:e].mean()), 1),
            "vignette": round(float(C("vignette")[s:e].mean()), 1),
            "popins": len(pops), "popin_t": [round((s + p) / FPS, 2) for p in pops][:40],
            "light_events": [[round((s + j) / FPS, 2), k] for j, k in lights][:20],
        })
    json.dump(shots, open(os.path.join(od, "shots.json"), "w"), ensure_ascii=False, indent=0)

    durs = np.array([s["dur"] for s in shots])
    cam = {}
    for s in shots:
        for m in s["camera"]:
            cam[m] = cam.get(m, 0) + 1
    trans = {}
    for s in shots[1:]:
        trans[s["into"]] = trans.get(s["into"], 0) + 1
    loud = {}
    lt = os.path.join(od, "loudness.txt")
    if os.path.exists(lt):
        txt = open(lt).read()
        m_ = re.findall(r"lavfi.r128.M=(-?[\d.]+)", txt)
        mom = np.array([float(x) for x in m_ if float(x) > -70])
        if len(mom):
            loud = {"momentary_LUFS_median": round(float(np.median(mom)), 1),
                    "p10": round(float(np.percentile(mom, 10)), 1), "p90": round(float(np.percentile(mom, 90)), 1)}
        ii = re.findall(r"lavfi.r128.I=(-?[\d.]+)", txt)
        if ii:
            loud["integrated_LUFS"] = float(ii[-1])
    shot_imgs = sorted(glob.glob(os.path.join(od, "shots", "*.jpg")))
    summ = {
        "video": name, "minutes": round(n / FPS / 60, 2), "shots": len(shots),
        "shot_len_s": {"mean": round(float(durs.mean()), 2),
                       "p10_p25_p50_p75_p90": [round(float(x), 1) for x in np.percentile(durs, [10, 25, 50, 75, 90])]},
        "cuts_per_min": round(len(shots) / (n / FPS / 60), 2),
        "popins_per_min": round(sum(s["popins"] for s in shots) / (n / FPS / 60), 1),
        "caption_changes_per_min": round(len(rising(cap, 6)) / (n / FPS / 60), 1),
        "camera_moves_by_shot": cam, "transitions": trans,
        "frames_with_camera_motion_pct": round(float(((np.abs(logs) > 0.0003) | (np.hypot(dx, dy) > 0.25)).mean() * 100), 1),
        "luma_p5_p50_p95": [round(float(x), 1) for x in np.percentile(luma, [5, 50, 95])],
        "contrast_median": round(float(np.median(C("contrast"))), 1),
        "sat_median": round(float(np.median(C("sat"))), 1),
        "vignette_median": round(float(np.median(C("vignette"))), 1),
        "dark_frames_pct(luma<40)": round(float((luma < 40).mean() * 100), 1),
        "light_events": sum(len(s["light_events"]) for s in shots),
        "loudness": loud,
        "palette": palette(shot_imgs[:: max(1, len(shot_imgs) // 60)]),
    }
    json.dump(summ, open(os.path.join(od, "summary.json"), "w"), ensure_ascii=False, indent=1)

    sd = os.path.join(od, "sheets")
    os.makedirs(sd, exist_ok=True)
    # every-3-seconds sheets, 6x8 tiles, timestamp burned in
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", video, "-an", "-vf",
                    "fps=1/3,scale=320:180,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:"
                    "box=1:boxcolor=black@0.7,tile=6x8",
                    os.path.join(sd, "t_%02d.jpg")], check=False)
    strips = sorted(glob.glob(os.path.join(od, "strips", "*.jpg")))
    for k in range(0, len(strips), 12):
        ims = [cv2.imread(p) for p in strips[k:k + 12]]
        ims = [cv2.putText(im, os.path.basename(p)[:-4], (4, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
               for im, p in zip(ims, strips[k:k + 12]) if im is not None]
        if ims:
            sheet = np.vstack(ims)
            sheet = cv2.resize(sheet, (1440, int(sheet.shape[0] * 1440 / sheet.shape[1])))
            cv2.imwrite(os.path.join(sd, f"cuts_{k // 12:02d}.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 82])
    print(name, json.dumps({k: summ[k] for k in ["minutes", "shots", "cuts_per_min", "popins_per_min"]}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
