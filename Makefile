.PHONY: build check clean

## claude.ai アカウントに上げる dist/*.plugin と dist/skills/*.zip を作る
build: check
	@python3 scripts/build.py

## push 前の自己点検
check:
	@python3 scripts/validate.py

clean:
	@rm -rf dist
