import typing
from PySide6.QtWidgets import QWidget
from common.localisation import tran

from constructor_app.widgets.ui_block_widget import Ui_BlockWidget
from b_logic.data_objects import BotMessage, BotVariant


class BlockWidget(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_BlockWidget()
        self._ui.setupUi(self)
        self.setMouseTracking(True)

    def init_style(self):
        pass

    def init_message(self, message: BotMessage):
        self._ui.name_bot_button.setText(message.text)

    def add_variant(self, variant: BotVariant):
        self._ui.listWidget.insertItem(self._ui.listWidget.count(), variant.text)

    def _tr(self, text: str) -> str:
        return tran('BlockWidget.manual', text)

