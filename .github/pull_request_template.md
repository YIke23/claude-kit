## 何を変えたか

<!-- 追加・更新したスキル名と、変えた狙いを 1〜3 行で -->

## 確認

- [ ] `make check` が通る（CI でも走る）
- [ ] 新規スキルなら `marketplace.json` の `skills` 配列に `./<name>` を足した
- [ ] `description` に呼ばれたい場面を書いた（ここが薄いと呼ばれない）

## マージ後にやること

- [ ] 開発機は不要（`make sync` が `--ff-only` まで済ませている）
- [ ] プラグインで入れている Mac は `claude plugin update <plugin>@yike-skills` → 再起動
- [ ] claude.ai アカウントに配るなら `make build` して `dist/studio.plugin` を上げ直す
