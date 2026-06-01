#!/usr/bin/env python3
"""导入现有小说内容到系统"""

import click
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def import_from_txt(file_path: str, chapter_marker: str = "第"):
    """
    从 TXT 文件导入小说
    
    Args:
        file_path: 小说文件路径
        chapter_marker: 章节标记（默认 "第"）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法打开文件: {e}")
        return

    chapters_dir = Path("./data/novel/chapters")
    chapters_dir.mkdir(parents=True, exist_ok=True)

    # 简单分章（可根据需要调整）
    lines = content.split('\n')
    current_chapter = 1
    current_title = f"第 {current_chapter} 章"
    current_content = []

    for line in lines:
        # 检测章节标记
        if chapter_marker in line and any(c.isdigit() for c in line):
            # 保存上一章
            if current_content:
                save_chapter(
                    current_chapter,
                    current_title,
                    '\n'.join(current_content),
                    chapters_dir
                )
                current_chapter += 1
                current_title = line.strip()
                current_content = []
        else:
            current_content.append(line)

    # 保存最后一章
    if current_content:
        save_chapter(
            current_chapter,
            current_title,
            '\n'.join(current_content),
            chapters_dir
        )

    print(f"\n✅ 导入完成！共 {current_chapter} 章")


def save_chapter(chapter_num: int, title: str, content: str, chapters_dir: Path):
    """保存章节"""
    chapter_file = chapters_dir / f"chapter_{chapter_num:03d}.json"

    data = {
        "chapter_num": chapter_num,
        "title": title,
        "content": content.strip(),
        "word_count": len(content),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "metadata": {}
    }

    with open(chapter_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 导入章节 {chapter_num}: {title}")


if __name__ == "__main__":
    print("\n📚 小说导入工具\n")

    file_path = input("请输入小说文件路径: ").strip()
    if not file_path:
        print("❌ 未输入文件路径")
        sys.exit(1)

    chapter_marker = input("输入章节标记 (默认 '第'): ").strip() or "第"

    import_from_txt(file_path, chapter_marker)
