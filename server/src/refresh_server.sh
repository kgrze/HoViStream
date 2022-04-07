#!/usr/bin/env bash

sudo yes | sudo cp -rf ../data/nginx.conf /etc/nginx/nginx.conf
cp -rf ../data/web/index.html /home/kgrze/HoViStream/www/html/
sudo systemctl reload nginx.service
echo "HoViStream server data refreshed"