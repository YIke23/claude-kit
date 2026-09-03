#!/usr/bin/env python3
"""push 前の自己点検。marketplace.json と各 SKILL.md の整合を見る。"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errs, warns = [], []

market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
listed = {s for p in market["plugins"] for s in p["skills"]}

for p in market["plugins"]:
    for rel in p["skills"]:
        if not (ROOT / rel / "SKILL.md").is_file():
            errs.append(f"{p['name']}: {rel}/SKILL.md がない")

for d in sorted((ROOT / "skills").iterdir()):
    if not d.is_dir():
        continue
    rel = f"./skills/{d.name}"
    if rel not in listed:
        warns.append(f"{d.name} はどのプラグインにも入っていない")
    f = d / "SKILL.md"
    if not f.is_file():
        errs.append(f"{d.name}: SKILL.md がない")
        continue
    text = f.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errs.append(f"{d.name}: フロントマターがない")
        continue
    fm = m.group(1)
    name = re.search(r'^name:\s*"?([^"\n]+)"?', fm, re.M)
    if not name or name.group(1).strip() != d.name:
        errs.append(f"{d.name}: name がフォルダ名と一致しない")
    desc = re.search(r"^description:\s*(.+)", fm, re.S | re.M)
    if not desc:
        errs.append(f"{d.name}: description がない")
    else:
        body = re.split(r"\n[a-z-]+:", desc.group(1))[0]
        n = len(body.strip())
        if n > 1536:
            errs.append(f"{d.name}: description が {n} 字。1536 字で切られる")
        elif n > 1200:
            warns.append(f"{d.name}: description が {n} 字。上限 1536 に近い")

for w in warns:
    print(f"WARN  {w}")
for e in errs:
    print(f"ERROR {e}")
print(f"\nスキル {len([d for d in (ROOT/'skills').iterdir() if d.is_dir()])} 本 / "
      f"プラグイン {len(market['plugins'])} 個 / エラー {len(errs)} 件")
sys.exit(1 if errs else 0)
