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

echo -e '\e[31mHoViStream initialization finished.\e[0m'
echo -e '\e[31m1. Run hovistream.py {input_path_to_movie_folder} {output_path_to_www_stream_content}\e[0m'
echo -e '\e[31m2. Run "ip addr show" to see what is Your IP address\e[0m'
echo -e '\e[31m3. Open web browser and type "http://<your IP address>" and You should see the list of movies available for local streaming.\e[0m'
echo -e '\e[31m4. Enjoy !!!\e[0m'