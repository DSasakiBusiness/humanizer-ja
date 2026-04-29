---
name: サンプル投稿（Before / After ペア）
about: AI 出力と望ましい humanize 結果のペアを投稿します
title: "[Sample] "
labels: ["sample-submission"]
assignees: []
---

## 投稿前の必須確認

以下すべてに該当することを確認してください（チェックを付けてください）：

- [ ] 投稿する Before / After 両方について、私が投稿する権利を持っています
- [ ] 個人情報・社内固有名詞は含まれていません（仮名・架空数値で置換済み）
- [ ] MIT ライセンスでの収録に同意します
- [ ] 第三者のブログや記事をスクレイピングしたものではありません

## モード

該当するものに `x` を入れてください：

- [ ] business（企業お知らせ・営業文・公式リリース）
- [ ] standard（ブログ・一般記事）
- [ ] note-style（note・Medium・公開エッセイ）
- [ ] casual（SNS・個人ブログ・チャット）
- [ ] technical-neutral（技術解説・Wikipedia 風）

## 元 AI のソース

該当するものに `x` を入れてください：

- [ ] claude-opus-4-7
- [ ] claude-sonnet
- [ ] chatgpt-4o / chatgpt-5
- [ ] gemini-2 / gemini-pro
- [ ] その他（モデル名を記載）：
- [ ] synthetic（手で AI 風に書いたもの）
- [ ] unknown

## Before（AI 出力）

```
[ここに AI 出力をそのまま貼ってください]
```

## After（望ましい humanize 結果）

```
[humanizer-ja で書き直したもの、または手で書き直したものを貼ってください]
```

## AskUserQuestion 該当

書き直し前にユーザーへ具体情報の質問が必要だった場合、その内容を記載：

- [ ] 該当なし（一般論や具体情報が揃っている場合）
- [ ] 該当あり（下記に記載）

質問内容（該当ありの場合）：

```
[例：「新サービス」が何のサービスか、リリース日、業績数値 など]
```

## 発火パターン

検出されたパターン番号を [SKILL.md](../SKILL.md) から拾って記載（分かる範囲で OK、不明なら空欄可）：

例：`[1, 2, 11, 17]`

## Notes（任意）

- なぜこのモードを選んだか
- 副作用や残課題
- 気になった点

## クレジット

- GitHub ハンドル：（例：@DSasakiBusiness、anonymous 希望ならその旨記載）
