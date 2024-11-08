from win32api import GetSystemMetrics
#
#
#
#
class WindowRect:
    x = GetSystemMetrics(0) // 4
    y = int(GetSystemMetrics(1) * 0.1)
    width = GetSystemMetrics(0) // 2
    height = int(GetSystemMetrics(1) * 0.8)
    #
    #
    #
    #
    def __init__(self, x: int = None, y: int = None, width: int = None, height: int = None):
        self.set_rect(x, y, width, height)
    #
    #
    #
    #
    def set_rect(self, x: int = None, y: int = None, width: int = None, height: int = None):
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        return self
