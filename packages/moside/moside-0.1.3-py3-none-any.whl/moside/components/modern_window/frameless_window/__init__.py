import sys

if sys.platform == "win32":
    from .windows import FramelessWindow
elif sys.platform == "linux":
    from .linux import FramelessWindow
