import typing
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import SIGNAL, SLOT, QSize

from common.localisation import tran

from constructor_app.widgets.ui_bot_item_sidebar import Ui_BotListItemWidget
from constructor_app.widgets.bot_extended import BotExtended


class BotListItemWidget(QWidget):
    """
    Надстройка айтема сайдбара
    """
    _FLAG_SIZE = QSize(30, 15)

    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_BotListItemWidget()
        self._ui.setupUi(self)
        # toDO: Добавить функцию инициализации QSS

    # Функция перекелючения/инициализации состояния бота (Бот включен/ бот выключен)
    def _change_bot_state(self, state: bool) -> None:
        # toDO: Заготовка для добавления новой фичи - изменение состояния бота
        # toDO: Перенести либо цвета либо QSS в новую цветовую схему или макросс
        if state:
            self._ui.indicator_bot.setStyleSheet(
                "QLabel{border-radius:6px; border:none; color:white;"
                "background-color:#4DAAFF;}")

            self._ui.indicator_bot.setText(self._tr("on"))
        else:
            self._ui.indicator_bot.setStyleSheet(
                "QLabel{border-radius:6px; border:none; color:white;"
                "background-color:#FF5F8F;}")
            self._ui.indicator_bot.setText(self._tr("off"))
        self._ui.indicator_bot.setFixedSize(self._FLAG_SIZE)

    def init_bot_data(self,  bot: BotExtended) -> None:
        assert isinstance(bot, BotExtended)
        self._ui.pixmap_bot.setPixmap(bot.bot_icon)
        self._ui.pixmap_bot.setScaledContents(True)
        self._ui.name_bot.setStyleSheet("color:rgba(255,255,255,100);")
        # toDo: Добавить автоматическое сокращение наименования "..."
        self._ui.name_bot.setText(bot.bot_description.bot_name)
        self._ui.name_bot.setWordWrap(True)
        self._change_bot_state(bot.bot_state)

    def _tr(self, text: str) -> str:
        return tran('ItemProjectsListWidget.manual', text)