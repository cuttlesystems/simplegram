#!/bin/bash
#docker login https://ramasuchka.kz:4443 --username=admin --password=admin
sudo docker login https://ramasuchka.kz:4443 --username=$1 --password-stdin
exit 0
