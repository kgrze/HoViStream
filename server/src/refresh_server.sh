#!/usr/bin/env bash
# author: kgrze
sudo yes | sudo cp -rf ./nginx/nginx.conf /etc/nginx/nginx.conf
sudo systemctl reload nginx.service
echo "HoViStream server data refreshed"