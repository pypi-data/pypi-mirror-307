from typing import Callable

from PySide6.QtCore import Qt, Signal, QMetaMethod
from PySide6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLayout, QSizePolicy

from .theme import Qss, StyleSheet
from ..core import ObjectMix
from ..gui import Font


class WidgetMix(ObjectMix):
    on_close = Signal()
    on_key_enter_pressed = Signal(QWidget)
    on_clicked = Signal(QWidget)

    def __init__(
            # a、b、c、d、e、f、g、h、i、j、k、l、m、n、o、p、q、r、s、t、u、v、w、x、y、z
            self, *args,
            attrs: Qt.WidgetAttribute | set[Qt.WidgetAttribute | set[Qt.WidgetAttribute]] = None,
            color_scheme='auto',  # light, dark, auto
            drop_shadow_effect: QGraphicsDropShadowEffect = None,
            font: Font = None,
            layout: QLayout = None,
            mouse_tracking: bool = None,
            parent: QWidget = None,
            qss: dict = None,
            win_title='',
            win_flags: Qt.WindowType = None,

            size: int | str = '',
            width: int | str = '',
            height: int | str = '',
            row_span=1,
            column_span=1,
            align_self=Qt.AlignmentFlag(0),

            closed: Callable = None,
            clicked: Callable[[QWidget], None] = None,
            key_enter_pressed: Callable[[QWidget], None] = None,
            **kwargs
    ):
        self.__is_pressed = False
        self.row_span = row_span
        self.column_span = column_span
        self.align_self = align_self
        super().__init__(parent=parent, *args, **kwargs)

        self.setProperty('custom-qss', qss or {})
        # 只使用一次，应用主题后就会删除。
        self.setProperty('color_scheme', color_scheme)
        self.setWindowTitle(win_title)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        if closed: self.on_close.connect(closed)
        if clicked: self.on_clicked.connect(clicked)
        if key_enter_pressed: self.on_key_enter_pressed.connect(key_enter_pressed)

        if font is not None: self.setFont(font)
        if win_flags is not None: self.setWindowFlags(win_flags)
        if mouse_tracking is not None: self.setMouseTracking(mouse_tracking)
        if drop_shadow_effect is not None: self.setGraphicsEffect(drop_shadow_effect)

        if attrs is not None:
            for x in attrs if isinstance(attrs, set) else {attrs}:
                if isinstance(x, set):
                    for a in x: self.setAttribute(a, False)
                    continue
                self.setAttribute(x)

        self.__init_size(size, width, height)
        if layout is not None:
            self.setLayout(layout)

    def closeEvent(self, e: QCloseEvent) -> None:
        super().closeEvent(e)
        self.on_close.emit()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        if e.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.on_key_enter_pressed.emit(self)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.__is_pressed = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        super().mouseReleaseEvent(e)
        if self.__is_pressed:
            self.__is_pressed = False
            if self.isSignalConnected(QMetaMethod.fromSignal(self.on_clicked)):
                self.on_clicked.emit(self)

    def setStyleSheet(self, qss: dict | Qss) -> None:
        if isinstance(qss, dict):
            qss = Qss(qss)
        super().setStyleSheet(f'{self.__class__.__name__} ' + qss.build())

    def __init_size(self, size='', w='', h=''):
        size, w, h = f'{size}', f'{w}', f'{h}'  # 将参数字符串化

        if any(x == 'full' for x in (size, w, h)):
            if size == 'full': w, h = [size] * 2
            policy = self.sizePolicy()
            if w is not None:
                policy.setHorizontalPolicy(QSizePolicy.Policy.MinimumExpanding)
            if h is not None:
                policy.setVerticalPolicy(QSizePolicy.Policy.MinimumExpanding)
            self.setSizePolicy(policy)

        w, h = ['' if x == 'full' else x for x in (w, h)]
        if any(x != '' for x in (size, w, h)):
            if size != '':
                size = size.split()
                w, h = (size + [size[0]])[:2]

            if w.endswith('px') and h.endswith('px'):
                self.setFixedSize(int(w[:-2]), int(h[:-2]))
            elif w.endswith('px'):
                if h != '':
                    self.resize(int(w[:-2]), int(h))
                self.setFixedWidth(int(w[:-2]))
            elif h.endswith('px'):
                if w != '':
                    self.resize(int(w), int(h[:-2]))
                self.setFixedHeight(int(h[:-2]))
            else:
                self.resize(int(w or self.width()), int(h or self.height()))


class Widget(WidgetMix, QWidget):
    def __init__(self, layout: QLayout = None, **kwargs):
        super().__init__(layout=layout, **kwargs)
        StyleSheet.apply(self)
