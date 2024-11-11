from typing import Callable

from PySide6.QtGui import QValidator, QIntValidator
from PySide6.QtWidgets import QLineEdit

from .widget import WidgetMix, StyleSheet


class Input(WidgetMix, QLineEdit):
    def __init__(self, text: object = '', *,
                 placeholder='',
                 read_only=False,
                 text_changed: Callable[[str], ...] = None,
                 validator: QValidator = None,
                 **kwargs
                 ):
        super().__init__(f'{text}', **kwargs)
        if text_changed: self.textChanged.connect(text_changed)
        if validator is not None: self.setValidator(validator)

        self.setReadOnly(read_only)
        self.setPlaceholderText(placeholder)
        StyleSheet.apply(self)


def setText(self, text: object, block_signals=False):
    super().setText(f'{text}')
    if block_signals: self.blockSignals(True)
    self.setCursorPosition(0)
    if block_signals: self.blockSignals(False)


class IntInput(Input):
    def __init__(self, text='', **kwargs):
        super().__init__(text, validator=QIntValidator(), **kwargs)
