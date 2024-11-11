from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea

from .frame import FrameMix


class AbsScrollAreaMix(FrameMix):
    def __init__(self, *,
                 hor_scroll_bar_policy=Qt.ScrollBarPolicy.ScrollBarAsNeeded,
                 ver_scroll_bar_policy=Qt.ScrollBarPolicy.ScrollBarAsNeeded,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setHorizontalScrollBarPolicy(hor_scroll_bar_policy)
        self.setVerticalScrollBarPolicy(ver_scroll_bar_policy)


class ScrollArea(AbsScrollAreaMix, QScrollArea):
    ...
