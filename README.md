# 可解释决策学习：设计与理论

这个仓库收两本相互配合的电子书：

| 书 | 目录 | 内容 |
|---|---|---|
| 甲篇《可解释决策规则的建模与持续改进：设计说明书》 | [`design/`](design/src/SUMMARY.md) | 逐层说明 `engine-cli-minimal` 当前的设计：目标、合同、各子系统的机制与设计决策。随仓库持续迭代 |
| 乙篇《LLM 驱动的可解释决策学习：理论与学术全景》 | [`theory/`](theory/src/SUMMARY.md) | 不依赖任何具体仓库，从数学预备讲到统计学习、符号学习、神经符号、因果、实验设计与前沿研究 |

甲篇讲"我们怎样做、为什么这样做"，乙篇讲"这些做法背后的理论，以及领域里其他人怎样做"。两本书都面向初学者，写作约定见 [STYLE.md](STYLE.md)。

## 阅读方式

| 方式 | 说明 |
|---|---|
| 在线阅读 | GitHub Pages 站点，首页列出两本书的网页版和 PDF 下载链接（启用方法见下文） |
| 离线 PDF | 每本书一个 PDF，A4 排版，带封面、页码和书签，练习答案全部展开 |
| 直接看源文件 | 源文件是 Markdown，公式用 `$...$` 和 `$$...$$`，可以在 GitHub 上直接阅读：[甲篇目录](design/src/SUMMARY.md)、[乙篇目录](theory/src/SUMMARY.md) |

目录中暂不可点的条目是尚未撰写的章节。

## 在本地构建

需要：

- [mdBook](https://github.com/rust-lang/mdBook) 0.4.40 和 [mdbook-katex](https://github.com/lzanini/mdbook-katex) 0.9.0；
- Node.js 18 或以上，以及 [Playwright](https://playwright.dev/) 和它的 Chromium（用来打印 PDF）；
- 中文字体（例如 Noto CJK）。

```bash
cargo install mdbook --version 0.4.40 --locked
cargo install mdbook-katex --version 0.9.0 --locked
npm install --no-save playwright@1.63.0
npx playwright install chromium
```

```bash
scripts/build.sh
```

产物写到 `build/site/`，结构和线上站点相同：

| 路径 | 内容 |
|---|---|
| `build/site/index.html` | 首页 |
| `build/site/design/`、`build/site/theory/` | 两本书的网页版 |
| `build/site/pdf/design.pdf`、`build/site/pdf/theory.pdf` | 离线 PDF |

公式样式从 KaTeX 的 CDN 加载，所以构建 PDF 时需要联网。无法联网时，可以先下载 KaTeX 0.16.4 的发布包，把环境变量 `KATEX_DIST` 设为其中的 `dist` 目录再构建。

## 发布到 GitHub Pages

`.github/workflows/pages.yml` 在 `main` 分支更新时自动构建网页版和 PDF 并发布，也可以在 Actions 页面手动运行。首次使用前，在仓库的 Settings → Pages 中把 Source 设为 **GitHub Actions**。

## 写作约定

- 每章一个文件，文件名以两位章号开头；章节顺序以各书的 `SUMMARY.md` 为准。
- 甲篇描述的是某一版本的仓库，版本写在甲篇第 0 章。仓库变化后，按新版本修订相应章节。
- 示例中的地址使用保留示例域名（如 `example.invalid`），模型标识使用虚构值。
- 风格与密度要求见 [STYLE.md](STYLE.md)。
