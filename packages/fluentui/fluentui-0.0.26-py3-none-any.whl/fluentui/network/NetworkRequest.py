import json
from typing import Callable

from PySide6.QtCore import Qt, QEventLoop, QUrl
from PySide6.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PySide6.QtWidgets import QApplication


class NetworkRequest(QNetworkRequest):
    __loop: QEventLoop = None
    manager = QNetworkAccessManager()

    def async_send(self, method: str,
                   data: dict = None, *,
                   finished: Callable = None,
                   download_progress: Callable[[int, int], None] = None,
                   upload_progress: Callable[[int, int], None] = None,
                   ) -> QNetworkReply:
        return self.send(method,
                         data,
                         sync=False,
                         finished=finished,
                         download_progress=download_progress,
                         upload_progress=upload_progress)

    def send(self, method: str,
             data: dict = None, *,
             sync=True,
             finished: Callable = None,
             download_progress: Callable[[int, int], None] = None,
             upload_progress: Callable[[int, int], None] = None,
             ) -> QNetworkReply:
        if method.upper() == 'POST':
            if data:
                if (ct := self.header('Content-Type')) == '':
                    data = '&'.join(f'{k}={v}' for k, v in data.items())
                    self.setHeader('Content-Type', 'application/x-www-form-urlencoded')
                if ct == 'application/json':
                    data = json.dumps(data).encode()
            reply = self.manager.post(self, data)
        else:
            reply = self.manager.get(self)

        if sync:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            if not self.__loop: self.__class__.__loop = QEventLoop()

            reply.finished.connect(self.__loop.quit)
            self.__loop.exec(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)

            QApplication.restoreOverrideCursor()
            return reply

        if finished: reply.finished.connect(finished)
        if upload_progress: reply.uploadProgress.connect(upload_progress)
        if download_progress: reply.downloadProgress.connect(download_progress)

        return reply

    def setHeader(self, header: QNetworkRequest.KnownHeaders | str, value: object) -> None:
        if isinstance(header, str):
            super().setRawHeader(header.encode(), f'{value}'.encode())
            return
        super().setHeader(header, value)

    def header(self, header: QNetworkRequest.KnownHeaders | str) -> object:
        if isinstance(header, str):
            return super().rawHeader(header).data().decode()
        return super().header(header)
    
    def urlString(self, options: QUrl.UrlFormattingOption) -> str:
        # noinspection PyUnresolvedReferences
        return self.url().toString(QUrl.FormattingOptions(options))
