import typing

from PySide6 import QtCore
from PySide6.QtCore import QRectF, Signal
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsItem

from b_logic.data_objects import BotMessage, BotVariant, BotDescription
from desktop_constructor_app.constructor_app.graphic_scene.block_graphics_item import BlockGraphicsItem
from desktop_constructor_app.constructor_app.graphic_scene.colors.scene_color_scheme import SceneColorScheme


class BotScene(QGraphicsScene):
    """
    Сцена для отображения редактора бота
    """

    # толщина линии границы рабочей области
    _WORKSPACE_BACKGROUND_LINE_THICKNESS = 5

    # стиль линии границы рабочей области
    _WORKSPACE_BACKGROUND_LINE_STYLE = QtCore.Qt.DotLine

    # минимальный размер рабочей области (если нет ни одного сообщения)
    _MIN_WORKSPACE_WIDTH = 640
    _MIN_WORKSPACE_HEIGHT = 480

    # событие возникающее, когда сцена (пользователь) запрашивает добавление нового варианта для сообщения
    # (в списке передаются варианты сообщения)
    request_add_new_variant = Signal(BotMessage, list)

    # пользователь запросил изменение сообщения
    # (в списке передаются варианты сообщения BotVariant)
    request_change_message = Signal(BlockGraphicsItem, list)

    # пользователь запросил изменение варианта
    request_change_variant = Signal(BlockGraphicsItem, BotVariant)

    selection_changed = Signal()

    def __init__(self, parent: QtCore.QObject):
        super().__init__(parent=parent)

        self._bot: typing.Optional[BotDescription] = None

        self._scene_color_scheme = SceneColorScheme()

        self._background_brush = QBrush(QColor(self._scene_color_scheme.workspace_background_color))

        self._background_pen = QPen(
            QColor(self._scene_color_scheme.workspace_background_border_color),
            self._WORKSPACE_BACKGROUND_LINE_THICKNESS,
            self._WORKSPACE_BACKGROUND_LINE_STYLE
        )
        self._background_rect = self.addRect(
            QtCore.QRect(0, 0, self._MIN_WORKSPACE_WIDTH, self._MIN_WORKSPACE_HEIGHT),
            pen=self._background_pen,
            brush=self._background_brush
        )

        self._message_graphics_list: typing.List[BlockGraphicsItem] = []
        self._connect_signals()

    def get_bot(self):
        return self._bot

    def set_bot(self, value: BotDescription):
        assert isinstance(value, BotDescription)
        self._bot = value

    def clear_scene(self) -> None:
        """
        Очистить все добавленные объекты со сцены
        """
        for message in self._message_graphics_list:
            self.removeItem(message)
        self._message_graphics_list.clear()

    def add_message(self, message: BotMessage, variants: typing.List[BotVariant]) -> BlockGraphicsItem:
        """
        Добавить сообщение на сцену
        Args:
            message: сообщение
            variants: варианты, относящиеся к сообщению
        """
        # проверяем, что id бота уникальный, не совпадает с другими id
        exists_bots_ids: typing.Set[int] = {message.id for message in self.get_all_messages()}
        assert message.id not in exists_bots_ids

        message_graphics = self._create_message_graphics(message, variants)
        self._message_graphics_list.append(message_graphics)

        # подписываемся на события созданного графического элемента блока (сообщения)
        message_graphics.signal_sender.add_variant_request.connect(self._on_add_variant)
        message_graphics.signal_sender.request_change_message.connect(self._on_change_message)
        message_graphics.signal_sender.request_change_variant.connect(self._on_change_variant)
        message_graphics.signal_sender.selected_item_changed.connect(self._on_selection_changed)

        return message_graphics

    def get_selected_messages(self) -> typing.List[BotMessage]:
        """
        Получить выделенные сообщения со сцены
        Returns:
            список выбранных сообщений
        """
        result: typing.List[BotMessage] = []
        for item in self.selectedItems():
            item: BlockGraphicsItem
            assert isinstance(item, BlockGraphicsItem)
            result.append(item.get_message())

        return result

    def delete_messages(self, messages: typing.List[BotMessage]) -> None:
        """
        Удалить заданные сообщения со сцены
        Args:
            messages: список сообщений для удаления
        """
        deleted_messages_ids: typing.List[typing.Optional[int]] = [message.id for message in messages]

        # гарантия, что все сообщения с id
        assert all(isinstance(message, int) for message in deleted_messages_ids)

        deleted_messages_ids_set = set(deleted_messages_ids)

        # гарантия, что нет одинаковых id
        assert len(deleted_messages_ids_set) == len(deleted_messages_ids)

        removed_graphics_items: typing.List[BlockGraphicsItem] = [
            message_graphics
            for message_graphics in self._message_graphics_list
            if message_graphics.get_message().id in deleted_messages_ids_set
        ]

        for removed_graphics_item in removed_graphics_items:
            self.removeItem(removed_graphics_item)
            self._message_graphics_list.remove(removed_graphics_item)

    def get_all_messages(self) -> typing.List[BotMessage]:
        """
        Получить список всех сообщений, которые находятся на сцене
        Returns:
            список всех сообщений со сцены
        """
        return [message_graphics.get_message() for message_graphics in self._message_graphics_list]

    def get_selected_blocks_graphics(self) -> typing.List[BlockGraphicsItem]:
        """
        Получить список выделенных блоков (графических элементов сцены)
        Returns:
            список графических элементов сцены
        """
        selected: typing.List[BlockGraphicsItem] = []
        for item in self._message_graphics_list:
            if item.isSelected():
                selected.append(item)
        return selected

    def _connect_signals(self):
        self.changed.connect(self._on_item_changed)
        self.selectionChanged.connect(self._on_selection_changed)

    def _on_add_variant(self, message: BotMessage, variants: typing.List[BotVariant]):
        self.request_add_new_variant.emit(message, variants)

    def _on_change_message(self, block: BlockGraphicsItem, variants: typing.List[BotVariant]):
        assert isinstance(block, BlockGraphicsItem)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        self.request_change_message.emit(block, variants)

    def _on_change_variant(self, block_graphics_item: BlockGraphicsItem, variant: BotVariant):
        assert isinstance(block_graphics_item, BlockGraphicsItem)
        assert isinstance(variant, BotVariant)
        self.request_change_variant.emit(block_graphics_item, variant)

    def _get_work_field_rect(self) -> QRectF:
        result = QRectF(0, 0, self._MIN_WORKSPACE_WIDTH, self._MIN_WORKSPACE_HEIGHT)
        for message_rect in self._message_graphics_list:
            result = result.united(message_rect.sceneBoundingRect())
        return result

    def _on_selection_changed(self):
        # сделаем, чтобы выделяемые объекты всегда находились поверх остальных
        for item in self.items():
            if isinstance(item, BlockGraphicsItem):
                item: BlockGraphicsItem
                item.setZValue(0.0)

        z_selected = 1.0
        for item in self.selectedItems():
            item: BlockGraphicsItem
            assert isinstance(item, BlockGraphicsItem)
            item.setZValue(z_selected)
            z_selected += 1.0

        self.selection_changed.emit()

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

    def _create_message_graphics(self, message: BotMessage, variants: typing.List[BotVariant]) -> BlockGraphicsItem:
        is_start_message: bool = (message.id == self._bot.start_message_id)
        message_graphics_item = BlockGraphicsItem(message, variants, is_start_message)
        self.addItem(message_graphics_item)

        assert isinstance(message_graphics_item, QGraphicsItem)
        return message_graphics_item

    def get_block_by_message_id(self, message_id: int) -> typing.Optional[BlockGraphicsItem]:
        """
        Получает блок по идентификатору сообщения.

        Args:
            message_id: Ид сообщения

        Returns:
            Искомый блок.
        """
        for block in self._message_graphics_list:
            if block.get_message().id == message_id:
                return block
