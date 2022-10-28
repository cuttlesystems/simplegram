# tg_bot_constructor

[Документация по проекту](./Docs/Index.md)

[Правила работы с git](./Docs/git_description.md)

## Как запустить проект локально(dev-режим):

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
- http://127.0.0.1:8000/api/message/id/123-890/ - получить информацию по заданному 
сообщению

