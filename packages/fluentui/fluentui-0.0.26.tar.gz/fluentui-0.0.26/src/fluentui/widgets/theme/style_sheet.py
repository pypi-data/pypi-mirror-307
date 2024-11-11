from enum import Enum
from types import ModuleType
from weakref import WeakKeyDictionary

from PySide6.QtWidgets import QWidget, QApplication

from . import light, dark
from .qss import Qss

widgets = WeakKeyDictionary[QWidget, str]()


class StyleSheet(Enum):
    Widget = 'Widget'
    Slider = 'Slider'
    Input = 'Input'
    Button = 'Button'
    PrimaryButton = 'PrimaryButton'
    SubtleButton = 'SubtleButton'
    DangerButton = 'DangerButton'
    InvisButton = 'InvisButton'
    RadioButton = 'RadioButton'

    def __call__(self, theme='light') -> dict:
        d: ModuleType = light if theme == 'light' else dark
        return d.__dict__.get(self.name, {})

    @classmethod
    def apply(cls, widget: QWidget, theme='auto') -> None:
        self = cls(widget.__class__.__name__)
        if widget not in widgets:
            theme = widget.property('color_scheme')
            widget.setProperty('color_scheme', None)

        if theme == 'auto':
            if parent := widget.parent():
                theme = widgets.get(parent, theme)  # 获取父主题
                if widgets.get(widget, None) == 'auto':
                    widgets.pop(widget, None)
            else:
                theme = QApplication.styleHints().colorScheme().name.lower()
                if widget not in widgets:
                    widgets[widget] = theme  # 记录 widget 的主题
                    widget.destroyed.connect(lambda: widgets.pop(widget, None))
        else:
            widgets[widget] = theme  # 记录 widget 的主题
            if widget not in widgets:
                widget.destroyed.connect(lambda: widgets.pop(widget, None))

        qss = Qss(self(theme))
        qss |= widget.property('custom-qss') or {}
        if not qss.d: return

        widget.setStyleSheet(qss)
        for x in widget.findChildren(QWidget):
            if widgets.get(x, None) != 'auto':
                continue
            qss = Qss(StyleSheet(x.__class__.__name__)(theme))
            qss |= x.property('custom-qss') or {}
            x.setStyleSheet(qss)
