"""测试 DeepSeek API 连接"""

import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()

from src.deepseek_api import DeepSeekAPI
from loguru import logger


def test_connection():
    """测试 API 连接"""
    print("\n🔧 DeepSeek API 连接测试\n")

    try:
        api = DeepSeekAPI()
        print("✓ API 客户端创建成功")
        print(f"  模型: {api.model}")
        print(f"  推理模式: {'启用' if api.enable_reasoning else '禁用'}")

        print("\n⏳ 测试连接...")
        if api.test_connection():
            print("✅ DeepSeek API 连接成功！")
            print("\n🚀 系统已就绪，可以开始使用了！")
            return True
        else:
            print("❌ DeepSeek API 连接失败")
            print("\n请检查：")
            print("  1. 网络连接是否正常")
            print("  2. .env 文件中的 DEEPSEEK_API_KEY 是否正确")
            print("  3. API Key 是否过期或无效")
            return False

    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("\n请在 .env 文件中配置 DEEPSEEK_API_KEY")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
