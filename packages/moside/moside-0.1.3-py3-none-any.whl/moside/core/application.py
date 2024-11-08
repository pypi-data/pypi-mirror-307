import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from loguru import logger

from .logger import modify_logger
from ..assets import resources  # noqa 载入资源文件
from ..configs.config import configs
from ..configs.preference import preferences


def create_modern_app(app_name, dev=False, log_level='INFO'):
    if app_name is None:
        raise ValueError('app_name is required.')

    # 设定个性化设置保存路径
    configs.app_name = app_name
    preferences.filepath = configs.config_dir / preferences.filepath.name
    preferences.persistent = True

    # 配置日志模块
    # 必须在logger初始化之前设置好log_level
    configs.log_level = log_level
    # 然后再定制logger
    modify_logger()

    # 配置开发模式（True从本地路径读取图片和样式，False从资源文件读取）
    configs.dev = dev
    if dev:
        logger.debug('Development mode enabled.')

    # 高分屏支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 如果是已存在的app实例
    if QApplication.instance():
        logger.debug('Use exist app instance')
        app = QApplication.instance()
    # 创建新的app实例
    else:
        logger.debug('Create new app instance')
        app = QApplication(sys.argv)
    # 解决子窗口关闭后鼠标指针样式失效的问题
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    return app
