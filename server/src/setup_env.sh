#!/usr/bin/env bash

sudo apt install nginx-full
sudo apt intall ffmpeg
sudo apt intall gpac

sudo chown -R $USER:$USER /etc/nginx
sudo chmod 755 -R /etc/nginx

sudo chown -R $USER:$USER /var/www
sudo chmod 755 -R /var/www

rm -rf /var/www
mkdir /var/www/media