from PySide6.QtCore import QUrl


class Url(QUrl):
    def toString(self, options=QUrl.UrlFormattingOption):
        # noinspection PyUnresolvedReferences
        super().toString(QUrl.UrlFormattingOptions(options))
