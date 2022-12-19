#!/bin/bash
#docker login https://ramasuchka.kz:4443 --username=admin --password=admin
# To Do: подумать, стоит ли поменять использование --password-stdin для параметра 'password' на --password=$parameter (как используется для параметра --username)
sudo docker login https://ramasuchka.kz:4443 --username=$1 --password-stdin
exit 0
