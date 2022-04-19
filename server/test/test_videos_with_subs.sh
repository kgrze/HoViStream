#!/usr/bin/env bash

mkdir -p /home/kgrze/HoViStream/media/batman
pushd /home/kgrze/HoViStream/media/batman
youtube-dl --all-subs -o batman.mp4 'https://www.youtube.com/watch?v=mqqft2x_Aa4&ab_channel=WarnerBros.Pictures'
popd

mkdir -p /home/kgrze/HoViStream/media/topgun
pushd /home/kgrze/HoViStream/media/topgun
youtube-dl --all-subs -o topgun.mp4  'https://www.youtube.com/watch?v=giXco2jaZ_4&ab_channel=ParamountPictures'
popd

mkdir -p /home/kgrze/HoViStream/media/tears_of_steel
pushd /home/kgrze/HoViStream/media/tears_of_steel
wget https://ia600603.us.archive.org/30/items/Tears-of-Steel/tears_of_steel_720p.mkv
wget https://download.blender.org/demo/movies/ToS/subtitles/TOS-en.srt
popd

pushd ../src
python hovistream.py "/home/kgrze/HoViStream/media" "/home/kgrze/HoViStream/www"
popd

echo "HoViStream sever is ready."