import typing
from typing import Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QGraphicsView, QMenu, QGraphicsScene

from desktop_constructor_app.constructor_app.graphic_scene.block_graphics_item import BlockGraphicsItem
from desktop_constructor_app.constructor_app.graphic_scene.bot_scene import BotScene


class BotView(QGraphicsView):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        assert isinstance(parent, Optional[QtWidgets.QWidget])
        super().__init__(parent)

        # контекстное меню для места, где нет блока
        self._context_menu_empty: typing.Optional[QMenu] = None

        self._context_menu_block: typing.Optional[QMenu] = None

        self._context_menu_position: typing.Optional[QPoint] = None

    def setup_empty_menu(self, context_menu: QMenu) -> None:
        assert isinstance(context_menu, QMenu)
        self._context_menu_empty = context_menu

    def setup_block_menu(self, context_menu: QMenu) -> None:
        assert isinstance(context_menu, QMenu)
        self._context_menu_block = context_menu

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
        self._context_menu_position: QPoint = event.pos()
        try:
            scene_pos: QPointF = self.mapToScene(self._context_menu_position)
            bot_scene: BotScene = typing.cast(BotScene, self.scene())
            assert isinstance(bot_scene, BotScene)
            scene_item = bot_scene.itemAt(scene_pos, QTransform())
            if isinstance(scene_item, BlockGraphicsItem):
                bot_scene.clearSelection()
                # for item in bot_scene.selectedItems():
                #     item.setSelected(False)

                if not scene_item.isSelected():
                    scene_item.setSelected(True)
                if self._context_menu_block is not None:
                    self._context_menu_block.exec(event.globalPos())
            else:
                if self._context_menu_empty is not None:
                    self._context_menu_empty.exec(event.globalPos())
        finally:
            self._context_menu_position = None

