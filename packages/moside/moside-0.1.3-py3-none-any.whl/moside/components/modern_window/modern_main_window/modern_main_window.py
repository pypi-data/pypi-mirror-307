from pathlib import Path

from PySide6.QtCore import QLibraryInfo
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy
from loguru import logger

from ..frameless_window import FramelessWindow
from ...modern_navbar.modern_navbar import ModernNavBar
from ...modern_preference import ModernPreference
from ...modern_titlebar import ModernTitleBar
from ....configs import navigations
from ....configs.config import configs
from ....configs.preference import preferences
from ....core import trans_manager
from ....utils.qss_loader import load_stylesheet


class ModernMainWindow(FramelessWindow, QMainWindow):
    def __init__(self, *args, **kwargs):
        logger.debug('ModernMainWindow init')
        super().__init__(*args, **kwargs)
        # logger.debug(ModernMainWindow.mro())

    def apply_modern(self):

        # #########################################################
        # 0. 无框架
        # #########################################################
        # 应用无框架模式，需要在所有基类都完成初始化之后再执行这些操作
        # 受继承顺序影响，在FramelessWindow的init中执行这些操作会丢失部分特性
        # 这里选择将这些操作单独封装成一个方法，在此处手动调用
        self.apply_frameless()

        # #########################################################
        # 1. 样式
        # #########################################################
        # 应用样式表
        if configs.dev:
            style_path = Path(__file__).parents[
                             3] / 'assets' / 'themes' / preferences.style.lower() / 'styles' / preferences.theme.lower()
        else:
            style_path = f':themes/{preferences.style.lower()}/styles/{preferences.theme.lower()}'
        style_sheets = load_stylesheet(style_path)
        # logger.debug(style_sheets)
        self.setStyleSheet(style_sheets)

        # #########################################################
        # 2. 创建好各个容器和组件
        # #########################################################
        # 取出原本的中央部件备用
        central_widget = self.takeCentralWidget()  # 获取原本的centralWidget

        # Container垂直结构
        self.container = QFrame(self)  # 创建modern容器
        self.container.setObjectName("ModernContainer")  # 容器名称
        QVBoxLayout(self.container)  # 创建垂直布局
        self.container.layout().setSpacing(0)  # 内间距
        self.container.layout().setContentsMargins(0, 0, 0, 0)  # 内边距
        self.setCentralWidget(self.container)  # 设置摩登容器为当前的centralWidget

        # Container垂直结构--TitleBar控件
        self.titlebar = ModernTitleBar(self.container)  # 创建标题栏
        self.container.layout().addWidget(self.titlebar)  # 加入布局

        # Container垂直结构--TitleBar控件--菜单栏
        if hasattr(self, 'menubar'):
            self.titlebar.layout().insertWidget(1, self.menubar)
            self.menubar.setParent(self.titlebar)
            self.menubar.raise_()
            self.menubar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 设置菜单栏为固定宽度
            if self.menubar.actions().__len__() > 0:
                self.titlebar.lbl_text.setAlignment(Qt.AlignVCenter | Qt.AlignRight)  # 垂直居中，水平右对齐

        # Container垂直结构--Body垂直布局
        self.ly_body = QHBoxLayout()  # 创建水平布局
        self.ly_body.setSpacing(0)  # 内间距
        self.ly_body.setContentsMargins(0, 0, 0, 0)  # 内边距
        self.container.layout().addLayout(self.ly_body)  # 加入布局

        # Container垂直结构--Body垂直布局--Content垂直布局
        self.frm_content = QFrame(self)
        self.frm_content.setObjectName("ModernContent")
        QVBoxLayout(self.frm_content)  # 创建垂直布局
        self.frm_content.layout().setSpacing(0)  # 内间距
        self.frm_content.layout().setContentsMargins(0, 0, 0, 0)  # 内边距
        self.ly_body.addWidget(self.frm_content)

        # Container垂直结构--Body垂直布局--Content垂直布局--Central水平布局
        self.ly_central = QHBoxLayout()  # 创建水平布局
        self.ly_central.setSpacing(0)  # 内间距
        self.ly_central.setContentsMargins(0, 0, 0, 0)  # 内边距
        self.frm_content.layout().addLayout(self.ly_central)
        # 替换centralWidget控件
        if central_widget:  # 如果获取到centralWidget
            self.ly_central.addWidget(central_widget)  # 将原本的centralWidget添加到正确的布局中
        else:
            # TODO 有没有一种可能，没有找到centralWidget的情况？
            pass
        self.setCentralWidget(self.container)  # 设置摩登容器为当前的centralWidget

        # Container垂直结构--Body垂直布局--Content垂直布局--状态栏
        if hasattr(self, 'statusbar'):
            self.frm_content.layout().addWidget(self.statusbar)  # 将状态栏加入到布局
            self.statusbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 设置状态栏为固定高度

        # 菜单栏与偏好
        self.preference = ModernPreference(self.container)  # 创建NavBarExtra控件
        if navigations.items:  # 如果App中有导航项
            self.navbar = ModernNavBar(self.container)  # 创建NavBar控件
            self.ly_body.insertWidget(0, self.navbar)  # 将NavBar插入布局

            self.ly_body.insertWidget(1, self.preference)  # 将偏好设置插入布局
            self.navbar.btn_preference.toggled.connect(self.preference.on_toggle)  # 连接按钮的切换事件
            self.titlebar.btn_settings.hide()  # 隐藏标题栏的设置按钮
        else:
            self.ly_central.addWidget(self.preference)
            self.titlebar.btn_settings.toggled.connect(self.preference.on_toggle)  # 连接按钮的切换事件

        # #########################################################
        # 3. 翻译
        # #########################################################
        # 翻译引擎
        # QT翻译引擎
        # 注册Qt内置翻译文件
        # logger.debug('QLibraryTranslationPath: ' + QLibraryInfo.path(QLibraryInfo.TranslationsPath))
        trans_manager.add(QLibraryInfo.path(QLibraryInfo.TranslationsPath), 'qt')  # 注册Qt内置翻译文件
        trans_manager.add(':i18n/', 'modern_main_window')  # 注册资源中的翻译文件
        trans_manager.apply(preferences.language)  # 应用翻译
