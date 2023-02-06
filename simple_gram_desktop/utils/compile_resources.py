import sys

from constructor_app.settings.get_application_data_dir import is_run_from_source, get_application_executable_dir


def compile_all_resources() -> None:
    """
    Автоматическая компиляция ресурсов приложения при запуске из исходников
        - Компилируются файлы форм (ui)
        - Компилируются файлы ресурсов (rc)
        - Компилируются файлы переводов (ts)
    """

    # компиляция ресурсов нужна (и может выполниться) только если запускаем из исходников
    if is_run_from_source():
        compile_scripts_dir = (
            get_application_executable_dir() / '..' / 'deploy' / 'build_desktop'
        ).resolve()

        compile_scripts_dir_str = str(compile_scripts_dir)

        # временно расширяем путь PYTHONPATH для поиска модулей
        sys.path.append(compile_scripts_dir_str)
        print(f'compile_scripts_dir path: ', compile_scripts_dir_str)

        # это импорт сделанный обходным путем, поэтому тут показывает как будто есть ошибка
        from compiling_transl_ui_rc import compile_translations, compile_ui_forms, compile_rc_files
        from create_venv import create_venv_in_build_desktop

        # вызов функции проверки существования и создания виртуального окружения в каталоге 'build_desktop'
        print('\n--- check \'build_desktop\' directory for \'venv\' existance and creation if it doesn\'t exist ---\n')
        create_venv_in_build_desktop()

        print('--- start resources compilation ---')
        compile_translations()
        compile_ui_forms()
        compile_rc_files()
        print('--- end resources compilation ---')

        # отключаем путь импорта модулей, который был добавлен временно
        sys.path.remove(compile_scripts_dir_str)
