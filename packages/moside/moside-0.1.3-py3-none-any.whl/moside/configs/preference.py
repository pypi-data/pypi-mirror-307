from enum import Enum

from .base import BaseConfig


class Languages(str, Enum):
    auto = 'Auto'
    en_us = 'en_US'
    zh_cn = 'zh_CN'

    def __str__(self):
        return self.value


class Styles(str, Enum):
    dracula = 'Dracula'

    def __str__(self):
        return self.value


class Themes(str, Enum):
    dark = 'Dark'
    light = 'Light'

    def __str__(self):
        return self.value


# TODO 考虑是否需要将json文件保存到用户目录
class Preference(BaseConfig):
    """
    “设置”，使用 Preference 来定义用户偏好设置或模块特定的可调整参数，这些参数可能会在运行时发生变化。

    Attributes:
        persistent (bool): 指示是否将设置保留到文件中。
        filename (str): 从中加载设置以及保存设置的 JSON 文件。
    """
    # i18n
    language: str = Languages.auto  # 当前语言

    # 摩登UI
    style: str = Styles.dracula  # 风格，目前暂时只有 'dracula'
    theme: str = Themes.dark  # 主题，接受 'light'、'dark'、'auto'，目前暂时只有 'dark'
    colorful: bool = True  # 启用彩色特效
    expand_navbar: bool = False  # 启动时展开导航栏


preferences = Preference()
