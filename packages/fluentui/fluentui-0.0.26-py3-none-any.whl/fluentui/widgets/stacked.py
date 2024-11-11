from PySide6.QtWidgets import QStackedWidget, QWidget

from .widget import WidgetMix


class StackedWidget(WidgetMix, QStackedWidget):
    def __init__(self,
                 *children: QWidget,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        for x in children or (): self.addWidget(x)
