import typing
from copy import copy
from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QListWidgetItem

from b_logic.data_objects import BotVariant, BotMessage
from constructor_app.widgets.bot_editor.ui_variant_editor_dialog import Ui_VariantEditorDialog


class VariantEditorDialog(QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_VariantEditorDialog()
        self._ui.setupUi(self)

        self._variant: typing.Optional[BotVariant] = None

    def set_dialog_data(self, variant: BotVariant, messages: typing.List[BotMessage]) -> None:
        """
        Установить вариант и сообщения для отображения в диалоговом окне.
        В диалоге можно будет менять данные варианта.
        Список сообщений нужен для выбора следующего сообщения варианта
        Args:
            variant: объект варианта для изменения
            messages: список сообщений для выбора следующего сообщения
        """
        assert isinstance(variant, BotVariant)
        assert all(isinstance(message, BotMessage) for message in messages)
        self._variant = variant
        self._ui.variant_text_edit.setText(self._variant.text)

        self._ui.next_message_select_list_widget.set_messages(messages)
        self._ui.next_message_select_list_widget.select_message(self._variant.next_message_id)

    def get_variant(self) -> BotVariant:
        """
        Получить вариант с учетом его изменений в диалоговом окне
        Returns:
            объект варианта
        """
        assert self._variant is not None
        # копируем объект исходного варианта, чтобы избежать побочных эффектов в вызывающем коде,
        # когда будем модифицировать его свойства
        variant = copy(self._variant)
        variant.text = self._ui.variant_text_edit.text()
        selected_message = self._ui.next_message_select_list_widget.get_selected_message()
        if selected_message is not None:
            variant.next_message_id = selected_message.id
        else:
            variant.next_message_id = None
        return variant
