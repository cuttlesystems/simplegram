from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtWidgets import QGraphicsView


class BotView(QGraphicsView):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        assert isinstance(parent, Optional[QtWidgets.QWidget])
        super().__init__(parent)
        