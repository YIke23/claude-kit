---
name: "fe-pr-create"
description: "フロントエンド(FE)のPull Requestを自動作成する。ブランチ名からチケット番号を抽出し、git diffを解析してUI/OpenAPI型定義/テストに分類し、規定テンプレートに沿ったPR本文を生成してgh CLIでPRを作成する。「FEのPRを作って」「PR作成」等で使用。"
---

## FE PR自動作成 skill

フロントエンド(FE)のPull Requestを、規定テンプレートに沿って自動作成する。

### 前提

- カレントディレクトリがgit管理下のFEリポジトリであること。
- privateリポジトリでも問題ない。`gh` CLIはユーザーのローカル認証を使うため、認証済みなら作成できる。

### 手順

#### 1. リポジトリ状態を確認

以下をbashで実行し、現状を把握する。

```bash
git rev-parse --abbrev-ref HEAD                 # 現在のブランチ名
git log --oneline origin/HEAD..HEAD 2>/dev/null || git log --oneline -20   # ベースからのコミット
git remote get-url origin                       # リモート確認
```

ベースブランチが不明な場合は `main` → `master` → `develop` の順で存在するものを使う。以下で確認できる。

```bash
git rev-parse --verify origin/main 2>/dev/null || git rev-parse --verify origin/develop 2>/dev/null
```

#### 2. 変更内容を取得

ベースブランチとの差分を取得する（`<base>` は手順1で決めたベースブランチ）。

```bash
git diff --stat origin/<base>...HEAD
git diff origin/<base>...HEAD
git log origin/<base>..HEAD --pretty=format:'%s%n%b'
```

未pushのブランチの場合は `origin/<base>...HEAD` の代わりに `<base>...HEAD` を使う。

#### 3. チケット番号を抽出

ブランチ名からチケット番号を自動抽出する。例:

- `feature/PROJ-123-add-login` → `PROJ-123`
- `fix/ABC-45_bugfix` → `ABC-45`
- `123-something` → `123`

正規表現の目安: `[A-Z]+-[0-9]+` を優先し、なければ先頭付近の数値列を使う。抽出できない場合はユーザーにチケット番号（またはチケットURL）を尋ねる。

#### 4. 変更を分類

git diffの変更ファイルを解析し、テンプレートの各セクションに振り分ける。

- **UI**: コンポーネント/ページ/スタイル系の変更（例: `.tsx`, `.vue`, `.css`, `pages/`, `components/`, `features/` 配下など）。
  - 見出し4(`####`)でページタイトル（またはコンポーネント名/画面名）を列挙し、その下に修正内容を箇条書き。
- **OpenAPI型定義**: 自動生成された型やAPIクライアントの変更（例: `openapi`, `generated`, `api/`, `*.gen.ts`, `schema` を含むパス）。修正内容を文章で説明。
- **テスト**: テストファイルの変更（例: `*.test.*`, `*.spec.*`, `__tests__/`, `.stories.*`）。テスト内容を箇条書き。

該当がないセクションは、テンプレートのコメントを残しつつ本文は空にする（エンジニアが後で追記できるように）。推測が難しい箇所（関連PR、スクショ、レビュワー向け事項の詳細）はテンプレートのコメントをそのまま残す。

#### 5. PR本文を組み立て

以下のテンプレートに埋める。`{{チケット番号}}` は手順3の値に置換する。「概要」直下のtodoリストは、コミットメッセージとdiffから要件を推測してチェック済み(`- [x]`)の箇条書きにする。

```markdown
## 概要

{{チケット番号}}

- [x] （要件をtodoリストで箇条書き。コミット/diffから推測）

### 関連するPR
- 
<!--
詳細はエンジニアが記載
-->

## 修正内容
### UI
#### （ページタイトル）
- （修正内容を箇条書き）

### OpenAPI型定義
（OpenAPI型定義の修正内容を説明。無ければコメントのまま空欄）
<!--
OpenAPI型定義の修正内容を説明
-->

### テスト
- （テスト内容を箇条書き）

## 動作確認（スクショなど）
<!--
見出し3でスクショ箇所を列挙。詳細はエンジニアが書く。
-->

## レビュワー向け事項
<!--
見出し3で項目列挙。Local環境でのUI確認方法、テスト方法、Storybookなど。
-->
```

**タイトル**: `[{{チケット番号}}] <変更概要>` の形式。変更概要はコミット/diffから簡潔に。

#### 6. 内容をユーザーに提示して確認

生成したPRタイトルと本文をユーザーに提示し、作成してよいか確認する。修正指示があれば反映する。

#### 7. PRを作成

`gh` CLIが利用可能かつ認証済みか確認する。

```bash
gh auth status
```

利用可能なら、本文を一時ファイルに書き出してPRを作成する。

```bash
gh pr create --base <base> --head <current-branch> \
  --title "<タイトル>" --body-file /tmp/pr_body.md --draft
```

- デフォルトはdraft(`--draft`)で作成する。ユーザーが通常PRを希望する場合は `--draft` を外す。
- 作成後、`gh pr view --web` のURLをユーザーに返す。
- ブランチが未pushの場合は先に `git push -u origin <current-branch>` が必要。ユーザーに確認してからpushする。

**フォールバック**: `gh` が未インストール/未認証、またはprivate参照不可などで作成できない場合は、生成したPRタイトルと本文(Markdown)をそのまま出力し、ユーザーが手動でPRを作成できるようにする。

### 注意

- 破壊的な操作（push、PR作成）は必ずユーザー確認後に実行する。
- 機微情報（トークン、認証情報）を本文に含めない。
- 推測できない項目は空欄＋コメントで残し、埋めすぎない。

