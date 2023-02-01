import typing
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import SIGNAL, SLOT

from common.localisation import tran

from constructor_app.widgets.ui_item_project_sidebar import Ui_ItemProjectsListWidget

class ItemProjectsListWidget(QWidget):
    """
    Надстройка айтема сайдбара
    """

    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_ItemProjectsListWidget()
        self._ui.setupUi(self)
        # toDO: Добавить функцию инициализации QSS

    def init_statemachine_item(self, state: bool) -> None:
        #toDO: Перенести либо цвета либо QSS в новую цветовую схему или макросс
        if state:
            self._ui.indicator_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#4DAAFF;}")

            self._ui.indicator_bot.setText(self._tr("on"))
        else:
            self._ui.indicator_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#FF5F8F;}")
            self._ui.indicator_bot.setText(self._tr("off"))

    def init_item_sidebar(self, icon: QPixmap, name: str, state: bool) -> None:
        self._ui.pixmap_bot.setPixmap(icon)
        self._ui.pixmap_bot.setScaledContents(True)
        self._ui.name_bot.setText(name)
        self.init_statemachine_item(state)

    def _tr(self, text: str) -> str:
        return tran('ItemProjectsListWidget.manual', text)