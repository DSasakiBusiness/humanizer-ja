# humanizer-ja

日本語の AI 生成テキストから「いかにも AI が書いた感」を取り除き、自然な日本語に書き直す Claude Code / OpenCode 向けスキルです。

[blader/humanizer](https://github.com/blader/humanizer)（MIT License, Siqi Chen 作）の非公式日本語派生版で、英語向けに最適化された原版では検出できない日本語固有の AI 文体パターン（過剰な敬体、抽象名詞化、「〜ということができる」型の冗長表現、決まり文句の枕詞、伝聞逃げ、太字の濫用、媚び表現 など）を扱います。

> **Disclaimer**: 本リポジトリは [blader/humanizer](https://github.com/blader/humanizer) の作者・管理者とは無関係の非公式プロジェクトです。問い合わせは本リポジトリの Issue にお願いします。

## インストール

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/DSasakiBusiness/humanizer-ja.git ~/.claude/skills/humanizer-ja
```

### OpenCode

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/DSasakiBusiness/humanizer-ja.git ~/.config/opencode/skills/humanizer-ja
```

`name: humanizer-ja` で登録されるため、本家 `humanizer` と同時インストールしても衝突しません。

## 使い方

### 基本

```
/humanizer-ja

[ここに直したい日本語テキストを貼る]
```

または直接お願いする：

```
このテキストを humanizer-ja で自然な日本語に直して：
[テキスト]
```

### トーンモード指定（v0.2.0 で追加）

書き直しのトーンを4つから選択できる。指定がない場合は **standard**。

| モード | 用途 | 特徴 |
|---|---|---|
| `business` | 企業お知らせ・営業文・公式リリース | 敬体維持、定型挨拶残す、「させていただく」段落1回まで、意見追加は控えめ |
| `standard` | ブログ・一般記事（デフォルト） | 敬体／常体ミックス、一人称あり、意見あり、リズム変化 |
| `casual` | SNS・個人ブログ・チャット | 常体中心、口語・体言止めOK、刺やユーモア強め |
| `technical-neutral` | 技術解説・Wikipedia 風 | 敬体／常体は原文準拠、一人称ゼロ、意見追加なし、事実のみ |

```
/humanizer-ja business

[ビジネス文書をここに貼る]
```

```
casual モードで書き直して：
[SNS 投稿のドラフト]
```

```
technical-neutral モードで humanize：
[技術解説の原稿]
```

明示指定がない場合は、原文の特徴（敬体率、カタカナビジネス語の有無、一人称の有無 など）から自動推定する。曖昧なときは確認を求める。

### 文体キャリブレーション（任意）

自分の過去の文章を渡すと、その文体に寄せて書き直します。モードと併用可：

```
/humanizer-ja business

私の文体サンプル：
[自分が書いた文章を 2〜3 段落]

このテキストを書き直して：
[直したいテキスト]
```

## 検出するパターン（31個）

`SKILL.md` に全パターンの Before / After 例つきで記載。

### 内容パターン（1〜18）

- 重要性インフレ、抽象名詞化、「〜することができる」型の冗長表現、断定回避、枕詞、伝聞逃げ、空疎な総括、機械的接続詞、カタカナビジネス語、形容語の過多、過剰敬体、三点列挙、文末リズム単調、メタ表現、両論併記の毒抜き、比喩テンプレ、「〜が大切です」型お説教、「〜していきたい」型未来志向

### 文体・装飾パターン（19〜25、v0.2.0 で追加）

- **太字（`** **`）の濫用** ← AI 出力で最も視覚的に分かりやすい AI 臭
- インラインヘッダ式箇条書き
- 絵文字の機械的配置
- 細切れ見出し（一行言い直しパターン）
- 同義語サイクリング
- 偽範囲（「A から Z まで」型）
- 主語省略・受動態の濫用

### チャットボット痕跡パターン（26〜29、v0.2.0 で追加）

- チャットボット痕跡（「お役に立てれば幸いです」など）
- 媚び・過剰肯定（「素晴らしいご質問ですね」など）
- 知識カットオフ言い訳（「私の学習データの範囲では」など）
- 権威ぶり構文（「本質的には」「真に重要なのは」など）

### 構造パターン（30〜31、v0.2.0 で追加）

- 知名度・媒体露出インフレ
- 「課題と展望」型の定型セクション

### 英語固有のため非対応のパターン

upstream に含まれる以下のパターンは英語の構造に依存するため非対応：`-ing` 語尾、is/are 回避、negative parallelisms、em dash 濫用、Title Case、curly quotes、ハイフン複合語。詳細は `SKILL.md` 末尾の appendix を参照。

## 由来とクレジット

- 原案：[blader/humanizer](https://github.com/blader/humanizer) by Siqi Chen（MIT License）
- そのさらなる土台：[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（CC BY-SA, by WikiProject AI Cleanup）
- 日本語パターンの設計、トーンモード、Before / After 例：本リポジトリ独自

英語パターンを翻訳したものではなく、日本語の AI 生成文に特有の癖を再収集しています。英語の文章を扱う場合は本家 [blader/humanizer](https://github.com/blader/humanizer) を併用してください。

## 検証レポート

v0.1.0 と v0.2.0 のルールが実際に日本語の不自然さを除去できるかを検証した結果を [EVALUATION.md](./EVALUATION.md) に記載しています。

v0.1.0 でのハイライト：

- ベストケース：原文に情報がある技術解説では期待通り機能（◎）
- 要注意：内容の薄い AI 文（企業お知らせ、商品紹介）では内容を補う越権が起きやすい（△）
- 既知の弱点：フォーマル度の自動判定がないため、ビジネス文書ではサンプル提供が必須

v0.2.0 で対応：

- トーンモード4個で「ビジネス文書が砕けすぎる」問題を解消
- 具体情報がない原文には `AskUserQuestion` で要求するルールを SKILL.md に明記
- 太字濫用、媚び表現など13パターンを追加で検出

評価方法の限界：単一モデルによる自己評価のため、実環境では人間による盲検評価を推奨。

## ライセンス

MIT License。詳細は [LICENSE](./LICENSE) を参照。本家 `humanizer` の著作権表示も保持しています。

## 貢献

- 検出すべき日本語 AI パターンの追加・改善 PR は歓迎します。
- Before / After の実例（実際の AI 出力と望ましい修正例）を添えると採用されやすいです。
- 既存パターンの改善、特に各モード向けの After 例の追加も歓迎します。
