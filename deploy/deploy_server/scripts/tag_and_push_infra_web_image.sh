#!/bin/bash
#cd ~/tg_bot_constructor/infra/
#sudo docker-compose build --no-cache web
#docker-compose build --no-cache web
#sudo docker-compose up --force-recreate -d web
#docker-compose up --force-recreate -d web
#sudo docker exec -it infra-web-1 bash -c "python manage.py migrate"
#docker exec infra-web-1 bash -c "python manage.py migrate"
#sudo docker exec infra-web-1 bash -c "python manage.py migrate"

# additional step
sudo docker tag infra-web ramasuchka.kz:4443/infra-web:latest
echo "Updated 'infra-web' image was tagged as 'ramasuchka.kz:4443/infra-web:latest'"
echo ""

sudo docker push ramasuchka.kz:4443/infra-web:latest
echo ""
echo "Updated 'infra-web' image was pushed to the Private Docker Registry as 'ramasuchka.kz:4443/infra-web:latest'"
echo ""

# deleting images after rebuild
sudo docker rmi -f infra_web:latest
sudo docker rmi -f infra-web:latest
sudo docker rmi -f ramasuchka.kz:4443/infra-web:latest
echo ""
echo "Deleting local images: 'infra_web', 'infra-web', 'ramasuchka.kz:4443/infra-web:latest'"
echo ""

# deleting images tagged as '<none>'
sudo docker rmi $(docker images | grep none | awk '{print $3}')
echo ""
echo "Deleting local images tagged as '<none>'..."
echo ""

ssh ubuntu@185.146.3.196 'sudo docker pull ramasuchka.kz:4443/infra-web:latest'
echo "Updated 'infra-web' image was pulled to the Server (185.146.3.196) as 'ramasuchka.kz:4443/infra-web:latest'"
echo ""
exit 0
