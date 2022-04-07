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

rm -rf /home/kgrze/HoViStream

mkdir -p /home/kgrze/HoViStream/www/html
mkdir -p /home/kgrze/HoViStream/www/stream
mkdir -p /home/kgrze/HoViStream/media
echo "HoViStream initialization finished."