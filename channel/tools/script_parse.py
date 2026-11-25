"""Parse an episode SCRIPT.md into timing units.

Unit kinds:
  line     one narrated sentence (keywords keep their colour)
  chapter  chapter card; spoken as e.g. "Night one. The first ring."
  rule     rule card (not spoken itself: the following "Rule n." lines are)
"""
import json
import re
import sys

NUM = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven"}
KW = re.compile(r"\[([rygb]):([^\]]+)\]")


def spoken_chapter(title):
    # "NIGHT 1 · THE FIRST RING" -> "Night one. The first ring."
    head, _, name = title.partition("·")
    head = head.strip().title()
    head = re.sub(r"\d", lambda m: NUM.get(m.group(0), m.group(0)), head)
    name = name.strip().capitalize()
    return f"{head}. {name}." if name else ""


def parse(path):
    units = []
    started = False
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if line.startswith("## "):
            started = True
            title = line[3:].strip()
            units.append({"kind": "chapter", "title": title, "spoken": spoken_chapter(title)})
            continue
        if not started or not line or line.startswith("---"):
            continue
        if line.startswith("### "):
            num, _, imp = line[4:].partition("|")
            units.append({"kind": "rule", "label": num.strip(), "imperative": imp.strip()})
            continue
        words = []
        for tok in re.split(r"(\[[rygb]:[^\]]+\])", line):
            if not tok:
                continue
            m = KW.fullmatch(tok)
            if m:
                for w in m.group(2).split():
                    words.append({"w": w, "c": m.group(1)})
            else:
                for w in tok.split():
                    words.append({"w": w, "c": None})
        units.append({"kind": "line", "text": KW.sub(lambda m: m.group(2), line), "words": words})
    return units


if __name__ == "__main__":
    u = parse(sys.argv[1])
    json.dump(u, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
    print(len(u), "units;", sum(x["kind"] == "line" for x in u), "lines")
