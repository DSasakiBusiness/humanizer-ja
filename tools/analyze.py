#!/usr/bin/env python3
"""
humanizer-ja コーパス分析スクリプト

日本語コーパス（livedoor news / CC-100 ja / Wikipedia 等）を読み込み、
SKILL.md の AI 臭パターンの出現頻度・記事率・1万字あたり率を集計する。

使い方:
  python3 analyze.py --corpus livedoor --input ~/Developer/jp-corpus/livedoor/text --output results/livedoor.json
  python3 analyze.py --corpus jsonl --input cc100_sample.jsonl --output results/cc100.json --max-articles 10000

出力:
  --output で指定した JSON ファイル + 同名 .md ファイル（読みやすいレポート）
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Pattern definitions（SKILL.md の 1〜33 パターンに対応）
# 完全一致ではなく代表的なシグナル語句で検出。誤検出を承知で頻度傾向を見る用途。
# ---------------------------------------------------------------------------
PATTERNS = {
    "1_重要性インフレ": [
        r"重要な役割を果た",
        r"欠かせない",
        r"不可欠な",
        r"象徴とも言える",
        r"代名詞",
        r"礎を築い",
        r"新たな地平",
        r"画期的な",
    ],
    "2_抽象名詞化": [
        r"利便性の向上",
        r"効率化の推進",
        r"最適化を図",
        r"生産性の向上",
        r"の実現を",
        r"の構築を",
        r"の確立を",
    ],
    "3_することができる": [
        r"することが可能",
        r"することができ",
    ],
    "4_断定回避": [
        r"と言えるでしょう",
        r"と考えられます",
        r"ではないでしょうか",
        r"と思われます",
        r"と推察されます",
    ],
    "5_枕詞": [
        r"近年[、,].{0,30}が注目",
        r"現代社会において",
        r"グローバル化が進む中",
        r"テクノロジーの進化に伴",
        r"重要性が高まっている昨今",
    ],
    "6_伝聞逃げ": [
        r"と言われています",
        r"とされています",
        r"考えられています",
        r"一般的に[^。]{0,30}と",
    ],
    "7_中身のない総括": [
        r"いかがでしたでしょうか",
        r"今後の動向に注目",
        r"ぜひ参考にし",
        r"皆さんも.{0,15}してみては",
        r"いかがでしょうか",
    ],
    "8_機械的接続詞": [
        r"\nまた[、,]",
        r"\nさらに[、,]",
        r"\n加えて[、,]",
        r"\n一方で[、,]",
        r"\nこのように[、,]",
    ],
    "9_カタカナビジネス語": [
        r"シナジー",
        r"ソリューション",
        r"ステークホルダー",
        r"コンセンサス",
        r"ペルソナ",
        r"アジェンダ",
        r"ナレッジ",
        r"アセット",
    ],
    "10_形容過多": [
        r"素晴らしい",
        r"魅力的な",
        r"興味深い",
        r"画期的な",
        r"優れた",
        r"洗練された",
        r"卓越した",
        r"革新的な",
        r"革命的な",
    ],
    "11_敬体過多": [
        r"させていただきます",
        r"させていただきたく",
        r"邁進してまいる",
        r"申し上げます",
    ],
    "12_三点列挙": [
        r"[、,][^、,。]{2,30}[、,][^、,。]{2,30}[、,]そして",
        r"[、,][^、,。]{2,30}[、,][^、,。]{2,30}[、,]さらに",
    ],
    "13_文末リズム単調_です連発": [
        # 3 連続以上の「です。」
        r"です。[^。]{0,80}です。[^。]{0,80}です。",
    ],
    "14_メタ表現": [
        r"本記事では",
        r"本稿では",
        r"以下では[^。]{0,30}解説",
        r"ここからは[^。]{0,30}述べ",
        r"まずは[^。]{0,20}確認",
    ],
    "15_両論併記の毒抜き": [
        r"賛否両論",
        r"意見が分かれる",
        r"メリットとデメリットの両面",
        r"一概には言えません",
    ],
    "16_比喩テンプレ": [
        r"氷山の一角",
        r"諸刃の剣",
        r"縁の下の力持ち",
        r"二人三脚",
        r"追い風となる",
        r"扉を開く",
    ],
    "17_お説教構文": [
        r"が大切です",
        r"が重要です",
        r"が求められて",
        r"が必要不可欠",
        r"することが望まれ",
    ],
    "18_していきたい型": [
        r"していきたいと思",
        r"してまいりたい",
        r"取り組んでまいります",
        r"進めていきたい",
    ],
    "19_太字濫用": [
        r"\*\*[^*\n]+\*\*",
    ],
    "20_インラインヘッダ箇条書き": [
        r"^[\-\*] ?\*\*[^*]+\*\*[:：]",
    ],
    "21_絵文字機械配置": [
        r"^[🚀✨💡✅🎯📊🔥🌟⭐]",
    ],
    "22_細切れ見出し": [
        # 見出し直後の短い1文（ウォームアップ）
        r"\n#+ [^\n]+\n\n[^\n]{3,25}\n\n",
    ],
    "24_偽範囲": [
        r"から[^、。\n]{3,30}まで[、，へ・]",
    ],
    "25_主語省略受動態": [
        r"が必要となります",
        r"が可能となります",
        r"が行われます",
    ],
    "26_チャットボット痕跡": [
        r"お役に立てれば幸",
        r"他にご質問が",
        r"ご参考までに",
        r"もしよろしければ",
    ],
    "27_媚び過剰肯定": [
        r"素晴らしいご質問",
        r"おっしゃる通り",
        r"鋭いご指摘",
        r"重要なご視点",
    ],
    "28_知識カットオフ言い訳": [
        r"学習データの範囲",
        r"公開されている情報による",
        r"確認できる範囲では",
    ],
    "29_権威ぶり構文": [
        r"本質的には",
        r"真に重要なのは",
        r"結局のところ",
        r"根本的に",
        r"その本質は",
    ],
    "30_媒体露出インフレ": [
        r"各種メディアで取り上げ",
        r"業界の第一人者",
        r"数十万人のフォロワー",
    ],
    "31_課題と展望型": [
        r"課題も残されて",
        r"課題と今後の展望",
        r"これらの課題に対し",
    ],
    "32_効いた型": [
        r"一番効いた",
        r"実際に効いた",
        r"が効いた",
        r"地味にきく",
        r"地味に効く",
        r"刺さった",
        r"ハマった",
        r"沁みる",
        r"響いた",
    ],
    "33_括弧多用": [
        r"（[^（）\n]{1,40}）",
    ],
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def load_livedoor(path):
    """livedoor news の text/<category>/<id>.txt 構造を読む。タイトル行までスキップして本文のみ返す。"""
    for category_dir in sorted(Path(path).iterdir()):
        if not category_dir.is_dir():
            continue
        for txt_file in sorted(category_dir.glob("*.txt")):
            if txt_file.name == "LICENSE.txt":
                continue
            try:
                lines = txt_file.read_text(encoding="utf-8").split("\n")
            except UnicodeDecodeError:
                lines = txt_file.read_text(encoding="utf-8", errors="replace").split("\n")
            body = "\n".join(lines[3:])
            yield f"{category_dir.name}/{txt_file.stem}", body, category_dir.name


def load_jsonl(path):
    """JSONL（各行に 'text' フィールド）を読む。CC-100 / OSCAR 用。"""
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            yield str(i), obj.get("text", ""), "jsonl"


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
SENT_END_FORMS = [
    "ました", "ません", "でした", "ます", "です",
    "である", "だった", "ている", "ない", "だ",
    "た", "る",
]


def analyze_text(text):
    stats = {
        "char_count": len(text),
        "paragraph_count": len([p for p in text.split("\n\n") if p.strip()]),
    }

    # Sentence-end distribution
    sentences = [s.strip() for s in re.split(r"[。！？\n]", text) if s.strip()]
    stats["sentence_count"] = len(sentences)

    sent_ends = Counter()
    for s in sentences:
        matched = False
        for form in SENT_END_FORMS:
            if s.endswith(form):
                sent_ends[form] += 1
                matched = True
                break
        if not matched:
            sent_ends["その他"] += 1
    stats["sentence_ends"] = dict(sent_ends)

    # Pattern matches
    pattern_counts = {}
    for name, regexes in PATTERNS.items():
        c = 0
        for r in regexes:
            c += len(re.findall(r, text, re.MULTILINE))
        pattern_counts[name] = c
    stats["patterns"] = pattern_counts

    return stats


def aggregate(stats_list, category_buckets=None):
    total_articles = len(stats_list)
    total_chars = sum(s["char_count"] for s in stats_list)
    total_sentences = sum(s["sentence_count"] for s in stats_list)

    pattern_totals = Counter()
    pattern_articles = Counter()
    for s in stats_list:
        for p, c in s["patterns"].items():
            pattern_totals[p] += c
            if c > 0:
                pattern_articles[p] += 1

    sent_end_totals = Counter()
    for s in stats_list:
        for k, v in s["sentence_ends"].items():
            sent_end_totals[k] += v

    return {
        "total_articles": total_articles,
        "total_chars": total_chars,
        "total_sentences": total_sentences,
        "avg_article_length": total_chars / total_articles if total_articles else 0,
        "patterns": {
            p: {
                "total_occurrences": pattern_totals[p],
                "articles_with_match": pattern_articles[p],
                "article_rate_pct": (
                    pattern_articles[p] / total_articles * 100 if total_articles else 0
                ),
                "rate_per_10k_chars": (
                    pattern_totals[p] / total_chars * 10000 if total_chars else 0
                ),
            }
            for p in PATTERNS
        },
        "sentence_ends": {
            k: {
                "count": v,
                "pct": v / total_sentences * 100 if total_sentences else 0,
            }
            for k, v in sorted(sent_end_totals.items(), key=lambda x: -x[1])
        },
    }


def format_markdown_report(result, corpus_name):
    lines = []
    lines.append(f"# コーパス分析レポート: {corpus_name}")
    lines.append("")
    lines.append("## 基本統計")
    lines.append("")
    lines.append(f"- 記事数: **{result['total_articles']:,}**")
    lines.append(f"- 総文字数: **{result['total_chars']:,}**")
    lines.append(f"- 総文数: **{result['total_sentences']:,}**")
    lines.append(f"- 1記事あたり平均文字数: **{result['avg_article_length']:.0f}**")
    lines.append("")

    lines.append("## 文末形の分布")
    lines.append("")
    lines.append("| 文末 | 件数 | 比率 |")
    lines.append("|---|--:|--:|")
    for form, info in result["sentence_ends"].items():
        lines.append(f"| {form} | {info['count']:,} | {info['pct']:.1f}% |")
    lines.append("")

    lines.append("## SKILL.md パターン出現頻度")
    lines.append("")
    lines.append("（記事率 = 該当パターンが1回以上現れた記事の割合 / 1万字率 = 1万字あたり出現回数）")
    lines.append("")
    lines.append("| # | パターン | 総出現 | 記事率 | 1万字率 |")
    lines.append("|---|---|--:|--:|--:|")
    sorted_patterns = sorted(
        result["patterns"].items(),
        key=lambda x: -x[1]["article_rate_pct"],
    )
    for name, info in sorted_patterns:
        lines.append(
            f"| {name.split('_')[0]} | {name.split('_', 1)[1]} | "
            f"{info['total_occurrences']:,} | "
            f"{info['article_rate_pct']:.2f}% | "
            f"{info['rate_per_10k_chars']:.3f} |"
        )
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True, choices=["livedoor", "jsonl"])
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-articles", type=int, default=None)
    args = parser.parse_args()

    if args.corpus == "livedoor":
        loader = load_livedoor(args.input)
    else:
        loader = load_jsonl(args.input)

    stats_list = []
    for i, (article_id, text, _category) in enumerate(loader):
        if args.max_articles and i >= args.max_articles:
            break
        stats_list.append(analyze_text(text))
        if (i + 1) % 1000 == 0:
            print(f"  ...{i + 1} articles processed", file=sys.stderr)

    result = aggregate(stats_list)
    result["corpus_name"] = os.path.basename(args.input)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    md_path = os.path.splitext(args.output)[0] + ".md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(format_markdown_report(result, args.corpus))

    print(f"\nWrote {args.output} and {md_path}")
    print(f"Articles: {result['total_articles']:,}, Chars: {result['total_chars']:,}")


if __name__ == "__main__":
    main()
