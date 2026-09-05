.PHONY: build check clean hooks sync

## claude.ai アカウントに上げる dist/*.plugin と dist/skills/*.zip を作る
build: check
	@python3 scripts/build.py

## push 前の自己点検
check:
	@python3 scripts/validate.py

## 作業ツリーの変更を PR 経由で main へ届ける（make sync m="fix: ..."）
sync: check
	@scripts/sync.sh "$(m)"

## pre-push フックを有効にする。各マシンで 1 回だけ
hooks:
	@git config core.hooksPath .githooks
	@echo 'core.hooksPath = .githooks（push 前に make check、main 直 push は拒否）'

clean:
	@rm -rf dist
