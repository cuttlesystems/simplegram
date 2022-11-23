import typing

import PySide6
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QRectF, QPoint, QPointF
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsItem


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


class BotScene(QGraphicsScene):
    def __init__(self, parent: QtCore.QObject):
        super().__init__(parent=parent)

        self._brush = QBrush(QColor(0xceffff))

        self._background_brush = QBrush(QColor(0xf0ffff))

        self._background_pen = QPen(QColor(0xc5ecec), 5, QtCore.Qt.DotLine)

        self._background_rect = self.addRect(
            QtCore.QRect(0, 0, 480, 640),
            pen=self._background_pen,
            brush=self._background_brush
        )

        self._messages_rects: typing.List[QGraphicsRectItem] = []

        self.add_message(100, 10)

        self.add_message(100, 180)

        self.changed.connect(self._on_item_changed)

    def add_message(self, x: int, y: int):
        self._messages_rects.append(self._create_message(x, y))

    def _get_work_field_rect(self) -> QRectF:
        result = QRectF(0, 0, 640, 480)
        for message_rect in self._messages_rects:
            result = result.united(message_rect.sceneBoundingRect())
        return result

    def _on_item_changed(self, region):
        print('changed ', region)

        items_bounding_rect: QRectF = self._get_work_field_rect()
        background_rect_size = self._extend_rect(items_bounding_rect, 50, 50)
        self._background_rect.setRect(background_rect_size)
        scene_rect_size = self._extend_rect(background_rect_size, 30, 30)
        self.setSceneRect(scene_rect_size)
        print('background rect ', background_rect_size)
        print('scene rect ', scene_rect_size)

    def _extend_rect(self, rect: QRectF, by_x: float, by_y: float) -> QRectF:
        x = rect.x() - by_x
        y = rect.y() - by_y
        width = rect.width() + by_x * 2
        height = rect.height() + by_y * 2
        return QRectF(x, y, width, height)

    def _create_message(self, x: int, y: int) -> QGraphicsItem:
        rect = MessageGraphicsItem(float(x), float(y))
        self.addItem(rect)

        assert isinstance(rect, QGraphicsItem)
        return rect
