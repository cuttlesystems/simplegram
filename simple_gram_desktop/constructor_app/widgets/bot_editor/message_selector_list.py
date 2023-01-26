# This Python file uses the following encoding: utf-8
import typing

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget
from b_logic.data_objects import BotMessage


class MessageSelectorList(QListWidget):
    """
    Список в котором можно выбрать следующее сообщение
    """

    _DATA_ROLE = Qt.UserRole + 1

    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)

    def set_messages(self, messages: typing.List[BotMessage]) -> None:
        """
        Установить список сообщений для отображения в списке
        Args:
            messages: список сообщений для отображения
        """
        assert isinstance(messages, list)
        assert all(isinstance(message, BotMessage) for message in messages)
        list_items: typing.List[QListWidgetItem] = []
        for message in messages:
            list_item = QListWidgetItem(message.text)
            list_item.setData(self._DATA_ROLE, message)
            list_items.append(list_item)

        self.clear()
        for item in list_items:
            self.addItem(item)

    def set_selected_message(self, message_id: typing.Optional[int]) -> None:
        """
        Установить выбранное в списке сообщение
        Args:
            message_id: идентификатор выбранного сообщения
        """
        assert isinstance(message_id, typing.Optional[int])

        # сбрасываем выделение текущего элемента
        self.setCurrentItem(QListWidgetItem())

        if message_id is not None:
            for item_index in range(self.count()):
                item = self.item(item_index)
                message: BotMessage = item.data(self._DATA_ROLE)
                assert isinstance(message, BotMessage)
                if message.id == message_id:
                    # выделяем заданный элемент
                    self.setCurrentItem(item)
                    break

    def get_selected_message(self) -> typing.Optional[BotMessage]:
        """
        Получить выбранное в списке сообщение
        Returns:
            объект выбранного сообщения или None, если не выбрано
        """
        current_message: typing.Optional[BotMessage] = None
        current_item = self.currentItem()
        if current_item is not None:
            assert isinstance(current_item, QListWidgetItem)
            current_message = current_item.data(self._DATA_ROLE)
        return current_message
