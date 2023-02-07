from dataclasses import dataclass

from PySide6.QtGui import QPixmap

from b_logic.data_objects import BotDescription


@dataclass(slots=True)
class BotExtended:
    # toDo: Renaming BotExtended
    bot_icon: QPixmap
    bot_description: BotDescription
    bot_state: bool
