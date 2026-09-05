#!/usr/bin/env python3
"""marketplace.json を読み、claude.ai アカウントに上げる .plugin と、
スキル単位の .zip を dist/ に組み立てる。

Mac 側は git から直接読むのでビルド不要。これはアカウント側専用。
"""
import json, pathlib, shutil, sys, zipfile

from skilllib import ROOT, skill_dirs

DIST = ROOT / "dist"
MARKET = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))


def zip_dir(src: pathlib.Path, out: pathlib.Path, arc_root: str = "") -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file() and ".DS_Store" not in p.name:
                z.write(p, pathlib.PurePosixPath(arc_root) / p.relative_to(src))


def build_plugin(entry: dict) -> pathlib.Path:
    name = entry["name"]
    stage = DIST / "_stage" / name
    if stage.exists():
        shutil.rmtree(stage)
    (stage / ".claude-plugin").mkdir(parents=True)
    (stage / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(
            {"name": name, "description": entry["description"], "author": MARKET["owner"]},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    for rel in entry["skills"]:
        src = ROOT / rel
        if not src.is_dir():
            sys.exit(f"ERROR: {rel} が見つかりません（marketplace.json を直してください）")
        shutil.copytree(src, stage / "skills" / src.name)
    out = DIST / f"{name}.plugin"
    zip_dir(stage, out)
    return out


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    made = [build_plugin(p) for p in MARKET["plugins"]]
    for skill in skill_dirs():
        out = DIST / "skills" / f"{skill.name}.zip"
        zip_dir(skill, out, skill.name)
        made.append(out)
    shutil.rmtree(DIST / "_stage", ignore_errors=True)
    for p in made:
        print(f"{p.stat().st_size // 1024:>5} KB  {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
