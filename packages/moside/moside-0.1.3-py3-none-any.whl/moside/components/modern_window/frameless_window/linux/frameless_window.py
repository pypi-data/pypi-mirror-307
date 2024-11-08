from PySide6.QtCore import QCoreApplication, Qt, QEvent, QObject
from loguru import logger

from .window_effect import LinuxWindowEffect
from .....utils.linux_utils import LinuxMoveResize


class FramelessWindow(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('Linux FramelessWindow init')
        self._resizeable = True
        self._resize_grip_wight = 8

    def apply_frameless(self):
        """
        应用框架模式。
        这些操作必须在所有基类都初始化之后再做。
        受继承顺序影响，将这些操作放在当前类的init方法里面的话，会导致一些功能失效。
        所以将这些操作放在apply_frameless方法里面，然后在最终的子类的init方法里面调用这个方法。
        """
        logger.debug('Linux FramelessWindow apply_frameless')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # 隐藏系统标题栏和边框
        self.windowEffect = LinuxWindowEffect(self)
        self.windowEffect.addWindowAnimation(self.winId())  # 窗体动画
        self.windowEffect.addShadowEffect(self.winId())  # 窗体阴影
        QCoreApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._resizeable:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPos() - self.pos()
        if pos.x() < self._resize_grip_wight:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width() - self._resize_grip_wight:
            edges |= Qt.RightEdge
        if pos.y() < self._resize_grip_wight:
            edges |= Qt.TopEdge
        if pos.y() >= self.height() - self._resize_grip_wight:
            edges |= Qt.BottomEdge

        # change cursor
        if et == QEvent.MouseMove and self.windowState() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        elif obj in (self, self.titlebar) and et == QEvent.MouseButtonPress and edges:
            LinuxMoveResize.starSystemResize(self, event.globalPos(), edges)

        return False
