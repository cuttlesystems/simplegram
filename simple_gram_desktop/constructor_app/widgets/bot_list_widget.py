import typing
from typing import List, Optional

from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import QSize

from constructor_app.widgets.bot_extended import BotExtended
from constructor_app.widgets.bot_item_sidebar import BotListItemWidget


class BotListWidget(QListWidget):
    """
    Надстройка сайдбара
    """

    def __init__(self, parent: typing.Optional[QListWidget] = None):
        # toDo: Если будет необходимо добавить функцию [night/light]mode
        super().__init__(parent)
        self.__init_stylesheet()

        self._ITEM_SIZE = QSize(210, 40)
        self._bots_list: List[BotExtended] = []
        self._bot_current_id: Optional[int] = None

    def __init_stylesheet(self):
        # toDo: добавить сигналы hover и селекта
        # toDo: Добавить настройки высоты айтема
        self.setStyleSheet(
            "QListWidget{border:none; background:none;}"
            "QListWidget::item{padding-left:20px; border:none; color:rgba(255,255,255,100);}"
            "QListWidget::item:hover{border-left:2px solid rgba(255,255,255,180); color:rgba(255,255,255,180);}"
            "QListWidget::item:selected{border:none; color:rgb(255,255,255); background:rgba(255,255,255,25);}")
        self.verticalScrollBar().setStyleSheet(
            "QScrollBar{background-color: black; width:4px; border:1px transparent black;}"
            "QScrollBar::handle{height: 10px; width:4px; border: 1px solid white; background-color:white;}"
            "QScrollBar::add-line{border:1px transparent black;  width:2px; background-color: black;}"
            "QScrollBar::sub-line{border:1px transparent black; width:2px; background-color: black;}")

    def add_bot(self, bot: BotExtended):
        assert isinstance(bot, BotExtended)
        row = self.count()
        item = QListWidgetItem()

        self._bots_list.append(bot)

        widget = BotListItemWidget()
        # toDo: добавить resizeMode
        item.setSizeHint(self._ITEM_SIZE)
        widget.init_bot_data(bot)
        self.insertItem(row, item)
        self.setItemWidget(item, widget)

    def get_bots(self) -> List[BotExtended]:
        # take bot in BotDescription and bot_state
        return self._bots_list

    def get_current_bot(self) -> Optional[BotExtended]:
        # take bot in BotDescription and bot_state
        row = self.currentRow()
        self._bot_current_id = self._bots_list[self.currentRow()].bot_description.id
        if row < 0:
            bot = None
        else:
            bot = self._bots_list[row]
        return bot

    def clear(self) -> None:
        if self.currentRow() > -1:
            self._bot_current_id = self._bots_list[self.currentRow()].bot_description.id
        self._bots_list.clear()
        super().clear()

    def update_current(self):
        if self._bot_current_id is not None:
            index = 0
            for bot in self._bots_list:
                if bot.bot_description.id == self._bot_current_id:
                    self.setCurrentRow(index)
                    break
                else:
                    self.clearSelection()
                index += 1

