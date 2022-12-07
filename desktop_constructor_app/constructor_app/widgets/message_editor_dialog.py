from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog

from desktop_constructor_app.constructor_app.widgets.ui_message_editor_dialog import Ui_MessageEditorDialog


class MessageEditorDialog(QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_MessageEditorDialog()
        self._ui.setupUi(self)
