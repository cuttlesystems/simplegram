import sys

from PySide6.QtWidgets import QApplication
import constructor_app.rc_bot_icons
from constructor_app.settings.get_application_data_dir import get_application_executable_dir, is_run_from_source
from constructor_app.utils.application_style import print_available_styles
from constructor_app.settings.language_manager import LanguageManager
from constructor_app.windows_manager import WindowsManager
import sys


def compile_all_resources():
    # компиляция ресурсов нужна (и может выполниться) только если запускаем из исходников
    if is_run_from_source():
        compile_scripts_dir = (
            get_application_executable_dir() / '..' / 'deploy' / 'build_desktop'
        ).resolve()

        compile_scripts_dir_str = str(compile_scripts_dir)

        # временно расширяем путь PYTHONPATH для поиска модулей
        sys.path.append(compile_scripts_dir_str)

        # это импорт сделанный обходным путем, поэтому тут показывает как будто есть ошибка
        from compiling_transl_ui_rc import compile_translations, compile_ui_forms, compile_rc_files

        print('--- start resources compilation ---')
        compile_translations()
        compile_ui_forms()
        compile_rc_files()
        print('--- end resources compilation ---')

        # отключаем путь импорта модулей, который был добавлен временно
        sys.path.remove(compile_scripts_dir_str)


if __name__ == "__main__":
    print_available_styles()
    compile_all_resources()

    app = QApplication(sys.argv)

    language_manager = LanguageManager()
    language_manager.check()
    language_manager.configure_language_by_settings(app)

    # ссылаемся на модуль, чтобы он не удалился при автоматическом рефакторинге
    _rc_module = constructor_app.rc_bot_icons

    windows_manager = WindowsManager()
    windows_manager.start()
    sys.exit(app.exec())
