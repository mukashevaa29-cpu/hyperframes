"""Per-frame analysis of one video, every frame at native fps.

Outputs into <outdir>/<name>/:
  frames.npz   per-frame metrics (luma, contrast, saturation, colour temp, vignette,
               cut score, global camera motion dx/dy/scale/rot)
  shots/NNNN.jpg  first frame of every detected shot (960x540)
  strips/NNNN.jpg 8-frame strip around every cut (-5..+2) to show the transition
"""
import collections
import os
import subprocess
import sys

import cv2
import numpy as np

W, H = 960, 540
SW, SH = 480, 270
CUT_HIST = 0.30
CUT_MAD = 10.0


def main(path, outdir):
    name = os.path.splitext(os.path.basename(path))[0]
    od = os.path.join(outdir, name)
    os.makedirs(os.path.join(od, "shots"), exist_ok=True)
    os.makedirs(os.path.join(od, "strips"), exist_ok=True)
    proc = subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-i", path, "-an", "-vf", f"scale={W}:{H}:flags=area",
         "-pix_fmt", "bgr24", "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
    fsz = W * H * 3
    rows = []
    prev_gray = prev_hist = None
    hist_buf = collections.deque(maxlen=6)  # small frames for strips
    pending_strips = []  # (cut_idx, frames_so_far)
    shot_idx = 0
    last_cut = -100
    i = 0
    yy, xx = np.mgrid[0:SH, 0:SW]
    r = np.hypot((xx - SW / 2) / (SW / 2), (yy - SH / 2) / (SH / 2))
    center_mask, edge_mask = r < 0.45, r > 1.0
    while True:
        buf = proc.stdout.read(fsz)
        if len(buf) < fsz:
            break
        big = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        small = cv2.resize(big, (SW, SH), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        lum = gray.astype(np.float32)
        b, g, rr = [small[..., k].astype(np.float32).mean() for k in range(3)]
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [16, 4, 4], [0, 180, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        hd = mad = chg_top = chg_cap = 0.0
        dx = dy = rot = 0.0
        sc = 1.0
        inl = 0.0
        if prev_gray is not None:
            hd = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
            diff = np.abs(lum - prev_gray.astype(np.float32))
            mad = float(diff.mean())
            cut_y = int(SH * 0.82)
            chg_top = float((diff[:cut_y] > 25).mean())
            chg_cap = float((diff[cut_y:] > 25).mean())
            pts = cv2.goodFeaturesToTrack(prev_gray, 300, 0.01, 8)
            if pts is not None and len(pts) >= 12:
                nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, pts, None, winSize=(21, 21), maxLevel=3)
                ok = st.ravel() == 1
                if ok.sum() >= 10:
                    m, inliers = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC,
                                                             ransacReprojThreshold=1.5)
                    if m is not None:
                        sc = float(np.hypot(m[0, 0], m[1, 0]))
                        rot = float(np.degrees(np.arctan2(m[1, 0], m[0, 0])))
                        # translation of the frame centre, in 480-px units
                        cx, cy = SW / 2, SH / 2
                        dx = float(m[0, 0] * cx + m[0, 1] * cy + m[0, 2] - cx)
                        dy = float(m[1, 0] * cx + m[1, 1] * cy + m[1, 2] - cy)
                        inl = float(inliers.sum()) / max(1, ok.sum())
        is_cut = prev_gray is None or (hd > CUT_HIST and mad > CUT_MAD and i - last_cut > 3)
        if is_cut:
            last_cut = i
            cv2.imwrite(os.path.join(od, "shots", f"{shot_idx:04d}.jpg"), big, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if i > 0:
                pending_strips.append([shot_idx, list(hist_buf), []])
            shot_idx += 1
        tiny = cv2.resize(small, (240, 135), interpolation=cv2.INTER_AREA)
        for ps in pending_strips:
            ps[2].append(tiny)
        done = [ps for ps in pending_strips if len(ps[2]) >= 3]
        for ps in done:
            frames = ps[1][-5:] + ps[2][:3]
            cv2.imwrite(os.path.join(od, "strips", f"{ps[0]:04d}.jpg"), np.hstack(frames),
                        [cv2.IMWRITE_JPEG_QUALITY, 80])
            pending_strips.remove(ps)
        hist_buf.append(tiny)
        rows.append([
            lum.mean(), lum.std(), np.percentile(lum, 2), np.percentile(lum, 98),
            hsv[..., 1].mean(), rr - b, lum[center_mask].mean() - lum[edge_mask].mean(),
            hd, mad, dx, dy, sc, rot, inl, 1.0 if is_cut else 0.0, hsv[..., 0].mean(),
            chg_top, chg_cap,
        ])
        prev_gray, prev_hist = gray, hist
        i += 1
    proc.wait()
    cols = ["luma", "contrast", "p2", "p98", "sat", "warm", "vignette", "hdist", "mad",
            "dx", "dy", "scale", "rot", "inlier", "cut", "hue", "chg_top", "chg_cap"]
    np.savez_compressed(os.path.join(od, "frames.npz"), data=np.array(rows, np.float32), cols=np.array(cols))
    print(f"{name}: {i} frames, {shot_idx} shots")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
