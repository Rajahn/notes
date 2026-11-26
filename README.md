# 可解释决策学习：设计与理论

这个仓库收两本相互配合的电子书：

| 书 | 目录 | 内容 |
|---|---|---|
| 甲篇《可解释决策规则的建模与持续改进：设计说明书》 | [`design/`](design/src/SUMMARY.md) | 逐层说明 `engine-cli-minimal` 当前的设计：目标、合同、各子系统的机制与设计决策 |
| 乙篇《LLM 驱动的可解释决策学习：理论与学术全景》 | [`theory/`](theory/src/SUMMARY.md) | 不依赖任何具体仓库，从数学预备讲到统计学习、符号学习、神经符号、因果、实验设计与前沿研究 |

甲篇讲"我们怎样做、为什么这样做"，乙篇讲"这些做法背后的理论，以及领域里其他人怎样做"。甲篇每章末尾列出对应的乙篇章节；乙篇的例子不引用甲篇的内部细节，可以单独阅读。

## 阅读

源文件是普通 Markdown，数学公式用 `$...$` 和 `$$...$$`，可以直接在 GitHub 上阅读：

- 甲篇目录：[design/src/SUMMARY.md](design/src/SUMMARY.md)
- 乙篇目录：[theory/src/SUMMARY.md](theory/src/SUMMARY.md)

目录中没有链接的条目是尚未撰写的章节。

## 构建电子书

需要 [mdBook](https://github.com/rust-lang/mdBook) 0.4.40 和 [mdbook-katex](https://github.com/lzanini/mdbook-katex) 0.9.0（生成网页版），以及 [Pandoc](https://pandoc.org/)（生成 EPUB）。

```bash
cargo install mdbook --version 0.4.40 --locked
cargo install mdbook-katex --version 0.9.0 --locked
```

```bash
scripts/build.sh
```

产物写到 `build/`：`build/design/html/`、`build/theory/html/` 是网页版（打开其中的 `index.html`），`build/design.epub`、`build/theory.epub` 是 EPUB。只装了其中一种工具时，脚本只生成对应格式。

## 写作约定

- 每章一个文件，文件名以两位章号开头；章节顺序以各书的 `SUMMARY.md` 为准。
- 甲篇描述的是某一版本的仓库，版本写在甲篇第 0 章。仓库变化后，按新版本修订相应章节。
- 示例中的地址使用保留示例域名（如 `example.invalid`），模型标识使用虚构值。
