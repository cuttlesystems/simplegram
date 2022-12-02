import typing

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QRectF, Signal
from PySide6.QtGui import QBrush, QColor, QPen, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from b_logic.data_objects import BotMessage, BotVariant


class MessageGraphicsItem(QGraphicsItem):
    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100
    _VARIANT_HEIGHT = 50
    _MESSAGE_COLOR = 0xceffff
    _TEXT_COLOR = 0x154545
    _PEN_COLOR = 0x137b7b
    _BORDER_THICKNESS = 3
    _ROUND_RADIUS = 30

    # message_moved = Signal(BotMessage)

    def __init__(self, message: BotMessage, variants: typing.List[BotVariant]):
        super().__init__()
        assert isinstance(message, BotMessage)
        assert all(isinstance(variant, BotVariant) for variant in variants)

        self._brush = QBrush(QColor(self._MESSAGE_COLOR))
        self._selected_pen = QPen(QColor(self._PEN_COLOR), self._BORDER_THICKNESS, QtCore.Qt.PenStyle.DotLine)
        self._normal_pen = QPen(QColor(self._PEN_COLOR), self._BORDER_THICKNESS, QtCore.Qt.PenStyle.SolidLine)

        self._message: BotMessage = message

        self._variants = variants

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

        self.setPos(QPointF(self._message.x, self._message.y))

    def get_message(self) -> BotMessage:
        return self._message

    def boundingRect(self) -> QRectF:
        rect = self._block_rect()
        x = rect.x() - self._BORDER_THICKNESS
        y = rect.y() - self._BORDER_THICKNESS
        width = rect.width() + self._BORDER_THICKNESS * 2
        height = rect.height() + self._BORDER_THICKNESS * 2
        return QRectF(x, y, width, height)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any) -> typing.Any:
        result = super().itemChange(change, value)
        # синхронизируем позицию графического элемента и координаты сообщения
        if change == QGraphicsItem.ItemPositionChange:
            assert isinstance(value, QPointF)
            new_position = value
            self._message.x = int(new_position.x())
            self._message.y = int(new_position.y())
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

        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(self._get_block_brush())
        painter.drawRoundedRect(self._block_rect(), 30, 30)

        if self.isSelected():
            painter.setPen(self._selected_pen)
        else:
            painter.setPen(self._normal_pen)

        painter.setBrush(self._brush)
        painter.drawRoundedRect(self._message_rect(), self._ROUND_RADIUS, self._ROUND_RADIUS)
        painter.setPen(QColor(self._TEXT_COLOR))
        painter.drawText(self._text_rect(), self._message.text)
        for variant_index, variant in enumerate(self._variants):
            painter.setBrush(QColor(0x376497))
            painter.drawRect(self._variant_rect(variant_index))
            painter.setPen(QColor(self._TEXT_COLOR))
            painter.drawText(self._variant_text_rect(variant_index), variant.text)

    def _get_block_brush(self) -> QBrush:
        gradient = QLinearGradient(0, 0, 100, 100)

        block_brush_color1 = QColor(0xb4e6ce)
        block_brush_color1.setAlpha(200)

        block_brush_color2 = QColor(0xaef7d5)
        block_brush_color2.setAlpha(50)

        gradient.setColorAt(0, block_brush_color1)
        gradient.setColorAt(1, block_brush_color2)
        block_brush = QBrush(gradient)
        return block_brush

    def _variant_rect(self, variant_index: int) -> QRectF:
        dy = self._VARIANT_HEIGHT + 20
        return QRectF(
            0,
            self._MSG_HEIGHT + 20 + dy * variant_index,
            self._MSG_WIDTH,
            self._VARIANT_HEIGHT)

    def _variant_text_rect(self, variant_index: int) -> QRectF:
        variant_rect = self._variant_rect(variant_index)
        return QRectF(
            variant_rect.x() + 10, variant_rect.y() + 10,
            variant_rect.width() - 5, variant_rect.height() - 5)

    def _message_rect(self) -> QRectF:
        return QRectF(0, 0, self._MSG_WIDTH, self._MSG_HEIGHT)

    def _text_rect(self) -> QRectF:
        return QRectF(25, 25, self._MSG_WIDTH - 50, self._MSG_HEIGHT - 50)

    def _block_rect(self) -> QRectF:
        rect = self._message_rect()
        for variant_index, variant in enumerate(self._variants):
            rect = rect.united(self._variant_rect(variant_index))

        x = rect.x() - 25
        y = rect.y() - 25
        width = rect.width() + 50
        height = rect.height() + 50
        return QRectF(x, y, width, height)