"""一致性检查模块 - 验证故事逻辑"""

from typing import Dict, List, Optional, Any
from .deepseek_api import DeepSeekAPI
from .deepseek_advanced import DeepSeekAdvanced
from .data_manager import DataManager
from loguru import logger


class ConsistencyChecker:
    """故事一致性检查器"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        data_dir: Optional[str] = None
    ):
        """
        初始化检查器

        Args:
            api_key: DeepSeek API Key
            data_dir: 数据目录
        """
        self.api = DeepSeekAPI(api_key=api_key)
        self.advanced = DeepSeekAdvanced(api=self.api)
        self.data = DataManager(data_dir=data_dir)

        logger.info("✅ 一致性检查器已初始化")

    def check_character_consistency(
        self,
        character_name: str,
        chapters: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        检查人物一致性

        Args:
            character_name: 人物名称
            chapters: 指定章节

        Returns:
            检查报告
        """
        logger.info(f"🔍 检查人物: {character_name}")

        mentions = self._get_character_mentions(character_name, chapters)

        if not mentions:
            return {
                "character": character_name,
                "status": "not_found",
                "message": f"人物 {character_name} 未找到"
            }

        context = "\n---\n".join([m["excerpt"] for m in mentions[:10]])

        prompt = f"""检查人物 '{character_name}' 的以下出现中的一致性问题。

【人物提及】
{context}

检查：
1. 性格一致性
2. 知识记忆连贯性
3. 关系是否一致
4. 时间线是否正确
5. 外貌描写是否一致
6. 语气风格是否一致

列出发现的矛盾和建议修正。"""

        analysis = self.api.chat_with_reasoning(
            [{"role": "system", "content": "你是一位资深的文学一致性检查专家。"},
             {"role": "user", "content": prompt}],
            depth="deep"
        )

        return {
            "character": character_name,
            "status": "checked",
            "mentions_count": len(mentions),
            "analysis": analysis.get("answer") or analysis.get("full_response")
        }

    def check_timeline_consistency(self) -> Dict[str, Any]:
        """
        检查时间线一致性

        Returns:
            检查结果
        """
        logger.info("⏰ 检查时间线一致性")

        chapters = self.data.list_chapters()
        timeline_events = []

        for ch in chapters:
            chapter_data = self.data.load_chapter(ch["chapter_num"])
            if chapter_data and "metadata" in chapter_data:
                meta = chapter_data["metadata"]
                if "timeline" in meta:
                    timeline_events.append({
                        "chapter": ch["chapter_num"],
                        "event": meta.get("timeline"),
                        "title": ch["title"]
                    })

        if not timeline_events:
            return {
                "status": "no_data",
                "message": "未找到时间线数据"
            }

        timeline_str = "\n".join([f"第{e['chapter']}章: {e['event']} ({e['title']})" for e in timeline_events])

        prompt = f"""检查以下故事时间线的一致性和逻辑性。

【故事时间线】
{timeline_str}

请检查：
1. 时间顺序是否正确
2. 时间跳跃是否合理
3. 季节/天气是否恰当
4. 是否有时代错误
5. 事件间隔是否合理"""

        analysis = self.api.chat_with_reasoning(
            [{"role": "system", "content": "你是一位时间线一致性专家。"},
             {"role": "user", "content": prompt}],
            depth="medium"
        )

        return {
            "status": "checked",
            "events_count": len(timeline_events),
            "analysis": analysis.get("answer") or analysis.get("full_response")
        }

    def full_consistency_check(
        self,
        include_characters: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        全面一致性检查

        Args:
            include_characters: 要检查的人物

        Returns:
            完整报告
        """
        logger.info("🔍 执行全面一致性检查")

        results = {
            "status": "checking",
            "checks": {}
        }

        # 检查时间线
        results["checks"]["timeline"] = self.check_timeline_consistency()

        # 检查人物
        characters = self.data.load_characters()
        chars_to_check = include_characters or list(characters.keys())[:3]

        results["checks"]["characters"] = {}
        for char in chars_to_check:
            results["checks"]["characters"][char] = self.check_character_consistency(char)

        logger.info("✅ 全面检查完成")
        return results

    def _get_character_mentions(
        self,
        character_name: str,
        chapters: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """获取人物所有出现"""
        mentions = []
        all_chapters = self.data.list_chapters()

        target_chapters = chapters or [ch["chapter_num"] for ch in all_chapters]

        for ch_num in target_chapters:
            chapter = self.data.load_chapter(ch_num)
            if chapter and character_name in chapter["content"]:
                content = chapter["content"]
                start_idx = 0

                while True:
                    idx = content.find(character_name, start_idx)
                    if idx == -1:
                        break

                    context_start = max(0, idx - 200)
                    context_end = min(len(content), idx + 200)
                    excerpt = content[context_start:context_end].strip()

                    mentions.append({
                        "chapter": ch_num,
                        "title": chapter["title"],
                        "excerpt": excerpt,
                        "position": idx
                    })

                    start_idx = idx + len(character_name)

        return mentions


if __name__ == "__main__":
    checker = ConsistencyChecker()
    report = checker.full_consistency_check()
    print(report)
