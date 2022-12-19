### Инструкция по осуществлению deploy'я обновлённого docker-контейнера 'infra-web' с приложением 'tg_bot_constructor'
### (deploy посредством выполнения скриптов на ubuntu)

1. выполните загрузку папки 'scripts' из корня репозитория 'tg_bot_constructor' и разместите её в домашней директории вашей системы Linux

2. в загруженной папке 'scripts' располагается файл 'docreg_password.txt';
   в нём следует разместить пароль для авторизации в Private Docker Registry

Примечание:
	для авторизации в Private Docker Registry используется username и password;
	настоящем - упрощённом - варианте username и password совпадают,
	что позволяет использовать для авторизации только один текстовый файл: 'docreg_password.txt')
	
3. для непосредственного запуска обновления docker-контейнера 'infra-web' с приложением 'tg_bot_constructor' на удалённом сервере
   требуется находясь в домашней директории вашей системы ubuntu локально запустить скрипт unit.sh, выполнив команду:
   ./scripts/unit.sh
   
   
После его запуска последовательно будет выполнен ряд операций в результате работы вложенных скриптов:
	- загрузка и локальная распаковка zip-архива ветки main репозитория 'tg_bot_constructor' (скрипт 'download_and_unzip_from_github_using_wget.sh')
	- пересборка образа 'infra-web' с опцией '--no-cache' (скрипт 'build_no_cache_infra_web_image.sh')
	- авторизация в Private Docker Registry на локальной машине с параметром командной строки '--password-stdin' (с чтением пароля для входа из файла ~/scripts/docreg_password.txt)
	  для выполнения операции push image (скрипт 'docreg_login_locally.sh')
	- авторизация в Private Docker Registry на удалённой машине для выполнения операции pull image (скрипт 'docreg_login_test.sh')
	- присвоение tag'а и загрузка (push) обновлённого образа 'infra-web' в Private Docker Registry как 'ramasuchka.kz:4443/infra-web:latest' (скрипт 'tag_and_push_infra_web_image.sh')
	- выход из Private Docker Registry на локальной машине с удалением данных авторизации
	- копирование модифицированного файла 'docker-compose.yml' на удалённый сервер командой:
		scp -r ~/tg_bot_constructor/infra/docker-compose.yml_move_2_server ubuntu@185.146.3.196:~/tg_bot_constructor/infra/docker-compose.yml
	- выполнение загрузки обновлённого образа 'infra-web' (требующих обновления слоёв docker-образа)
	  и осуществление пересборки контейнера из обновлённого образа с автоматическим перезапуском и
	  применением миграций в случае необходимости (скрипт 'pull_updated_infra_web_image_restart_container.sh')
		ssh ubuntu@185.146.3.196 'bash -s' < ~/scripts/pull_updated_infra_web_image_restart_container.sh
	- выход из Private Docker Registry на удалённом сервере с удалением данных авторизации

