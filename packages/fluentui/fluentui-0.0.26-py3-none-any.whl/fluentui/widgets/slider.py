from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider

from .widget import WidgetMix, StyleSheet


class Slider(WidgetMix, QSlider):
    def __init__(self, *length: int, value=0,
                 orient=Qt.Orientation.Horizontal,
                 value_changed: Callable[[int], None] = None,
                 **kwargs):
        super().__init__(orient, **kwargs)
        if value_changed: self.valueChanged.connect(value_changed)
        if length:
            if len(length) == 1: length = (0, length[0])
            self.setRange(*length)
        self.setValue(int(value))
        StyleSheet.apply(self)
