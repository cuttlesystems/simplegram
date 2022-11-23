from PySide6 import QtCore
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsItem


class BotScene(QGraphicsScene):
    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100

    def __init__(self, parent: QtCore.QObject):
        super().__init__(parent=parent)

        self._brush = QBrush(QColor(0xceffff))

        self._background_brush = QBrush(QColor(0xf0ffff))

        self.setBackgroundBrush(self._background_brush)

        self.add_message(10, 10)

        self.add_message(10, 180)

    def add_message(self, x: int, y: int):
        self._create_message(x, y)

    def _create_message(self, x: int, y: int) -> QGraphicsRectItem:
        rect: QGraphicsRectItem = self.addRect(
            QtCore.QRect(x, y, self._MSG_WIDTH, self._MSG_HEIGHT), brush=self._brush)

        rect.setFlag(QGraphicsItem.ItemIsMovable, True)
        assert isinstance(rect, QGraphicsRectItem)
        return rect
