﻿# Правила работы с git

## Новая функциональность и исправление ошибок

Подготовку нового функционала и исправление ошибок необходимо проводить в отдельной ветке, ответвленной от ветки в которую необходимо внести правки.

## Именование веток
Имя создаваемой ветки должно состоять из краткого описания функциональности или исправляемой ошибки, далее идет прямой слеш и **имя ветки от которой производилось ответвление**. Обычно это ветка `main`.
Пример

    implement_api_methods/main

## Вливание веток
Для вливания изменений из ветки в ветку от которой производилось ответвление необходимо использовать **Pull Request** на Github. Пулл реквест создается в ту ветку от которой производилось ответвление. Далее созданный запрос передается на код ревью. Если в ходе проверки возникают пожелания по улучшению кода, то разработчик кода вносит исправления по улучшению кода в эту же ветку. После того, как все пожелания учтены пулл реквест принимается и изменения оказываются в основной ветке.

## Программы для работы с git
Для более удобной работы с git можно использовать программы, предоставляющие графический интерфейс просмотра репозитория, сравнения файлов, удобного решения конфликтов.

 - [GitExtensions](http://gitextensions.github.io/) для просмотра
   репозитория, выполнения коммитов, стягивания новых изменений из
   репозитория, удобного переключения веток
 - [TortoiseGit](https://tortoisegit.org/download/) имеет удобный
   интерфейс сравнения файлов, решения конфликтов, предоставляет
   возможность просмотра репозитория


[Уроки](https://www.youtube.com/playlist?list=PLRs8EELOYKc44Y_fKFvADdPXbrYZDQqr0) по работе с *системой контроля версий - GIT* (YouTube Playlist)