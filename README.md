# tg_bot_constructor
## Как запустить проект локально(dev-режим):

[Документация по проекту](./Docs/Index.md)

- Клонировать репозиторий и перейти в директорию с файлом manage.py:

```
git@github.com:cuttlesystems/tg_bot_constructor.git
cd backend/tg_bot_constructor/bot_constructor
```

- Из дериктории с manage.py выполнить миграции и создать суперюзера:

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

- Запустить проект локально:

```
python3 manage.py runserver
```
## Проект запущен и доступен по адресу:
- http://127.0.0.1:8000/api/first_endpoint/ - первый эндпоинт
- http://127.0.0.1:8000/admin/ - админ зона