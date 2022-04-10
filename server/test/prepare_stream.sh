#!/usr/bin/env bash

rm -rf /home/kgrze/HoViStream/www/html/
rm -rf /home/kgrze/HoViStream/media

cp -rf ../data/web/index.html /home/kgrze/HoViStream/www/html/

mkdir -p /home/kgrze/HoViStream/media/batman
pushd /home/kgrze/HoViStream/media/batman
youtube-dl --all-subs -o batman.mp4 'https://www.youtube.com/watch?v=mqqft2x_Aa4&ab_channel=WarnerBros.Pictures'
popd
python ../src/convert_to_stream.py /home/kgrze/HoViStream/media/batman/batman.mp4 /home/kgrze/HoViStream/www/stream/batman /home/kgrze/HoViStream/media/batman/batman.en-US.vtt
cp -rf ../data/web/batman.html /home/kgrze/HoViStream/www/html/
rm -rf /home/kgrze/HoViStream/media/batman

mkdir -p /home/kgrze/HoViStream/media/topgun
pushd /home/kgrze/HoViStream/media/topgun
youtube-dl --all-subs -o topgun.mp4  'https://www.youtube.com/watch?v=giXco2jaZ_4&ab_channel=ParamountPictures'
popd
python ../src/convert_to_stream.py /home/kgrze/HoViStream/media/topgun/topgun.mp4 /home/kgrze/HoViStream/www/stream/topgun /home/kgrze/HoViStream/media/topgun/topgun.en-US.vtt
cp -rf ../data/web/topgun.html /home/kgrze/HoViStream/www/html/
rm -rf /home/kgrze/HoViStream/media/topgun

mkdir -p /home/kgrze/HoViStream/media/tears_of_steel
pushd /home/kgrze/HoViStream/media/tears_of_steel
wget https://ia600603.us.archive.org/30/items/Tears-of-Steel/tears_of_steel_720p.mkv
wget https://download.blender.org/demo/movies/ToS/subtitles/TOS-en.srt
popd
python ../src/convert_to_stream.py /home/kgrze/HoViStream/media/tears_of_steel/tears_of_steel_720p.mkv /home/kgrze/HoViStream/www/stream/tears_of_steel /home/kgrze/HoViStream/media/tears_of_steel/TOS-en.srt
cp -rf ../data/web/tos.html /home/kgrze/HoViStream/www/html/
rm -rf /home/kgrze/HoViStream/media/tears_of_steel

../src/refresh_server.sh
echo "HoViStream sever is ready."