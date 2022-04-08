#!/usr/bin/env bash

rm -rf /home/kgrze/HoViStream/media

cp -rf ../data/web/index.html /home/kgrze/HoViStream/www/html/

mkdir -p /home/kgrze/HoViStream/media/batman
pushd /home/kgrze/HoViStream/media/batman
youtube-dl --all-subs -o batman.mp4 'https://www.youtube.com/watch?v=mqqft2x_Aa4&ab_channel=WarnerBros.Pictures'
popd
python ../src/convert_to_stream.py /home/kgrze/HoViStream/media/batman/batman.mp4 /home/kgrze/HoViStream/www/stream/batman
cp -rf ../data/web/batman.html /home/kgrze/HoViStream/www/html/
rm -rf /home/kgrze/HoViStream/media/batman

mkdir -p /home/kgrze/HoViStream/media/topgun
pushd /home/kgrze/HoViStream/media/topgun
youtube-dl --all-subs -o topgun.mp4  'https://www.youtube.com/watch?v=giXco2jaZ_4&ab_channel=ParamountPictures'
popd
python ../src/convert_to_stream.py /home/kgrze/HoViStream/media/topgun/topgun.mp4 /home/kgrze/HoViStream/www/stream/topgun
cp -rf ../data/web/topgun.html /home/kgrze/HoViStream/www/html/
rm -rf /home/kgrze/HoViStream/media/topgun

../src/refresh_server.sh
echo "HoViStream sever is ready."