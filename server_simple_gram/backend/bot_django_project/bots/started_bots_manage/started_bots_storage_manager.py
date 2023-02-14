import json
from typing import Optional

from bots.models import StartedBotsStorage
from bot_constructor.log_configs import logger_django


class StartedBotsStorageManager:
    """Класс для хранения информации о запущенных ботах при перезапуске сервера"""
    _STARTED_BOTS_DB_MODEL = StartedBotsStorage

    def save_data(self, bots_list: list) -> None:
        """
        Сохраняет список id запущенных ботов в БД.
        Args:
            bots_list: список id запущенных ботов
        """
        assert isinstance(bots_list, list)
        bots_list_json = json.dumps(bots_list)
        instance = self._STARTED_BOTS_DB_MODEL(bots_list=bots_list_json)
        instance.save()
        logger_django.info_logging('Running bots info written in database.')

    def load_data(self) -> Optional[list]:
        """
        Получает запись из БД (список id запущенных ботов), а после удаляет эту запись.
        Returns:
            Список id запущенных ботов или None.
        """
        bots_list = None
        if len(self._STARTED_BOTS_DB_MODEL.objects.all()) > 0:
            last_object = self._STARTED_BOTS_DB_MODEL.objects.latest()
            bots_list = json.loads(last_object.bots_list)
            logger_django.info_logging(f'Received data about started bots from database: {bots_list}.')
            last_object.delete()
            logger_django.info_logging(f'Object with data, about started bots, deleted from database.')
        return bots_list
