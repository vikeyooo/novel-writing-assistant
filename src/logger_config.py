"""日志配置模块"""

import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def setup_logger():
    """设置日志系统"""
    log_dir = os.getenv("LOG_DIR", "./data/logs")
    os.makedirs(log_dir, exist_ok=True)

    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_rotation = os.getenv("LOG_ROTATION", "500 MB")
    log_retention = os.getenv("LOG_RETENTION", "7")

    # 移除默认处理器
    logger.remove()

    # 控制台输出
    logger.add(
        lambda msg: print(msg, end=""),
        format="<level>{time:YYYY-MM-DD HH:mm:ss}</level> | <level>{level: <8}</level> | {message}",
        level=log_level
    )

    # 文件输出
    logger.add(
        os.path.join(log_dir, "app.log"),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level=log_level,
        rotation=log_rotation,
        retention=f"{log_retention} days",
        encoding="utf-8"
    )

    logger.info("✅ 日志系统已初始化")


if __name__ == "__main__":
    setup_logger()
    logger.info("测试日志")
