from typing import Optional

import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QTreeView


class PropertiesView(QTreeView):
    _COLUMN_NAME_INDEX = 0

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        super().setModel(model)
        self.resizeColumnToContents(self._COLUMN_NAME_INDEX)
