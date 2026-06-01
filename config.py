# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置类"""
    
    # 基础路径
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    
    # API配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_BASE = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com/v1')
    DEEPSEEK_MODEL = 'deepseek-chat'
    
    # 搜索API配置
    BING_SEARCH_API_KEY = os.getenv('BING_SEARCH_API_KEY', '')
    
    # 数据库配置
    DATABASE_PATH = DATA_DIR / 'novel_assistant.db'
    
    # 文档配置
    DOCUMENTS_PATH = DATA_DIR / 'documents'
    NOVELS_PATH = DATA_DIR / 'novels'
    CACHE_PATH = DATA_DIR / 'cache'
    EXPORTS_PATH = DATA_DIR / 'exports'
    
    # UI配置
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    WINDOW_TITLE = '小说大师AI创作助手'
    
    # 模型参数
    MAX_TOKENS = 4096
    TEMPERATURE = 0.7
    TOP_P = 0.95
    
    # 上下文配置
    MAX_CONTEXT_TOKENS = 32000
    CONTEXT_MEMORY_SIZE = 100
    
    # 文件支持
    SUPPORTED_FORMATS = ['.txt', '.md', '.docx', '.pdf']
    MAX_FILE_SIZE = 100 * 1024 * 1024
    
    # 功能开关
    ENABLE_INTERNET_SEARCH = True
    ENABLE_LOCAL_DOCUMENTS = True
    ENABLE_CONTEXT_LEARNING = True
    ENABLE_REGENERATE = True
    ENABLE_COPY = True
    ENABLE_SHARE = True
    
    @classmethod
    def create_dirs(cls):
        """创建必要的目录"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.DOCUMENTS_PATH.mkdir(exist_ok=True)
        cls.NOVELS_PATH.mkdir(exist_ok=True)
        cls.CACHE_PATH.mkdir(exist_ok=True)
        cls.EXPORTS_PATH.mkdir(exist_ok=True)

config = Config()
