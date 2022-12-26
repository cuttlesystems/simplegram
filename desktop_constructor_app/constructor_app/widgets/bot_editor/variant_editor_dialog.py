import typing
from copy import copy
from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QListWidgetItem

from b_logic.data_objects import BotVariant, BotMessage
from desktop_constructor_app.constructor_app.widgets.bot_editor.ui_variant_editor_dialog import Ui_VariantEditorDialog


class VariantEditorDialog(QDialog):
    _DATA_ROLE = Qt.UserRole + 1

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_VariantEditorDialog()
        self._ui.setupUi(self)

        self._variant: typing.Optional[BotVariant] = None

    def set_dialog_data(self, variant: BotVariant, messages: typing.List[BotMessage]) -> None:
        assert isinstance(variant, BotVariant)
        assert all(isinstance(message, BotMessage) for message in messages)
        self._variant = variant
        self._ui.variant_text_edit.setText(self._variant.text)
        list_items: typing.List[QListWidgetItem] = []
        for message in messages:
            list_item = QListWidgetItem(message.text)
            list_item.setData(self._DATA_ROLE, message)
            list_items.append(list_item)
        self._ui.next_message_select_list_widget.clear()
        for item in list_items:
            self._ui.next_message_select_list_widget.addItem(item)
        for item in list_items:
            message: BotMessage = item.data(self._DATA_ROLE)
            assert isinstance(message, BotMessage)
            if message.id == variant.next_message_id:
                self._ui.next_message_select_list_widget.setCurrentItem(item)

    def get_variant(self) -> BotVariant:
        variant = copy(self._variant)
        variant.text = self._ui.variant_text_edit.text()
        selected_message = self._get_current_message()
        if selected_message is not None:
            variant.next_message_id = selected_message.id
        else:
            variant.next_message_id = None
        return variant

    def _get_current_message(self) -> Optional[BotMessage]:
        current_message = None
        current_item = self._ui.next_message_select_list_widget.currentItem()
        if current_item is not None:
            assert isinstance(current_item, QListWidgetItem)
            current_message = current_item.data(self._DATA_ROLE)
        return current_message
