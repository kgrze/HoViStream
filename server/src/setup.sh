#!/usr/bin/env bash

sudo apt install ffmpeg
sudo apt install gpac
sudo apt install youtube-dl
sudo apt install qnapi
sudo apt install libgd-dev

sudo apt install nginx-full

python -m pip install jinja2
wget https://github.com/shaka-project/shaka-packager/releases/download/v2.6.1/packager-linux-x64

sudo mv packager-linux-x64 /usr/local/bin/packager
sudo chmod 755 /usr/local/bin/packager

./refresh_server.sh

echo 'HoViStream initialization finished.'
echo '1. Copy movies to /home/$USER/HoViStream/media'
echo '2. Run hovistream.py script'
echo '3. Run "ip addr show" to see what is Your IP address'
echo '4. Open web browser and type "http://<your IP address>" and You should see the list of movies available for local streaming.'
echo 'Enjoy !!!'