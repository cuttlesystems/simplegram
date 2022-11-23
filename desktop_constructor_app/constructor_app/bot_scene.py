import typing

from PySide6 import QtCore
from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsItem


class BotScene(QGraphicsScene):
    _MSG_WIDTH = 150
    _MSG_HEIGHT = 100

    def __init__(self, parent: QtCore.QObject):
        super().__init__(parent=parent)

        self._brush = QBrush(QColor(0xceffff))

        self._background_brush = QBrush(QColor(0xf0ffff))

        # self.setSceneRect(5, 5, 300, 300)

        self._background_rect = self.addRect(QtCore.QRect(0, 0, 480, 640), brush=self._background_brush)

        self._messages_rects: typing.List[QGraphicsRectItem] = []

        self.add_message(10, 10)

        self.add_message(10, 180)

        self.changed.connect(self._on_item_changed)

        self._internal_scene_change = False

    def add_message(self, x: int, y: int):
        self._messages_rects.append(self._create_message(x, y))

    def _get_bounding_rect(self) -> QRectF:
        result = QRectF(0, 0, 0, 0)
        for message_rect in self._messages_rects:
            result = result.united(message_rect.sceneBoundingRect())
        return result

    def _on_item_changed(self, region):
        print('changed ', region)

        if not self._internal_scene_change:
            self._internal_scene_change = True
            try:
                items_bounding_rect: QRectF = self._get_bounding_rect()
                x = items_bounding_rect.x() - 5
                y = items_bounding_rect.y() - 5
                width = items_bounding_rect.width() + 10
                height = items_bounding_rect.height() + 10
                background_rect_size = QRectF(x, y, width, height)
                self._background_rect.setRect(background_rect_size)
                print('background rect ', background_rect_size)
            finally:
                self._internal_scene_change = False

    def _create_message(self, x: int, y: int) -> QGraphicsRectItem:
        rect: QGraphicsRectItem = self.addRect(
            QtCore.QRect(x, y, self._MSG_WIDTH, self._MSG_HEIGHT), brush=self._brush)

        rect.setFlag(QGraphicsItem.ItemIsMovable, True)
        assert isinstance(rect, QGraphicsRectItem)
        return rect
