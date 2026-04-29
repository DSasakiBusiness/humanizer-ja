# samples/

humanizer-ja のパターン改善・モード調整・検証強化のための **Before / After サンプル集** です。

実 AI 出力（ChatGPT / Claude / Gemini など）と、それを humanizer-ja で書き直した版をペアで保管します。新パターンの発見、既存パターンの精度測定、モード自動推定の改善、すべての根拠データになります。

## ディレクトリ構成

```
samples/
├── README.md            ← 本ファイル
├── CONTRIBUTING.md      ← 投稿ガイド（PR / Issue どちらも可）
└── pairs/               ← Before / After ペア
    ├── 001-business-quarterly-report.md
    ├── 002-standard-blog-side-job.md
    ├── 003-note-style-remote-work.md
    ├── 004-casual-sns-gadget.md
    └── 005-technical-neutral-oauth.md
```

## サンプルの種類

各ペアファイルは frontmatter で属性を明記します：

- `mode`: business / standard / note-style / casual / technical-neutral
- `source`: Synthetic / claude-opus / chatgpt-4o / gemini-2 / unknown / 投稿者本人の文章 など
- `license`: MIT / CC0 / CC BY / その他
- `patterns`: 検出された SKILL.md パターン番号
- `contributor`: 投稿者ハンドル（任意・anonymous 可）

## 現在のシードサンプル

v0.3.1 時点で以下 5 件（各モード 1 件）。EVALUATION.md の検証で使用したものを正規化したもの。

| # | タイトル | モード | パターン |
|---|---|---|---|
| 001 | 四半期業績概況のドラフト | business | 1, 2, 3, 4, 11, 17, 18 |
| 002 | 副業の始め方ブログ冒頭 | standard | 1, 2, 3, 5, 7, 14, 17, 18, 26 |
| 003 | リモートワーク3年で学んだこと | note-style | 1, 2, 3, 5, 7, 12, 14, 17, 18, 22, 26 |
| 004 | 新しいガジェットの SNS 投稿 | casual | 1, 10, 11, 22, 26 |
| 005 | OAuth 2.0 とは | technical-neutral | 1, 2, 3, 10, 15, 17, 29 |

## 投稿方法

詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) を参照。要約：

1. **PR で投稿**：`pairs/` に新ファイルを追加（番号は連番）。
2. **Issue で投稿**：GitHub の Issue テンプレートから貼り付けるだけ。後でメンテナがファイル化します。

どちらの方法でも、**著作権と個人情報の確認は必須**です。

## 利用上の注意

- ここに収録されているサンプルはすべて **MIT ライセンス** または投稿者が指定した互換ライセンスです。
- 個人を特定できる情報（PII）を含むサンプルは収録しません。
- 商用利用も MIT の範囲で可能です。
