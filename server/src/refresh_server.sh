#!/usr/bin/env bash

sudo yes | cp -rf ../data/nginx.config /etc/nginx/nginx.config
sudo yes | cp -rf ../data/web/index.html /var/www/html/index.html
sudo systemctl reload nginx.service