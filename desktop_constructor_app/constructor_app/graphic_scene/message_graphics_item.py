import typing

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QRectF, Signal
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsItem

from b_logic.data_objects import BotMessage


class MessageGraphicsItem(QGraphicsItem):
    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100
    _MESSAGE_COLOR = 0xceffff
    _PEN_COLOR = 0x137b7b
    _BORDER_THICKNESS = 5
    _ROUND_RADIUS = 30

    # message_moved = Signal(BotMessage)

    def __init__(self, x: float, y: float, message: BotMessage):
        super().__init__()
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(message, BotMessage)

        self._brush = QBrush(QColor(self._MESSAGE_COLOR))
        self._selected_pen = QPen(QColor(self._PEN_COLOR), self._BORDER_THICKNESS, QtCore.Qt.PenStyle.DotLine)
        self._normal_pen = QPen(QColor(self._PEN_COLOR), self._BORDER_THICKNESS, QtCore.Qt.PenStyle.SolidLine)

        self._message: BotMessage = message

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

        self.setPos(QPointF(x, y))

        # после setPos происходит зануление координат, чуть подкостыляем пока что так
        self._message.x = int(x)
        self._message.y = int(y)

    def get_message(self) -> BotMessage:
        return self._message

    def boundingRect(self) -> QRectF:
        rect = self._graphic_rect()
        x = rect.x() - self._BORDER_THICKNESS
        y = rect.y() - self._BORDER_THICKNESS
        width = rect.width() + self._BORDER_THICKNESS * 2
        height = rect.height() + self._BORDER_THICKNESS * 2
        return QRectF(x, y, width, height)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any) -> typing.Any:
        result = super().itemChange(change, value)
        # синхронизируем позицию графического элемента и координаты сообщения
        if change == QGraphicsItem.ItemPositionChange:
            position = self.pos()
            self._message.x = int(position.x())
            self._message.y = int(position.y())
            # self.message_moved.emit(self._message)
        return result

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionGraphicsItem,
            widget: typing.Optional[QtWidgets.QWidget]):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(option, QtWidgets.QStyleOptionGraphicsItem)
        assert isinstance(widget, QtWidgets.QWidget) or widget is None
        if self.isSelected():
            painter.setPen(self._selected_pen)
        else:
            painter.setPen(self._normal_pen)
        painter.setBrush(self._brush)
        painter.drawRoundedRect(self._graphic_rect(), self._ROUND_RADIUS, self._ROUND_RADIUS)
        painter.drawText(self._text_rect(), self._message.text)

    def _graphic_rect(self) -> QRectF:
        return QRectF(0, 0, self._MSG_WIDTH, self._MSG_HEIGHT)

    def _text_rect(self) -> QRectF:
        return QRectF(25, 25, self._MSG_WIDTH - 50, self._MSG_HEIGHT - 50)
