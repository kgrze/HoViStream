#!/usr/bin/env bash

sudo yes | sudo cp -rf ../data/nginx.conf /etc/nginx/nginx.conf
sudo yes | sudo cp -rf ../data/web/index.html /var/www/html/index.html
sudo systemctl reload nginx.service