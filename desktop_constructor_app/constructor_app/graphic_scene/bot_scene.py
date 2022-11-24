import typing

from PySide6 import QtCore
from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsItem

from desktop_constructor_app.constructor_app.graphic_scene.message_graphics_item import MessageGraphicsItem


class BotScene(QGraphicsScene):
    """
    Сцена для отображения редактора бота
    """

    _WORKSPACE_BACKGROUND_COLOR = 0xf0ffff
    _WORKSPACE_BACKGROUND_BORDER_COLOR = 0xc5ecec
    _WORKSPACE_BACKGROUND_LINE_THICKNESS = 5
    _WORKSPACE_BACKGROUND_LINE_STYLE = QtCore.Qt.DotLine
    _MIN_WORKSPACE_WIDTH = 640
    _MIN_WORKSPACE_HEIGHT = 480

    def __init__(self, parent: QtCore.QObject):
        super().__init__(parent=parent)

        self._background_brush = QBrush(QColor(self._WORKSPACE_BACKGROUND_COLOR))

        self._background_pen = QPen(
            QColor(self._WORKSPACE_BACKGROUND_BORDER_COLOR),
            self._WORKSPACE_BACKGROUND_LINE_THICKNESS,
            self._WORKSPACE_BACKGROUND_LINE_STYLE
        )

        self._background_rect = self.addRect(
            QtCore.QRect(0, 0, self._MIN_WORKSPACE_WIDTH, self._MIN_WORKSPACE_HEIGHT),
            pen=self._background_pen,
            brush=self._background_brush
        )

        self._messages_rects: typing.List[QGraphicsRectItem] = []

        self.add_message(100, 10)

        self.add_message(100, 180)

        self.changed.connect(self._on_item_changed)

    def add_message(self, x: int, y: int):
        self._messages_rects.append(self._create_message(x, y))

    def get_selected_items(self) -> typing.List[QGraphicsRectItem]:
        return self.selectedItems()

    def delete_messages(self, messages: typing.List[QGraphicsRectItem]):
        for del_mes in messages:
            self._messages_rects.remove(del_mes)
            self.removeItem(del_mes)

    def _get_work_field_rect(self) -> QRectF:
        result = QRectF(0, 0, self._MIN_WORKSPACE_WIDTH, self._MIN_WORKSPACE_HEIGHT)
        for message_rect in self._messages_rects:
            result = result.united(message_rect.sceneBoundingRect())
        return result

    def _on_item_changed(self, region: typing.List[QRectF]):
        assert all(isinstance(r, QRectF) for r in region)
        items_bounding_rect: QRectF = self._get_work_field_rect()
        background_rect_size = self._extend_rect(items_bounding_rect, 50, 50)
        self._background_rect.setRect(background_rect_size)
        scene_rect_size = self._extend_rect(background_rect_size, 30, 30)
        self.setSceneRect(scene_rect_size)

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
