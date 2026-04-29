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

### トーンモード指定（v0.3.0 で 5 モードに拡張）

書き直しのトーンを 5 つから選択できる。指定がない場合は **standard**。

| モード | 用途 | 特徴 |
|---|---|---|
| `business` | 企業お知らせ・営業文・公式リリース | 敬体維持、定型挨拶残す、「させていただく」段落1回まで、意見追加は控えめ |
| `standard` | ブログ・一般記事（デフォルト） | 敬体／常体ミックス、一人称あり、意見あり、リズム変化 |
| `note-style` | note・Medium・公開エッセイ | 敬体中心、一人称「私」、意見あり、刺は控えめ、polish 度高（v0.3.0 で追加） |
| `casual` | SNS・個人ブログ・チャット | 常体中心、口語・体言止めOK、刺やユーモア強め |
| `technical-neutral` | 技術解説・Wikipedia 風 | 敬体／常体は原文準拠、一人称ゼロ、意見追加なし、事実のみ。API リファレンス／チュートリアル／解説記事のサブ規約あり（v0.3.0 で追加） |

```
/humanizer-ja business

[ビジネス文書をここに貼る]
```

```
note-style モードで書き直して：
[note 記事の下書き]
```

```
casual モードで書き直して：
[SNS 投稿のドラフト]
```

```
technical-neutral モードで humanize：
[API ドキュメント／チュートリアル／解説記事の原稿]
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

## 検出するパターン（33個）

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

### rewriter 自身が再導入しがちなパターン（32〜33、v0.3.1 で追加）

humanize の過程で、rewriter（Claude / GPT 等）自身が「人間らしさ」を演出しようとして無自覚に再導入しがちな癖。最終 anti-AI パスの Step 2 チェックリストで明示的に検査される。

- 「効いた」型の経験談ぶり構文（一番効いた、実際に効いた、地味にきく、刺さった、ハマった など）
- 説明の（カッコ）多用（用語のたびに定義を括弧で挟む癖、「（例：〜）」の連発）

両者とも v0.3.0 公開後にユーザーから「自分の出力で再導入している」との指摘を受け、独立パターン化された。

### 英語固有のため非対応のパターン

upstream に含まれる以下のパターンは英語の構造に依存するため非対応：`-ing` 語尾、is/are 回避、negative parallelisms、em dash 濫用、Title Case、curly quotes、ハイフン複合語。詳細は `SKILL.md` 末尾の appendix を参照。

## 由来とクレジット

- 原案：[blader/humanizer](https://github.com/blader/humanizer) by Siqi Chen（MIT License）
- そのさらなる土台：[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（CC BY-SA, by WikiProject AI Cleanup）
- 日本語パターンの設計、トーンモード、Before / After 例：本リポジトリ独自

英語パターンを翻訳したものではなく、日本語の AI 生成文に特有の癖を再収集しています。英語の文章を扱う場合は本家 [blader/humanizer](https://github.com/blader/humanizer) を併用してください。

## 検証レポート

v0.3.0 の検証結果を [EVALUATION.md](./EVALUATION.md) に記載しています（v0.1.0 / v0.2.0 の検証履歴は git コミット履歴から参照可能）。

v0.3.0 検証のハイライト：

- **5 モード機能性**：5 モードすべてで期待通りの書き分け（◎×5）。note-style の追加で business と standard の中間域がカバーされた。
- **AskUserQuestion ガードレール**：6 サンプルで決定木検証 → 6/6 で期待通り発火／非発火（実機ライブテストは別環境で必要）。
- **rewriter 自己 AI 臭再導入チェック**：意図的に問題を含む書き直し版に対し、Step 2 チェックリストが 4/4 検出。
- **5 モード自動推定**：8 サンプルで 8/8 正解（v0.2.0 の 5/6 から改善）。
- **technical-neutral サブ規約**：API リファレンス／チュートリアル／解説記事 で異なる慣習を明示的に扱える。

評価方法の限界：

- 単一モデル自己評価（書き直し・採点ともに Claude が実施、独立性なし）
- 実機 `AskUserQuestion` 動作の確認は別環境必要
- 盲検人間評価は本リポジトリ内では実施不可、EVALUATION.md 末尾に **ユーザー側で実施するための推奨手順**を記載

実利用前には以下を強く推奨：

1. ローカル Claude Code で humanizer-ja をロードし AskUserQuestion 動作を確認
2. EVALUATION.md 記載の盲検評価手順を 3 名以上の評価者で実施
3. business / technical-neutral モードの出力は人間の最終チェックを通す

## ライセンス

MIT License。詳細は [LICENSE](./LICENSE) を参照。本家 `humanizer` の著作権表示も保持しています。

## 貢献・サンプル投稿

実 AI 出力と望ましい humanize 結果のペアを投稿してください。新パターン発見・既存パターン精度測定・モード自動推定改善の根拠データになります。

### 投稿方法（2 通り）

| 方法 | 向いている人 | 流れ |
|---|---|---|
| **PR** | GitHub に慣れている | `samples/pairs/NNN-<mode>-<short-description>.md` を追加 → PR テンプレートに沿って情報を埋める |
| **Issue** | GitHub に不慣れ | [Sample submission Issue](https://github.com/DSasakiBusiness/humanizer-ja/issues/new?template=sample-submission.md) テンプレートに貼り付け → メンテナがファイル化 |

詳細は [samples/CONTRIBUTING.md](./samples/CONTRIBUTING.md) を参照。投稿前に必ず以下を確認してください：

- **著作権**：自分の AI 入出力か、自分が書いた文章のみ。第三者ブログのスクレイピングは不可
- **個人情報**：氏名・社内固有名詞は仮名・架空数値で置換
- **ライセンス同意**：MIT で収録されることに同意

### 既存サンプル

[samples/pairs/](./samples/pairs/) に v0.3.1 時点で 5 件（各モード 1 件）のシードサンプルあり。

### パターン追加・改善の提案

新しい AI 臭パターンの追加や既存パターン改善は [Pattern suggestion Issue](https://github.com/DSasakiBusiness/humanizer-ja/issues/new?labels=pattern-suggestion&title=%5BPattern%5D+) からどうぞ。Before / After 例があると採用されやすいです。
