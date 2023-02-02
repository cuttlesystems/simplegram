import typing
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import SIGNAL, SLOT

from constructor_app.widgets.bot_item_sidebar import BotListItemWidget

class BotListWidget(QListWidget):
    """
    Надстройка айтема сайдбара
    """

    def __init__(self, parent: typing.Optional[QListWidget] = None):
        # toDo: Если будет необходимо добавить функцию [night/light]mode
        super().__init__(parent)
        self.__init_stylesheet()

    def __init_stylesheet(self):
        # toDo: добавить сигналы hover и селекта
        # toDo: Добавить настройки высоты айтема
        self.setStyleSheet(
            "QListWidget{border:none; background:transparent;}"
            "QListWidget::item{padding-left:20px; border:none; color:rgba(255,255,255,100);}"
            "QListWidget::item:hover{border-left:2px solid rgba(255,255,255,180); color:rgba(255,255,255,180);}"
            "QListWidget::item:selected{border:none; color:rgb(255,255,255); background:rgba(255,255,255,25);}")

    # Заготовква для дальнейшей реализации добавления бота из списка бокового меню
    def add_bot(self, icon: QPixmap, name: str, state: bool, row: int):
        # toDo: Добавить подгрузку списка проектов с сервера
        item = QListWidgetItem()
        widget = BotListItemWidget()
        widget.init_bot_data(icon, name, state)
        self.insertItem(row, item)
        self.setItemWidget(item, widget)

    # Заготовква для дальнейшей реализации удаления бота из списка бокового меню
    def remove_bot(self, row: int):
        # toDo: Добавить удаление из списка проектов с сервера
        item = self.item(row)
        self.removeItemWidget(item)

    #Заготовква для дальнейшей реализации изменения состояния бота
    def bot_state_changed(self, state: bool, row: int):
        # toDo: Добавить изменение состояние элемента списка sidebar
        widget = BotListItemWidget()
        item = self.item(row)