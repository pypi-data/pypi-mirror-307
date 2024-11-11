from PySide6.QtCore import QAbstractItemModel
from PySide6.QtWidgets import QComboBox

from .widget import WidgetMix


class ComboBox(WidgetMix, QComboBox):
    def __init__(self, *,
                 max_visible=10,
                 items: list[str | dict | tuple] = None,
                 model: QAbstractItemModel = None,
                 editable=False,
                 select: int | str = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.setStyleSheet(self.qss.merge({
            'padding': '5 0',
            'border': '1 solid #d1d1d1',
            'border-radius': 4,
            '::drop-down': {'border': 'none', 'width': '20'},
            '::down-arrow': {
                'width': '16',
                'height': '16',
                'right': '4',
                'image': 'url(:/icons/chevron_down.svg)',
            }
        }))

        self.setEditable(editable)
        self.setMaxVisibleItems(max_visible)

        if model is not None:
            self.setModel(model)
        elif items:
            if isinstance(items[0], str):
                self.addItems(items)
            else:
                self.setItems(items)

        if isinstance(select, int):
            self.setCurrentIndex(select)
        elif isinstance(select, str):
            self.setCurrentText(select)

    def setItems(self, items: list[dict]) -> None:
        self.clear()
        for x in items:
            if not isinstance(x, tuple):  # dict
                x = tuple(x.items())[0]
            self.addItem(x[1], x[0])

    def selectText(self, text: str) -> int:
        if (index := self.findText(text)) >= 0:
            self.setCurrentIndex(index)
        return index

    def selectEditText(self, text: str) -> int:
        if (index := self.findText(text)) >= 0:
            self.setCurrentIndex(index)
        if index == -1:
            self.setEditText(text.strip())
        return index

    def selectData(self, data: object) -> int:
        if (index := self.findData(data)) >= 0:
            self.setCurrentIndex(index)
        return index
