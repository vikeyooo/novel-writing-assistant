#!/usr/bin/env python3
"""初始化本地数据结构"""

import os
import json
from pathlib import Path


def init_novel_structure():
    """创建初始小说数据结构"""
    data_dir = Path("./data/novel")
    data_dir.mkdir(parents=True, exist_ok=True)

    # 创建 characters.json
    characters_file = data_dir / "characters.json"
    if not characters_file.exists():
        with open(characters_file, 'w', encoding='utf-8') as f:
            json.dump({"characters": {}}, f, ensure_ascii=False, indent=2)
        print("✅ 创建 characters.json")

    # 创建 worldbuilding.json
    worldbuilding_file = data_dir / "worldbuilding.json"
    if not worldbuilding_file.exists():
        with open(worldbuilding_file, 'w', encoding='utf-8') as f:
            json.dump({"worldbuilding": {}}, f, ensure_ascii=False, indent=2)
        print("✅ 创建 worldbuilding.json")

    # 创建 metadata.json
    metadata_file = data_dir / "metadata.json"
    if not metadata_file.exists():
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump({
                "title": "未命名小说",
                "author": "匿名作者",
                "status": "创作中",
                "total_planned_words": 5000000,
                "created_at": "2024-01-01"
            }, f, ensure_ascii=False, indent=2)
        print("✅ 创建 metadata.json")

    # 创建 chapters 目录
    chapters_dir = data_dir / "chapters"
    chapters_dir.mkdir(exist_ok=True)
    print("✅ 创建 chapters 目录")

    # 创建日志和备份目录
    Path("./data/logs").mkdir(parents=True, exist_ok=True)
    Path("./data/search_cache").mkdir(parents=True, exist_ok=True)
    Path("./data/backups").mkdir(parents=True, exist_ok=True)
    print("✅ 创建日志和缓存目录")

    print("\n✨ 数据结构初始化完成！")


if __name__ == "__main__":
    init_novel_structure()
