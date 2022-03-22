#!/usr/bin/env bash

sudo apt install nginx-full
sudo apt install ffmpeg
sudo apt install gpac
sudo apt install youtube-dl
wget https://github.com/shaka-project/shaka-packager/releases/download/v2.6.1/packager-linux-x64

sudo mv packager-linux-x64 /usr/local/bin/packager
sudo chmod 755 /usr/local/bin/packager

sudo chown -R $USER:$USER /etc/nginx
sudo chmod 755 -R /etc/nginx/*

sudo chown -R $USER:$USER /var/www
sudo chmod 755 -R /var/www/*

sudo rm -rf /var/www
sudo mkdir -p /var/www/html
sudo mkdir -p /var/www/media