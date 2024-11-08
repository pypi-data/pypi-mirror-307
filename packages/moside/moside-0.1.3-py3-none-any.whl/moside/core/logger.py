import io
import sys

from ..configs.config import configs


def modify_logger():
    from loguru import logger
    # 移除默认的日志处理器，因为它的格式不理想
    logger.remove()
    # 添加默认日志记录器
    if sys.stderr is not None and sys.stdout is not None:
        logger.add(sys.stderr, level=configs.log_level)  # 将日志输出到标准错误输出，以便及时刷新
    else:
        sys.stderr = sys.stdout = io.StringIO()  # 如果当前程序运行在无终端的环境中，随便重定向一个输出

    return logger
