from PySide6.QtCore import Slot, QMetaObject, QCoreApplication
from PySide6.QtWidgets import QFrame

from .design import Ui_ModernPreference
from ...configs.preference import preferences, Languages, Styles, Themes
from ...core.translation import trans_manager
from ...utils.animation import create_animation


class ModernPreference(QFrame, Ui_ModernPreference):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setMaximumWidth(0)  # 默认不显示
        self.setMinimumWidth(0)  # 默认不显示

        # Self 动画
        self.animation_on = create_animation(self, b'minimumWidth', 0, 240)
        self.animation_off = create_animation(self, b'minimumWidth', 240, 0)

        # 加载翻译选项
        for member in Languages:
            self.cmb_lang.addItem('', member)
            if preferences.language == member:
                self.cmb_lang.setCurrentIndex(self.cmb_lang.count() - 1)
        # 为当前组件连接翻译器
        trans_manager.signal_apply.connect(lambda: self.retranslateUi(self))

        # 加载风格选项
        for member in Styles:
            self.cmb_style.addItem(member, member)
            if preferences.style == member:
                self.cmb_style.setCurrentIndex(self.cmb_style.count() - 1)

        # 加载主题选项
        for member in Themes:
            self.cmb_theme.addItem(member, member)
            if preferences.theme == member:
                self.cmb_theme.setCurrentIndex(self.cmb_theme.count() - 1)

        # 应用呼吸特效
        self.chk_colorful.setChecked(preferences.colorful)

        # 展开导航
        self.chk_expand.setChecked(preferences.expand_navbar)

        # 连接信号槽
        QMetaObject.connectSlotsByName(self)

    @Slot(int)
    def on_cmb_lang_currentIndexChanged(self, index):
        preferences.language = self.cmb_lang.itemData(index)
        trans_manager.apply(preferences.language)

    @Slot(bool)
    def on_chk_colorful_toggled(self, checked):
        self.window().titlebar.frm_colorful.show() if checked else self.window().titlebar.frm_colorful.hide()
        preferences.colorful = checked

    @Slot(bool)
    def on_chk_expand_toggled(self, checked):
        preferences.expand_navbar = checked

    def on_toggle(self, checked):
        if checked:
            self.animation_off.stop()
            self.animation_on.stop()
            self.animation_on.start()
        else:
            self.animation_off.stop()
            self.animation_on.stop()
            self.animation_off.start()

    def retranslateUi(self, obj):
        super().retranslateUi(obj)

        for i in range(self.cmb_lang.count()):
            source_text = self.cmb_lang.itemData(i)
            self.cmb_lang.setItemText(i, QCoreApplication.translate("ModernPreference", source_text, None))
