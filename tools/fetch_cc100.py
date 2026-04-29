#!/usr/bin/env python3
"""
CC-100 ja コーパスから N 件 streaming で取得して JSONL に保存。

使い方:
  python3 fetch_cc100.py --count 10000 --output cc100_sample.jsonl --min-chars 200

CC-100 は Hugging Face datasets 経由で取得。フルダウンロード不要（streaming）。
"""

import argparse
import json
import sys

from datasets import load_dataset


CANDIDATE_DATASETS = [
    # name, config, text_field, trust_remote_code
    ("range3/cc100-ja", None, "text", False),
    ("oscar-corpus/OSCAR-2301", "ja", "text", True),
    ("mc4", "ja", "text", False),
    ("allenai/c4", "ja", "text", False),
]


def try_load(count, min_chars, output_path):
    last_error = None
    for ds_name, config, text_field, trust in CANDIDATE_DATASETS:
        try:
            print(f"Trying {ds_name} (config={config})...", file=sys.stderr)
            kwargs = dict(streaming=True)
            if trust:
                kwargs["trust_remote_code"] = True
            if config:
                ds = load_dataset(ds_name, config, split="train", **kwargs)
            else:
                ds = load_dataset(ds_name, split="train", **kwargs)
            return harvest(ds, text_field, count, min_chars, output_path, ds_name)
        except Exception as e:
            print(f"  failed: {type(e).__name__}: {e}", file=sys.stderr)
            last_error = e
            continue
    raise RuntimeError(f"All candidate datasets failed. Last: {last_error}")


def harvest(ds, text_field, count, min_chars, output_path, source_name):
    written = 0
    examined = 0
    with open(output_path, "w", encoding="utf-8") as out:
        for example in ds:
            examined += 1
            text = example.get(text_field, "")
            if len(text) < min_chars:
                continue
            out.write(json.dumps({"text": text, "_source": source_name}, ensure_ascii=False) + "\n")
            written += 1
            if written % 1000 == 0:
                print(f"  wrote {written} (examined {examined})", file=sys.stderr)
            if written >= count:
                break
    print(f"\nFinished. {written} docs written to {output_path}", file=sys.stderr)
    print(f"Source: {source_name}", file=sys.stderr)
    return written


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10000)
    parser.add_argument("--min-chars", type=int, default=200)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try_load(args.count, args.min_chars, args.output)


if __name__ == "__main__":
    main()
