# yike-kit

Claude のスキルを 1 箇所で管理し、2 台の Mac と 2 つの claude.ai アカウントへ配るためのリポジトリ。

## 構成

| プラグイン | 中身 | 配布先 |
|---|---|---|
| `pr-flow` | be-pr-create, fe-pr-create | Mac のみ（git を触るため） |
| `studio` | web-image-builder, icon-builder, eli15, paas-onboarding | Mac + 会社/個人アカウント |

分割の軸は「機能」ではなく **誰に配るか**。アカウントへ上げるのは `studio` だけで済む。

## Mac への導入（各マシンで 1 回）

```bash
claude plugin marketplace add git@github.com:<you>/claude-kit.git
claude plugin install pr-flow@yike-kit
claude plugin install studio@yike-kit
```

private リポジトリでも動く。**SSH リモートを使うこと** — バックグラウンド自動更新が
ssh-agent でそのまま認証できる。HTTPS を使うなら先に `gh auth setup-git` を実行しておく。

`~/.claude/settings.json` に入れておくと、pull 失敗時に既存の clone を捨てずに済む。

```json
{ "env": { "CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE": "1" } }
```

`marketplace.json` に `version` を書かないこと。書くと毎回上げない限り更新が止まる。
省略していればコミット SHA を追って自動更新される。

## アカウント（Claude Desktop / iPhone）への配布

アカウント側は GitHub を見に行かない。**ここだけは手作業になる。**

```bash
make release        # dist/studio.plugin ができる
```

`dist/studio.plugin` を **Customize > Plugins** に上げる。会社と個人で1回ずつ、計2回。
中に studio の4本が入っているので、これ1ファイルで済む。

`pr-flow` は手元の git を触るので、アカウントには上げない。Mac 側の自動更新だけで足りる。

呼び出し名は Mac もアカウントも `/studio:eli15` で揃う。プラグイン名を合わせてあるため。

**素の `/eli15` を使いたい場合だけ**、`dist/skills/eli15.zip` を Customize > Skills に上げる。
スキル1本 = zip 1つなので、増やすほど手作業が増える。

**Customize > Plugins の「Add from a repository」は当てにしない。**
git URL を登録できるが、Cowork でスキルが読まれない不具合の報告がある。試すのは自由。

会社が Team / Enterprise プランなら、組織設定からアップロードして全員に配る手もある。

## 入れていないもの

`docx` / `pptx` / `xlsx` / `pdf` / `skill-creator` は Anthropic の Proprietary ライセンス。
リポジトリには置かない。アカウント側で有効化したまま使う。
