# yike-kit

Claude のスキルを 1 箇所で管理し、2 台の Mac と 2 つの claude.ai アカウントへ配るリポジトリ。
構成は [anthropics/skills](https://github.com/anthropics/skills) に合わせてある。

## 構成

```
.claude-plugin/marketplace.json   どのスキルをどのプラグインに束ねるかの定義
skills/<skill-name>/SKILL.md      スキル本体。1 フォルダ 1 スキル、フラットに並べる
template/SKILL.md                 新しいスキルを作るときの雛形
scripts/                          アカウント配布用のビルドと、push 前の点検
```

スキルの所属はフォルダ構造ではなく `marketplace.json` の `skills` 配列で決まる。
束ね方を変えたいときは JSON を直すだけでよく、ファイルは動かさない。

| プラグイン | 中身 | 配布先 |
|---|---|---|
| `studio` | web-image-builder, icon-builder, eli15, paas-onboarding | Mac + claude.ai アカウント |
| `pr-flow` | be-pr-create, fe-pr-create | Mac のみ（手元の git を触るため） |

呼び出しは `/studio:eli15` のように `プラグイン名:スキル名` になる。

## Mac への導入（各マシンで 1 回）

```bash
claude plugin marketplace add git@github.com:<you>/claude-kit.git
claude plugin install studio@yike-kit
claude plugin install pr-flow@yike-kit
```

**SSH リモートを使うこと。** HTTPS だと最初の登録は通るのに、バックグラウンドの
自動更新だけが無言で失敗する。HTTPS を使うなら先に `gh auth setup-git` を実行しておく。

取得に失敗したとき既存の複製を捨てないよう、`~/.claude/settings.json` に足しておく。

```json
{ "env": { "CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE": "1" } }
```

`marketplace.json` のプラグイン項目に `version` を書かないこと。
書くとリリースごとに上げない限り更新が止まる。省略していればコミットを追って自動更新される。

## claude.ai アカウントへの配布

アカウント側は GitHub を見に行かない。ここだけ手作業になる。

```bash
make build          # dist/ に .plugin と skills/*.zip ができる
```

`dist/studio.plugin` を **Customize > Plugins** に上げる。会社と個人で 1 回ずつ、計 2 回。
4 スキルが 1 ファイルに入っているので、これだけで済む。

素の `/eli15` で呼びたい場合だけ `dist/skills/eli15.zip` を **Customize > Skills** に上げる。
スキル 1 本 = zip 1 つなので、増やすほど手作業が増える。

`pr-flow` はアカウントに上げない。手元の git を触るスキルなので使い道がない。

## スキルを追加・更新する

`main` へ直接 push しない。ブランチを切って PR を出し、GitHub でマージする。
PR では CI が `make check` を走らせるので、壊れた SKILL.md が main に入らない。

```bash
git switch -c skill/<name>
# skills/<name>/SKILL.md を書く（template/SKILL.md をコピーして始める）
# 新規なら marketplace.json の skills 配列に ./skills/<name> を足す
make check
git add -A && git commit -m "add: <name> スキルを追加"
git push -u origin skill/<name>
gh pr create
```

check が緑になったら GitHub でマージする。マージ後の反映は次節。

`make check` は SKILL.md の `name` とフォルダ名の一致、`description` の有無と長さ、
どのプラグインにも属していないスキルを見る。description が 1536 字を超えると
切り捨てられて意図した場面で呼ばれなくなるため、ここで止める。

## マージしたあとの反映

**Mac は放っておいても追いつかない。** `marketplace update` は marketplace の複製を
新しくするだけで、入っているプラグインの版は切り替わらない。各プラグインを明示的に
更新して、セッションを再起動する。

```bash
claude plugin marketplace update yike-kit
claude plugin update studio@yike-kit
claude plugin update pr-flow@yike-kit
```

反映できたかは `plugin list` の SHA ではなく、**再起動後の新規セッションで
`/studio:<skill>` が候補に出るか**で確かめる。`plugin validate` も `plugin details` も
名前空間の問題は素通りするので、この 2 つを根拠にしない。

claude.ai アカウントへ配るスキルを触ったなら、`make build` して
`dist/studio.plugin` を上げ直す。

## 入れていないもの

`docx` / `pptx` / `xlsx` / `pdf` / `skill-creator` は Anthropic の Proprietary ライセンス。
リポジトリには置かない。claude.ai アカウント側で有効にしたまま使う。
