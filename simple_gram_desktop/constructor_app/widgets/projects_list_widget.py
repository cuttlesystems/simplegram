import typing
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import SIGNAL, SLOT

from constructor_app.widgets.item_project_sidebar import ItemProjectsListWidget

class ProjectsListWidget(QListWidget):
    """
    Надстройка айтема сайдбара
    """

    def __init_stylesheet(self):
        # toDo: добавить сигналы hover и селекта
        # toDo: Добавить настройки высоты айтема
        self.setStyleSheet(
            "QListWidget{border:none; background:transparent;}"
            "QListWidget::item{padding-left:20px; border:none; color:rgba(255,255,255,100);}"
            "QListWidget::item:hover{border-left:2px solid rgba(255,255,255,180); color:rgba(255,255,255,180);}"
            "QListWidget::item:selected{border:none; color:rgb(255,255,255); background:rgba(255,255,255,25);}")

    def add_item_sidebar(self, icon: QPixmap, name: str, state: bool, row: int):
        # toDo: Добавить подгрузку списка проектов с сервера
        item = QListWidgetItem()
        widget = ItemProjectsListWidget()
        widget.init_item_sidebar(icon, name, state)
        self.insertItem(row, item)
        self.setItemWidget(item, widget)

    def remove_item_sidebar(self, row: int):
        # toDo: Добавить удаление из списка проектов с сервера
        item = self.item(row)
        self.removeItemWidget(item)

    def init_state_sidebar(self, state: bool, row: int):
        # toDo: Добавить изменение состояние элемента списка sidebar
        widget = ItemProjectsListWidget()
        item = self.item(row)
