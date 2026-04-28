# humanizer-ja

日本語の AI 生成テキストから「いかにも AI が書いた感」を取り除き、自然な日本語に書き直す Claude Code / OpenCode 向けスキルです。

[blader/humanizer](https://github.com/blader/humanizer)（MIT License, Siqi Chen 作）の非公式日本語派生版で、英語向けに最適化された原版では検出できない日本語固有の AI 文体パターン（過剰な敬体、抽象名詞化、「〜ということができる」型の冗長表現、決まり文句の枕詞、伝聞逃げ、など）を扱います。

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

```
/humanizer-ja

[ここに直したい日本語テキストを貼る]
```

または直接お願いする：

```
このテキストを humanizer-ja で自然な日本語に直して：
[テキスト]
```

### 文体キャリブレーション（任意）

自分の過去の文章を渡すと、その文体に寄せて書き直します：

```
/humanizer-ja

私の文体サンプル：
[自分が書いた文章を 2〜3 段落]

このテキストを humanizer-ja で書き直して：
[直したいテキスト]
```

## 検出する主なパターン

`SKILL.md` に詳細を記載。代表的なもの：

- 重要性インフレ（「重要な役割を果たしている」「不可欠な存在」）
- 抽象名詞化・漢語率の過剰（「〜性」「〜化」「〜的」連発）
- 「〜することができる」型の冗長表現
- 「〜と言えるでしょう」「〜と考えられます」など断定回避
- 「近年、〜が注目を集めています」型の枕詞
- 出典なしの「〜と言われています」「〜とされています」
- 「いかがでしたでしょうか」型の中身のない総括
- 「また、」「さらに、」「一方で、」の機械的接続詞
- カタカナビジネス語の濫用（「シナジー」「ソリューション」「コミット」）
- 文末リズムの単調さ（全文「〜です。」「〜ます。」）
- ほか多数

## 由来とクレジット

- 原案：[blader/humanizer](https://github.com/blader/humanizer) by Siqi Chen（MIT License）
- そのさらなる土台：[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（CC BY-SA, by WikiProject AI Cleanup）
- 日本語パターンの設計：本リポジトリ独自

英語パターンを翻訳したものではなく、日本語の AI 生成文に特有の癖を再収集しています。英語の文章を扱う場合は本家 [blader/humanizer](https://github.com/blader/humanizer) を併用してください。

## 検証レポート

v0.1.0 のルールが実際に日本語の不自然さを除去できるかを5つのサンプル（SEO記事、企業お知らせ、商品紹介、技術ブログ結論、技術解説）で検証した結果を [EVALUATION.md](./EVALUATION.md) に記載しています。

ハイライト：

- **ベストケース**：原文に情報がある技術解説では期待通り機能（◎）
- **要注意**：内容の薄い AI 文（企業お知らせ、商品紹介）では humanize 時に内容を補う越権が起きやすい（△）
- **推奨運用**：「具体情報を含む原文」+「Voice Calibration サンプル」のセットで使う
- **既知の弱点**：v0.1.0 ではフォーマル度の自動判定がないため、ビジネス文書ではサンプル提供が必須
- **評価方法の限界**：単一モデルによる自己評価のため、実環境では人間による盲検評価を推奨

## ライセンス

MIT License。詳細は [LICENSE](./LICENSE) を参照。本家 `humanizer` の著作権表示も保持しています。

## 貢献

- 検出すべき日本語 AI パターンの追加・改善 PR は歓迎します。
- Before / After の実例（実際の AI 出力と望ましい修正例）を添えると採用されやすいです。
