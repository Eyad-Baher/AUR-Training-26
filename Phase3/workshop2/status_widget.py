from PySide6.QtCore import QObject, QUrl
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import QWidget
from assets import get_asset  


class StatusWidget(QQuickWidget):

    def __init__(self,widget_filepath: str,data_bridge: QObject | None = None,parent: QWidget | None = None,):
        super().__init__(parent)

        self.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)

        self.setInitialProperties({"clockData": data_bridge})

        self.setSource(QUrl.fromLocalFile(get_asset(widget_filepath)))