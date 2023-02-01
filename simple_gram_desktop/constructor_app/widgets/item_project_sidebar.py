import typing
from PySide6.QtWidgets import QWidget
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

    def _tr(self, text: str) -> str:
        return tran('ClientWidget.manual', text)