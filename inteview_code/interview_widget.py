from PySide6.QtWidgets import QWidget, QMessageBox

from desktop_constructor_app.constructor_app.widgets.ui_interview_widget import Ui_InterviewWidget


class InterviewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._ui = Ui_InterviewWidget()
        self._ui.setupUi(self)

        self._ui.add_button.clicked.connect(self._on_sum)

    def _on_sum(self, _checked: bool):
        sum = int(self._ui.line_num_1.text()) + int(self._ui.line_num_2.text())
        QMessageBox.information(self, 'Result', f'Sum is {sum}')
