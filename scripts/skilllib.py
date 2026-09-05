#!/usr/bin/env python3
"""スキルの置き場所の決まりを 1 箇所にまとめる。validate.py と build.py が使う。"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# スキルではないルート直下のフォルダ。ここに SKILL.md が紛れると
# Claude Code がスキルとして読んでしまうので validate.py が ERROR で止める。
INFRA = {"scripts", "dist"}


def skill_dirs() -> list[pathlib.Path]:
    """ルート直下で SKILL.md を持つフォルダがスキル。Claude Code 自身と同じ判定。"""
    return sorted(
        d
        for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").is_file()
    )
