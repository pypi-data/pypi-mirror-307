from PySide6.QtGui import QColor, QFontDatabase, QFont


class FontDatabase(QFontDatabase):
    @classmethod
    def applicationFontFamilies(cls, fileNames: list[str]) -> list[str]:
        return [super().applicationFontFamilies(y) for
                y in [super().addApplicationFont(x) for x in fileNames]]


class Font(QFont):
    def __init__(self,
                 families='Segoe UI, Microsoft YaHei UI, PingFang SC', *,
                 pixel=0,
                 point=0,
                 weight=QFont.Weight.Normal,
                 italic=False,
                 ):
        super().__init__([x.strip() for x in families.split(',')], -1, weight, italic)
        if pixel > 0: self.setPixelSize(pixel)
        if point > 0: self.setPointSize(point)


class Color(QColor):
    def __init__(self, name='', alpha: float = 1):
        super().__init__(name)
        self.setAlphaF(alpha)
