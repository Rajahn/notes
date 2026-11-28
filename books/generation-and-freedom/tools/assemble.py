#!/usr/bin/env python3
"""Assemble the book from its chapter sources and verify local references."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
CJK = re.compile(r"[\u4e00-\u9fff]")
REF = re.compile(r"\b(?:VII|VI|IV|III|II|V|I)-\d{2}\b")
LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)\)")
PART_NAMES = ("", "一", "二", "三", "四", "五", "六", "七")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def title(text: str) -> str:
    first = text.splitlines()[0]
    if not first.startswith("# "):
        raise ValueError("Each chapter must begin with one level-one heading")
    return first[2:].strip()


def relocate_links(text: str, source: Path) -> str:
    def change(match: re.Match[str]) -> str:
        label, target = match.groups()
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            return match.group(0)
        base, sep, anchor = target.partition("#")
        absolute = (source.parent / unquote(base)).resolve()
        relative = absolute.relative_to(ROOT).as_posix()
        return f"[{label}]({relative}{sep}{anchor})"

    return LINK.sub(change, text)


def main() -> None:
    chapters: dict[int, Path] = {}
    for path in sorted((ROOT / "src").glob("[0-9][0-9]-*.md")):
        number = int(path.name[:2])
        if number in chapters:
            raise ValueError(f"Duplicate chapter number: {number}")
        chapters[number] = path
    if set(chapters) != set(range(39)):
        raise ValueError(f"Expected introduction, 37 chapters and conclusion; got {sorted(chapters)}")

    contents = {number: read(path) for number, path in chapters.items()}
    research_paths = sorted((ROOT / "research").glob("[0-9][0-9]-*.md"))
    research_texts = {path: read(path) for path in research_paths}
    for part in CONFIG["parts"]:
        if not (ROOT / "research" / part["research"]).is_file():
            raise ValueError(f"Missing part research: {part['number']}")

    reference_definitions: dict[str, Path] = {}
    for path, text in research_texts.items():
        for line in text.splitlines():
            if line.startswith("### "):
                found = REF.search(line)
                if found:
                    reference = found.group(0)
                    if reference in reference_definitions:
                        raise ValueError(f"Duplicate reference ID: {reference}")
                    reference_definitions[reference] = path

    cited: set[str] = set()
    for number, text in contents.items():
        title(text)
        if len(CJK.findall(text)) < 900:
            raise ValueError(f"Chapter {number:02d} is too short to be complete")
        if re.search(r"TODO|TBD|待撰写|正文待补|此处占位", text, re.I):
            raise ValueError(f"Unfinished marker in chapter {number:02d}")
        if text.count("$$") % 2:
            raise ValueError(f"Unpaired display math delimiters in chapter {number:02d}")
        cited.update(REF.findall(text))
    undefined = cited - reference_definitions.keys()
    if undefined:
        raise ValueError(f"Undefined references: {sorted(undefined)}")

    summary = ["# 全书目录", "", f"[{title(contents[0])}]({chapters[0].name})", ""]
    manuscript = [
        f"# {CONFIG['title']}",
        "",
        f"## {CONFIG['subtitle']}",
        "",
        f"{CONFIG['edition']} · 版本 {CONFIG['version']} · 研究截止：{CONFIG['research_cutoff']}",
        "",
        "本文件由逐章正文与研究附录汇编。构造例子、形式命题、经验判断和规范主张分别标明；各部文献编号见文末对应调研。",
        "",
        "## 阅读目录",
        "",
        f"- [{title(contents[0])}](#chapter-00)",
    ]

    for part in CONFIG["parts"]:
        part_title = f"第{PART_NAMES[part['number']]}部　{part['title']}"
        summary.extend([f"# {part_title}", ""])
        manuscript.extend(["", f"**{part_title}**", ""])
        for number in range(part["first"], part["last"] + 1):
            heading = title(contents[number])
            summary.append(f"- [{heading}]({chapters[number].name})")
            manuscript.append(f"- [{heading}](#chapter-{number:02d})")
        summary.extend(["", f"[本部文献调研](../research/{part['research']})", ""])
    summary.extend([f"[{title(contents[38])}]({chapters[38].name})", "", "# 研究附录", ""])
    manuscript.extend(["", f"- [{title(contents[38])}](#chapter-38)", "", "### 研究附录", ""])
    for path, text in research_texts.items():
        summary.append(f"- [{title(text)}](../research/{path.name})")
        manuscript.append(f"- [{title(text)}](#research-{path.name[:2]})")
    summary.extend(["", "[返回书稿首页](../README.md)", ""])
    (ROOT / "src" / "SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")

    first_chapters = {part["first"]: part for part in CONFIG["parts"]}
    for number, source in sorted(chapters.items()):
        if number in first_chapters:
            part = first_chapters[number]
            manuscript.extend([
                "", "---", "",
                f"# 第{PART_NAMES[part['number']]}部　{part['title']}", ""
            ])
        else:
            manuscript.extend(["", "---", ""])
        manuscript.extend([f'<a name="chapter-{number:02d}"></a>', ""])
        body = relocate_links(contents[number], source)
        body = re.sub(r"^(#{1,5}) ", r"#\1 ", body, flags=re.M)
        manuscript.append(body.rstrip())

    manuscript.extend(["", "---", "", "# 研究附录", ""])
    for source, text in research_texts.items():
        manuscript.extend(["", f'<a name="research-{source.name[:2]}"></a>', ""])
        body = relocate_links(text, source)
        body = re.sub(r"^(#{1,5}) ", r"#\1 ", body, flags=re.M)
        manuscript.append(body.rstrip())
    (ROOT / "MANUSCRIPT.md").write_text("\n".join(manuscript).strip() + "\n", encoding="utf-8")

    stats = {
        "version": CONFIG["version"],
        "research_cutoff": CONFIG["research_cutoff"],
        "body_han_characters": sum(len(CJK.findall(text)) for text in contents.values()),
        "numbered_chapters": 37,
        "introduction_and_conclusion": 2,
        "reference_entries": len(reference_definitions),
        "cited_reference_entries": len(cited),
        "research_han_characters": sum(len(CJK.findall(text)) for text in research_texts.values()),
        "parts": [
            {
                "part": part["number"],
                "title": part["title"],
                "chapters": part["last"] - part["first"] + 1,
                "han_characters": sum(
                    len(CJK.findall(contents[number]))
                    for number in range(part["first"], part["last"] + 1)
                ),
            }
            for part in CONFIG["parts"]
        ],
        "chapter_sha256": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in chapters.values()
        },
    }
    (ROOT / "STATS.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    broken = []
    for source in ROOT.rglob("*.md"):
        for match in LINK.finditer(read(source)):
            target = match.group(2)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0])
            if not (source.parent / target).exists():
                broken.append((str(source.relative_to(ROOT)), target))
    if broken:
        raise ValueError(f"Broken local links: {broken}")
    print(json.dumps({key: value for key, value in stats.items() if key != "chapter_sha256"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
