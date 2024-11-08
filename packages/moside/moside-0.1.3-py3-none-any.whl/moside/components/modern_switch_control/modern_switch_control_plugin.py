from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon, QPixmap

from moside.components.modern_switch_control import ModernSwitchControl


class SwitchControlPlugin(QDesignerCustomWidgetInterface):
    def __init__(self, parent=None):
        super(SwitchControlPlugin, self).__init__()
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return ModernSwitchControl(parent=parent)

    def name(self):
        return "ModernSwitchControl"

    def group(self):
        return "moside"

    def icon(self):
        return QIcon(_logo_pixmap)

    def toolTip(self):
        return "A customized and modern toggle-switch"

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return (
            '<widget class="ModernSwitchControl" name=\"ModernSwitchControl\">\n'
            "</widget>\n"
        )

    def includeFile(self):
        return "ModernSwitchControl"


_logo_16x16_xpm = []
_logo_pixmap = QPixmap(_logo_16x16_xpm)
