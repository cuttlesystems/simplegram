import typing
from typing import Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QGraphicsView, QMenu


class BotView(QGraphicsView):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        assert isinstance(parent, Optional[QtWidgets.QWidget])
        super().__init__(parent)

        self._context_menu: typing.Optional[QMenu] = None

    def setup_menu(self, context_menu: QMenu) -> None:
        assert isinstance(context_menu, QMenu)
        self._context_menu = context_menu

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        self._context_menu.exec(event.globalPos())
        print('contextMenuEvent')
