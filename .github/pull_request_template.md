## 何を変えたか

<!-- 追加・更新したスキル名と、変えた狙いを 1〜3 行で -->

## 確認

- [ ] `make check` が通る（CI でも走る）
- [ ] 新規スキルなら `marketplace.json` の `skills` 配列に足した
- [ ] `description` に呼ばれたい場面を書いた（ここが薄いと呼ばれない）

## マージ後にやること

- [ ] Mac 2 台で `claude plugin update <plugin>@yike-kit` → 再起動
- [ ] claude.ai アカウントに配るなら `make build` して `dist/studio.plugin` を上げ直す
