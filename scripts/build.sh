#!/usr/bin/env bash
# 构建两本书：网页版（mdBook + mdbook-katex）和离线 PDF（Playwright 打印 mdBook 的 print.html）。
# 产物写到 build/site/，结构与 GitHub Pages 站点一致：
#   build/site/index.html          首页
#   build/site/design/、theory/    两本书的网页版
#   build/site/pdf/design.pdf、theory.pdf
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site="$root/build/site"
rm -rf "$site"
mkdir -p "$site/pdf"

for tool in mdbook mdbook-katex node; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "missing $tool; see README.md" >&2
    exit 1
  fi
done

cp "$root/site/index.html" "$site/index.html"

for book in design theory; do
  mdbook build "$root/$book" --dest-dir "$site/$book"
  echo "html: build/site/$book/index.html"
  node "$root/scripts/pdf.js" "$site/$book/print.html" "$site/pdf/$book.pdf"
done
