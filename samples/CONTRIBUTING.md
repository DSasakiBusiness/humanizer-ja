# humanizer-ja サンプル投稿ガイド

実 AI 出力と「望ましい humanize 結果」のペアを投稿してください。投稿物は humanizer-ja のルール改善・モード調整・新パターン発見の根拠データとして使われます。

## 投稿前の必須確認（3 項目）

すべて満たすことを確認してから投稿してください：

1. **著作権**：投稿する文章のすべてについて、あなたが投稿する権利を持っていること。具体的には：
   - **AI 出力（Before）**：あなた自身が ChatGPT / Claude / Gemini 等に入力して受け取った出力、または明示的に再配布許可された出力。
   - **書き直し（After）**：あなた自身が書いた、または humanizer-ja を使って生成した出力。
   - **他人のブログ・記事のスクレイピングは禁止**（著作権侵害となります）。
2. **個人情報**：氏名・住所・電話番号・メールアドレス・社内固有名詞（プロジェクト名、製品コードネーム）を含まないこと。仮名・架空の数値に置換してください。
3. **ライセンス同意**：投稿物を **MIT ライセンス**（または互換）で本リポジトリに収録することに同意すること。

## 投稿方法

### 方法 A：Pull Request（推奨）

GitHub に慣れている場合の手順：

1. リポジトリを fork
2. `samples/pairs/` に新しいファイルを追加
   - 名前：`NNN-<mode>-<short-description>.md`（例：`006-business-press-release.md`）
   - 番号 NNN：既存ファイルの最大番号 +1
3. 下記「ファイル形式」に従って記述
4. PR 作成時のテンプレートに従って情報を埋める

### 方法 B：Issue（GitHub に不慣れな場合）

1. [Issue を新規作成](https://github.com/DSasakiBusiness/humanizer-ja/issues/new/choose)
2. 「Sample submission」テンプレートを選択
3. テンプレートに沿って Before / After を貼り付け
4. メンテナがファイル化して PR を作成します

## ファイル形式

`samples/pairs/NNN-<mode>-<short-description>.md` の中身：

```markdown
---
id: NNN
mode: business | standard | note-style | casual | technical-neutral
source: claude-opus-4-7 | chatgpt-4o | gemini-2 | synthetic | own-writing | unknown
license: MIT
contributor: <your-handle> | anonymous
patterns: [1, 2, 11]
askuserquestion: true | false
---

# タイトル（モード名を含めると探しやすい）

## Before

> [AI 出力をそのまま貼る。複数段落OK]

## After

> [humanize 後の文章]

## Notes

- どのパターンが何回発火したか
- なぜそのモードが適切と判断したか
- AskUserQuestion で何を補完したか（該当する場合）
- 副作用・残課題・気になる点
```

### frontmatter フィールドの意味

| フィールド | 説明 |
|---|---|
| `id` | 連番（ファイル名と一致） |
| `mode` | 5 モードのいずれか |
| `source` | 元の AI 出力の生成元。`synthetic` は手で AI 風に書いたもの。`own-writing` は投稿者が AI を真似て書いた文 |
| `license` | MIT または互換ライセンス |
| `contributor` | GitHub ハンドル、ニックネーム、または `anonymous` |
| `patterns` | SKILL.md のパターン番号配列 |
| `askuserquestion` | 書き直し前に質問が必要だった場合 true |

## 採用基準

すべての投稿を必ず採用するわけではありません。下記を満たすものを優先採用します：

- **AI 臭が明確**：Before に humanizer-ja のパターン 1 つ以上が確実に発火
- **書き直しが妥当**：After が指定モードのトーン規約に整合し、意味を歪めていない
- **モード判断が適切**：選んだモードが文書の用途に合っている
- **重複が少ない**：既存サンプルと類似度が高すぎないこと

採用されない場合も、コメントで理由をフィードバックします。

## 不採用となるもの

- 著作権の確認が取れない第三者の文章
- PII が含まれているもの
- AI 臭の検出が困難な、ほぼ人間が書いた文章を「Before」として投稿したもの
- 投稿者がライセンス同意を明確にしていないもの

## 投稿者へのクレジット

- frontmatter の `contributor` フィールドに記載
- メジャーバージョンリリース時の CHANGELOG / リリースノートで言及
- `anonymous` を希望する場合はその旨明記

## 質問・相談

投稿前に「これは投稿していい？」と確認したい場合は、[Discussions](https://github.com/DSasakiBusiness/humanizer-ja/discussions) または Issue で気軽に相談してください。
