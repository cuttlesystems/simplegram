# tg_bot_constructor

[Вступительное слово к проекту](./docs/draft_introductory_remarks_to_the_StartUp.md)

[Документация по проекту](./docs/Index.md)

[Правила работы с *git*](./docs/git_description.md)

[Данные для тестирования телеграмм бота](./docs/telegabot_info.md)

[Инструкция по осуществлению *deploy'я* обновлённого *docker*-контейнера](./docs/deploy_from_ubuntu.md)

[Инструкция по созданию исполняемого файла (*Win, Linux*) с помощью утилиты *PyInstaller*](./docs/create_executable_file.md)

[Структура репозитория](./docs/repo_struct.md)

### Организация разработки

[Проведение собеседования](./docs/interview.md)

[Дисциплина труда](./docs/working_time.md)

## Как запустить проект локально(dev-режим):

- Клонировать репозиторий и перейти в директорию с файлом manage.py:

```
git@github.com:cuttlesystems/tg_bot_constructor.git
cd backend/tg_bot_constructor/bot_constructor
```

- Из дириктории с manage.py выполнить миграции и создать суперюзера:

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

- Запустить проект локально:

```
python3 manage.py runserver
```
## Проект запущен и доступен по адресу:
- http://127.0.0.1:8000/

[Курс](https://www.youtube.com/playlist?list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ) видеоуроков (*YouTube Playlist*) по разработке бота для *Telegram* на *Python*  с использованием фреймворка *aiogram*. За основу взят пример фриланс проекта - бот для пиццерии. Подробно рассмотрены все этапы создания бота и все темы: *Polling*, *webhook*, кнопки, инлайн клавиатуры, меню, клиентская часть, админка, машина состояний (*FSM*)
## Примеры api запросов:

### Регистрация пользователя и получение токена:

#### Регистрация пользователя:

- POST запрос на эндпоинт:
```
http://127.0.0.1:8000/api/users/
```
- в теле запроса(body):
```
{
    "username": "boris",
    "email": "boris@boris.com",
    "password": "boris123"
}
```
- ответ:
- status: 201 Created
```
{
    "email": "boris@boris.com",
    "username": "boris",
    "id": 4
}
```
#### Получение токена для зарегистрированного пользователя:

- POST запрос на эндпоинт:
```
http://127.0.0.1:8000/api/auth/token/login/
```
- в теле запроса(body):
```
{
    "username": "boris",
    "password": "boris123"
}
```
- ответ:
- status: 200 OK
```
{
    "auth_token": "1a30836b4e02ec825b587bd72412b6d239d8bc30"
}
```
- Данный **токен** передается в заголовке запроса для аутентификации пользователя.
- Пример: 'Authorization: Token 1a30836b4e02ec825b587bd72412b6d239d8bc30'

#### Обращение к REST API
- http://127.0.0.1:8000/api/bots/ - работа с ботами пользователя. Можно получить список ботов 
пользователя или создать нового.
- http://127.0.0.1:8000/api/bots/93/ - получить бота по идентификатору, изменить его параметры или удалить
- http://127.0.0.1:8000/api/bots/93/messages/ - сообщения бота с id = 93. 
Можно получить список сообщений или создать новое
- http://127.0.0.1:8000/api/message/396/ - получить, поменять или удалить сообщение 
с заданным идентификатором
- http://127.0.0.1:8000/api/messages/396/variants/ - получить варианты заданного сообщения
- http://127.0.0.1:8000/api/variant/461/ - получить, поменять или удалить заданный вариант
- http://127.0.0.1:8000/admin/ - админ зона


#### Пример заполнения .env файла для работы с перемеными окружения
- Создать в директории infra/ файл .env
- пример заполнения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bot_constructor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=172.21.0.1
DB_PORT=5432

SECRET_KEY = 'django-insecure-@a#@3^g@a#@3^g7vh@a#@3^g@a#@3^g@a#@3^g@a#@3^g'
```