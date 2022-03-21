#!/usr/bin/env bash

sudo rm -rf /var/www/media
sudo mkdir -p /var/www/media/batman/stream

cd /var/www/media/batman
sudo youtube-dl --all-subs -o batman.mp4 'https://www.youtube.com/watch?v=mqqft2x_Aa4&ab_channel=WarnerBros.Pictures'

sudo ffmpeg -y -i batman.mp4 -c:v libx264 \
 -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
 -vf scale=-2:2160 -b:v 6000k -maxrate 6000k \
 -movflags faststart -bufsize 8600k \
 -profile:v main -preset fast -an "batman_2160p.mp4"

sudo ffmpeg -y -i batman.mp4 -c:v libx264 \
 -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
 -vf scale=-2:1080 -b:v 4300k -maxrate 4300k \
 -movflags faststart -bufsize 8600k \
 -profile:v main -preset fast -an "batman_1080p.mp4"

sudo ffmpeg -y -i batman.mp4 -c:v libx264 \
 -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
 -vf scale=-2:720 -b:v 3500k -maxrate 3500k \
 -movflags faststart -bufsize 8600k \
 -profile:v main -preset fast -an "batman_720p.mp4"

sudo ffmpeg -y -i batman.mp4 -map 0:1 -vn -c:a aac -b:a 128k -ar 48000 -ac 2 batman_audio.m4a

sudo MP4Box -add batman.en-US.vtt:lang=en-US subtitle_en.mp4

sudo MP4Box -dash 4000 -frag 4000 -rap \
-segment-name 'segment_$RepresentationID$_' -fps 24 \
batman_2160p.mp4#video:id=2160p \
batman_1080p.mp4#video:id=1080p \
batman_720p.mp4#video:id=720p \
batman_audio.m4a#audio:id=English:role=main \
subtitle_en.mp4:role=subtitle \
-out stream/batman.mpd
