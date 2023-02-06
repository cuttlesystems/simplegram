from typing import Optional

from b_logic.bot_processes_manager import BotProcessesManagerSingle
from utils.notification_sender import NotificationSender


class NotificationSenderToBotManager(NotificationSender):

    def __init__(self):
        self.bot_process_manager: Optional[BotProcessesManagerSingle] = None

    def send_error(self, process_id: int):
        bot_id: int = self.bot_process_manager.find_bot_id_by_process_id(process_id)
        print(f'bot id: {bot_id}')
        print(f'bot id: {bot_id}')
        print(f'bot id: {bot_id}')
