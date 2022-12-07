#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

from django.core.management import execute_from_command_line


if __name__ == '__main__':
    # добавить путь с django проектом в каталог поиска модулей
    sys.path.append(str(Path(__file__).parent / 'backend' / 'bot_django_project'))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.bot_django_project.bot_constructor.settings')
    execute_from_command_line([
        __file__,
        'runserver',
        # разрешить подключаться другим
        # '0.0.0.0:8000'
    ])
