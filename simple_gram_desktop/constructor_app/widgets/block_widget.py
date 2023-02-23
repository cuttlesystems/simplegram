import typing
from PySide6.QtWidgets import QWidget
from common.localisation import tran

from constructor_app.widgets.ui_block_widget import Ui_BlockWidget


class BlockWidget(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_BlockWidget()
        self._ui.setupUi(self)
        self.setMouseTracking(True)

    def _tr(self, text: str) -> str:
        return tran('BlockWidget.manual', text)

