#!/usr/bin/env bash

mkdir -p /home/$USER/HoViStream/media/batman
pushd /home/$USER/HoViStream/media/batman
youtube-dl --all-subs -o batman.mp4 'https://www.youtube.com/watch?v=mqqft2x_Aa4&ab_channel=WarnerBros.Pictures'
popd

mkdir -p /home/$USER/HoViStream/media/topgun
pushd /home/$USER/HoViStream/media/topgun
youtube-dl --all-subs -o topgun.mp4  'https://www.youtube.com/watch?v=giXco2jaZ_4&ab_channel=ParamountPictures'
popd

mkdir -p /home/$USER/HoViStream/media/tears_of_steel
pushd /home/$USER/HoViStream/media/tears_of_steel
wget https://ia600603.us.archive.org/30/items/Tears-of-Steel/tears_of_steel_720p.mkv
wget https://download.blender.org/demo/movies/ToS/subtitles/TOS-en.srt
popd

pushd ../src
python hovistream.py "/home/$USER/HoViStream/media" "/home/$USER/HoViStream/www"
popd

echo "HoViStream sever is ready."