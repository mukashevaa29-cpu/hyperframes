"""Shared shot-list helpers for The Rule Stories episodes (marks, panels, silhouettes, dots)."""
import sys

sys.path.insert(0, "/home/user/hyperframes/channel/tools")
from art2 import character  # noqa: E402  (v2 rig: reference-level detail)
CHAR_SCALE = 1.12

def ch(cid, who, x, y=860, s=1.45, **kw):
    return character(cid, who, x, y, s * CHAR_SCALE, **kw)


def X(x, y, s=1.0):
    """Red cross mark."""
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-70" y="-12" width="140" height="24" rx="10" fill="#ef3b4f" transform="rotate(45)"/>'
            f'<rect x="-70" y="-12" width="140" height="24" rx="10" fill="#ef3b4f" transform="rotate(-45)"/></g>')


def CHECK(x, y, s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-50,0 L-14,36 L54,-40" stroke="#3fbf7f" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'


def RING(x, y, r, color="#7fb8ff"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-width="7" opacity="0.9"/>'


def WAVES(x, y, color="#ffd43b", s=1.0):
    """Ringing waves either side of a point."""
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round">'
            '<path d="M-50,-30 Q-66,0 -50,30"/><path d="M-72,-46 Q-96,0 -72,46"/><path d="M50,-30 Q66,0 50,30"/><path d="M72,-46 Q96,0 72,46"/></g>')


def panel(x, y, w, h, inner, fill="#1d1e29", k=1.2):
    """Card for an icon on the infographic stage: bigger, with a soft shadow and a lighter top band."""
    w, h = w * k, h * k
    return (f'<g transform="translate({x} {y})"><rect x="{-w/2+10}" y="{-h/2+14}" width="{w}" height="{h}" rx="26" fill="#000" opacity="0.35"/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="26" fill="{fill}"/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h*0.18}" rx="26" fill="#ffffff" opacity="0.05"/>'
            f'<rect x="{-w/2+3}" y="{-h/2+3}" width="{w-6}" height="{h-6}" rx="23" fill="none" stroke="#ffffff" stroke-opacity="0.08" stroke-width="3"/>'
            f'<g transform="scale({k})">{inner}</g></g>')


def SIL(x, y, s=1.0, color="#06070c"):
    """Black silhouette figure."""
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{color}"><ellipse cx="0" cy="-262" rx="48" ry="54"/>'
            '<rect x="-56" y="-222" width="112" height="130" rx="30"/><rect x="-32" y="-110" width="26" height="110" rx="8"/>'
            '<rect x="6" y="-110" width="26" height="110" rx="8"/></g>')


def COUCH_FRONT():
    """Front of the couch drawn over seated characters (living_room bg)."""
    return ('<rect x="800" y="700" width="680" height="110" rx="30" fill="#6a5a80"/>'
            '<rect x="780" y="640" width="90" height="190" rx="34" fill="#5a4a6e"/><rect x="1410" y="640" width="90" height="190" rx="34" fill="#5a4a6e"/>')


def TVBOX(x, y, inner):
    return (f'<g transform="translate({x} {y})"><rect x="-190" y="-120" width="380" height="240" rx="14" fill="#0b0c10"/>'
            f'<rect x="-176" y="-106" width="352" height="212" rx="6" fill="#24407a"/>'
            f'<svg x="-176" y="-106" width="352" height="212" overflow="hidden">{inner}</svg></g>')


def CURSOR(x, y, s=1.6):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0,0 L0,44 L11,33 L19,52 L27,48 L19,30 L34,30 Z" fill="#fff" stroke="#111" stroke-width="3" stroke-linejoin="round"/></g>')


def DOTS(n=20, y=520, color="#ef3b4f", r=22):
    x0 = 960 - (n - 1) * (r * 2 + 12) / 2
    return "".join(f'<circle cx="{x0 + k * (r * 2 + 12):.0f}" cy="{y}" r="{r}" fill="{color}"/>' for k in range(n))
