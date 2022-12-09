import typing
from copy import copy
from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog

from b_logic.data_objects import BotVariant, BotMessage
from desktop_constructor_app.constructor_app.widgets.ui_variant_editor_dialog import Ui_VariantEditorDialog


class VariantEditorDialog(QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_VariantEditorDialog()
        self._ui.setupUi(self)

        self._variant: typing.Optional[BotVariant] = None

    def set_dialog_data(self, variant: BotVariant, messages: typing.List[BotMessage]):
        assert isinstance(variant, BotVariant)
        assert all(isinstance(message, BotMessage) for message in messages)
        self._variant = variant
        self._ui.variant_text_edit.setText(self._variant.text)
        messages_texts = [message.text for message in messages]
        self._ui.next_message_select_list_widget.clear()
        self._ui.next_message_select_list_widget.addItems(messages_texts)

    def apply_variant_changes(self):
        self._variant.text = self._ui.variant_text_edit.text()
