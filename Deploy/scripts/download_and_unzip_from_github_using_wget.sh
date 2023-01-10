#!/bin/bash
GH_USER=cuttlesystems
GH_REPO=tg_bot_constructor
GH_BRANCH=main
MY_TOKEN_CREATED_ON_GITHUB=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

# To Do:
# 	необходимо отделить логику от конфигурационных переменных -
#	один файл - с логикой взаимодействия, другой файл - с конфигурационными переменными;
#	или же все конфигурационные переменные вынести в 'env' файл

DIR=./"$GH_REPO"
echo "Будет выполнена загрузка zip-файла из репозитория '"$GH_REPO"' организации '"$GH_USER"';"
echo "ветка: '"$GH_BRANCH"';"
echo ""
if [ -d "$DIR" ]
	then
		WORKING_BOT_BACKUP_DIR_CREATION_TIME=$(date +%d-%m-%Y_%T)
#		mv -n ./"$GH_REPO" ./"$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME
               cp -r ./"$GH_REPO" ./"$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME
                echo "Выполнено переименование директории '"$GH_REPO"' с прежними версиями файлов в директорию '$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME"'"
	else
		mkdir -p ./$GH_REPO/infra
fi

# To Do: убрать лишнее
echo 'B_ENGINE=django.db.backends.postgresql
DB_NAME=bot_constructor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=zarFad-huqdit-qavry0
DB_HOST=172.21.0.1
DB_PORT=5432

DOMAIN_HOST=ramasuchka.kz
HOST_PROTOCOL=https' > ./$GH_REPO/infra/.env
echo ""
# директория с версиями файлов до последних изменений
#LAST_WORKING_BOT_DIR=
# To Do: add server answer check on zip-file download
curl -H "Authorization: token "$MY_TOKEN_CREATED_ON_GITHUB -L https://api.github.com/repos/$GH_USER/$GH_REPO/zipball/$GH_BRANCH > $GH_REPO-$GH_BRANCH.zip
echo ""
echo "zip-архив загружен"
echo ""
unzip -q -o ./"$GH_REPO-$GH_BRANCH.zip"
#mv -f ./$(unzip -Z -1 ./"$GH_REPO-$GH_BRANCH.zip" | head -1) ~/$GH_REPO
#-t ДИРЕКТОРИЯ или --target-directory=ДИРЕКТОРИЯ
#Переместить все исходные файлы в директорию, которая указана в аргументе опции.
#mv -f ./$(unzip -Z -1 ./"$GH_REPO-$GH_BRANCH.zip" | head -1)/*/ --target-directory=./$GH_REPO
cp -r ./$(unzip -Z -1 ./"$GH_REPO-$GH_BRANCH.zip" | head -1)/* ./$GH_REPO
rm -rf ./$(unzip -Z -1 ./"$GH_REPO-$GH_BRANCH.zip" | head -1)

echo "Распаковка загруженного из репозитория архива выполнена с заменой файлов"
echo ""

# python script 'get_commit_info_from_github_api.py' call from deploy script
python3 ~/$GH_REPO'/utils/get_commit_info_from_github_api.py' 'Bearer '$MY_TOKEN_CREATED_ON_GITHUB
#echo '"'./$GH_REPO/utils/get_commit_info_from_github_api.py'"' '"'Bearer $MY_TOKEN_CREATED_ON_GITHUB'"'

if [ -d "$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME ] && [ -f "$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME/infra/.env ]
        then
		cp ./"$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME/infra/.env ./"$GH_REPO"/infra/
		echo "Копирование ранее созданного файла '.env' из директории с прежними версиями файлов '$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME"' в обновлённую директорию '"$GH_REPO"'"
		echo ""
	else
                echo "В директории с прежними версиями файлов '$GH_REPO"_$WORKING_BOT_BACKUP_DIR_CREATION_TIME"' не существует файла '.env', поэтому он не может быть скопирован в директорию '"$GH_REPO"' с обновлёнными файлами"
fi
if [ ! -f "$GH_REPO"/infra/.env ]
        then
                echo "В директории '$GH_REPO/infra/' не существует файла '.env'"
                echo "Создайте файл '.env' в директории '$GH_REPO/infra/'"
fi
rm ./"$GH_REPO-$GH_BRANCH.zip"
echo ""
echo "Выполнено удаление zip-архива"
echo ""
exit 0
