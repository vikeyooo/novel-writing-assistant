"""DeepSeek V4 小说创意助手 - 主程序初始化文件"""

__version__ = "2.0.0"
__author__ = "vikeyooo"
__description__ = "基于 DeepSeek V4 的本地化小说创意写作辅助工具"

from .deepseek_api import DeepSeekAPI
from .deepseek_advanced import DeepSeekAdvanced
from .web_searcher import WebSearcher
from .data_manager import DataManager
from .writing_assistant import WritingAssistant
from .consistency_checker import ConsistencyChecker
from .logger_config import setup_logger

__all__ = [
    'DeepSeekAPI',
    'DeepSeekAdvanced',
    'WebSearcher',
    'DataManager',
    'WritingAssistant',
    'ConsistencyChecker',
    'setup_logger',
]
