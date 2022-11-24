import typing
from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsItem

from b_logic.data_objects import BotMessage
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

        self._message_graphics_list: typing.List[MessageGraphicsItem] = []

        self.changed.connect(self._on_item_changed)

    def clear_scene(self):
        for message in self._message_graphics_list:
            self.removeItem(message)
        self._message_graphics_list.clear()

    def add_message(self, message: BotMessage):
        # todo: тут надо проверять, что id уникальный и не конфликтует
        message_graphics = self._create_message_graphics(message)
        self._message_graphics_list.append(message_graphics)

    def get_selected_messages(self) -> typing.List[BotMessage]:
        result: typing.List[BotMessage] = []
        for item in self.selectedItems():
            item: MessageGraphicsItem
            assert isinstance(item, MessageGraphicsItem)
            result.append(item.get_message())

        return result

    def delete_messages(self, messages: typing.List[BotMessage]):
        deleted_messages_ids: typing.List[typing.Optional[int]] = [message.id for message in messages]

        # гарантия, что все сообщения с id
        assert all(isinstance(message, int) for message in deleted_messages_ids)

        deleted_messages_ids_set = set(deleted_messages_ids)

        # гарантия, что нет одинаковых id
        assert len(deleted_messages_ids_set) == len(deleted_messages_ids)

        removed_graphics_items: typing.List[MessageGraphicsItem] = [
            message_graphics
            for message_graphics in self._message_graphics_list
            if message_graphics.get_message().id in deleted_messages_ids_set
        ]

        for removed_graphics_item in removed_graphics_items:
            self.removeItem(removed_graphics_item)
            self._message_graphics_list.remove(removed_graphics_item)

    def get_all_messages(self) -> typing.List[BotMessage]:
        return [message_graphics.get_message() for message_graphics in self._message_graphics_list]

    def _get_work_field_rect(self) -> QRectF:
        result = QRectF(0, 0, self._MIN_WORKSPACE_WIDTH, self._MIN_WORKSPACE_HEIGHT)
        for message_rect in self._message_graphics_list:
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

    def _create_message_graphics(self, message: BotMessage) -> MessageGraphicsItem:
        rect = MessageGraphicsItem(float(message.x), float(message.y), message)
        self.addItem(rect)

        assert isinstance(rect, QGraphicsItem)
        return rect
