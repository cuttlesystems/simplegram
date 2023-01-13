import inspect
import logging.handlers

from utils.get_root_dir import get_project_root_dir

# Настройки логеров определены в settings.py в переменной LOGGING (dict) по ключу 'loggers'
_LOGGER_DJANGO = logging.getLogger('django')


class BackendLogger:
    """
    Класс-оболочка для логирования внутри проекта.
    """
    def __init__(self, logger: logging.Logger):
        assert isinstance(logger, logging.Logger)
        self.logger = logger

    def debug_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.debug(f'{path_to_file} - {message}')

    def info_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.info(f'{path_to_file} - {message}')

    def warning_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.warning(f'{path_to_file} - {message}')

    def error_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.error(f'{path_to_file} - {message}')

    def _get_path_from_call_stack(self) -> str:
        """
        Возвращает путь к файлу в котором был вызван логгер.

        Returns: Полный путь к файлу
        """
        return inspect.stack()[2].filename

    def _remove_home_dirs_from_path(self, path: str) -> str:
        """
        Обрезает часть пути находящегося выше корневой директории.

        Args:
            path: Полный путь к файлу

        Returns: Путь к файлу начиная с корневой директории.
        """
        assert isinstance(path, str)
        root_path = get_project_root_dir()
        part_of_path_before_root_dir = str(root_path.parent)
        return path.replace(part_of_path_before_root_dir, '', 1)


logger_django = BackendLogger(_LOGGER_DJANGO)
