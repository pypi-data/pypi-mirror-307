from ctypes import cast
from ctypes.wintypes import LPRECT, MSG

import win32con
import win32gui
from PySide6.QtCore import Qt, QEvent, QObject
from PySide6.QtGui import QCursor
from loguru import logger

from .c_structures import LPNCCALCSIZE_PARAMS
from .window_effect import WindowsWindowEffect
from .....utils import win32_utils as win_utils
from .....utils.win32_utils import Taskbar


class FramelessWindow(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('Windows FramelessWindow init')
        self._resizeable = True
        self._resize_grip_wight = 8

    def apply_frameless(self):
        """
        应用框架模式。
        这些操作必须在所有基类都初始化之后再做。
        受继承顺序影响，将这些操作放在当前类的init方法里面的话，会导致一些功能失效。
        所以将这些操作放在apply_frameless方法里面，然后在最终的子类的init方法里面调用这个方法。
        """
        logger.debug('Windows FramelessWindow apply_frameless')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # 隐藏系统标题栏和边框
        self.windowEffect = WindowsWindowEffect(self)
        self.windowEffect.addWindowAnimation(self.winId())  # 窗体动画
        self.windowEffect.addShadowEffect(self.winId())  # 窗体阴影
        self.windowHandle().screenChanged.connect(self.__on_screen_changed)  # 监听屏幕变化
        self.nativeEvent = self.__nativeEvent  # 重写nativeEvent方法

    def __on_screen_changed(self):
        hwnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    def event(self, event):
        # 解决状态栏移动位置后功能失效的问题
        if event.type() == QEvent.StatusTip and hasattr(self, 'statusbar'):
            self.statusbar.showMessage(event.tip())
            return True
        return super().event(event)

    def __nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return False, 0

        if msg.message == win32con.WM_NCHITTEST and self._resizeable:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w = self.frameGeometry().width()
            h = self.frameGeometry().height()

            # fixes https://github.com/zhiyiYo/PyQt-Frameless-Window/issues/98
            bw = 0 if win_utils.isMaximized(msg.hWnd) or win_utils.isFullScreen(msg.hWnd) else self._resize_grip_wight
            lx = xPos < bw
            rx = xPos > w - bw
            ty = yPos < bw
            by = yPos > h - bw
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            isMax = win_utils.isMaximized(msg.hWnd)
            isFull = win_utils.isFullScreen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                ty = win_utils.getResizeBorderThickness(msg.hWnd, False)
                rect.top += ty
                rect.bottom -= ty

                tx = win_utils.getResizeBorderThickness(msg.hWnd, True)
                rect.left += tx
                rect.right -= tx

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and Taskbar.isAutoHide():
                position = Taskbar.getPosition(msg.hWnd)
                if position == Taskbar.LEFT:
                    rect.top += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.BOTTOM:
                    rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.LEFT:
                    rect.left += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.RIGHT:
                    rect.right -= Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result

        return False, 0
