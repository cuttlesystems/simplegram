import typing

from PySide6.QtWidgets import QWidget

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from constructor_app.widgets.bot_editor.bot_editor_form import BotEditorForm


class BotEditorFormExtended(BotEditorForm):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        bot_api = BotApiByRequests("https://ramasuchka.kz/")
        bot_api.authentication("admin", "adminpass")
        bot = bot_api.get_bot_by_id(73)
        super().__init__(parent, bot_api)
        self.set_bot(bot)
