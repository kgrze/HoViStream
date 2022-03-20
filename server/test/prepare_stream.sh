#!/usr/bin/env bash

rm -rf /var/www/media
mkdir -p /var/www/media/bbb/stream

pushd /var/www/media/bbb
wget https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_5MB.mp4

mv Big_Buck_Bunny_1080_10s_5MB.mp4 bbb_1080.mp4

ffmpeg -y -i bbb_1080p.mp4 -c:v libx264 \
 -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
 -vf scale=-2:2160 -b:v 6000k -maxrate 6000k \
 -movflags faststart -bufsize 8600k \
 -profile:v main -preset fast -an "bbb_2160p.mp4"

 ffmpeg -y -i bbb_1080p.mp4 -c:v libx264 \
 -r 24 -x264opts 'keyint=48:min-keyint=48:no-scenecut' \
 -vf scale=-2:720 -b:v 3500k -maxrate 3500k \
 -movflags faststart -bufsize 8600k \
 -profile:v main -preset fast -an "bbb_720p.mp4"

 ffmpeg -y -i bbb_1080p.mp4 -map 0:1 -vn -c:a aac -b:a 128k -ar 48000 -ac 2 bbb_audio.m4a

 MP4Box -dash 4000 -frag 4000 -rap \
-segment-name 'segment_$RepresentationID$_' -fps 24 \
bbb_2160.mp4#video:id=2160p \
bbb_1080.mp4#video:id=1080p \
bbb_720.mp4#video:id=720p \
bbb_audio.m4a#audio:id=English:role=main \
-out stream/bbb.mpd

 popd
