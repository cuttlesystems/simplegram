import typing

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QRectF, Signal
from PySide6.QtGui import QBrush, QColor, QPen, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from b_logic.data_objects import BotMessage, BotVariant


class MessageGraphicsItem(QGraphicsItem):
    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100

    _VARIANT_WIDTH = 150
    _VARIANT_HEIGHT = 50

    _MESSAGE_COLOR = 0xceffff
    _TEXT_COLOR = 0x154545
    _PEN_COLOR = 0x137b7b
    _BORDER_THICKNESS = 3
    _ROUND_RADIUS = 30
    _VARIANT_BACKGROUND = 0x9edee6
    _BLOCK_RECT_EXTEND_SPACE = 25
    _MESSAGE_TEXT_ALIGN = 25
    _VARIANT_TEXT_ALIGN = 5
    _BOUNDING_RECT_SPARE_PAINTING_DISTANCE = 2
    _VARIANT_DISTANCE = 25

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
        x = rect.x() - self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE
        y = rect.y() - self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE
        width = rect.width() + self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE * 2
        height = rect.height() + self._BOUNDING_RECT_SPARE_PAINTING_DISTANCE * 2
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

        self._draw_block(painter)

        self._draw_message(painter)

        for variant_index, variant in enumerate(self._variants):
            self._draw_variant(painter, variant, variant_index)

    def _draw_block(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self._get_block_brush())
        painter.drawRoundedRect(self._block_rect(), 30, 30)

    def _draw_message(self, painter: QtGui.QPainter):
        if self.isSelected():
            painter.setPen(self._selected_pen)
        else:
            painter.setPen(self._normal_pen)

        painter.setBrush(self._brush)
        painter.drawRoundedRect(self._message_rect(), self._ROUND_RADIUS, self._ROUND_RADIUS)
        painter.setPen(QColor(self._TEXT_COLOR))
        painter.drawText(self._message_text_rect(), self._message.text)

    def _draw_variant(self, painter: QtGui.QPainter, variant: BotVariant, index: int):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(variant, BotVariant)
        assert isinstance(index, int)
        painter.setBrush(QColor(self._VARIANT_BACKGROUND))
        painter.setPen(self._normal_pen)
        painter.drawRect(self._variant_rect(index))
        painter.setPen(QColor(self._TEXT_COLOR))
        painter.drawText(self._variant_text_rect(index), variant.text)

    def _get_block_brush(self) -> QBrush:
        gradient = QLinearGradient(0, 0, 100, 100)

        block_brush_color_top_left = QColor(0xb4e6ce)
        block_brush_color_top_left.setAlpha(200)

        block_brush_color_right_bottom = QColor(0xaef7d5)
        block_brush_color_right_bottom.setAlpha(50)

        gradient.setColorAt(0.0, block_brush_color_top_left)
        gradient.setColorAt(1.0, block_brush_color_right_bottom)
        block_brush = QBrush(gradient)
        return block_brush

    def _variant_rect(self, variant_index: int) -> QRectF:
        dy = self._VARIANT_HEIGHT + self._VARIANT_DISTANCE
        return QRectF(
            0,
            self._MSG_HEIGHT + self._VARIANT_DISTANCE + dy * variant_index,
            self._VARIANT_WIDTH,
            self._VARIANT_HEIGHT)

    def _variant_text_rect(self, variant_index: int) -> QRectF:
        variant_rect = self._variant_rect(variant_index)
        return QRectF(
            variant_rect.x() + self._VARIANT_TEXT_ALIGN,
            variant_rect.y() + self._VARIANT_TEXT_ALIGN,
            variant_rect.width() - self._VARIANT_TEXT_ALIGN * 2,
            variant_rect.height() - self._VARIANT_TEXT_ALIGN * 2
        )

    def _message_rect(self) -> QRectF:
        return QRectF(0, 0, self._MSG_WIDTH, self._MSG_HEIGHT)

    def _message_text_rect(self) -> QRectF:
        return QRectF(
            self._MESSAGE_TEXT_ALIGN,
            self._MESSAGE_TEXT_ALIGN,
            self._MSG_WIDTH - self._MESSAGE_TEXT_ALIGN * 2,
            self._MSG_HEIGHT - self._MESSAGE_TEXT_ALIGN * 2
        )

    def _block_rect(self) -> QRectF:
        rect = self._message_rect()
        for variant_index, variant in enumerate(self._variants):
            rect = rect.united(self._variant_rect(variant_index))

        x = rect.x() - self._BLOCK_RECT_EXTEND_SPACE
        y = rect.y() - self._BLOCK_RECT_EXTEND_SPACE
        width = rect.width() + 2 * self._BLOCK_RECT_EXTEND_SPACE
        height = rect.height() + 2 * self._BLOCK_RECT_EXTEND_SPACE
        return QRectF(x, y, width, height)
