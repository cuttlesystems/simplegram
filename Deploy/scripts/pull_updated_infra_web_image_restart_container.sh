#!/bin/bash

# to avoid multi '<none>' images on the server we should remove 'infra-web:latest' image before pull update for it from the registry
# '-f' force removing option
sudo docker rmi -f infra-web:latest

# to avoid multi '<none>' images on the server we should remove 'ramasuchka.kz:4443/infra-web:latest' image before pull update for it from the registry
# '-f' force removing option
sudo docker rmi -f ramasuchka.kz:4443/infra-web:latest

# pull updated image from the registry
sudo docker pull ramasuchka.kz:4443/infra-web:latest
echo ""

# tag updated image as 'infra-web:latest'
sudo docker tag ramasuchka.kz:4443/infra-web:latest infra-web:latest
echo ""

cd ~/tg_bot_constructor/infra/
#sudo docker-compose build --no-cache web
#docker-compose build --no-cache web

# forced recreation of the 'infra-web' container with updated image and start
sudo docker-compose up --force-recreate -d web
#docker-compose up --force-recreate -d web
echo ""

# then migrate in started container
#sudo docker exec -it infra-web-1 bash -c "python manage.py migrate"
#docker exec infra-web-1 bash -c "python manage.py migrate"
sudo docker exec infra-web-1 bash -c "python manage.py migrate"
exit 0
