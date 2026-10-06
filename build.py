#!/usr/bin/env python3
"""Build Rabbit Hole: validates data/questions.json and writes index.html.

Usage:
    python3 build.py                 # validate + build
    python3 build.py --check         # validate only
    python3 build.py --link URL      # set the link used in share messages
"""
import argparse
import json
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data" / "questions.json"
TEMPLATE = ROOT / "src" / "template.html"
OUT = ROOT / "index.html"
CONFIG = ROOT / "config.json"

TARGET = {1: 80, 2: 112, 3: 64}  # pleb / maxi / cypherpunk


def validate(qs):
    errors = []
    ids = [q["id"] for q in qs]
    if sorted(ids) != list(range(256)):
        errors.append("Τα id πρέπει να είναι ακριβώς 0..255, το καθένα μία φορά.")
    for q in qs:
        tag = q.get("hex", q.get("id"))
        if q["weight"] not in (1, 2, 3):
            errors.append(f"{tag}: weight πρέπει να είναι 1, 2 ή 3")
        opts = [q["answer"], *q["wrong"]]
        if len(q["wrong"]) != 3 or len(set(opts)) != 4:
            errors.append(f"{tag}: χρειάζονται 1 σωστή και 3 διαφορετικές λάθος απαντήσεις")
        for k in ("question", "answer", "why"):
            if not str(q.get(k, "")).strip():
                errors.append(f"{tag}: κενό πεδίο {k}")
        if q["hex"] != "0x%02X" % q["id"]:
            errors.append(f"{tag}: το hex δεν ταιριάζει με το id")
    texts = [q["question"] for q in qs]
    for t, n in Counter(texts).items():
        if n > 1:
            errors.append(f"Διπλή ερώτηση: {t}")
    counts = Counter(q["weight"] for q in qs)
    if dict(counts) != TARGET:
        errors.append(f"Αναλογία {dict(counts)} αντί για {TARGET}")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--link")
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text("utf-8")) if CONFIG.exists() else {}
    if args.link:
        cfg["link"] = args.link
        CONFIG.write_text(json.dumps(cfg, indent=2), "utf-8")
    link = cfg.get("link", "")

    qs = json.loads(DATA.read_text("utf-8"))
    errors = validate(qs)
    verified = sum(1 for q in qs if q.get("verified"))
    print(f"{len(qs)} ερωτήσεις · {verified} επαληθευμένες σε πηγή · {256 - verified} εκκρεμούν")
    if errors:
        print("\nΣΦΑΛΜΑΤΑ:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    if args.check:
        print("OK")
        return

    bank = [[q["id"], q["weight"], q["question"], q["answer"], *q["wrong"], q["why"]] for q in qs]
    js = "[\n" + "".join("  " + json.dumps(b, ensure_ascii=False) + ",\n" for b in bank) + "]"
    page = TEMPLATE.read_text("utf-8").replace("__BANK__", js).replace("__LINK__", link)
    i = page.index("</style>") + len("</style>")
    html = (
        '<!doctype html>\n<html lang="el">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + page[:i] + "\n</head>\n<body>\n" + page[i:] + "</body>\n</html>\n"
    ).replace("body{font-family:var(--text);", "body{margin:0;font-family:var(--text);", 1)
    OUT.write_text(html, "utf-8")
    print(f"OK → {OUT.name}")


if __name__ == "__main__":
    main()
