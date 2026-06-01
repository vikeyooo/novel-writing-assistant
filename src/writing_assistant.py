"""核心写作助手模块 - 整合所有功能"""

from typing import Optional, List, Dict, Any
from .deepseek_api import DeepSeekAPI
from .deepseek_advanced import DeepSeekAdvanced
from .web_searcher import WebSearcher
from .data_manager import DataManager
from loguru import logger


class WritingAssistant:
    """小说写作助手 - 集成所有创意功能"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        data_dir: Optional[str] = None,
        search_engine: Optional[str] = None
    ):
        """
        初始化写作助手

        Args:
            api_key: DeepSeek API Key
            data_dir: 本地数据目录
            search_engine: 搜索引擎偏好
        """
        self.api = DeepSeekAPI(api_key=api_key)
        self.advanced = DeepSeekAdvanced(api=self.api)
        self.data = DataManager(data_dir=data_dir)
        self.searcher = WebSearcher(engine=search_engine)

        logger.info("🎭 写作助手已初始化")

    def suggest_plot(
        self,
        chapter_num: int,
        previous_chapters: int = 3,
        search_keywords: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """
        建议故事情节发展

        Args:
            chapter_num: 当前章节号
            previous_chapters: 参考的前几章
            search_keywords: 搜索关键词
            **kwargs: 其他参数

        Returns:
            情节建议
        """
        logger.info(f"📖 为第 {chapter_num} 章生成情节建议")

        # 收集前文上下文
        context_chapters = []
        for i in range(max(1, chapter_num - previous_chapters), chapter_num):
            ch = self.data.load_chapter(i)
            if ch:
                context_chapters.append(f"【{ch['title']}】\n{ch['content'][:500]}...")

        context_text = "\n\n".join(context_chapters)

        # 搜索相关信息
        search_context = ""
        if search_keywords:
            logger.info(f"🔍 搜索关键词: {search_keywords}")
            results = self.searcher.search_multiple(search_keywords)
            for query, res_list in results.items():
                if res_list:
                    search_context += f"\n【{query}】\n"
                    for r in res_list[:2]:
                        search_context += f"- {r['title']}: {r['snippet']}\n"

        prompt = f"""基于以下故事背景，为第 {chapter_num} 章提供详细的情节建议。

【最近故事背景】
{context_text}

{f"【参考资料】{search_context}" if search_context else ""}

请提供：
1. 主要情节发展
2. 人物互动
3. 潜在冲突或转折
4. 节奏建议
5. 预留的伏笔"""

        messages = [
            {"role": "system", "content": "你是一位资深的小说创意顾问和编剧。"},
            {"role": "user", "content": prompt}
        ]

        return self.advanced.api.generate_creative(prompt, context=context_text, length="long", use_reasoning=True) or "生成失败"

    def analyze_character(
        self,
        character_name: str,
        search_references: bool = False,
        **kwargs
    ) -> str:
        """
        深入分析人���

        Args:
            character_name: 人物名称
            search_references: 是否搜索参考资料
            **kwargs: 其他参数

        Returns:
            人物分析
        """
        logger.info(f"🧠 分析人物: {character_name}")

        characters = self.data.load_characters()
        char_data = characters.get(character_name, {})

        return self.advanced.character_deep_dive(character_name, context=str(char_data))["answer"]

    def research_topic(
        self,
        topic: str,
        num_sources: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        研究主题获取背景资料

        Args:
            topic: 研究主题
            num_sources: 来源数量
            **kwargs: 其他参数

        Returns:
            研究结果
        """
        logger.info(f"📚 研究主题: {topic}")

        search_results = self.searcher.search(topic, num_results=num_sources)

        if not search_results:
            return {"topic": topic, "status": "failed", "message": "搜索无结果"}

        # 让 AI 合成信息
        context = "\n".join([
            f"- {r['title']}: {r['snippet']}" for r in search_results[:3]
        ])

        prompt = f"""基于以下搜索结果，为小说作者综合介绍 '{topic}' 的关键信息。

【搜索结果】
{context}

请提供：
1. 核心事实和背景
2. 历史或文化背景（如适用）
3. 有趣的细节
4. 相关的衍生主题
5. 进一步研究建议"""

        synthesis = self.api.generate_creative(prompt, length="medium", use_reasoning=True)

        return {
            "topic": topic,
            "status": "success",
            "raw_results": search_results,
            "synthesis": synthesis,
            "source_count": len(search_results)
        }

    def brainstorm_ideas(
        self,
        theme: str,
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        头脑风暴生成创意

        Args:
            theme: 创意主题
            context: 故事背景
            **kwargs: 其他参数

        Returns:
            创意想法
        """
        logger.info(f"💡 主题头脑风暴: {theme}")

        ideas = self.advanced.multi_angle_brainstorm(theme)

        result = "\n\n".join([
            f"【{angle}】\n{idea[:500]}..." for angle, idea in ideas.items()
        ])

        return result

    def improve_writing(
        self,
        text: str,
        aspect: str = "general",
        **kwargs
    ) -> str:
        """
        改进文本质量

        Args:
            text: 原始文本
            aspect: 改进方向
            **kwargs: 其他参数

        Returns:
            改进建议和修订版本
        """
        logger.info(f"✨ 改进文本: {aspect}")

        result = self.advanced.feedback_and_improvement(text, focus_areas=[aspect])
        return result.get("answer") or result.get("full_response")

    def write_continuation(
        self,
        chapter_num: int,
        length: str = "medium",
        tone: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        续写故事

        Args:
            chapter_num: 当前章节号
            length: 输出长度
            tone: 语调
            **kwargs: 其他参数

        Returns:
            续写内容
        """
        logger.info(f"✍️ 续写第 {chapter_num} 章")

        prev_chapter = self.data.load_chapter(chapter_num - 1)
        if not prev_chapter:
            return "前一章节未找到"

        context_text = prev_chapter['content'][-1000:]  # 最后1000字

        return self.api.generate_creative(
            f"继续讲述故事",
            context=context_text,
            style=tone,
            length=length,
            use_reasoning=True
        ) or "续写失败"


if __name__ == "__main__":
    assistant = WritingAssistant()

    # 测试
    ideas = assistant.brainstorm_ideas("穿越到古代的年轻女性")
    print(ideas)
