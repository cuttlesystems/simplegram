from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog

from desktop_constructor_app.constructor_app.widgets.ui_variant_editor_dialog import Ui_VariantEditorDialog


class VariantEditorDialog(QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_VariantEditorDialog()
        self._ui.setupUi(self)


