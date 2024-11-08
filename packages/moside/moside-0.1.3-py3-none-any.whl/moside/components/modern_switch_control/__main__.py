import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

from .modern_switch_control import ModernSwitchControl


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(400, 400)
        self.setWindowTitle("SwitchControl test")
        self.setStyleSheet("""
		background-color: #222222;
		""")
        switch_control = ModernSwitchControl()
        h_box = QHBoxLayout()
        h_box.addWidget(switch_control, Qt.AlignCenter, Qt.AlignCenter)
        self.setLayout(h_box)
        self.show()


app = QApplication(sys.argv)
form = Form()
if __name__ == '__main__':
    sys.exit(app.exec_())
