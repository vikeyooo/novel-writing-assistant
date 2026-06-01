#!/usr/bin/env python3
"""导出小说为文本文件"""

import click
import json
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_manager import DataManager


def export_novel():
    """导出小说"""
    print("\n📤 小说导出工具\n")

    output_path = input("输入输出文件路径 (默认 './小说.txt'): ").strip() or "./小说.txt"

    try:
        manager = DataManager()
        success = manager.export_to_txt(output_path)

        if success:
            print(f"\n✅ 导出成功！")
            print(f"📄 文件位置: {output_path}")
        else:
            print("❌ 导出失败")

    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    export_novel()
