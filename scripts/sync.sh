#!/usr/bin/env bash
# 作業ツリーの変更を PR 経由で main まで届ける。
#
# ~/.claude/skills はこのリポジトリの作業ツリーそのもので、動いている Claude が
# 直接そこを読んでいる。ブランチを切り替えると目の前でスキルが入れ替わるので、
# ローカルは main のまま動かさない。push 先だけ sync/<日時> ブランチにする。
set -euo pipefail

msg="${1:-}"
if [ -z "$msg" ]; then
	echo 'ERROR: コミットメッセージが要る。make sync m="fix: ..."' >&2
	exit 1
fi

branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" != "main" ]; then
	echo "ERROR: main で実行すること（今は $branch）。sync はブランチを切り替えない前提で組んである。" >&2
	exit 1
fi

git fetch --quiet origin main
read -r behind ahead < <(git rev-list --left-right --count origin/main...HEAD | tr '\t' ' ')

if [ "$behind" -gt 0 ] && [ "$ahead" -gt 0 ]; then
	echo "ERROR: ローカル main と origin/main が分岐している（behind $behind / ahead $ahead）。手で直すこと。" >&2
	exit 1
fi
if [ "$behind" -gt 0 ]; then
	echo "→ origin/main に $behind 件遅れているので先に追いつく"
	git merge --ff-only origin/main
fi

if [ -n "$(git status --porcelain)" ]; then
	git add -A
	git commit -q -m "$msg"
	echo "→ commit: $(git log --oneline -1)"
elif [ "$ahead" -eq 0 ]; then
	echo "変更がない。何もしない。"
	exit 0
else
	echo "→ 未 push のコミットが $ahead 件あるのでそれを送る"
fi

sync_branch="sync/$(date +%Y%m%d-%H%M%S)"
echo "→ push: $sync_branch"
git push --quiet origin "HEAD:refs/heads/$sync_branch"

pr=$(gh pr create --base main --head "$sync_branch" --title "$msg" --body "\
\`make sync\` から作った PR。

## 何を変えたか

$msg

## 確認

- [x] \`make check\`（pre-push フックで実行済み。CI でも走る）
")
echo "→ PR: $pr"

# チェックが登録されるまで少し待ってから見張る
for _ in 1 2 3 4 5 6 7 8 9 10; do
	if gh pr checks "$pr" >/dev/null 2>&1; then break; fi
	sleep 3
done
gh pr checks "$pr" --watch --fail-fast

gh pr merge "$pr" --merge
git push --quiet origin --delete "$sync_branch" || true

git fetch --quiet origin main
git merge --ff-only origin/main
echo "→ main: $(git log --oneline -1)"

if [ -n "$(git status --porcelain)" ]; then
	echo "WARN: 作業ツリーに差分が残っている" >&2
	git status --short >&2
fi
