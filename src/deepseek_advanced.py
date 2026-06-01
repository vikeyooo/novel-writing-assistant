"""DeepSeek V4 高级功能模块"""

import json
from typing import Optional, Dict, List, Any
from .deepseek_api import DeepSeekAPI
from loguru import logger


class DeepSeekAdvanced:
    """DeepSeek V4 高级功能集合"""

    def __init__(self, api: Optional[DeepSeekAPI] = None):
        """
        初始化高级功能模块

        Args:
            api: DeepSeekAPI 实例
        """
        self.api = api or DeepSeekAPI()

    def deep_analysis(
        self,
        text: str,
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        深度分析文本 - 使用 V4 的推理模式

        Args:
            text: 要分析的文本
            analysis_type: 分析类型

        Returns:
            详细的分析结果
        """
        analysis_prompts = {
            "comprehensive": """对以下文本进行全面分析，包括：
1. 整体结构和逻辑
2. 语言和修辞特点
3. 情感和气氛
4. 潜在的改进方向
5. 亮点和不足之处""",
            "creative_potential": """分析这段文本的创意潜力：
1. 能否扩展为更长的故事？
2. 有哪些有趣的次情节空间？
3. 角色发展的可能性？
4. 潜在的转折点？""",
            "emotional_resonance": """分析文本的情感共鸣：
1. 主要情感是什么？
2. 情感转变如何呈现？
3. 读者可能的反应？
4. 如何增强情感冲击？"""
        }

        prompt = analysis_prompts.get(analysis_type, analysis_prompts["comprehensive"])

        result = self.api.chat_with_reasoning([
            {"role": "system", "content": "你是一位资深的文学批评家和创意顾问。"},
            {"role": "user", "content": f"{prompt}\n\n【文本】\n{text}"}
        ], depth="deep")

        return result

    def multi_angle_brainstorm(
        self,
        topic: str,
        angles: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        从多个角度头脑风暴 - 生成多样化的想法

        Args:
            topic: 主题
            angles: 分析角度（为空则使用默认角度）

        Returns:
            不同角度的创意建议
        """
        if not angles:
            angles = [
                "浪漫冒险",
                "黑暗悬疑",
                "科幻未来",
                "历史寓言",
                "心理剧局"
            ]

        results = {}

        for angle in angles:
            prompt = f"""从'{angle}'的角度，为以下主题生成创意故事想法：
主题：{topic}

要求：
- 独特的视角
- 具体的情节要素
- 人物设定
- 故事张力"""

            response = self.api.generate_creative(
                prompt,
                style=angle,
                length="medium",
                use_reasoning=True
            )

            results[angle] = response or "生成失败"
            logger.info(f"✅ 生成角度：{angle}")

        return results

    def character_deep_dive(
        self,
        character_name: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        深入分析人物 - 性格、动机、弧线等

        Args:
            character_name: 人物名称
            context: 故事背景

        Returns:
            详细的人物分析
        """
        prompt = f"""深入分析人物：{character_name}

请提供：
1. 核心性格特征
2. 隐藏的动机和欲望
3. 心理弱点
4. 潜在的成长弧线
5. 与其他角色的动态关系
6. 如何使其更复杂和真实
7. 可能的转折点

{'故事背景：' + context if context else ''}"""

        result = self.api.chat_with_reasoning([
            {"role": "system", "content": "你是一位资深的人物心理学专家和编剧。"},
            {"role": "user", "content": prompt}
        ], depth="deep")

        return result

    def plot_structure_analysis(
        self,
        plot_outline: str
    ) -> Dict[str, Any]:
        """
        分析故事结构和情节走向

        Args:
            plot_outline: 情节概述

        Returns:
            结构分析结果
        """
        prompt = f"""分析以下故事结构：

【情节概述】
{plot_outline}

请分析：
1. 整体结构（三幕式/五幕式/其他）
2. 情节高潮和低潮点
3. 转折点的有效性
4. 冲突的递升
5. 结局的说服力
6. 潜在的节奏问题
7. 改进建议"""

        result = self.api.chat_with_reasoning([
            {"role": "system", "content": "你是一位资深的编剧和故事结构专家。"},
            {"role": "user", "content": prompt}
        ], depth="deep")

        return result

    def dialogue_generation(
        self,
        character1_name: str,
        character2_name: str,
        scene: str,
        character_details: Optional[Dict[str, str]] = None
    ) -> str:
        """
        生成自然的对话

        Args:
            character1_name: 第一个人物
            character2_name: 第二个人物
            scene: 场景描述
            character_details: 人物详情

        Returns:
            生成的对话
        """
        prompt = f"""为以下场景生成自然的对话：

人物 1：{character1_name}
人物 2：{character2_name}
场景：{scene}

要求：
- 对话要自然和真实
- 反映人物个性
- 推进故事情节
- 避免冗长的说教

{self._format_character_details(character_details)}"""

        return self.api.generate_creative(
            prompt,
            length="medium",
            use_reasoning=False  # 对话生成不需要推理
        ) or "对话生成失败"

    def worldbuilding_expansion(
        self,
        world_concept: str,
        aspect: str = "general"
    ) -> Dict[str, str]:
        """
        扩展和完善世界观设定

        Args:
            world_concept: 世界概念
            aspect: 关注方面 (general/culture/technology/economy/history/geography)

        Returns:
            世界观详细设定
        """
        aspects_prompt = {
            "general": "从各个角度全面展开这个世界的设定",
            "culture": "详细描述这个世界的文化、习俗和社会结构",
            "technology": "描述这个世界的技术水平和实现方式",
            "economy": "解释这个世界的经济系统和贸易体系",
            "history": "创作这个世界的历史背景和重要事件",
            "geography": "详细描述这个世界的地理环境和气候"
        }

        prompt = f"""为以下世界观概念进行详细的设定扩展：

【世界概念】
{world_concept}

【扩展方向】
{aspects_prompt.get(aspect, aspects_prompt['general'])}

要求：
- 逻辑一致和自洽
- 具体的细节和例子
- 考虑长期的影响
- 独特和有趣"""

        result = self.api.chat_with_reasoning([
            {"role": "system", "content": "你是一位资深的世界观设计师和创意导演。"},
            {"role": "user", "content": prompt}
        ], depth="deep")

        return result

    def style_transfer(
        self,
        text: str,
        target_style: str
    ) -> str:
        """
        风格转换 - 用不同风格重写文本

        Args:
            text: 原始文本
            target_style: 目标风格

        Returns:
            转换后的文本
        """
        prompt = f"""用'{target_style}'的风格重写以下文本，保持原意但改变表达方式：

【原始文本】
{text}

【目标风格】
{target_style}

要求：
- 保留所有关键信息
- 完全转换风格
- 确保质量不下降
- 使其引人入胜"""

        return self.api.generate_creative(
            prompt,
            style=target_style,
            length="medium",
            use_reasoning=True
        ) or "风格转换失败"

    def feedback_and_improvement(
        self,
        text: str,
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        详细反馈和改进建议

        Args:
            text: 要反馈的文本
            focus_areas: 关注的方面

        Returns:
            反馈和改进建议
        """
        if not focus_areas:
            focus_areas = ["故事"、"人物"、"对话"、"节奏"、"语言"]

        prompt = f"""请对以下文本提供详细的反馈和改进建议：

【文本】
{text}

【关注方面】
{', '.join(focus_areas)}

对每个方面提供：
1. 当前做得好的地方
2. 需要改进的具体方面
3. 提供 2-3 个具体的改进建议
4. 示例修改"""

        result = self.api.chat_with_reasoning([
            {"role": "system", "content": "你是一位资深的编辑和创意顾问。"},
            {"role": "user", "content": prompt}
        ], depth="medium")

        return result

    @staticmethod
    def _format_character_details(details: Optional[Dict[str, str]]) -> str:
        """格式化人物详情"""
        if not details:
            return ""
        lines = ["人物详情："]
        for key, value in details.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)


if __name__ == "__main__":
    advanced = DeepSeekAdvanced()

    # 测试多角度头脑风暴
    print("\n🎨 多角度头脑风暴...")
    ideas = advanced.multi_angle_brainstorm("穿越到古代的年轻女性")
    for angle, idea in ideas.items():
        print(f"\n【{angle}】\n{idea[:300]}...")
