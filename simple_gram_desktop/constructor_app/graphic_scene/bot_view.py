import typing
from typing import Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QGraphicsView, QMenu, QGraphicsScene

from constructor_app.graphic_scene.block_graphics_item import BlockGraphicsItem
from constructor_app.graphic_scene.bot_scene import BotScene


class BotView(QGraphicsView):
    """
    Графический вид для отображения графической сцены бота
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        assert isinstance(parent, Optional[QtWidgets.QWidget])
        super().__init__(parent)

        # контекстное меню для блока
        self._context_menu_block: typing.Optional[QMenu] = None

        # контекстное меню пустого места
        self._context_menu_empty: typing.Optional[QMenu] = None

        # переменная хранит координаты точки откуда было вызвано контекстное меню
        # (не None когда контекстное меню отображается)
        self._context_menu_position: typing.Optional[QPoint] = None

    def setup_empty_menu(self, context_menu: QMenu) -> None:
        """
        Установить контекстное меню, которое будет отображаться для пустого места
        Args:
            context_menu: меню
        """
        assert isinstance(context_menu, QMenu)
        self._context_menu_empty = context_menu

    def setup_block_menu(self, context_menu: QMenu) -> None:
        """
        Установить контекстное меню, которое будет отображаться для блока
        Args:
            context_menu: меню
        """
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
        """
        Получить центральную точку виджета в относительных координатах виджета
        Returns:
            точка в относительных координатах виджета
        """
        return QPoint(round(self.width() / 2), round(self.height() / 2))

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        assert isinstance(event.pos(), QPoint)
        self._context_menu_position: QPoint = event.pos()
        try:
            # пересчитаем координаты события мыши в координаты сцены
            scene_pos: QPointF = self.mapToScene(self._context_menu_position)

            bot_scene: BotScene = typing.cast(BotScene, self.scene())
            assert isinstance(bot_scene, BotScene)

            # найдем графический элемент сцены, который находится по координатам клика
            scene_item = bot_scene.itemAt(scene_pos, QTransform())

            # если клик для вызова контекстного меню произведен по блоку
            if isinstance(scene_item, BlockGraphicsItem):

                # если блок, по которому произведен клик не является частью текущего выделения,
                # то сбросим существующее выделение и сформируем новое из одного этого блока
                if scene_item not in bot_scene.selectedItems():
                    bot_scene.clearSelection()
                    scene_item.setSelected(True)

                if self._context_menu_block is not None:
                    self._context_menu_block.exec(event.globalPos())
            else:
                # если клик для вызова контекстного меню произведен вне блока
                if self._context_menu_empty is not None:
                    self._context_menu_empty.exec(event.globalPos())
        finally:
            self._context_menu_position = None

