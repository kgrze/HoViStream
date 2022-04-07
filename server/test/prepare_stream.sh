#!/usr/bin/env bash

rm -rf /home/kgrze/HoViStream/media
mkdir -p /home/kgrze/HoViStream/media/batman

pushd /home/kgrze/HoViStream/media/batman
youtube-dl --all-subs -o batman.mp4 'https://www.youtube.com/watch?v=mqqft2x_Aa4&ab_channel=WarnerBros.Pictures'
popd

python ../src/convert_to_stream.py /home/kgrze/HoViStream/media/batman/batman.mp4 /home/kgrze/HoViStream/www/stream/batman

rm -rf /home/kgrze/HoViStream/media/batman

../src/refresh_server.sh
echo "HoViStream sever is ready."