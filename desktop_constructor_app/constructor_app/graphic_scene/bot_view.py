import typing
from typing import Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QPointF, QPoint
from PySide6.QtWidgets import QGraphicsView, QMenu


class BotView(QGraphicsView):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        assert isinstance(parent, Optional[QtWidgets.QWidget])
        super().__init__(parent)

        self._context_menu: typing.Optional[QMenu] = None
        self._context_menu_position: typing.Optional[QPoint] = None

    def setup_menu(self, context_menu: QMenu) -> None:
        assert isinstance(context_menu, QMenu)
        self._context_menu = context_menu

    def get_context_menu_position(self) -> typing.Optional[QPoint]:
        """
        В момент, когда открыто контекстное меню, можно получить координаты вызова контекстного меню.
        Когда контекстное меню не открыто вернет None
        Returns:
            Позиция открытия контекстного меню в относительных координатах виджета, либо None
        """
        return self._context_menu_position

    def get_central_point(self) -> QPoint:
        return QPoint(round(self.width() / 2), round(self.height() / 2))

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        assert isinstance(event.pos(), QPoint)
        self._context_menu_position = event.pos()
        try:
            self._context_menu.exec(event.globalPos())
        finally:
            self._context_menu_position = None

