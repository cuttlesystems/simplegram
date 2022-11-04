#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django.core.management import execute_from_command_line


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.bot_django_project.bot_constructor.settings')
    execute_from_command_line([__file__, 'runserver'])
