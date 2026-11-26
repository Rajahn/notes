#!/usr/bin/env bash
# 构建两本书的网页版（mdBook + mdbook-katex）和 EPUB（Pandoc）。
# 产物写到仓库根目录的 build/ 下。缺少某个工具时跳过对应格式。
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$root/build"
mkdir -p "$out"

books=(design theory)
built=0

# 从 SUMMARY.md 按顺序取出已撰写章节的文件（跳过空链接的草稿条目）。
chapters() {
  local src="$1"
  grep -oE '\]\([^)]+\.md\)' "$src/SUMMARY.md" | sed -E 's/^\]\((.*)\)$/\1/' |
    while read -r file; do printf '%s\n' "$src/$file"; done
}

title() {
  sed -nE 's/^title *= *"(.*)"$/\1/p' "$1/book.toml"
}

if command -v mdbook >/dev/null 2>&1 && command -v mdbook-katex >/dev/null 2>&1; then
  for book in "${books[@]}"; do
    mdbook build "$root/$book" --dest-dir "$out/$book/html"
    echo "html: build/$book/html/index.html"
  done
  built=1
else
  echo "skip html: mdbook or mdbook-katex not found" >&2
fi

if command -v pandoc >/dev/null 2>&1; then
  for book in "${books[@]}"; do
    mapfile -t files < <(chapters "$root/$book/src")
    pandoc "${files[@]}" \
      --from markdown+tex_math_dollars \
      --to epub3 --mathml \
      --toc --toc-depth=2 \
      --split-level=1 \
      --metadata title="$(title "$root/$book")" \
      --metadata lang=zh-CN \
      --resource-path="$root/$book/src" \
      --output "$out/$book.epub"
    echo "epub: build/$book.epub"
  done
  built=1
else
  echo "skip epub: pandoc not found" >&2
fi

if [ "$built" -eq 0 ]; then
  echo "nothing built: install mdbook + mdbook-katex, or pandoc" >&2
  exit 1
fi
