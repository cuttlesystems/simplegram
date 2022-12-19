#!/bin/bash
./scripts/download_and_unzip_from_github_using_wget.sh

# build with '--no-cache' option 'infra-web' image
./scripts/build_no_cache_infra_web_image.sh

# local docker registry login with '--password-stdin' to push docker image
./scripts/docreg_login_locally.sh $(cat ~/scripts/docreg_password.txt) < ~/scripts/docreg_password.txt


# remote docker registry login through 'ssh' and with 2 command line parameters (without '--password-stdin') to pull docker image to the server
echo ""
echo "remote docker registry logging in"
./scripts/docreg_login_test.sh
echo ""



# tag and push updated 'infra-web' image to the Private Docker Registry as 'ramasuchka.kz:4443/infra-web:latest'"
./scripts/tag_and_push_infra_web_image.sh
echo ""
echo "image pushed"

# local docker registry logout
echo ""
sudo docker logout https://ramasuchka.kz:4443
echo "local docker registry logout"
echo ""

## duplicated   ***TO REMOVE***
## remote docker registry login through 'ssh' and with 2 command line parameters (without '--password-stdin') to pull docker image to the server
#echo ""
#echo "remote docker registry logging in"
#./scripts/docreg_login_test.sh
#echo ""



# copy modified 'docker-compose.yml' file to remote server
#scp -r ~/tg_bot_constructor/infra/docker-compose.yml_move_2_server ubuntu@185.146.3.196:~/tg_bot_constructor/infra/docker-compose.yml

# To Do: IP адрес и наименование сервера брать из переменной

# recreate_restart_infra_web_container_migrate.sh
echo ""
echo "recreation of a container started"
ssh ubuntu@185.146.3.196 'bash -s' < ~/scripts/pull_updated_infra_web_image_restart_container.sh
echo ""

# remote docker registry logout
ssh ubuntu@185.146.3.196 'sudo docker logout https://ramasuchka.kz:4443'

exit 0
