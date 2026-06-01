"""DeepSeek V4 API 封装模块 - 充分发挥 V4 的所有功能"""

import os
import json
from typing import Optional, List, Dict, Any, Generator
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class DeepSeekAPI:
    """DeepSeek V4 API 客户端 - 完整功能集成"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        初始化 DeepSeek V4 API 客户端

        Args:
            api_key: API Key
            base_url: API 基础 URL
            model: 模型名称 (deepseek-v4-pro / deepseek-v4)
            timeout: 请求超时时间
            max_retries: 最大重试次数
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or os.getenv(
            "DEEPSEEK_API_BASE",
            "https://api.deepseek.com/v1"
        )
        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
        self.timeout = timeout
        self.max_retries = max_retries

        # 获取高级参数
        self.temperature = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("DEEPSEEK_MAX_TOKENS", "4000"))
        self.top_p = float(os.getenv("DEEPSEEK_TOP_P", "0.95"))
        self.enable_reasoning = os.getenv("DEEPSEEK_ENABLE_REASONING", "true").lower() == "true"
        self.reasoning_depth = os.getenv("DEEPSEEK_REASONING_DEPTH", "medium")

        if not self.api_key:
            raise ValueError("❌ DEEPSEEK_API_KEY 未找到，请在 .env 文件中配置")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout
        )

        logger.info(f"✅ DeepSeek V4 API 已初始化 | 模型: {self.model} | 推��模式: {self.enable_reasoning}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Optional[str]:
        """
        发送聊天完成请求到 DeepSeek V4

        Args:
            messages: 消息列表
            temperature: 采样温度
            max_tokens: 最大输出 token
            stream: 是否流式输出
            **kwargs: 其他参数

        Returns:
            响应文本或 None
        """
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or self.max_tokens

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                    top_p=self.top_p,
                    **kwargs
                )

                if stream:
                    return response

                return response.choices[0].message.content

            except (APIConnectionError, RateLimitError) as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ API 错误 (重试 {attempt + 1}/{self.max_retries}): {e}")
                    import time
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                logger.error(f"❌ API 调用失败: {e}")
                return None

            except APIError as e:
                logger.error(f"❌ DeepSeek API 错误: {e}")
                return None

            except Exception as e:
                logger.error(f"❌ 未预期的错误: {e}")
                return None

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        流式聊天响应 - 实时输出

        Args:
            messages: 消息列表
            temperature: 采样温度
            max_tokens: 最大输出 token
            **kwargs: 其他参数

        Yields:
            响应文本片段
        """
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or self.max_tokens

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                top_p=self.top_p,
                **kwargs
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"❌ 流式输出错误: {e}")
            yield None

    def chat_with_reasoning(
        self,
        messages: List[Dict[str, str]],
        depth: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        启用推理模式的聊天 - DeepSeek V4 特有功能
        
        此功能让 DeepSeek 进行深度思考，产生更高质量的创意

        Args:
            messages: 消息列表
            depth: 推理深度 (light/medium/deep)
            **kwargs: 其他参数

        Returns:
            包含推理过程和最终答案的字典
        """
        depth = depth or self.reasoning_depth

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # 推理模式使用较低温度
                max_tokens=8000,  # V4 支持更长输出
                top_p=0.9,
                **{
                    **kwargs,
                    "reasoning_mode": depth  # DeepSeek V4 推理参数
                }
            )

            # 提取推理过程和最终答案
            content = response.choices[0].message.content

            return {
                "reasoning": self._extract_reasoning(content),
                "answer": self._extract_answer(content),
                "full_response": content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

        except Exception as e:
            logger.error(f"❌ 推理模式错误: {e}")
            return {"error": str(e)}

    def analyze_text(
        self,
        text: str,
        instruction: str = "分析以下文本：",
        use_reasoning: bool = True,
        **kwargs
    ) -> Optional[str]:
        """
        分析文本内容 - 使用推理模式获得更深入的分析

        Args:
            text: 要分析的文本
            instruction: 分析指令
            use_reasoning: 是否使用推理模式
            **kwargs: 其他参数

        Returns:
            分析结果
        """
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的小说编辑和文学评论家。你的任务是提供深入的、建设性的反馈。"
            },
            {
                "role": "user",
                "content": f"{instruction}\n\n{text}"
            }
        ]

        if use_reasoning and self.enable_reasoning:
            result = self.chat_with_reasoning(messages, depth="medium", **kwargs)
            return result.get("answer") or result.get("full_response")

        return self.chat(messages, **kwargs)

    def generate_creative(
        self,
        prompt: str,
        context: Optional[str] = None,
        style: Optional[str] = None,
        length: str = "medium",
        use_reasoning: bool = True,
        **kwargs
    ) -> Optional[str]:
        """
        生成创意内容 - 特别优化用于小说写作

        Args:
            prompt: 创意请求
            context: 背景信息
            style: 写作风格
            length: 输出长度 (short/medium/long)
            use_reasoning: 是否使用推理模式
            **kwargs: 其他参数

        Returns:
            生成的创意内容
        """
        # 长度对应的 token 数
        length_tokens = {
            "short": 800,
            "medium": 1500,
            "long": 3000
        }

        system_msg = "你是一位富有创意的专业小说作家。你的写作充满想象力、细节丰富、情感深刻。"
        if style:
            system_msg += f"\n写作风格：{style}"

        content_parts = [prompt]
        if context:
            content_parts.insert(0, f"背景信息：{context}")

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": "\n\n".join(content_parts)}
        ]

        max_tokens = length_tokens.get(length, 1500)

        if use_reasoning and self.enable_reasoning:
            result = self.chat_with_reasoning(messages, depth="deep", max_tokens=max_tokens, **kwargs)
            return result.get("answer") or result.get("full_response")

        return self.chat(messages, max_tokens=max_tokens, **kwargs)

    def check_consistency(
        self,
        content: str,
        check_type: str = "general",
        use_reasoning: bool = True,
        **kwargs
    ) -> Optional[str]:
        """
        检查内容一致性 - 使用推理模式进行深度检查

        Args:
            content: 要检查的内容
            check_type: 检查类型 (general/character/timeline/worldbuilding)
            use_reasoning: 是否使用推理模式
            **kwargs: 其他参数

        Returns:
            检查结果
        """
        check_prompts = {
            "general": "检查这段文本的逻辑一致性、矛盾之处和异常。",
            "character": "检查人物一致性 - 人物的性格、行为和描述是否一致？",
            "timeline": "检查时间线一致性 - 日期和时间关系是否正确？",
            "worldbuilding": "检查世界观一致性 - 世界设定和规则是否一致？"
        }

        instruction = check_prompts.get(check_type, check_prompts["general"])
        return self.analyze_text(content, instruction, use_reasoning, **kwargs)

    def suggest_continuation(
        self,
        previous_text: str,
        style_guide: Optional[str] = None,
        length: str = "medium",
        **kwargs
    ) -> Optional[str]:
        """
        建议故事续写 - 保持连贯性和风格一致

        Args:
            previous_text: 前文内容
            style_guide: 风格指南
            length: 续写长度
            **kwargs: 其他参数

        Returns:
            续写内容
        """
        prompt = "基于以下故事内容，建议接下来会发生什么。保持与人物和情节的一致性。"

        return self.generate_creative(
            prompt,
            context=previous_text,
            style=style_guide,
            length=length,
            use_reasoning=True,
            **kwargs
        )

    def test_connection(self) -> bool:
        """
        测试 API 连接

        Returns:
            连接是否成功
        """
        try:
            response = self.chat(
                [{"role": "user", "content": "你好"}],
                max_tokens=10
            )
            return response is not None
        except Exception as e:
            logger.error(f"❌ 连接测试失败: {e}")
            return False

    @staticmethod
    def _extract_reasoning(content: str) -> str:
        """从响应中提取推理过程"""
        if "<reasoning>" in content and "</reasoning>" in content:
            start = content.find("<reasoning>") + len("<reasoning>")
            end = content.find("</reasoning>")
            return content[start:end].strip()
        return ""

    @staticmethod
    def _extract_answer(content: str) -> str:
        """从响应中提取最终答案"""
        if "<answer>" in content and "</answer>" in content:
            start = content.find("<answer>") + len("<answer>")
            end = content.find("</answer>")
            return content[start:end].strip()
        return content


if __name__ == "__main__":
    api = DeepSeekAPI()

    # 测试连接
    if api.test_connection():
        logger.info("✅ DeepSeek V4 API 连接成功")
    else:
        logger.error("❌ DeepSeek V4 API 连接失败")

    # 测试推理模式
    print("\n🧠 测试推理模式...")
    result = api.chat_with_reasoning([
        {"role": "user", "content": "为一部时间旅行爱情故事写开头"}
    ])
    print(f"\n🤔 推理过程:\n{result.get('reasoning', 'N/A')}")
    print(f"\n✍️ 生成内容:\n{result.get('answer', 'N/A')}")
