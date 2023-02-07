import typing
from typing import List
from dataclasses import dataclass

from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize

from b_logic.bot_api.i_bot_api import BotDescription
from constructor_app.widgets.bot_item_sidebar import BotListItemWidget

@dataclass(slots=True)
class BotExtended:
    # toDo: Renaming BotExtended
    bot_icon: QPixmap
    bot_description: BotDescription
    bot_state: bool

class BotListWidget(QListWidget):
    """
    Надстройка сайдбара
    """
    _ITEM_SIZE = QSize(210, 40)
    _bots_list: List[BotExtended] = []

    def __init__(self, parent: typing.Optional[QListWidget] = None):
        # toDo: Если будет необходимо добавить функцию [night/light]mode
        super().__init__(parent)
        self.__init_stylesheet()

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
        # Заготовква для дальнейшей реализации добавления бота из списка бокового меню
        row = self.count()
        item = QListWidgetItem()

        self._bots_list.append(bot)

        widget = BotListItemWidget()
        # toDo: добавить resizeMode
        item.setSizeHint(self._ITEM_SIZE)
        widget.init_bot_data(bot.bot_icon, bot.bot_description, bot.bot_state)
        self.insertItem(row, item)
        self.setItemWidget(item, widget)

    def remove_bot(self, row: int):
        # Заготовква для дальнейшей реализации удаления бота из списка бокового меню
        # toDo: Добавить удаление из списка проектов с сервера
        item = self.item(row)
        self.removeItemWidget(item)

    #Заготовква для дальнейшей реализации изменения состояния бота
    def bot_state_changed(self, state: bool, row: int):
        # toDo: Add checkabled for item sidebar and server
        widget = BotListItemWidget()
        item = self.item(row)

    def get_bots(self) -> List[BotExtended]:
        # take bot in BotDescription and bot_state
        return self._bots_list

    def get_current_bot(self) -> BotExtended:
        # take bot in BotDescription and bot_state
        row = self.currentRow()
        bot = self._bots_list[row]
        return bot
