# tg_bot_constructor

[Документация по проекту](./Docs/Index.md)

[Правила работы с git](./Docs/git_description.md)

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
- http://127.0.0.1:8000/api/first_endpoint/ - первый эндпоинт
- http://127.0.0.1:8000/admin/ - админ зона
- http://127.0.0.1:8000/api/message/id/123-890/ - получить информацию по заданному 
сообщению


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
