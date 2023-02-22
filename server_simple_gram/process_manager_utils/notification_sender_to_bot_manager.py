from typing import Optional

from b_logic.bot_processes_manager import BotProcessesManagerSingle
from process_manager_utils.notification_sender import NotificationSender


class NotificationSenderToBotManager(NotificationSender):

    def __init__(self):
        self._bot_process_manager: Optional[BotProcessesManagerSingle] = None

    def set_process_manager(self, bot_process_manager):
        self._bot_process_manager = bot_process_manager

    def send_terminated_notification(self, process_id: int):
        bot_id: int = self._bot_process_manager.find_bot_id_by_process_id(process_id)
        self._bot_process_manager.mark_process_as_error(bot_id)
