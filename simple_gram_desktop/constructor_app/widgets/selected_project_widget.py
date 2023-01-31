import typing

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Slot, Signal

from constructor_app.widgets.ui_selected_project_widget import Ui_SelectedProjectWidget

class SelectedProjectWidget(QWidget):
    ActivatedBotSignal = Signal(bool)
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_SelectedProjectWidget()
        self._ui.setupUi(self)
        self._ui.switchActivatedBot.clicked.connect(self._switchBot)
        self._init_StyleSheet()

    def _init_StyleSheet(self):
        self._ui.groupBox.setStyleSheet("QGroupBox{border-radius:22px; border:none; "
                                        "background-color:rgb(255,255,255);}")
        self._ui.openInRedactorButton.setStyleSheet("QPushButton{background-color:rgb(57,178,146);border:none;"
                                                    "color:white;border-radius:8px;}")

    def _switchBot(self):
        if(self._ui.switchActivatedBot.isChecked()):
            self._ui.markerActivisionBot.setStyleSheet("QLabel{border-radius:8px; border:none; color:white;"
                                                       "background-color:#4DAAFF;}")
            self._ui.markerActivisionBot.setText(u"Бот запущен")
            self.ActivatedBotSignal.emit(True)
        else:
            self._ui.markerActivisionBot.setStyleSheet("QLabel{border-radius:8px; border:none; color:white;"
                                                       "background-color:#FF5F8F;}")
            self._ui.markerActivisionBot.setText(u"Бот не активен")
            self.ActivatedBotSignal.emit(False)

