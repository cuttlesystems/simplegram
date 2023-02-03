import typing

from PySide6.QtWidgets import QWidget

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from constructor_app.widgets.bot_editor_widget import BotEditorWidget


class BotEditorFormExtended(BotEditorWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        bot_api = BotApiByRequests("https://ramasuchka.kz/")
        bot_api.authentication("admin", "adminpass")
        bot = bot_api.get_bot_by_id(73)
        self.set_bot(bot)
        super().__init__(parent, bot_api)
