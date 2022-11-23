import typing

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsItem


class MessageGraphicsItem(QGraphicsItem):
    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100
    _MESSAGE_COLOR = 0xceffff
    _PEN_COLOR = 0x137b7b
    _BORDER_THICKNESS = 5

    def __init__(self, x: float, y: float):
        super().__init__()
        assert isinstance(x, float)
        assert isinstance(y, float)

        self._brush = QBrush(QColor(self._MESSAGE_COLOR))
        self._normal_pen = QPen(QColor(self._PEN_COLOR), self._BORDER_THICKNESS, QtCore.Qt.PenStyle.DotLine)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.setPos(QPointF(x, y))

    def _graphic_rect(self) -> QRectF:
        return QRectF(0, 0, self._MSG_WIDTH, self._MSG_HEIGHT)

    def boundingRect(self) -> QRectF:
        rect = self._graphic_rect()
        x = rect.x() - self._BORDER_THICKNESS
        y = rect.y() - self._BORDER_THICKNESS
        width = rect.width() + self._BORDER_THICKNESS * 2
        height = rect.height() + self._BORDER_THICKNESS * 2
        return QRectF(x, y, width, height)

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionGraphicsItem,
            widget: typing.Optional[QtWidgets.QWidget]):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(option, QtWidgets.QStyleOptionGraphicsItem)
        assert isinstance(widget, QtWidgets.QWidget) or widget is None
        painter.setPen(self._normal_pen)
        painter.setBrush(self._brush)
        painter.drawRect(self._graphic_rect())
