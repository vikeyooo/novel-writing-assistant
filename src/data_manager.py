"""本地数据管理 - 完全本地存储，无云端依赖"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger


class DataManager:
    """本地小说数据管理器"""

    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化数据管理器

        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir or os.getenv("DATA_DIR", "./data")
        self.novel_dir = os.path.join(self.data_dir, "novel")
        self.chapters_dir = os.path.join(self.novel_dir, "chapters")

        # 创建目录
        os.makedirs(self.chapters_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "logs"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "backups"), exist_ok=True)

        logger.info(f"✅ 数据管理器初始化: {self.data_dir}")

    def save_chapter(
        self,
        chapter_num: int,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        保存章节

        Args:
            chapter_num: 章节号
            title: 章节标题
            content: 章节内容
            metadata: 元数据

        Returns:
            是否成功
        """
        try:
            chapter_file = os.path.join(self.chapters_dir, f"chapter_{chapter_num:03d}.json")

            data = {
                "chapter_num": chapter_num,
                "title": title,
                "content": content,
                "word_count": len(content),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }

            with open(chapter_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ 章节已保存 #{chapter_num}: {title}")
            return True

        except Exception as e:
            logger.error(f"❌ 保存章节失败: {e}")
            return False

    def load_chapter(self, chapter_num: int) -> Optional[Dict[str, Any]]:
        """
        加载章节

        Args:
            chapter_num: 章节号

        Returns:
            章节数据或 None
        """
        try:
            chapter_file = os.path.join(self.chapters_dir, f"chapter_{chapter_num:03d}.json")

            if not os.path.exists(chapter_file):
                logger.warning(f"⚠️ 章节 {chapter_num} 不存在")
                return None

            with open(chapter_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"❌ 加载章节失败: {e}")
            return None

    def list_chapters(self) -> List[Dict[str, Any]]:
        """
        列表所有章节

        Returns:
            章节元数据列表
        """
        chapters = []

        for filename in sorted(os.listdir(self.chapters_dir)):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(self.chapters_dir, filename), 'r', encoding='utf-8') as f:
                        chapter_data = json.load(f)
                        chapters.append({
                            "chapter_num": chapter_data["chapter_num"],
                            "title": chapter_data["title"],
                            "word_count": chapter_data["word_count"],
                            "created_at": chapter_data["created_at"]
                        })
                except Exception as e:
                    logger.warning(f"⚠️ 读取章节失败 {filename}: {e}")

        return chapters

    def save_characters(self, characters: Dict[str, Dict[str, Any]]) -> bool:
        """
        保存人物档案

        Args:
            characters: 人物数据

        Returns:
            是否成功
        """
        try:
            filepath = os.path.join(self.novel_dir, "characters.json")
            data = {
                "characters": characters,
                "updated_at": datetime.now().isoformat(),
                "total_characters": len(characters)
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ {len(characters)} 个人物已保存")
            return True

        except Exception as e:
            logger.error(f"❌ 保存人物失败: {e}")
            return False

    def load_characters(self) -> Dict[str, Dict[str, Any]]:
        """
        加载人物档案

        Returns:
            人物数据
        """
        try:
            filepath = os.path.join(self.novel_dir, "characters.json")

            if not os.path.exists(filepath):
                return {}

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("characters", {})

        except Exception as e:
            logger.error(f"❌ 加载人物失败: {e}")
            return {}

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取小说统计信息

        Returns:
            统计数据
        """
        chapters = self.list_chapters()
        total_words = sum(ch["word_count"] for ch in chapters)

        return {
            "total_chapters": len(chapters),
            "total_words": total_words,
            "total_characters": len(self.load_characters()),
            "average_chapter_length": total_words // len(chapters) if chapters else 0
        }

    def export_to_txt(self, output_path: str) -> bool:
        """
        导出为纯文本文件

        Args:
            output_path: 输出路径

        Returns:
            是否成功
        """
        try:
            chapters = self.list_chapters()
            full_text = []

            for ch in chapters:
                chapter_data = self.load_chapter(ch["chapter_num"])
                if chapter_data:
                    full_text.append(f"# {chapter_data['title']}\n")
                    full_text.append(chapter_data['content'])
                    full_text.append("\n\n")

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(''.join(full_text))

            logger.info(f"✅ 已导出到: {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ 导出失败: {e}")
            return False


if __name__ == "__main__":
    manager = DataManager()

    # 保存章节
    manager.save_chapter(
        1,
        "故事开始",
        "这是第一章的开头...",
        {"characters": ["主角"], "timeline": "2024-01-01"}
    )

    # 查看统计
    stats = manager.get_statistics()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
